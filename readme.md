


# 🔓 DeobX - Advanced Deobfuscation Tool

[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com/Athexblackhat/deobx)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey.svg)]()

> **DeobX** is a powerful, feature-rich deobfuscation tool designed to reverse engineer and clean obfuscated Bash and Python scripts. With its intuitive CLI interface, advanced detection algorithms, and beautiful terminal animations, DeobX makes script analysis both efficient and enjoyable.

---

## ✨ Features

### 🎯 Core Capabilities
- ✅ **Multi-language Support** — Handles both Bash and Python scripts
- ✅ **Advanced Detection** — Identifies 15+ obfuscation techniques
- ✅ **Recursive Decoding** — Handles multiple layers of obfuscation
- ✅ **Intelligent Analysis** — Confidence-based technique detection
- ✅ **Auto-formatting** — Beautifies Python code with autopep8

### 🔍 Detected Obfuscation Techniques

| Technique | Detection Rate | Description |
|-----------|:--------------:|-------------|
| Base64 Encoding | 90% | Single and multiple layer encoding |
| Hexadecimal Encoding | 95% | `\x00` style hex escapes |
| Unicode Escapes | 90% | `\u0000` and `\U00000000` patterns |
| Gzip/Zlib Compression | 85% | Compressed payload detection |
| Python Marshal | 95% | Serialized code objects |
| eval/exec | 75% | Dynamic code execution |
| ROT13/ROT-N | 85% | Caesar cipher variants |
| XOR Encryption | 60% | Basic XOR patterns |
| String Reversal | 70% | Reverse string operations |

### 🎨 User Interface
- 🖥️ **Beautiful CLI** — Color-coded output with emoji icons
- 🎬 **Smooth Animations** — Spinners, progress bars, and typewriter effects
- 📊 **Visual Statistics** — Graphical size comparison bars
- 🎮 **Interactive Mode** — Real-time command-line interface
- 📁 **Batch Processing** — Process entire directories at once

### 📊 Reporting Features
- 📄 **Detailed Analysis Reports** — Comprehensive deobfuscation reports
- 🔐 **File Hashing** — MD5 and SHA256 checksums
- 📈 **Statistical Analysis** — Size reduction metrics and technique frequency
- 💾 **Save Options** — Export deobfuscated code and reports

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Athexblackhat/deobx.git
cd deobx

# Make it executable (Linux/Mac)
chmod +x deobx.py

# Install dependencies (optional - for Python formatting)
pip install autopep8
```

### Basic Usage

```bash
# Deobfuscate a single file
python deobx.py -f script.py

# With aggressive mode and verbose output
python deobx.py -f malware.sh -a -v

# Process all Python files in a directory
python deobx.py -d ./suspicious/ "*.py"

# Save output to specific file
python deobx.py -f payload.py -o clean_code.py

# Launch interactive mode
python deobx.py -i

# Disable animations for faster processing
python deobx.py -f script.py --no-anim
```

---

## 📖 Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-f, --file` | File to deobfuscate | `-f script.py` |
| `-d, --directory` | Directory to process | `-d ./scripts/` |
| `-o, --output` | Output file path | `-o result.py` |
| `-a, --aggressive` | Enable aggressive deobfuscation | `-a` |
| `-v, --verbose` | Enable verbose output | `-v` |
| `-i, --interactive` | Run in interactive mode | `-i` |
| `--pattern` | File pattern for directory | `--pattern "*.sh"` |
| `--no-anim` | Disable animations | `--no-anim` |

---

## 🎮 Interactive Mode

Launch with `python deobx.py -i`, then use:

```
deobx> help                    # Show help menu
deobx> file script.py          # Process a single file
deobx> dir ./scripts/ *.py     # Process directory
deobx> verbose                 # Toggle verbose mode
deobx> aggressive              # Toggle aggressive mode
deobx> stats                   # Show statistics
deobx> clear                   # Clear screen
deobx> exit                    # Exit program
```

---

## 📊 Sample Output

```

                                                               
  ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗                  
  ██╔══██╗██╔════╝██╔═══██╗██╔══██╗╚██╗██╔╝                  
  ██║  ██║█████╗  ██║   ██║██████╔╝ ╚███╔╝                   
  ██║  ██║██╔══╝  ██║   ██║██╔══██╗ ██╔██╗                   
  ██████╔╝███████╗╚██████╔╝██████╔╝██╔╝ ██╗                  
  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝                  
                                                               
  Advanced Deobfuscation Tool             
       


[i] Processing: obfuscated.py

============================================================
  DEOBFUSCATION REPORT
============================================================

📄 File: obfuscated.py
🔤 Language: PYTHON
⏰ Timestamp: 2024-01-15T10:30:45

📊 Size Comparison:
  Original:      ████████████████████████████████ 45,678 bytes
  Deobfuscated:  ████████████ 12,345 bytes
  Reduction:     73.0%

🔐 Hashes:
  MD5:    a1b2c3d4e5f678901234567890123456
  SHA256: 1234567890abcdef...

🔍 Detected Obfuscation Techniques:
  ▶ base64 (90%)
     Found 3 potential Base64 encoded strings
  ▶ hex (95%)
     Hexadecimal encoding detected (12 instances)
  ▶ eval_exec (75%)
     eval/exec usage detected

[✓] Successfully deobfuscated obfuscated.py
```

---

## 🛠️ How It Works

### 1. Detection Phase
- **Language Detection** — Analyzes shebang and syntax patterns
- **Technique Identification** — Scans for known obfuscation patterns
- **Confidence Scoring** — Rates detection reliability
- **Strategy Selection** — Chooses appropriate deobfuscation methods

### 2. Deobfuscation Phase
- **Base64 Extraction** — Identifies and decodes base64 strings
- **Hex/Unicode Decoding** — Converts escape sequences
- **Compression Handling** — Decompresses gzip/zlib content
- **Dynamic Code Resolution** — Handles eval/exec statements
- **Formatting** — Beautifies output for readability

### 3. Analysis Phase
- **Statistics Generation** — Calculates reduction metrics
- **Report Creation** — Generates detailed analysis
- **Hash Verification** — Creates file checksums
- **History Tracking** — Maintains processing records

---

## 🔧 Advanced Usage

### Aggressive Mode

For heavily obfuscated scripts:

```bash
python deobx.py -f obfuscated.py -a
```

Enables: recursive base64 decoding, deep eval/exec content extraction, and enhanced pattern matching.

### Batch Processing

```bash
python deobx.py -d ./malware_samples/ "*.sh" -v
```

Generates individual deobfuscated files, a comprehensive summary report, and technique frequency analysis.

### Custom Output

```bash
python deobx.py -f suspicious.py -o cleaned.py
```

---

---

## 🔒 Security Notice

> ⚠️ **DeobX is designed for legitimate use only.**

**Intended uses:**
- Security research and analysis
- Educational purposes
- Legitimate script recovery
- Malware analysis in controlled environments

**Do NOT use this tool for:**
- Unauthorized access to systems
- Circumventing software protections
- Any illegal activities

---


---

## 📝 Roadmap

- [ ] GUI version with Qt/Tkinter
- [ ] JavaScript/Node.js deobfuscation
- [ ] PowerShell script support
- [ ] Web-based API
- [ ] Machine learning-based detection
- [ ] Plugin system for custom deobfuscators
- [ ] Docker containerization
- [ ] VS Code extension
- [ ] Real-time monitoring mode
- [ ] Cloud-based scanning

---

## 🐛 Known Issues

- Some obfuscation techniques may require manual intervention
- Very large files (>100MB) may cause performance issues
- Certain XOR encryption patterns require key guessing

---

## 📚 Resources

- [Python Obfuscation Techniques](https://docs.python.org)
- [Bash Obfuscation Methods](https://www.gnu.org/software/bash/)
- [OWASP Deobfuscation Guide](https://owasp.org)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/Athexblackhat/deobx/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Athexblackhat/deobx/discussions)

---

<div align="center">
  Built with 🖤 by <strong>ATHEX BLACK HAT</strong> — for security researchers
</div>