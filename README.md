# Cybersecurity Reconnaissance Toolkit

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An automated reconnaissance and enumeration toolkit designed for ethical hacking and CTF competitions. This tool orchestrates various security tools (nmap, feroxbuster, sublist3r) to perform comprehensive target analysis.

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for:
- Ethical hacking and penetration testing
- CTF (Capture The Flag) competitions
- Educational purposes
- Authorized security assessments

**Only use this tool on systems you own or have explicit written permission to test.** Unauthorized access to computer systems is illegal and punishable by law.

## 🚀 Features

- **Automated Port Scanning**: Uses nmap for fast and accurate port detection
- **Service Version Detection**: Identifies services and their versions
- **Port-Specific Enumeration**:
  - **Web (80/443/8080/8443)**: HTTP headers, feroxbuster, sublist3r
  - **FTP (21)**: Banner grabbing, anonymous login checks
  - **SSH (22)**: Version detection, banner analysis
  - **SMB (139/445)**: Share enumeration
  - **DNS (53)**: Zone transfers, record queries
  - **Databases (1433/3306/5432)**: MySQL, PostgreSQL, MSSQL enumeration
- **User Confirmation**: Optional prompts before running each tool
- **Dual Reports**: Generates both JSON and styled HTML reports
- **Colored Output**: Easy-to-read terminal output with color coding

## 📋 Prerequisites

### Required Tools

- **Python 3.8+**
- **nmap** (critical - required for port scanning)

### Optional Tools

- **feroxbuster** - Web directory enumeration
- **sublist3r** - Subdomain discovery
- **smbclient** - SMB share enumeration

### Installation

#### Windows

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Install nmap
# Download from: https://nmap.org/download.html

# Install feroxbuster (optional)
# Download from: https://github.com/epi052/feroxbuster/releases

# Install sublist3r (optional)
pip install sublist3r

# Install database enumeration libraries (optional)
pip install -r requirements-db.txt
```

#### Linux

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install tools
sudo apt-get update
sudo apt-get install nmap smbclient

# Install feroxbuster
wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster_amd64.deb
sudo dpkg -i feroxbuster_amd64.deb

# Install sublist3r
pip install sublist3r

# Install database enumeration libraries (optional)
pip install -r requirements-db.txt
```

## 🎯 Usage

### Basic Usage

```bash
# Scan a target with confirmation prompts
python recon_toolkit.py -t 192.168.1.100

# Scan a domain
python recon_toolkit.py -t example.com
```

### Advanced Usage

```bash
# Custom output directory
python recon_toolkit.py -t 192.168.1.100 -o ./my_reports

# Skip confirmation prompts (auto-run)
python recon_toolkit.py -t 192.168.1.100 --no-confirm

# Quick scan only (no deep enumeration)
python recon_toolkit.py -t 192.168.1.100 --quick

# Custom port range
python recon_toolkit.py -t 192.168.1.100 --ports 1-10000

# Verbose mode for debugging
python recon_toolkit.py -t 192.168.1.100 -v

# Combine options
python recon_toolkit.py -t 10.10.10.50 -o ./ctf_reports --no-confirm -v
```

### Help

```bash
# Display help and all options
python recon_toolkit.py -h
python recon_toolkit.py --help
```

## 📊 Output

The tool generates two types of reports:

1. **JSON Report**: Machine-readable format for further processing
2. **HTML Report**: Styled, human-readable report with:
   - Executive summary
   - Port scan results table
   - Service-specific enumeration findings
   - Timestamps and metadata

Reports are saved in the output directory with timestamps:
```
reports/
├── 192.168.1.100_20231123_143022.json
└── 192.168.1.100_20231123_143022.html
```

## ⚙️ Configuration

Edit `config.py` to customize:

- Scan timeouts
- Tool paths (if not in system PATH)
- Feroxbuster wordlists
- Confirmation mode default
- Port mappings for enumeration

## 🔧 Project Structure

```
Cybersecurity/
├── recon_toolkit.py          # Main application
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── requirements-db.txt        # Optional database libraries
├── README.md                  # This file
├── DATABASE_ENUM.md           # Database enumeration guide
└── modules/
    ├── port_scanner.py        # Nmap integration
    ├── web_enum.py            # Web enumeration
    ├── ftp_enum.py            # FTP enumeration
    ├── ssh_enum.py            # SSH enumeration
    ├── smb_enum.py            # SMB enumeration
    ├── dns_enum.py            # DNS enumeration
    ├── db_enum.py             # Database enumeration
    ├── utils.py               # Utility functions
    └── report_generator.py    # Report generation
```

## 🎓 CTF Tips

- Use `--quick` for initial reconnaissance
- Use `--no-confirm` once you trust the workflow
- Check HTML reports for easy-to-read summaries
- Use JSON reports for scripting and automation
- Customize port ranges based on CTF hints

## 🤝 Contributing

This is a personal toolkit for ethical hacking and CTFs. Feel free to fork and customize for your needs!

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [nmap](https://nmap.org/) - Network scanning
- [feroxbuster](https://github.com/epi052/feroxbuster) - Web enumeration
- [sublist3r](https://github.com/aboul3la/Sublist3r) - Subdomain discovery
- [python-nmap](https://pypi.org/project/python-nmap/) - Python nmap wrapper

---

**Remember**: Always obtain proper authorization before testing any system!
