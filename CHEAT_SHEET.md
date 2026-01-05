# Quick Command Cheat Sheet

## 🚀 Basic Commands

### 1. Simple Scan (with confirmations)
```bash
python recon_toolkit.py -t 192.168.1.100
```
**What it does:** Scans target, asks before running each tool

---

### 2. Auto-Run Everything
```bash
python recon_toolkit.py -t 192.168.1.100 --no-confirm
```
**What it does:** Scans and runs ALL tools automatically (no questions)

---

### 3. Quick Scan Only
```bash
python recon_toolkit.py -t 192.168.1.100 --quick
```
**What it does:** Only scans ports, skips enumeration tools

---

### 4. Custom Output Folder
```bash
python recon_toolkit.py -t 192.168.1.100 -o ./my_scans
```
**What it does:** Saves reports to `./my_scans/` folder

---

### 5. Scan Specific Ports
```bash
python recon_toolkit.py -t 192.168.1.100 --ports 1-10000
```
**What it does:** Scans ports 1-10000 instead of default

---

### 6. Verbose Mode (Debug)
```bash
python recon_toolkit.py -t 192.168.1.100 -v
```
**What it does:** Shows detailed debug information

---

## 🎯 Common Use Cases

### CTF Competition
```bash
# Quick overview
python recon_toolkit.py -t ctf-box.local --quick

# Full scan
python recon_toolkit.py -t ctf-box.local --no-confirm
```

### Penetration Test
```bash
# Careful scan with confirmations
python recon_toolkit.py -t client-server.com -o ./client_pentest
```

### Database Server
```bash
# Focus on database ports
python recon_toolkit.py -t db-server.local --ports 1433,3306,5432
```

### Web Application
```bash
# Focus on web ports
python recon_toolkit.py -t webapp.com --ports 80,443,8080,8443
```

---

## 📊 What Gets Scanned Automatically

| Port | Service | What Gets Enumerated |
|------|---------|---------------------|
| 21 | FTP | Banner, anonymous login |
| 22 | SSH | Version, banner |
| 53 | DNS | Zone transfer, records |
| 80/443 | HTTP/HTTPS | Headers, directories, subdomains |
| 139/445 | SMB | Shares, anonymous access |
| 1433 | MSSQL | Version, auth check |
| 3306 | MySQL | Version, banner, auth check |
| 5432 | PostgreSQL | Version, auth check |
| 8080/8443 | HTTP/HTTPS | Headers, directories, subdomains |

---

## 📁 Where Are Reports Saved?

**Default location:**
```
./reports/
├── <target>_<timestamp>.json    (Machine-readable)
└── <target>_<timestamp>.html    (Human-readable)
```

**Example:**
```
./reports/
├── 192.168.1.100_20231126_234500.json
└── 192.168.1.100_20231126_234500.html
```

**Open HTML report:**
- Windows: Double-click the `.html` file
- Linux: `firefox ./reports/*.html`

---

## ⚙️ Installation Quick Reference

### Required
```bash
# Python packages
pip install -r requirements.txt

# nmap (download from https://nmap.org/download.html)
```

### Optional (Recommended)
```bash
# Database enumeration
pip install -r requirements-db.txt

# Subdomain discovery
pip install sublist3r

# Web directory enumeration
# Download feroxbuster from: https://github.com/epi052/feroxbuster/releases
```

---

## 🆘 Help Command

```bash
python recon_toolkit.py --help
```

Shows all available options and examples.

---

## ⚠️ Legal Notice

**ONLY USE ON AUTHORIZED SYSTEMS**
- Systems you own
- Systems you have written permission to test
- CTF competition targets
- Educational lab environments

**Unauthorized scanning is ILLEGAL!**

---

## 🔗 Documentation Files

- `USAGE_GUIDE.md` - Detailed usage examples (this file)
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `DATABASE_ENUM.md` - Database enumeration details
- `IMPLEMENTATION_SUMMARY.md` - What was added

---

**Quick Start:**
```bash
cd C:\Users\sabba\OneDrive\Desktop\Cybersecurity
python recon_toolkit.py -t scanme.nmap.org
```
