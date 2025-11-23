# Quick Start Guide - VM Setup

This guide will help you set up and run the Recon Toolkit in your VM.

## Step 1: Install Python Dependencies

```bash
# Navigate to the project directory
cd Cybersecurity

# Install Python packages
pip install -r requirements.txt
```

**Required packages:**
- python-nmap
- requests
- beautifulsoup4
- jinja2
- colorama

## Step 2: Install External Tools

### Critical (Required)
- **nmap**: Download from https://nmap.org/download.html

### Optional (Recommended for full functionality)
- **feroxbuster**: https://github.com/epi052/feroxbuster/releases
- **sublist3r**: `pip install sublist3r`
- **smbclient**: Usually pre-installed on Linux, or install via package manager

## Step 3: Verify Installation

```bash
# Test the help menu
python recon_toolkit.py --help

# Check dependencies
python recon_toolkit.py -t scanme.nmap.org --quick
```

## Step 4: Run Your First Scan

### Safe Test Target
```bash
# scanme.nmap.org is a safe, legal target for testing
python recon_toolkit.py -t scanme.nmap.org
```

### Your Own Target
```bash
# Replace with your target IP/domain
python recon_toolkit.py -t <your-target>
```

## Common Commands

```bash
# Quick scan (no deep enumeration)
python recon_toolkit.py -t <target> --quick

# Full scan with confirmations
python recon_toolkit.py -t <target>

# Auto-run without confirmations
python recon_toolkit.py -t <target> --no-confirm

# Custom output directory
python recon_toolkit.py -t <target> -o ./my_scans

# Verbose mode for debugging
python recon_toolkit.py -t <target> -v
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'nmap'"
```bash
pip install python-nmap
```

### "nmap not found"
- Make sure nmap is installed and in your system PATH
- On Windows: Add nmap installation directory to PATH
- On Linux: `sudo apt-get install nmap`

### "feroxbuster not installed"
- This is optional - the tool will skip web directory enumeration
- Install from: https://github.com/epi052/feroxbuster/releases

## File Structure After Setup

```
Cybersecurity/
├── recon_toolkit.py          # Main script
├── config.py                  # Configuration
├── requirements.txt           # Python deps
├── README.md                  # Full documentation
├── QUICKSTART.md             # This file
├── modules/
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── web_enum.py
│   ├── ftp_enum.py
│   ├── ssh_enum.py
│   ├── smb_enum.py
│   ├── dns_enum.py
│   ├── utils.py
│   └── report_generator.py
└── reports/                   # Created automatically
    ├── <target>_<timestamp>.json
    └── <target>_<timestamp>.html
```

## Next Steps

1. Install all dependencies in your VM
2. Test with scanme.nmap.org
3. Review the generated HTML report
4. Customize `config.py` if needed
5. Use in your CTF competitions!

---

**Remember**: Only scan systems you own or have permission to test!
