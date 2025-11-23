"""
Port scanning module using nmap
"""

import nmap
import logging
from typing import Dict, List, Optional, Any
from modules.utils import run_command

# ============================================================================
# NMAP SCANNER
# ============================================================================

class PortScanner:
    """Nmap-based port scanner"""
    
    def __init__(self, target: str, port_range: Optional[str] = None):
        """
        Initialize port scanner
        
        Args:
            target: Target IP or domain
            port_range: Optional port range (e.g., "1-1000")
        """
        self.target = target
        self.port_range = port_range
        self.logger = logging.getLogger(__name__)
        self.nm = nmap.PortScanner()
    
    def quick_scan(self) -> Dict[str, Any]:
        """
        Perform quick port scan to identify open ports
        
        Returns:
            Dictionary with scan results
        """
        self.logger.info(f"Starting quick scan on {self.target}")
        
        try:
            # Build scan arguments
            args = "-sS -T4"
            if self.port_range:
                args += f" -p {self.port_range}"
            else:
                args += " --top-ports 1000"
            
            self.logger.debug(f"Nmap arguments: {args}")
            
            # Run scan
            self.nm.scan(hosts=self.target, arguments=args)
            
            # Parse results
            results = self._parse_scan_results()
            
            self.logger.info(f"Quick scan complete. Found {len(results.get('ports', []))} open ports")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error during quick scan: {str(e)}")
            return {
                'error': str(e),
                'ports': []
            }
    
    def version_scan(self, ports: List[int]) -> Dict[str, Any]:
        """
        Perform version detection scan on specific ports
        
        Args:
            ports: List of ports to scan
            
        Returns:
            Dictionary with detailed scan results
        """
        if not ports:
            self.logger.warning("No ports provided for version scan")
            return {'ports': []}
        
        self.logger.info(f"Starting version scan on {len(ports)} ports")
        
        try:
            # Build port list
            port_list = ','.join(map(str, ports))
            
            # Build scan arguments
            args = f"-sV -sC -T4 -p {port_list}"
            
            self.logger.debug(f"Nmap arguments: {args}")
            
            # Run scan
            self.nm.scan(hosts=self.target, arguments=args)
            
            # Parse results
            results = self._parse_scan_results(detailed=True)
            
            self.logger.info(f"Version scan complete")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error during version scan: {str(e)}")
            return {
                'error': str(e),
                'ports': []
            }
    
    def _parse_scan_results(self, detailed: bool = False) -> Dict[str, Any]:
        """
        Parse nmap scan results
        
        Args:
            detailed: Whether to include detailed information
            
        Returns:
            Dictionary with parsed results
        """
        results = {
            'target': self.target,
            'ports': []
        }
        
        try:
            # Check if target was scanned
            if self.target not in self.nm.all_hosts():
                self.logger.warning(f"No scan results for {self.target}")
                return results
            
            # Get host info
            host = self.nm[self.target]
            
            # Parse each protocol
            for proto in host.all_protocols():
                ports = host[proto].keys()
                
                for port in ports:
                    port_info = host[proto][port]
                    
                    port_data = {
                        'port': port,
                        'protocol': proto,
                        'state': port_info.get('state', 'unknown'),
                        'service': port_info.get('name', ''),
                        'product': port_info.get('product', ''),
                        'version': port_info.get('version', ''),
                        'extrainfo': port_info.get('extrainfo', ''),
                    }
                    
                    # Build version string
                    version_parts = []
                    if port_data['product']:
                        version_parts.append(port_data['product'])
                    if port_data['version']:
                        version_parts.append(port_data['version'])
                    if port_data['extrainfo']:
                        version_parts.append(f"({port_data['extrainfo']})")
                    
                    port_data['version'] = ' '.join(version_parts) if version_parts else ''
                    
                    # Add script results if detailed
                    if detailed and 'script' in port_info:
                        port_data['scripts'] = port_info['script']
                    
                    results['ports'].append(port_data)
            
            # Sort ports by port number
            results['ports'].sort(key=lambda x: x['port'])
            
        except Exception as e:
            self.logger.error(f"Error parsing scan results: {str(e)}")
        
        return results

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def scan_target(target: str, port_range: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform complete scan on target (quick scan + version detection)
    
    Args:
        target: Target IP or domain
        port_range: Optional port range
        
    Returns:
        Dictionary with complete scan results
    """
    logger = logging.getLogger(__name__)
    
    scanner = PortScanner(target, port_range)
    
    # Quick scan to find open ports
    logger.info("Phase 1: Quick port scan")
    quick_results = scanner.quick_scan()
    
    if 'error' in quick_results:
        return quick_results
    
    # Get list of open ports
    open_ports = [
        p['port'] for p in quick_results.get('ports', [])
        if p.get('state') == 'open'
    ]
    
    if not open_ports:
        logger.info("No open ports found")
        return quick_results
    
    # Version detection on open ports
    logger.info(f"Phase 2: Version detection on {len(open_ports)} open ports")
    version_results = scanner.version_scan(open_ports)
    
    return version_results
