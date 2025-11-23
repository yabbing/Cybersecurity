"""
FTP enumeration module
"""

import socket
import logging
from typing import Dict, Any, Optional
import config

# ============================================================================
# FTP ENUMERATION
# ============================================================================

class FTPEnumerator:
    """FTP service enumeration"""
    
    def __init__(self, target: str, port: int = 21):
        """
        Initialize FTP enumerator
        
        Args:
            target: Target IP or domain
            port: FTP port (default 21)
        """
        self.target = target
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform FTP enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'service': 'ftp',
            'banner': None,
            'anonymous_login': False,
            'error': None
        }
        
        # Get banner
        self.logger.info(f"Attempting FTP banner grab on {self.target}:{self.port}")
        banner = self._get_banner()
        if banner:
            results['banner'] = banner
        
        # Try anonymous login
        self.logger.info("Checking for anonymous FTP access")
        anon_result = self._check_anonymous_login()
        results['anonymous_login'] = anon_result
        
        return results
    
    def _get_banner(self) -> Optional[str]:
        """
        Get FTP banner
        
        Returns:
            Banner string or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.FTP_TIMEOUT)
            sock.connect((self.target, self.port))
            
            # Receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            
            sock.close()
            
            return banner
            
        except socket.timeout:
            self.logger.error("FTP connection timed out")
        except Exception as e:
            self.logger.error(f"Error getting FTP banner: {str(e)}")
        
        return None
    
    def _check_anonymous_login(self) -> bool:
        """
        Check if anonymous FTP login is allowed
        
        Returns:
            True if anonymous login works, False otherwise
        """
        try:
            from ftplib import FTP
            
            ftp = FTP()
            ftp.connect(self.target, self.port, timeout=config.FTP_TIMEOUT)
            
            # Try anonymous login
            response = ftp.login('anonymous', 'anonymous@')
            
            ftp.quit()
            
            return '230' in response  # 230 = successful login
            
        except Exception as e:
            self.logger.debug(f"Anonymous login failed: {str(e)}")
            return False

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_ftp(target: str, port: int = 21) -> Dict[str, Any]:
    """
    Enumerate FTP service
    
    Args:
        target: Target IP or domain
        port: FTP port
        
    Returns:
        Dictionary with enumeration results
    """
    enumerator = FTPEnumerator(target, port)
    return enumerator.enumerate()
