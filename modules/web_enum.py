"""
Web service enumeration module
"""

import logging
import requests
from typing import Dict, Any, Optional
from modules.utils import run_command, check_tool_installed
import config

# ============================================================================
# WEB ENUMERATION
# ============================================================================

class WebEnumerator:
    """Web service enumeration"""
    
    def __init__(self, target: str, port: int, use_https: bool = False):
        """
        Initialize web enumerator
        
        Args:
            target: Target IP or domain
            port: Port number
            use_https: Whether to use HTTPS
        """
        self.target = target
        self.port = port
        self.protocol = "https" if use_https else "http"
        self.base_url = f"{self.protocol}://{target}:{port}"
        self.logger = logging.getLogger(__name__)
    
    def enumerate(self) -> Dict[str, Any]:
        """
        Perform web enumeration
        
        Returns:
            Dictionary with enumeration results
        """
        results = {
            'port': self.port,
            'protocol': self.protocol,
            'url': self.base_url,
            'headers': {},
            'directories': [],
            'subdomains': [],
            'errors': []
        }
        
        # Get HTTP headers
        self.logger.info(f"Fetching HTTP headers from {self.base_url}")
        headers = self._get_headers()
        if headers:
            results['headers'] = headers
        
        return results
    
    def _get_headers(self) -> Optional[Dict[str, str]]:
        """
        Get HTTP headers from target
        
        Returns:
            Dictionary of headers or None
        """
        try:
            response = requests.head(
                self.base_url,
                timeout=10,
                verify=False,
                allow_redirects=True
            )
            
            return dict(response.headers)
            
        except requests.exceptions.SSLError:
            # Try with HTTP if HTTPS fails
            if self.protocol == "https":
                self.logger.warning("SSL error, trying HTTP")
                try:
                    http_url = f"http://{self.target}:{self.port}"
                    response = requests.head(http_url, timeout=10, allow_redirects=True)
                    return dict(response.headers)
                except:
                    pass
        except Exception as e:
            self.logger.error(f"Error fetching headers: {str(e)}")
        
        return None
    
    def run_feroxbuster(self) -> Optional[str]:
        """
        Run feroxbuster for directory enumeration
        
        Returns:
            Output from feroxbuster or None
        """
        if not check_tool_installed('feroxbuster'):
            self.logger.warning("feroxbuster not installed, skipping")
            return None
        
        self.logger.info(f"Running feroxbuster on {self.base_url}")
        
        try:
            command = [
                'feroxbuster',
                '-u', self.base_url,
                '-t', str(config.FEROXBUSTER_THREADS),
                '--silent'
            ]
            
            if config.FEROXBUSTER_WORDLIST:
                command.extend(['-w', config.FEROXBUSTER_WORDLIST])
            
            returncode, stdout, stderr = run_command(
                command,
                timeout=config.FEROXBUSTER_TIMEOUT
            )
            
            if returncode == 0:
                return stdout
            else:
                self.logger.error(f"feroxbuster error: {stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error running feroxbuster: {str(e)}")
            return None
    
    def run_sublist3r(self) -> Optional[str]:
        """
        Run sublist3r for subdomain enumeration
        
        Returns:
            Output from sublist3r or None
        """
        if not check_tool_installed('sublist3r'):
            self.logger.warning("sublist3r not installed, skipping")
            return None
        
        # Extract domain from target (remove port if present)
        domain = self.target.split(':')[0]
        
        self.logger.info(f"Running sublist3r on {domain}")
        
        try:
            command = [
                'sublist3r',
                '-d', domain,
                '-t', '10'
            ]
            
            returncode, stdout, stderr = run_command(
                command,
                timeout=config.SUBLIST3R_TIMEOUT
            )
            
            if returncode == 0 or stdout:  # sublist3r sometimes returns non-zero even on success
                return stdout
            else:
                self.logger.error(f"sublist3r error: {stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error running sublist3r: {str(e)}")
            return None

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def enumerate_web(target: str, port: int, run_tools: bool = True) -> Dict[str, Any]:
    """
    Enumerate web service
    
    Args:
        target: Target IP or domain
        port: Port number
        run_tools: Whether to run additional tools (feroxbuster, sublist3r)
        
    Returns:
        Dictionary with enumeration results
    """
    # Determine if HTTPS
    use_https = port in [443, 8443]
    
    enumerator = WebEnumerator(target, port, use_https)
    results = enumerator.enumerate()
    
    # Run additional tools if requested
    if run_tools:
        ferox_output = enumerator.run_feroxbuster()
        if ferox_output:
            results['feroxbuster_output'] = ferox_output
        
        sublist3r_output = enumerator.run_sublist3r()
        if sublist3r_output:
            results['sublist3r_output'] = sublist3r_output
    
    return results
