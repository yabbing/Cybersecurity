"""
SMB enumeration module
"""

import socket
import logging
from typing import Dict, Any, Optional
from modules.utils import run_command, check_tool_installed
import config

# ============================================================================
# SMB ENUMERATION
# ============================================================================

class SMBEnumerator:
    """SMB/CIFS service enumeration"""
    
    def __init__(self, target: str, port: int = 445):
        """
        Initialize SMB enumerator
        
        Args:
            target: Target IP or domain
            port: SMB port (default 445)
        """
        self.target = target
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform SMB enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'service': 'smb',
            'shares': [],
            'version': None,
            'error': None
        }
        
        # Try to enumerate shares with smbclient
        if check_tool_installed('smbclient'):
            self.logger.info(f"Enumerating SMB shares on {self.target}")
            shares = self._enumerate_shares()
            if shares:
                results['shares'] = shares
        else:
            self.logger.warning("smbclient not installed, skipping share enumeration")
            results['error'] = "smbclient not available"
        
        return results
    
    def _enumerate_shares(self) -> Optional[list]:
        """
        Enumerate SMB shares
        
        Returns:
            List of share names or None
        """
        try:
            # Try null session
            command = [
                'smbclient',
                '-L', self.target,
                '-N'  # No password (null session)
            ]
            
            returncode, stdout, stderr = run_command(
                command,
                timeout=config.SMB_TIMEOUT
            )
            
            if returncode == 0 and stdout:
                # Parse share names from output
                shares = []
                in_shares_section = False
                
                for line in stdout.split('\n'):
                    line = line.strip()
                    
                    if 'Sharename' in line:
                        in_shares_section = True
                        continue
                    
                    if in_shares_section and line:
                        # Parse share line
                        parts = line.split()
                        if parts and not line.startswith('-'):
                            share_name = parts[0]
                            if share_name not in ['IPC$', 'print$']:  # Skip system shares
                                shares.append(share_name)
                
                return shares if shares else None
            
        except Exception as e:
            self.logger.error(f"Error enumerating SMB shares: {str(e)}")
        
        return None

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_smb(target: str, port: int = 445) -> Dict[str, Any]:
    """
    Enumerate SMB service
    
    Args:
        target: Target IP or domain
        port: SMB port
        
    Returns:
        Dictionary with enumeration results
    """
    enumerator = SMBEnumerator(target, port)
    return enumerator.enumerate()
