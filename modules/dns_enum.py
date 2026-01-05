"""
DNS enumeration module
"""

import socket
import logging
from typing import Dict, Any, List, Optional
from modules.utils import run_command
import config

# ============================================================================
# DNS ENUMERATION
# ============================================================================

class DNSEnumerator:
    """DNS service enumeration"""
    
    def __init__(self, target: str, port: int = 53):
        """
        Initialize DNS enumerator
        
        Args:
            target: Target IP or domain
            port: DNS port (default 53)
        """
        self.target = target
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform DNS enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'service': 'dns',
            'records': {},
            'zone_transfer': None,
            'error': None
        }
        
        # Try zone transfer
        self.logger.info(f"Attempting DNS zone transfer on {self.target}")
        zone_transfer = self._attempt_zone_transfer()
        if zone_transfer:
            results['zone_transfer'] = zone_transfer
        
        # Query common DNS records
        self.logger.info("Querying DNS records")
        records = self._query_dns_records()
        if records:
            results['records'] = records
        
        return results
    
    def _attempt_zone_transfer(self) -> Optional[str]:
        """
        Attempt DNS zone transfer (AXFR)
        
        Returns:
            Zone transfer output or None
        """
        try:
            # Try using dig for zone transfer
            command = ['dig', f'@{self.target}', 'axfr']
            
            returncode, stdout, stderr = run_command(
                command,
                timeout=config.DNS_TIMEOUT
            )
            
            if returncode == 0 and stdout and 'Transfer failed' not in stdout:
                return stdout
            
        except Exception as e:
            self.logger.debug(f"Zone transfer failed: {str(e)}")
        
        return None
    
    def _query_dns_records(self) -> Dict[str, List[str]]:
        """
        Query common DNS record types
        
        Returns:
            Dictionary of record types and their values
        """
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        
        for record_type in record_types:
            try:
                # Use nslookup for basic queries
                command = ['nslookup', '-type=' + record_type, self.target]
                
                returncode, stdout, stderr = run_command(
                    command,
                    timeout=config.DNS_TIMEOUT
                )
                
                if returncode == 0 and stdout:
                    # Parse results
                    results = self._parse_nslookup_output(stdout, record_type)
                    if results:
                        records[record_type] = results
                        
            except Exception as e:
                self.logger.debug(f"Error querying {record_type} records: {str(e)}")
        
        return records
    
    def _parse_nslookup_output(self, output: str, record_type: str) -> List[str]:
        """
        Parse nslookup output
        
        Args:
            output: nslookup output
            record_type: Type of record queried
            
        Returns:
            List of parsed results
        """
        results = []
        
        try:
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and headers
                if not line or line.startswith('Server:') or line.startswith('Address:'):
                    continue
                
                # Look for relevant data
                if record_type == 'A' and 'Address:' in line:
                    parts = line.split('Address:')
                    if len(parts) > 1:
                        results.append(parts[1].strip())
                
                elif record_type == 'MX' and 'mail exchanger' in line:
                    results.append(line)
                
                elif record_type == 'NS' and 'nameserver' in line:
                    results.append(line)
                
                elif record_type == 'TXT' and '=' in line:
                    results.append(line)
                
                elif record_type in line:
                    results.append(line)
        
        except Exception as e:
            self.logger.error(f"Error parsing nslookup output: {str(e)}")
        
        return results

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_dns(target: str, port: int = 53) -> Dict[str, Any]:
    """
    Enumerate DNS service
    
    Args:
        target: Target IP or domain
        port: DNS port
        
    Returns:
        Dictionary with enumeration results
    """
    enumerator = DNSEnumerator(target, port)
    return enumerator.enumerate()
