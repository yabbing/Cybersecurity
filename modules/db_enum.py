"""
Database enumeration module
Supports MySQL, PostgreSQL, and MSSQL
"""

import socket
import logging
from typing import Dict, Any, Optional, List
import config

# ============================================================================
# DATABASE ENUMERATION
# ============================================================================

class DatabaseEnumerator:
    """Database service enumeration"""
    
    # Default ports for database services
    DB_PORTS = {
        'mysql': 3306,
        'postgresql': 5432,
        'mssql': 1433
    }
    
    def __init__(self, target: str, port: int):
        """
        Initialize database enumerator
        
        Args:
            target: Target IP or domain
            port: Database port
        """
        self.target = target
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.db_type = self._detect_db_type()
    
    def _detect_db_type(self) -> str:
        """
        Detect database type based on port
        
        Returns:
            Database type string
        """
        for db_type, default_port in self.DB_PORTS.items():
            if self.port == default_port:
                return db_type
        
        # Default to unknown
        return 'unknown'
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform database enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'service': f'database ({self.db_type})',
            'db_type': self.db_type,
            'version': None,
            'banner': None,
            'accessible': False,
            'authentication_required': None,
            'error': None
        }
        
        # Check if port is open
        self.logger.info(f"Checking database service on {self.target}:{self.port}")
        if not self._check_port_open():
            results['error'] = 'Port is not accessible'
            return results
        
        results['accessible'] = True
        
        # Enumerate based on database type
        if self.db_type == 'mysql':
            self._enumerate_mysql(results)
        elif self.db_type == 'postgresql':
            self._enumerate_postgresql(results)
        elif self.db_type == 'mssql':
            self._enumerate_mssql(results)
        else:
            self.logger.warning(f"Unknown database type for port {self.port}")
            results['error'] = 'Unknown database type'
        
        return results
    
    def _check_port_open(self) -> bool:
        """
        Check if the database port is open
        
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.DB_TIMEOUT)
            result = sock.connect_ex((self.target, self.port))
            sock.close()
            
            return result == 0
            
        except Exception as e:
            self.logger.error(f"Error checking port: {str(e)}")
            return False
    
    def _enumerate_mysql(self, results: Dict[str, Any]) -> None:
        """
        Enumerate MySQL database
        
        Args:
            results: Results dictionary to update
        """
        self.logger.info("Attempting MySQL enumeration")
        
        try:
            # Try to get MySQL banner/version
            banner = self._get_mysql_banner()
            if banner:
                results['banner'] = banner
                results['version'] = self._parse_mysql_version(banner)
            
            # Check if authentication is required
            auth_required = self._check_mysql_auth()
            results['authentication_required'] = auth_required
            
        except Exception as e:
            self.logger.error(f"MySQL enumeration error: {str(e)}")
            results['error'] = str(e)
    
    def _get_mysql_banner(self) -> Optional[str]:
        """
        Get MySQL server banner
        
        Returns:
            Banner string or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.DB_TIMEOUT)
            sock.connect((self.target, self.port))
            
            # MySQL sends initial handshake packet
            data = sock.recv(1024)
            sock.close()
            
            if data:
                # Parse MySQL handshake packet
                # Format: protocol version (1 byte) + server version (null-terminated string)
                try:
                    # Skip protocol version byte
                    version_start = 1
                    version_end = data.find(b'\x00', version_start)
                    
                    if version_end > version_start:
                        version = data[version_start:version_end].decode('utf-8', errors='ignore')
                        return version
                except Exception as e:
                    self.logger.debug(f"Error parsing MySQL banner: {str(e)}")
                    return data.hex()[:100]  # Return hex representation if parsing fails
            
        except socket.timeout:
            self.logger.error("MySQL connection timed out")
        except Exception as e:
            self.logger.error(f"Error getting MySQL banner: {str(e)}")
        
        return None
    
    def _parse_mysql_version(self, banner: str) -> Optional[str]:
        """
        Parse MySQL version from banner
        
        Args:
            banner: MySQL banner string
            
        Returns:
            Version string or None
        """
        try:
            # MySQL version format: 5.7.33-0ubuntu0.18.04.1
            # Extract major.minor.patch
            parts = banner.split('-')
            if parts:
                return parts[0]
            return banner
        except Exception as e:
            self.logger.debug(f"Error parsing MySQL version: {str(e)}")
            return banner
    
    def _check_mysql_auth(self) -> bool:
        """
        Check if MySQL requires authentication
        
        Returns:
            True if authentication is required
        """
        try:
            # Try importing mysql connector
            try:
                import mysql.connector
                
                # Attempt connection with no credentials
                conn = mysql.connector.connect(
                    host=self.target,
                    port=self.port,
                    user='',
                    password='',
                    connect_timeout=config.DB_TIMEOUT
                )
                conn.close()
                return False  # No auth required
                
            except ImportError:
                self.logger.warning("mysql-connector-python not installed, skipping auth check")
                return None
            except mysql.connector.Error:
                return True  # Auth required
                
        except Exception as e:
            self.logger.debug(f"MySQL auth check error: {str(e)}")
            return True
    
    def _enumerate_postgresql(self, results: Dict[str, Any]) -> None:
        """
        Enumerate PostgreSQL database
        
        Args:
            results: Results dictionary to update
        """
        self.logger.info("Attempting PostgreSQL enumeration")
        
        try:
            # Try to get PostgreSQL version
            version = self._get_postgresql_version()
            if version:
                results['version'] = version
            
            # Check if authentication is required
            auth_required = self._check_postgresql_auth()
            results['authentication_required'] = auth_required
            
        except Exception as e:
            self.logger.error(f"PostgreSQL enumeration error: {str(e)}")
            results['error'] = str(e)
    
    def _get_postgresql_version(self) -> Optional[str]:
        """
        Get PostgreSQL version
        
        Returns:
            Version string or None
        """
        try:
            # Try importing psycopg2
            try:
                import psycopg2
                
                # Attempt connection to get version
                conn = psycopg2.connect(
                    host=self.target,
                    port=self.port,
                    user='postgres',
                    password='',
                    connect_timeout=config.DB_TIMEOUT
                )
                
                cursor = conn.cursor()
                cursor.execute('SELECT version();')
                version = cursor.fetchone()[0]
                
                cursor.close()
                conn.close()
                
                return version
                
            except ImportError:
                self.logger.warning("psycopg2 not installed, skipping version check")
                return None
            except Exception:
                # Connection failed, but we can still try to get error message
                return None
                
        except Exception as e:
            self.logger.debug(f"PostgreSQL version check error: {str(e)}")
            return None
    
    def _check_postgresql_auth(self) -> bool:
        """
        Check if PostgreSQL requires authentication
        
        Returns:
            True if authentication is required
        """
        try:
            # Try importing psycopg2
            try:
                import psycopg2
                
                # Attempt connection with default credentials
                conn = psycopg2.connect(
                    host=self.target,
                    port=self.port,
                    user='postgres',
                    password='',
                    connect_timeout=config.DB_TIMEOUT
                )
                conn.close()
                return False  # No auth required
                
            except ImportError:
                self.logger.warning("psycopg2 not installed, skipping auth check")
                return None
            except psycopg2.OperationalError:
                return True  # Auth required
                
        except Exception as e:
            self.logger.debug(f"PostgreSQL auth check error: {str(e)}")
            return True
    
    def _enumerate_mssql(self, results: Dict[str, Any]) -> None:
        """
        Enumerate MSSQL database
        
        Args:
            results: Results dictionary to update
        """
        self.logger.info("Attempting MSSQL enumeration")
        
        try:
            # Try to get MSSQL version and info
            version_info = self._get_mssql_info()
            if version_info:
                results['version'] = version_info.get('version')
                results['banner'] = version_info.get('banner')
            
            # Check if authentication is required
            auth_required = self._check_mssql_auth()
            results['authentication_required'] = auth_required
            
        except Exception as e:
            self.logger.error(f"MSSQL enumeration error: {str(e)}")
            results['error'] = str(e)
    
    def _get_mssql_info(self) -> Optional[Dict[str, str]]:
        """
        Get MSSQL server information
        
        Returns:
            Dictionary with version and banner info
        """
        try:
            # Try importing pymssql
            try:
                import pymssql
                
                # Attempt connection to get version
                conn = pymssql.connect(
                    server=self.target,
                    port=self.port,
                    user='sa',
                    password='',
                    timeout=config.DB_TIMEOUT
                )
                
                cursor = conn.cursor()
                cursor.execute('SELECT @@VERSION;')
                version = cursor.fetchone()[0]
                
                cursor.close()
                conn.close()
                
                return {
                    'version': version,
                    'banner': version
                }
                
            except ImportError:
                self.logger.warning("pymssql not installed, skipping version check")
                return None
            except Exception:
                return None
                
        except Exception as e:
            self.logger.debug(f"MSSQL info check error: {str(e)}")
            return None
    
    def _check_mssql_auth(self) -> bool:
        """
        Check if MSSQL requires authentication
        
        Returns:
            True if authentication is required
        """
        try:
            # Try importing pymssql
            try:
                import pymssql
                
                # Attempt connection with default credentials
                conn = pymssql.connect(
                    server=self.target,
                    port=self.port,
                    user='sa',
                    password='',
                    timeout=config.DB_TIMEOUT
                )
                conn.close()
                return False  # No auth required
                
            except ImportError:
                self.logger.warning("pymssql not installed, skipping auth check")
                return None
            except pymssql.Error:
                return True  # Auth required
                
        except Exception as e:
            self.logger.debug(f"MSSQL auth check error: {str(e)}")
            return True

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_database(target: str, port: int) -> Dict[str, Any]:
    """
    Enumerate database service
    
    Args:
        target: Target IP or domain
        port: Database port
        
    Returns:
        Dictionary with enumeration results
    """
    enumerator = DatabaseEnumerator(target, port)
    return enumerator.enumerate()
