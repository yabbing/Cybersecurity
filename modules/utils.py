"""
Utility functions for the Cybersecurity Reconnaissance Toolkit
"""

import subprocess
import sys
import os
import shutil
from datetime import datetime
from typing import Optional, Tuple, List
import logging
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(verbose: bool = False, log_file: Optional[str] = None):
    """
    Configure logging for the application
    
    Args:
        verbose: Enable verbose (DEBUG) logging
        log_file: Optional file path for log output
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# ============================================================================
# TOOL AVAILABILITY CHECKING
# ============================================================================

def check_tool_installed(tool_name: str, tool_path: Optional[str] = None) -> bool:
    """
    Check if a tool is installed and available
    
    Args:
        tool_name: Name of the tool to check
        tool_path: Optional custom path to the tool
        
    Returns:
        True if tool is available, False otherwise
    """
    if tool_path and os.path.exists(tool_path):
        return True
    
    # Check if tool is in system PATH
    return shutil.which(tool_name) is not None

def check_all_dependencies() -> dict:
    """
    Check all required tools and return their availability status
    
    Returns:
        Dictionary mapping tool names to availability status
    """
    tools = {
        'nmap': check_tool_installed('nmap'),
        'feroxbuster': check_tool_installed('feroxbuster'),
        'sublist3r': check_tool_installed('sublist3r'),
        'smbclient': check_tool_installed('smbclient'),
    }
    
    return tools

def print_dependency_status(tools_status: dict):
    """
    Print the status of tool dependencies with color coding
    
    Args:
        tools_status: Dictionary of tool availability status
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Dependency Check")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    for tool, available in tools_status.items():
        status = f"{Fore.GREEN}✓ Installed" if available else f"{Fore.RED}✗ Not Found"
        print(f"  {tool:15} {status}{Style.RESET_ALL}")
    
    print()
    
    # Check if any critical tools are missing
    critical_tools = ['nmap']
    missing_critical = [tool for tool in critical_tools if not tools_status.get(tool, False)]
    
    if missing_critical:
        print(f"{Fore.RED}⚠ Critical tools missing: {', '.join(missing_critical)}")
        print(f"{Fore.YELLOW}The toolkit requires nmap to function.{Style.RESET_ALL}\n")
        return False
    
    # Warn about optional tools
    optional_tools = ['feroxbuster', 'sublist3r', 'smbclient']
    missing_optional = [tool for tool in optional_tools if not tools_status.get(tool, False)]
    
    if missing_optional:
        print(f"{Fore.YELLOW}⚠ Optional tools missing: {', '.join(missing_optional)}")
        print(f"{Fore.YELLOW}Some enumeration features will be limited.{Style.RESET_ALL}\n")
    
    return True

# ============================================================================
# COMMAND EXECUTION
# ============================================================================

def run_command(
    command: List[str],
    timeout: int = 60,
    capture_output: bool = True
) -> Tuple[int, str, str]:
    """
    Execute a command with timeout and error handling
    
    Args:
        command: Command and arguments as a list
        timeout: Timeout in seconds
        capture_output: Whether to capture stdout/stderr
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.debug(f"Running command: {' '.join(command)}")
        
        result = subprocess.run(
            command,
            timeout=timeout,
            capture_output=capture_output,
            text=True
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout} seconds")
        return -1, "", f"Command timed out after {timeout} seconds"
        
    except FileNotFoundError:
        logger.error(f"Command not found: {command[0]}")
        return -1, "", f"Command not found: {command[0]}"
        
    except Exception as e:
        logger.error(f"Error running command: {str(e)}")
        return -1, "", str(e)

# ============================================================================
# USER INTERACTION
# ============================================================================

def get_user_confirmation(prompt: str, default: bool = True) -> bool:
    """
    Ask user for confirmation
    
    Args:
        prompt: Question to ask the user
        default: Default answer if user just presses Enter
        
    Returns:
        True if user confirms, False otherwise
    """
    default_str = "Y/n" if default else "y/N"
    
    while True:
        response = input(f"{Fore.YELLOW}[?] {prompt} [{default_str}]: {Style.RESET_ALL}").strip().lower()
        
        if not response:
            return default
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print(f"{Fore.RED}Please answer 'y' or 'n'{Style.RESET_ALL}")

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def print_banner():
    """Print the tool banner"""
    banner = f"""
{Fore.CYAN}{'='*60}
   ____                   _____           _ _    _ _   
  |  _ \\ ___  ___ ___  _ |_   _|__   ___ | | | _(_) |_ 
  | |_) / _ \\/ __/ _ \\| '_ \\| |/ _ \\ / _ \\| | |/ / | __|
  |  _ <  __/ (_| (_) | | | | | (_) | (_) | |   <| | |_ 
  |_| \\_\\___|\\___\\___/|_| |_|_|\\___/ \\___/|_|_|\\_\\_|\\__|
                                                        
  Automated Reconnaissance & Enumeration Toolkit
  For Ethical Hacking & CTF Competitions
{'='*60}{Style.RESET_ALL}
"""
    print(banner)

def print_section(title: str):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_success(message: str):
    """Print a success message"""
    print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Print an error message"""
    print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Print an info message"""
    print(f"{Fore.BLUE}[i] {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

# ============================================================================
# FILE OPERATIONS
# ============================================================================

def ensure_directory(directory: str):
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    os.makedirs(directory, exist_ok=True)

def get_timestamp() -> str:
    """
    Get current timestamp as a string
    
    Returns:
        Timestamp string in format YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename
