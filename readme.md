<a href="https://github.com/Athexhacker/ReconPro"><img src="/src/logo.png" alt="0" border="0" /></a> 

# 🔍 Network Security Toolkit - Real-Time Network Scanner & Monitoring Tool

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

A comprehensive, professional-grade network security toolkit with a modern GUI interface. This tool combines multiple network scanning, monitoring, and analysis capabilities into one powerful application.

## ⚠️ LEGAL DISCLAIMER

**IMPORTANT: This tool is for AUTHORIZED SECURITY TESTING ONLY!**

Scanning networks, systems, or devices without explicit written permission is ILLEGAL and may violate:
- Computer Fraud and Abuse Act (CFAA)
- Various state and international laws
- Terms of service agreements
- Privacy regulations

**By using this tool, you certify that you have:**
- ✓ Written permission to test ALL target systems
- ✓ Authority from the network owner
- ✓ Proper authorization documentation

Use only on networks you own or have written authorization to test.

---

## 📋 Table of Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed Usage](#-detailed-usage)
- [Tools Overview](#-tools-overview)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 🌐 Network Scanner
- **ARP Scan**: Discover all devices on local network using ARP requests
- **Ping Sweep**: ICMP echo requests to find live hosts across subnets
- **MAC Address Detection**: Identify device manufacturers
- **Hostname Resolution**: Automatic reverse DNS lookup

### 🔌 Port Scanner (Nmap Integration)
- Multiple scan types (TCP Connect, SYN Stealth, UDP)
- Service version detection
- OS fingerprinting
- Configurable port ranges
- Real-time scan progress

### 🌍 OSINT Tools
- **IP Geolocation**: Country, city, ISP, coordinates via ip-api.com
- **WHOIS Lookup**: Domain registration details
- **DNS Records**: A, AAAA, MX, TXT, NS, CNAME records
- **Reverse DNS**: PTR record lookup
- **Subdomain Discovery**: Common subdomain enumeration

### ⚠️ Vulnerability Scanner
- SSL/TLS security analysis
- Security headers checker (HSTS, CSP, X-Frame-Options)
- Common port risk assessment
- Admin panel discovery
- Outdated software detection

### 📡 Packet Sniffer
- Live packet capture using Scapy
- Protocol filtering (TCP/UDP/ICMP)
- Real-time packet display
- Configurable capture count
- Interface selection

### 📊 Continuous Monitoring
- Real-time host status monitoring
- Change detection alerts
- Popup notifications
- Configurable alert triggers

### 📈 Reporting
- Comprehensive PDF reports
- HTML export with charts
- CSV data export
- JSON results storage
- Custom report generation

---

## 📸 Screenshots

*[Screenshots would be inserted here]*

| Main Dashboard | Network Scanner | Port Scanner |
|:---:|:---:|:---:|
|![Main](screenshots/main.png)|![Network](screenshots/network.png)|![Port](screenshots/port.png)|

| OSINT Tools | Vulnerability Scanner | Packet Sniffer |
|:---:|:---:|:---:|
|![OSINT](screenshots/osint.png)|![Vuln](screenshots/vuln.png)|![Sniffer](screenshots/sniffer.png)|

---

## 🔧 Requirements

### System Requirements
- **Python**: 3.6 or higher
- **RAM**: 512MB minimum (2GB recommended)
- **Disk Space**: 100MB for tools and dependencies
- **OS**: Windows 7+, Linux (any distribution), macOS 10.12+

### Core Dependencies
```bash
# Essential libraries
python-nmap>=0.7.1     # Nmap integration
python-whois>=0.8.0    # WHOIS lookups
dnspython>=2.2.0       # DNS queries
ping3>=4.0.0          # ICMP ping
requests>=2.28.0       # HTTP requests

# Optional but recommended
scapy>=2.4.5          # Packet manipulation (for ARP scan & sniffer)
reportlab>=3.6.0      # PDF report generation
jinja2>=3.1.0         # HTML template rendering
```

### External Tools
- **Nmap**: Must be installed separately ([Download Nmap](https://nmap.org/download.html))
  - Windows: Download installer from nmap.org
  - Linux: `sudo apt-get install nmap` (Debian/Ubuntu)
  - macOS: `brew install nmap`

---

## 📥 Installation

### Step 1: Clone or Download
```bash
# Clone the repository
git clone https://github.com/Athexhacker/ReconPro.git
cd ReconPro

# Or download the script directly
wget https://raw.githubusercontent.com/Athexhacker/ReconPro/main/run.py
```

### Step 2: Install Python Dependencies
```bash
# Install all required packages
pip install python-nmap python-whois dnspython ping3 requests

# Optional: Install additional features
pip install scapy reportlab jinja2
```

### Step 3: Install Nmap
#### Windows:
1. Download installer from [https://nmap.org/download.html](https://nmap.org/download.html)
2. Run installer (ensure "Add Nmap to PATH" is checked)

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install nmap
```

#### Linux (CentOS/RHEL):
```bash
sudo yum install nmap
```

#### macOS:
```bash
brew install nmap
```

### Step 4: Verify Installation
```bash
# Test Nmap installation
nmap --version

# Test Python dependencies
python -c "import nmap; import whois; import dns; import ping3; print('All good!')"
```

---

## 🚀 Quick Start

### Basic Usage
```bash
# Run with default settings
python run.py

# Run with admin privileges (required for some features)
sudo python run.py  # Linux/macOS
# Right-click and "Run as Administrator" on Windows
```

### First Scan Workflow
1. **Accept the legal warning** when prompted
2. **Add a target** (IP address or domain name)
3. **Select a tool tab** (e.g., Network Scanner)
4. **Configure options** (port range, scan type, etc.)
5. **Click "Start Scan"** and watch real results appear
6. **Generate a report** from the Results tab

### Quick Commands
| Action | Menu Path | Shortcut |
|--------|-----------|----------|
| Add Target | Enter in input field | Ctrl+A |
| Start Scan | Tools → Select Tool | Ctrl+S |
| Stop Monitoring | Monitoring → Stop | Ctrl+Shift+S |
| Generate Report | File → Export Report | Ctrl+R |
| New Session | File → New Session | Ctrl+N |
| Exit | File → Exit | Ctrl+Q |

---

## 📖 Detailed Usage

### 1. Network Scanner Tab

**Purpose**: Discover all live hosts on your network

**Configuration**:
- **Network Range**: CIDR notation (e.g., `192.168.1.0/24`)
- **Scan Type**: ARP (faster, local network only) or ICMP Ping (works across subnets)

**Example**:
```python
# Scan entire local network
Network Range: 192.168.1.0/24
Click "ARP Scan"

# Sample Output:
Found 5 devices:
IP Address        MAC Address
192.168.1.1       aa:bb:cc:dd:ee:ff  (Router)
192.168.1.100     11:22:33:44:55:66  (Windows PC)
  └─ Hostname: DESKTOP-ABC123
```

### 2. Port Scanner Tab

**Purpose**: Identify open ports and running services

**Configuration**:
- **Port Range**: Start and end ports (e.g., 1-1024)
- **Scan Type**: Select from dropdown
  - TCP Connect Scan (-sT): Complete TCP handshake
  - SYN Stealth Scan (-sS): Half-open scanning
  - UDP Scan (-sU): UDP port scanning
  - Service Version (-sV): Detect service versions
  - OS Detection (-O): Identify operating system
  - Aggressive Scan (-A): Enable all advanced options

**Example**:
```bash
Target: scanme.nmap.org
Port Range: 1-1000
Scan Type: Service Version (-sV)

# Sample Output:
Host: 45.33.32.156 (scanme.nmap.org)
State: up

Protocol: tcp
  22/tcp    open     ssh     OpenSSH 6.6.1p1
  80/tcp    open     http    Apache httpd 2.4.7
  9929/tcp  open     nping-echo Nping echo
```

### 3. OSINT Tools Tab

**Purpose**: Gather public information about targets

**Available Modules**:
- **IP Geolocation**: Physical location data
- **WHOIS**: Domain registration information
- **DNS Records**: All DNS record types
- **Reverse DNS**: PTR record lookup

**Example Output**:
```
OSINT Report for: example.com

📍 IP GEOLOCATION:
  Country: United States
  Region: California
  City: Los Angeles
  ISP: Example ISP Inc.
  Coordinates: 34.0522, -118.2437

📋 WHOIS INFORMATION:
  Registrar: Example Registrar
  Creation Date: 1995-08-14
  Name Servers: a.iana-servers.net, b.iana-servers.net

🔍 DNS RECORDS:
  A Records:
    93.184.216.34
  MX Records:
    10 mail.example.com
```

### 4. Vulnerability Scanner Tab

**Purpose**: Identify common security issues

**Checks Performed**:
- **SSL/TLS Issues**: Certificate validation, protocol support
- **Security Headers**: HSTS, CSP, X-Frame-Options
- **Open Ports Risk**: Categorized by risk level
- **Admin Panels**: Discovery of common admin paths

**Risk Assessment**:
| Port | Service | Risk Level |
|------|---------|------------|
| 21 | FTP | HIGH - Cleartext credentials |
| 23 | Telnet | HIGH - Unencrypted |
| 445 | SMB | HIGH - Common attack vector |
| 22 | SSH | MEDIUM - Needs monitoring |
| 80/443 | HTTP/HTTPS | LOW - Standard services |

### 5. Packet Sniffer Tab

**Purpose**: Capture and analyze live network traffic

**Requirements**:
- Admin/root privileges
- Scapy library installed
- Proper network interface selected

**Configuration**:
- **Filter**: BPF syntax (e.g., "tcp port 80", "udp", "icmp")
- **Count**: Number of packets to capture
- **Interface**: Network interface to listen on

**Example Capture**:
```
[14:23:45] TCP: 192.168.1.100:54321 -> 93.184.216.34:80
[14:23:46] TCP: 93.184.216.34:80 -> 192.168.1.100:54321
[14:23:47] ICMP: 192.168.1.1 -> 192.168.1.100 (Type: 8)
```

### 6. Monitoring & Alerts

**Purpose**: Continuous tracking of target status

**Alert Triggers**:
- Host goes offline
- Host comes online
- New port opens
- Service changes

**Configuration**:
1. Click "Set Alerts" in Monitoring menu
2. Select trigger conditions
3. Choose notification method
4. Start monitoring

---

---

## 🔍 Troubleshooting

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| ARP scan returns no results | Missing privileges | Run as admin/root |
| | Wrong network range | Verify network range (try 192.168.0.0/24 or 10.0.0.0/24) |
| | Firewall blocking | Temporarily disable firewall for testing |
| Nmap not found | Nmap not installed | Install Nmap from nmap.org |
| | Nmap not in PATH | Add Nmap to system PATH |
| Packet sniffer fails | Scapy not installed | `pip install scapy` |
| | Wrong interface | Check available interfaces in dropdown |
| API calls failing | Rate limited | Wait 60 seconds between requests |
| | No internet | Check internet connection |
| GUI not displaying | Tkinter missing | `sudo apt-get install python3-tk` (Linux) |
| Permission denied | Insufficient rights | Run with admin/root privileges |

### Debug Mode
```bash
# Enable verbose logging
python run.py --debug

# Log to file
python run.py --logfile scan.log
```

---

## 📚 API Reference

### Internal APIs Used

| API | Endpoint | Rate Limit | Purpose |
|-----|----------|------------|---------|
| ip-api.com | `http://ip-api.com/json/{ip}` | 45/min | Geolocation |
| whois | Local library | N/A | Domain registration |
| DNS | System resolver | N/A | DNS lookups |


---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/Athexhacker/NMAP-GUI.git
cd NMAP-GUI

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings for all functions
- Include type hints
- Write unit tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---


## 🙏 Acknowledgments

- **Nmap** - For the incredible scanning engine
- **Scapy** - For packet manipulation capabilities
- **ip-api.com** - For free geolocation API
- **Python Community** - For amazing libraries and tools
- **All Contributors** - Who help improve this tool

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-15 | Initial release |
| 1.1.0 | 2024-02-01 | Added packet sniffer |
| 1.2.0 | 2024-03-01 | Enhanced reporting |
| 1.3.0 | 2024-04-01 | Monitoring & alerts |

---

**Made with ❤️ for the security community**

*Remember: With great power comes great responsibility. Use ethically!*