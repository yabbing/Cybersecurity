"""
SSH enumeration module
"""

import socket
import logging
from typing import Dict, Any, Optional
import config

# ============================================================================
# SSH ENUMERATION
# ============================================================================

class SSHEnumerator:
    """SSH service enumeration"""
    
    def __init__(self, target: str, port: int = 22):
        """
        Initialize SSH enumerator
        
        Args:
            target: Target IP or domain
            port: SSH port (default 22)
        """
        self.target = target
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform SSH enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'service': 'ssh',
            'banner': None,
            'version': None,
            'error': None
        }
        
        # Get SSH banner
        self.logger.info(f"Attempting SSH banner grab on {self.target}:{self.port}")
        banner = self._get_banner()
        if banner:
            results['banner'] = banner
            results['version'] = self._parse_version(banner)
        
        return results
    
    def _get_banner(self) -> Optional[str]:
        """
        Get SSH banner
        
        Returns:
            Banner string or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.SSH_TIMEOUT)
            sock.connect((self.target, self.port))
            
            # Receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            
            sock.close()
            
            return banner
            
        except socket.timeout:
            self.logger.error("SSH connection timed out")
        except Exception as e:
            self.logger.error(f"Error getting SSH banner: {str(e)}")
        
        return None
    
    def _parse_version(self, banner: str) -> Optional[str]:
        """
        Parse SSH version from banner
        
        Args:
            banner: SSH banner string
            
        Returns:
            Version string or None
        """
        try:
            # SSH banner format: SSH-protoversion-softwareversion comments
            # Example: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
            if banner.startswith('SSH-'):
                parts = banner.split('-', 2)
                if len(parts) >= 3:
                    return parts[2]
            
            return banner
            
        except Exception as e:
            self.logger.error(f"Error parsing SSH version: {str(e)}")
            return None

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_ssh(target: str, port: int = 22) -> Dict[str, Any]:
    """
    Enumerate SSH service
    
    Args:
        target: Target IP or domain
        port: SSH port
        
    Returns:
        Dictionary with enumeration results
    """
    enumerator = SSHEnumerator(target, port)
    return enumerator.enumerate()
