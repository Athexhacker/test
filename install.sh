#!/bin/bash

# ReconPro - Advanced Installation Script
# Author: ATHEX BLACK HAT
# Version: 2.0

# Color codes for hacking vibe
GREEN='\033[0;32m'
DARK_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' 
BOLD='\033[1m'


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/install.log"
PROGRESS_WIDTH=50


clear
echo -e "${GREEN}"
cat << "EOF"
    ____                       ____            
   / __ \___  _________  ___  / __ \_________ 
  / /_/ / _ \/ ___/ __ \/ _ \/ /_/ / ___/ __ \
 / _, _/  __/ /__/ /_/ /  __/ ____/ /  / /_/ /
/_/ |_|\___/\___/ .___/\___/_/   /_/   \____/ 
               /_/                            
EOF
echo -e "${DARK_GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          Advanced Installation Script v2.0               ║"
echo "║              [ System Initializing... ]                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"


matrix_rain() {
    local lines=$1
    local chars="01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    for ((i=0; i<$lines; i++)); do
        for ((j=0; j<$(tput cols); j++)); do
            if [ $((RANDOM % 10)) -eq 0 ]; then
                echo -ne "${GREEN}${chars:$((RANDOM % ${#chars})):1}${NC}"
            else
                echo -ne " "
            fi
        done
        echo
        sleep 0.05
    done
}


loading_animation() {
    local message=$1
    local pid=$2
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    local i=0
    
    echo -ne "${GREEN}[${NC} "
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % ${#spin} ))
        echo -ne "\b${spin:$i:1}"
        sleep 0.1
    done
    echo -e "\b${GREEN}✓${NC}] ${GREEN}$message completed${NC}"
}


progress_bar() {
    local current=$1
    local total=$2
    local message=$3
    local percentage=$((current * 100 / total))
    local filled=$((current * PROGRESS_WIDTH / total))
    local empty=$((PROGRESS_WIDTH - filled))
    
    printf "\r${GREEN}[${NC}"
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "${GREEN}]${NC} %3d%% %s" "$percentage" "$message"
}


glitch_effect() {
    local text=$1
    local glitch_chars="!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    for ((i=0; i<${#text}; i++)); do
        echo -ne "${GREEN}${text:$i:1}${NC}"
        sleep 0.02
    done
    echo -ne " "
    
  
    if [ $((RANDOM % 5)) -eq 0 ]; then
        echo -ne "${DARK_GREEN}${glitch_chars:$((RANDOM % ${#glitch_chars})):1}${NC}"
        sleep 0.1
        echo -ne "\b \b"
    fi
}


typewriter() {
    local text=$1
    local delay=${2:-0.03}
    
    for ((i=0; i<${#text}; i++)); do
        echo -ne "${GREEN}${text:$i:1}${NC}"
        sleep $delay
    done
    echo
}


check_system() {
  
    echo -e "${CYAN}       🔍 SYSTEM REQUIREMENTS CHECK                   ${NC}"
    
    
    # Check OS
    typewriter "[*] Detecting operating system..." 0.01
    sleep 0.5
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${GREEN}[✓] OS: Linux detected${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${GREEN}[✓] OS: macOS detected${NC}"
    else
        echo -e "${RED}[✗] Unsupported OS: $OSTYPE${NC}"
        exit 1
    fi
    
    typewriter "[*] Checking Python installation..." 0.01
    if command -v python3 &>/dev/null; then
        python_version=$(python3 --version)
        echo -e "${GREEN}[✓] $python_version detected${NC}"
    else
        echo -e "${RED}[✗] Python3 not found. Please install Python3${NC}"
        exit 1
    fi
    
    typewriter "[*] Checking pip installation..." 0.01
    if command -v pip3 &>/dev/null; then
        pip_version=$(pip3 --version | cut -d' ' -f1-2)
        echo -e "${GREEN}[✓] $pip_version detected${NC}"
    else
        echo -e "${YELLOW}[!] pip3 not found. Installing pip...${NC}"
        install_pip
    fi
    
    typewriter "[*] Checking internet connection..." 0.01
    if ping -c 1 google.com &>/dev/null; then
        echo -e "${GREEN}[✓] Internet connection active${NC}"
    else
        echo -e "${YELLOW}[!] No internet connection. Some features may be limited${NC}"
    fi
    
    sleep 1
}

install_pip() {
    echo -e "${YELLOW}[!] Installing pip...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update &>/dev/null
        sudo apt-get install -y python3-pip &>/dev/null
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        sudo easy_install pip &>/dev/null
    fi
    
    if command -v pip3 &>/dev/null; then
        echo -e "${GREEN}[✓] pip3 installed successfully${NC}"
    else
        echo -e "${RED}[✗] Failed to install pip3${NC}"
        exit 1
    fi
}

install_dependencies() {
    echo -e "${CYAN}         📦 INSTALLING DEPENDENCIES                     ${NC}"
  
    
    declare -a deps=(
        "requests"
        "beautifulsoup4"
        "colorama"
        "tqdm"
        "paramiko"
        "scapy"
        "nmap"
        "python-nmap"
        "argparse"
        "datetime"
        "json"
        "urllib3"
        "selenium"
        "pycryptodome"
    )
    
    total=${#deps[@]}
    current=0
    
    typewriter "[*] Setting up Python virtual environment..." 0.01
    if command -v python3 -m venv &>/dev/null; then
        python3 -m venv reconpro_env &>/dev/null &
        loading_animation "Virtual environment" $!
        source reconpro_env/bin/activate &>/dev/null
        echo -e "${GREEN}[✓] Virtual environment activated${NC}"
    fi
    
    echo -e "\n${GREEN}[*] Starting dependency installation...${NC}\n"
    

    for dep in "${deps[@]}"; do
        current=$((current + 1))
        progress_bar $current $total "Installing $dep"
        
      
        glitch_effect "$dep"
        
     
        pip3 install --quiet "$dep" &>/dev/null &
        loading_animation "$dep" $!
        
        
        if [ $((RANDOM % 5)) -eq 0 ]; then
            matrix_rain 3
        fi
    done
    
    echo -e "\n${GREEN}[✓] All dependencies installed successfully!${NC}\n"
    
    typewriter "[*] Installed packages summary:" 0.02
    pip3 list --format=columns | head -n 5
    echo -e "${GREEN}... and more${NC}\n"
}
hacking_animation() {
    clear
    echo -e "${GREEN}"
    
    for ((i=0; i<20; i++)); do
        for ((j=0; j<$(tput cols); j+=3)); do
            if [ $((RANDOM % 2)) -eq 0 ]; then
                printf "\033[%d;%dH%s" $((RANDOM % LINES)) $j "$(echo $((RANDOM % 2)))"
            fi
        done
        sleep 0.05
    done
    
    # Binary rain
    for ((i=0; i<10; i++)); do
        echo -e "$(for j in {1..50}; do echo -n $((RANDOM % 2)); done)"
        sleep 0.1
    done
    
    echo -e "${NC}"
    clear
}

# Create config file
create_config() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           ⚙️  CONFIGURATION SETUP                          ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}\n"
    
    typewriter "[*] Creating configuration file..." 0.02
    
    cat > "$SCRIPT_DIR/src/main/config.json" << EOF
{
    "version": "2.0",
    "install_path": "$SCRIPT_DIR",
    "python_path": "$(which python3)",
    "dependencies_installed": true,
    "install_date": "$(date)",
    "system": "$OSTYPE",
    "user": "$USER"
}
EOF
    
    echo -e "${GREEN}[✓] Configuration file created${NC}\n"
}

execute_run() {
    echo -e "${CYAN}           🚀 EXECUTING RECONPRO                           ${NC}"
    
    if [ -f "$SCRIPT_DIR/src/main/ReconPro.py" ]; then
        typewriter "[*] Initializing ReconPro engine..." 0.01
        sleep 0.5
        
        echo -e "\n${GREEN}"
        for i in {1..3}; do
            echo -ne "▰"
            sleep 0.2
        done
        for i in {1..3}; do
            echo -ne "▰"
            sleep 0.1
        done
        echo -e " ${BOLD}LAUNCHING RECONPRO${NC}\n"
        
        matrix_rain 5
        
        echo -e "${GREEN}[✓] Executing ...${NC}\n"
        cd "$SCRIPT_DIR/src"
        
        if [ -f "$SCRIPT_DIR/reconpro_env/bin/activate" ]; then
            source "$SCRIPT_DIR/reconpro_env/bin/activate"
        fi
        
        python3 ReconPro.py
    else
        echo -e "${RED}[✗] Error: run.py not found in src directory!${NC}"
        echo -e "${YELLOW}[!] Please ensure run.py exists in: $SCRIPT_DIR/src/${NC}"
        exit 1
    fi
}

main() {
   
    hacking_animation
    echo -e "\n${GREEN}${BOLD}Welcome to ReconPro Installation${NC}\n"
    typewriter "Initializing secure installation protocol..." 0.02
    sleep 1
    
    check_system
    
    
    echo -e "\n${YELLOW}[?] Ready to install ReconPro dependencies? (y/n)${NC} "
    read -n 1 -s answer
    if [[ ! "$answer" =~ ^[Yy]$ ]]; then
        echo -e "\n${RED}[!] Installation cancelled by user${NC}"
        exit 0
    fi
    echo -e "\n"
    
    exec 2> "$LOG_FILE"
    
    install_dependencies
    create_config

    echo -e "${GREEN}          ✅ INSTALLATION COMPLETE!                       ${NC}"
    
    for i in {5..1}; do
        echo -ne "${GREEN}Launching ReconPro in $i...${NC}\r"
        sleep 1
    done
    echo -e "\n"
    
    execute_run
}
trap 'echo -e "\n${RED}[!] Installation interrupted${NC}"; exit 1' INT
main