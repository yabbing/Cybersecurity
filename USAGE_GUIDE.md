# Usage Guide - How to Run the Reconnaissance Toolkit

## Prerequisites

Before running the toolkit, make sure you have:

### 1. Install Python Dependencies
```bash
# Navigate to the project directory
cd C:\Users\sabba\OneDrive\Desktop\Cybersecurity

# Install required Python packages
pip install -r requirements.txt
```

### 2. Install Required Tools
- **nmap** (REQUIRED) - Download from https://nmap.org/download.html
  - On Windows: Install and add to PATH
  - On Linux: `sudo apt-get install nmap`

### 3. Install Optional Tools (Recommended)
```bash
# For enhanced web enumeration
# Download feroxbuster from: https://github.com/epi052/feroxbuster/releases

# For subdomain discovery
pip install sublist3r

# For database enumeration (MySQL, PostgreSQL, MSSQL)
pip install -r requirements-db.txt
```

---

## Basic Usage

### Command Format
```bash
python recon_toolkit.py -t <target> [options]
```

### Example 1: Basic Scan with Confirmations
```bash
python recon_toolkit.py -t 192.168.1.100
```

**What happens:**
1. Toolkit scans the target for open ports using nmap
2. Displays all open ports found
3. **Asks you for confirmation** before running each enumeration tool
4. Generates JSON and HTML reports

**Example Output:**
```
╔══════════════════════════════════════════════════════════╗
║     CYBERSECURITY RECONNAISSANCE TOOLKIT                 ║
║     For Ethical Hacking & CTF Competitions Only          ║
╚══════════════════════════════════════════════════════════╝

[*] Dependency Check
[+] nmap: INSTALLED
[+] feroxbuster: INSTALLED
[+] sublist3r: INSTALLED

[*] Port Scanning: 192.168.1.100
[*] Target: 192.168.1.100

[+] Found 4 open ports
  Port 22/tcp - ssh OpenSSH 8.2
  Port 80/tcp - http Apache 2.4.41
  Port 3306/tcp - mysql
  Port 5432/tcp - postgresql

[*] Service Enumeration

Run SSH enumeration on port 22? [y/N] y
[*] Running ssh enumeration on port 22...
[+] Completed ssh enumeration on port 22

Run WEB enumeration on port 80? [y/N] y
Run feroxbuster and sublist3r? (may take time) [y/N] y
[*] Running web enumeration on port 80...
[+] Completed web enumeration on port 80

Run DATABASE enumeration on port 3306? [y/N] y
[*] Running database enumeration on port 3306...
[+] Completed database enumeration on port 3306

Run DATABASE enumeration on port 5432? [y/N] y
[*] Running database enumeration on port 5432...
[+] Completed database enumeration on port 5432

[*] Generating Reports

[+] Reports generated successfully:
  JSON: ./reports/192.168.1.100_20231126_234500.json
  HTML: ./reports/192.168.1.100_20231126_234500.html

[*] Scan Complete
[+] Reconnaissance complete for 192.168.1.100
```

---

## Advanced Usage

### Example 2: Auto-Run (No Confirmations)
```bash
python recon_toolkit.py -t 192.168.1.100 --no-confirm
```

**What happens:**
- Scans the target
- **Automatically runs ALL enumeration tools** without asking
- Generates reports

**Use when:** You trust the workflow and want fast results

---

### Example 3: Quick Scan Only (No Deep Enumeration)
```bash
python recon_toolkit.py -t 192.168.1.100 --quick
```

**What happens:**
- Only performs port scanning
- **Skips all enumeration** (no feroxbuster, no database checks, etc.)
- Generates basic report with port information

**Use when:** You just want to know what ports are open

---

### Example 4: Custom Output Directory
```bash
python recon_toolkit.py -t 192.168.1.100 -o ./my_scans
```

**What happens:**
- Saves reports to `./my_scans/` instead of `./reports/`

---

### Example 5: Custom Port Range
```bash
python recon_toolkit.py -t 192.168.1.100 --ports 1-10000
```

**What happens:**
- Scans ports 1-10000 instead of default top 1000 ports

---

### Example 6: Verbose Mode (Debugging)
```bash
python recon_toolkit.py -t 192.168.1.100 -v
```

**What happens:**
- Shows detailed debug information
- Useful for troubleshooting

---

### Example 7: Combine Multiple Options
```bash
python recon_toolkit.py -t 10.10.10.50 -o ./ctf_scans --no-confirm -v
```

**What happens:**
- Scans target 10.10.10.50
- Saves to `./ctf_scans/`
- Auto-runs everything without confirmations
- Shows verbose output

---

## What Each Enumeration Tool Does

### SSH Enumeration (Port 22)
- Grabs SSH banner
- Detects SSH version
- Identifies server software (OpenSSH, etc.)

### FTP Enumeration (Port 21)
- Grabs FTP banner
- Tests for anonymous login
- Checks FTP version

### Web Enumeration (Ports 80, 443, 8080, 8443)
- Grabs HTTP headers
- Runs **feroxbuster** for directory/file discovery
- Runs **sublist3r** for subdomain enumeration
- Detects web server and technologies

### SMB Enumeration (Ports 139, 445)
- Enumerates SMB shares
- Checks for anonymous access
- Lists available shares

### DNS Enumeration (Port 53)
- Attempts zone transfer (AXFR)
- Queries DNS records (A, AAAA, MX, NS, TXT, SOA)
- Enumerates DNS information

### Database Enumeration (Ports 1433, 3306, 5432) ✨ NEW
- **MySQL (3306)**: Banner grab, version detection, auth check
- **PostgreSQL (5432)**: Version detection, auth check
- **MSSQL (1433)**: Version detection, banner info, auth check

---

## Understanding the Reports

### JSON Report
Machine-readable format for scripting and automation.

**Location:** `./reports/<target>_<timestamp>.json`

**Example:**
```json
{
  "target": "192.168.1.100",
  "scan_date": "2023-11-26 23:45:00",
  "ports": [
    {
      "port": 3306,
      "state": "open",
      "service": "mysql",
      "version": "MySQL 8.0.27"
    }
  ],
  "enumeration_results": {
    "database_3306": {
      "port": 3306,
      "service": "database (mysql)",
      "db_type": "mysql",
      "version": "8.0.27",
      "banner": "8.0.27-0ubuntu0.20.04.1",
      "accessible": true,
      "authentication_required": true
    }
  }
}
```

### HTML Report
Human-readable styled report with tables and formatting.

**Location:** `./reports/<target>_<timestamp>.html`

**Contains:**
- Executive summary
- Port scan results table
- Service-specific enumeration findings
- Timestamps and metadata

**Open in browser:** Double-click the HTML file to view in your web browser

---

## Common Scenarios

### Scenario 1: CTF Competition
```bash
# Quick initial scan
python recon_toolkit.py -t ctf-box.local --quick

# Full scan with all tools
python recon_toolkit.py -t ctf-box.local --no-confirm

# Check the HTML report for findings
start ./reports/ctf-box_*.html
```

### Scenario 2: Penetration Test (Authorized)
```bash
# Comprehensive scan with confirmations
python recon_toolkit.py -t client-server.com -o ./client_pentest

# Review each step before proceeding
# Answer y/n to each enumeration prompt
```

### Scenario 3: Bug Bounty (Authorized Scope)
```bash
# Scan specific ports
python recon_toolkit.py -t target.example.com --ports 80,443,8080,8443

# Focus on web enumeration
```

### Scenario 4: Database Server Assessment
```bash
# Scan database ports specifically
python recon_toolkit.py -t db-server.local --ports 1433,3306,5432

# The toolkit will automatically run database enumeration
```

---

## Troubleshooting

### "nmap not found"
**Solution:**
- Install nmap from https://nmap.org/download.html
- Add nmap to your system PATH
- On Windows: `C:\Program Files\Nmap\` should be in PATH

### "feroxbuster not installed"
**Solution:**
- This is optional - the toolkit will skip web directory enumeration
- Install from: https://github.com/epi052/feroxbuster/releases
- Or run with `--quick` to skip enumeration

### "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
- Database libraries are optional
- Install with: `pip install -r requirements-db.txt`
- The toolkit will still work but with limited database enumeration

### "Permission denied" or "Access denied"
**Solution:**
- You may need administrator/root privileges for some scans
- On Windows: Run PowerShell/CMD as Administrator
- On Linux: Use `sudo python recon_toolkit.py -t <target>`

### No open ports found
**Solution:**
- Verify the target IP/hostname is correct
- Check if a firewall is blocking the scan
- Try a different port range: `--ports 1-65535`

---

## Command Reference

### Required Arguments
- `-t, --target` - Target IP address or domain name

### Optional Arguments
- `-o, --output` - Output directory for reports (default: ./reports)
- `--no-confirm` - Skip confirmation prompts and run all scans automatically
- `--quick` - Run quick scan only (skip deep enumeration)
- `--ports` - Specify custom port range (e.g., "1-10000")
- `-v, --verbose` - Enable verbose output for debugging
- `-h, --help` - Display help and all options

---

## Best Practices

### 1. Always Get Authorization
- Only scan systems you own or have written permission to test
- Unauthorized scanning is illegal

### 2. Start with Quick Scan
```bash
python recon_toolkit.py -t <target> --quick
```
- Get a quick overview first
- Then run full enumeration if needed

### 3. Use Confirmation Mode First
- Don't use `--no-confirm` until you understand what each tool does
- Review each enumeration step

### 4. Save Reports Organized
```bash
python recon_toolkit.py -t <target> -o ./projects/client_name/scans
```
- Keep reports organized by project/client

### 5. Review HTML Reports
- HTML reports are easier to read than JSON
- Share HTML reports with team members
- Use JSON for automation/scripting

---

## Next Steps

1. **Test the toolkit:**
   ```bash
   python recon_toolkit.py -t scanme.nmap.org
   ```

2. **Install optional tools** for full functionality:
   ```bash
   pip install -r requirements-db.txt
   pip install sublist3r
   ```

3. **Read the documentation:**
   - `README.md` - Full documentation
   - `DATABASE_ENUM.md` - Database enumeration details
   - `QUICKSTART.md` - Quick start guide

4. **Customize configuration:**
   - Edit `config.py` to adjust timeouts, paths, and settings

---

## Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for:
- Ethical hacking and penetration testing
- CTF (Capture The Flag) competitions
- Educational purposes
- Authorized security assessments

**Only use this tool on systems you own or have explicit written permission to test.**

Unauthorized access to computer systems is illegal and punishable by law.

---

**Remember:** Always obtain proper authorization before testing any system!
