"""
Cybersecurity Reconnaissance Toolkit
Main application entry point

For Ethical Hacking & CTF Competitions Only
"""

import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, Any

# Import configuration
import config

# Import modules
from modules.utils import (
    setup_logging, check_all_dependencies, print_dependency_status,
    print_banner, print_section, print_success, print_error, print_info,
    get_user_confirmation, ensure_directory, get_timestamp, sanitize_filename
)
from modules.port_scanner import scan_target
from modules.report_generator import generate_reports

# Import enumeration modules
from modules.web_enum import enumerate_web
from modules.ftp_enum import enumerate_ftp
from modules.ssh_enum import enumerate_ssh
from modules.smb_enum import enumerate_smb
from modules.dns_enum import enumerate_dns

# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class ReconToolkit:
    """Main reconnaissance toolkit orchestrator"""
    
    def __init__(self, args):
        """
        Initialize the toolkit
        
        Args:
            args: Parsed command-line arguments
        """
        self.target = args.target
        self.output_dir = args.output
        self.port_range = args.ports
        self.confirmation_mode = not args.no_confirm
        self.quick_mode = args.quick
        self.verbose = args.verbose
        
        # Setup logging
        self.logger = setup_logging(self.verbose, config.LOG_FILE)
        
        # Scan data storage
        self.scan_data = {
            'target': self.target,
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ports': [],
            'enumeration_results': {},
            'total_ports_scanned': 0
        }
    
    def run(self):
        """Execute the reconnaissance workflow"""
        
        print_banner()
        
        # Check dependencies
        print_section("Dependency Check")
        tools_status = check_all_dependencies()
        if not print_dependency_status(tools_status):
            print_error("Critical dependencies missing. Please install nmap.")
            return False
        
        # Port scanning phase
        print_section(f"Port Scanning: {self.target}")
        print_info(f"Target: {self.target}")
        if self.port_range:
            print_info(f"Port Range: {self.port_range}")
        
        scan_results = scan_target(self.target, self.port_range)
        
        if 'error' in scan_results:
            print_error(f"Scan failed: {scan_results['error']}")
            return False
        
        # Store port scan results
        self.scan_data['ports'] = scan_results.get('ports', [])
        self.scan_data['total_ports_scanned'] = 1000  # Default nmap top ports
        
        open_ports = [p for p in self.scan_data['ports'] if p.get('state') == 'open']
        
        if not open_ports:
            print_info("No open ports found")
        else:
            print_success(f"Found {len(open_ports)} open ports")
            
            # Display open ports
            for port_info in open_ports:
                port = port_info['port']
                service = port_info.get('service', 'unknown')
                version = port_info.get('version', '')
                print_info(f"  Port {port}/tcp - {service} {version}")
        
        # Enumeration phase
        if not self.quick_mode and open_ports:
            print_section("Service Enumeration")
            
            for port_info in open_ports:
                port = port_info['port']
                service = port_info.get('service', 'unknown')
                
                # Determine enumeration type
                enum_type = config.PORT_ENUM_MAPPING.get(port)
                
                if not enum_type:
                    continue
                
                # Ask for confirmation
                if self.confirmation_mode:
                    prompt = f"Run {enum_type.upper()} enumeration on port {port}?"
                    if not get_user_confirmation(prompt):
                        print_info(f"Skipping {enum_type} enumeration on port {port}")
                        continue
                
                # Run appropriate enumeration
                print_info(f"Running {enum_type} enumeration on port {port}...")
                
                try:
                    enum_result = self._run_enumeration(enum_type, port)
                    
                    if enum_result:
                        enum_key = f"{enum_type}_{port}"
                        self.scan_data['enumeration_results'][enum_key] = enum_result
                        print_success(f"Completed {enum_type} enumeration on port {port}")
                    
                except Exception as e:
                    print_error(f"Error during {enum_type} enumeration: {str(e)}")
                    self.logger.error(f"Enumeration error: {str(e)}", exc_info=True)
        
        # Generate reports
        print_section("Generating Reports")
        
        ensure_directory(self.output_dir)
        
        # Create filename
        timestamp = get_timestamp()
        safe_target = sanitize_filename(self.target)
        base_filename = f"{safe_target}_{timestamp}"
        
        # Generate reports
        report_paths = generate_reports(
            self.scan_data,
            self.output_dir,
            base_filename
        )
        
        if report_paths:
            print_success("Reports generated successfully:")
            for report_type, path in report_paths.items():
                print_info(f"  {report_type.upper()}: {path}")
        else:
            print_error("Failed to generate reports")
        
        print_section("Scan Complete")
        print_success(f"Reconnaissance complete for {self.target}")
        
        return True
    
    def _run_enumeration(self, enum_type: str, port: int) -> Dict[str, Any]:
        """
        Run specific enumeration based on type
        
        Args:
            enum_type: Type of enumeration (web, ftp, ssh, smb, dns)
            port: Port number
            
        Returns:
            Enumeration results dictionary
        """
        if enum_type == 'web':
            # Ask about running additional tools
            run_tools = True
            if self.confirmation_mode:
                run_tools = get_user_confirmation(
                    "Run feroxbuster and sublist3r? (may take time)"
                )
            return enumerate_web(self.target, port, run_tools)
        
        elif enum_type == 'ftp':
            return enumerate_ftp(self.target, port)
        
        elif enum_type == 'ssh':
            return enumerate_ssh(self.target, port)
        
        elif enum_type == 'smb':
            return enumerate_smb(self.target, port)
        
        elif enum_type == 'dns':
            return enumerate_dns(self.target, port)
        
        return {}

# ============================================================================
# CLI INTERFACE
# ============================================================================

def parse_arguments():
    """Parse command-line arguments"""
    
    parser = argparse.ArgumentParser(
        description='Automated Reconnaissance & Enumeration Toolkit for Ethical Hacking & CTFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -t 192.168.1.100
  %(prog)s -t example.com -o ./my_reports
  %(prog)s -t 10.10.10.50 --no-confirm
  %(prog)s -t scanme.nmap.org --quick
  %(prog)s -t 192.168.1.100 --ports 1-10000 -v

Legal Notice:
  This tool is for AUTHORIZED security testing only.
  Only use on systems you own or have explicit permission to test.
  Unauthorized access to computer systems is illegal.
        '''
    )
    
    # Required arguments
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target IP address or domain name'
    )
    
    # Optional arguments
    parser.add_argument(
        '-o', '--output',
        default='./reports',
        help='Output directory for reports (default: ./reports)'
    )
    
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='Skip confirmation prompts and run all scans automatically'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick scan only (skip deep enumeration)'
    )
    
    parser.add_argument(
        '--ports',
        help='Specify custom port range (e.g., "1-10000")'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    return parser.parse_args()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create and run toolkit
        toolkit = ReconToolkit(args)
        success = toolkit.run()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n[!] Fatal error: {str(e)}")
        logging.error("Fatal error", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
