"""
Configuration file for the Cybersecurity Reconnaissance Toolkit
"""

import os

# ============================================================================
# GENERAL SETTINGS
# ============================================================================

# Enable/disable confirmation prompts before running each enumeration tool
CONFIRMATION_MODE = True

# Verbose output for debugging
VERBOSE = False

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Default output directory for reports
OUTPUT_DIR = "./reports"

# Report filename format (will be formatted with timestamp and target)
REPORT_FILENAME_FORMAT = "{target}_{timestamp}"

# ============================================================================
# SCAN SETTINGS
# ============================================================================

# Default nmap scan parameters
NMAP_QUICK_SCAN = "-sS -T4 --top-ports 1000"
NMAP_VERSION_SCAN = "-sV -sC -T4"
NMAP_TIMEOUT = 300  # seconds

# Default port range (None = use nmap defaults)
DEFAULT_PORT_RANGE = None

# ============================================================================
# TOOL PATHS
# ============================================================================
# Leave as None to use system PATH, or specify full path if needed

NMAP_PATH = None  # e.g., "C:\\Program Files\\Nmap\\nmap.exe"
FEROXBUSTER_PATH = None
SUBLIST3R_PATH = None
SMBCLIENT_PATH = None

# ============================================================================
# ENUMERATION SETTINGS
# ============================================================================

# Feroxbuster settings
FEROXBUSTER_WORDLIST = None  # Use default wordlist if None
FEROXBUSTER_THREADS = 10
FEROXBUSTER_TIMEOUT = 300  # seconds

# Sublist3r settings
SUBLIST3R_TIMEOUT = 180  # seconds

# DNS enumeration settings
DNS_TIMEOUT = 30  # seconds

# FTP enumeration settings
FTP_TIMEOUT = 30  # seconds

# SSH enumeration settings
SSH_TIMEOUT = 30  # seconds

# SMB enumeration settings
SMB_TIMEOUT = 60  # seconds

# Database enumeration settings
DB_TIMEOUT = 30  # seconds

# ============================================================================
# PORT MAPPINGS
# ============================================================================

# Map ports to enumeration modules
PORT_ENUM_MAPPING = {
    21: "ftp",
    22: "ssh",
    53: "dns",
    80: "web",
    139: "smb",
    443: "web",
    445: "smb",
    1433: "database",  # MSSQL
    3306: "database",  # MySQL
    5432: "database",  # PostgreSQL
    8080: "web",
    8443: "web",
}

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = None  # Set to a path to enable file logging
