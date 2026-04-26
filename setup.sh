#!/bin/bash

# INJECTOR-X Requirements Installer
echo "         INJECTOR-X - Requirements Installation              "
echo ""
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &> /dev/null; then
    PYTHON=python
    PIP=pip
else
    echo "[✗] Python not found. Installing..."
    pkg install python -y || apt install python3 -y
    PYTHON=python3
    PIP=pip3
fi
echo "[✓] Python: $($PYTHON --version)"
echo "[*] Upgrading pip..."
$PIP install --upgrade pip
if [ -f "requirements.txt" ]; then
    echo "[*] Installing Python packages..."
    $PIP install -r requirements.txt
else
    echo "[!] requirements.txt not found!"
    echo "[*] Installing core packages..."
    $PIP install requests colorama beautifulsoup4 cryptography pysocks jinja2 pyyaml
fi
if [ ! -f "$HOME/sqlmap/sqlmap.py" ]; then
    echo "[*] Installing SQLMap..."
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$HOME/sqlmap"
else
    echo "[✓] SQLMap already installed"
fi
echo ""
echo "[✓] All requirements installed successfully!"
echo "[*] You can now run: ./setup.sh"