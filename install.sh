#!/bin/bash

# SQL MAP PRO - Animated Installation Script
# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Clear screen
clear

# Function for cool typing animation
type_animation() {
    text="$1"
    color="$2"
    for ((i=0; i<${#text}; i++)); do
        echo -en "${color}${text:$i:1}${NC}"
        sleep 0.03
    done
    echo ""
}

# Function for matrix-like rain effect in background
matrix_effect() {
    for ((i=0; i<3; i++)); do
        echo -e "${GREEN}$(head -c 50 /dev/urandom | tr -dc '01' | fold -w 50 | head -n 1)${NC}"
    done
}

# Animated ASCII Banner
show_banner() {
    local frames=(
"${RED}   _____  ____  _        __  __  ___    _   _  ____  ${NC}
${YELLOW}  / ____|/ __ \| |      |  \/  |/ _ \  | \ | |/ __ \ ${NC}
${GREEN} | (___ | |  | | |      | \  / | | | | |  \| | |  | |${NC}
${BLUE}  \___ \| |  | | |      | |\/| | | | | | .   | |  | |${NC}
${PURPLE}  ____) | |__| | |____  | |  | | |_| | | |\  | |__| |${NC}
${CYAN} |_____/ \___\_\______| |_|  |_|\___/  |_| \_|\____/ ${NC}"

"${RED}   ░██████  ░█████  ██▓     ███▄ ▄███▓ ▄▄▄       ██▓███  ${NC}
${YELLOW}  ██▒  ██▒██▒  ██▒▓██▒    ▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒${NC}
${GREEN} ██░  ██▒██░  ██▒▒██░    ▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒${NC}
${BLUE}▒██   ██▒███████▒▒██░    ▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒${NC}
${PURPLE}░ ████▓▒░▒▒ ▓░▒░▒░██████▒▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░${NC}
${CYAN}░ ▒░▒░▒░ ░▒ ░ ░░ ░ ▒░▓  ░░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░${NC}
${RED}  ░ ▒ ▒░ ░░   ░ ░░ ░ ▒  ░░  ░      ░  ▒   ▒▒ ░░▒ ░     ${NC}
${YELLOW}░ ░ ░ ▒   ░         ░ ░   ░      ░     ░   ▒   ░░       ${NC}
${GREEN}    ░ ░              ░  ░       ░          ░  ░         ${NC}"

"${CYAN}╔══════════════════════════════════════════════════════════╗${NC}
${PURPLE}║     ███████  ██████  ██      ███    ███  █████  ██████  ║${NC}
${BLUE}║     ██      ██    ██ ██      ████  ████ ██   ██ ██   ██ ║${NC}
${GREEN}║     ███████ ██    ██ ██      ██ ████ ██ ███████ ██████  ║${NC}
${YELLOW}║          ██ ██    ██ ██      ██  ██  ██ ██   ██ ██      ║${NC}
${RED}║     ███████  ██████  ███████ ██      ██ ██   ██ ██      ║${NC}
${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    )

    for frame in "${frames[@]}"; do
        clear
        echo -e "$frame"
        echo ""
        echo -e "${WHITE}⚡ ADVANCED SQL INJECTION TOOL ⚡${NC}"
        matrix_effect
        sleep 0.3
    done
}

# Loading bar animation
loading_bar() {
    echo -ne "${CYAN}\n[${NC}"
    for ((i=0; i<=50; i++)); do
        echo -ne "${GREEN}▓${NC}"
        sleep 0.02
    done
    echo -e "${CYAN}]${NC} ${WHITE}100%${NC}\n"
}

# Main installation function
main() {
    # Show animated banner
    show_banner
    
    echo -e "\n${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}            INITIALIZING SQL MAP PRO INSTALLATION            ${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}\n"

    # Check Python installation
    type_animation "🔍 Checking Python installation..." "${YELLOW}"
    if command -v python3 &>/dev/null; then
        echo -e "${GREEN}✓ Python 3 is installed${NC}"
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        echo -e "${GREEN}✓ Python is installed${NC}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗ Python is not installed. Please install Python 3.8 or higher.${NC}"
        exit 1
    fi

    # Check Python version
    python_version=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if (($(echo "$python_version < 3.8" | bc -l))); then
        echo -e "${RED}✗ Python 3.8 or higher is required. Found version $python_version${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ Python version $python_version is compatible${NC}"
    fi

    # Create virtual environment
    type_animation "\n🔧 Creating virtual environment..." "${BLUE}"
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"

    # Activate virtual environment
    source venv/bin/activate

    # Install requirements
    type_animation "📦 Installing required packages..." "${PURPLE}"
    echo -e "${YELLOW}"
    
    # Create requirements.txt if it doesn't exist
    if [ ! -f "requirements.txt" ]; then
        cat > requirements.txt << EOF
requests>=2.28.0
colorama>=0.4.6
beautifulsoup4>=4.11.0
lxml>=4.9.0
urllib3>=1.26.0
selenium>=4.0.0
EOF
    fi

    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ All packages installed successfully${NC}"

    # Create src directory and main.py if they don't exist
    type_animation "📁 Setting up project structure..." "${CYAN}"
    
    mkdir -p src
    
    if [ ! -f "src/sql-map-pro.py" ]; then
        cat > src/sql-map-pro << 'EOF'
#!/usr/bin/env python3
"""
SQL MAP PRO - Main Application
"""

import sys
import time
import os
try:
    from colorama import init, Fore, Style
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

class SQLMapPro:
    def __init__(self):
        self.name = "SQL MAP PRO"
        self.version = "2.0.0"
        
    def print_banner(self):
        """Display the application banner"""
        banner = f"""
{Fore.RED}   ░██████  ░█████  ██▓     ███▄ ▄███▓ ▄▄▄       ██▓███  
{Fore.YELLOW}  ██▒  ██▒██▒  ██▒▓██▒    ▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒
{Fore.GREEN} ██░  ██▒██░  ██▒▒██░    ▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒
{Fore.BLUE}▒██   ██▒███████▒▒██░    ▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒
{Fore.MAGENTA}░ ████▓▒░▒▒ ▓░▒░▒░██████▒▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░
{Fore.CYAN}░ ▒░▒░▒░ ░▒ ░ ░░ ░ ▒░▓  ░░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░
{Fore.RED}  ░ ▒ ▒░ ░░   ░ ░░ ░ ▒  ░░  ░      ░  ▒   ▒▒ ░░▒ ░     
{Fore.YELLOW}░ ░ ░ ▒   ░         ░ ░   ░      ░     ░   ▒   ░░       
{Fore.GREEN}    ░ ░              ░  ░       ░          ░  ░         
{Fore.WHITE}═══════════════════════════════════════════════════════════
{Fore.CYAN}              ADVANCED SQL INJECTION TOOL v{self.version}
{Fore.WHITE}═══════════════════════════════════════════════════════════{Style.RESET_ALL}
        """
        print(banner)
        
    def loading_animation(self):
        """Display a loading animation"""
        print(f"{Fore.YELLOW}Initializing SQL MAP PRO", end="")
        for i in range(5):
            time.sleep(0.3)
            print(f"{Fore.GREEN}.", end="", flush=True)
        print(f"{Fore.GREEN} Ready!\n")
        
    def run(self):
        """Main application logic"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.print_banner()
        self.loading_animation()
        
        print(f"{Fore.WHITE}╔{'═'*50}╗")
        print(f"{Fore.WHITE}║{Fore.CYAN}{'SQL MAP PRO - Main Menu':^50}{Fore.WHITE}║")
        print(f"{Fore.WHITE}╠{'═'*50}╣")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  1. {Fore.GREEN}Scan Target URL{' ':<36}{Fore.WHITE}║")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  2. {Fore.GREEN}Database Detection{' ':<34}{Fore.WHITE}║")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  3. {Fore.GREEN}Table Extraction{' ':<35}{Fore.WHITE}║")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  4. {Fore.GREEN}Data Dump{' ':<42}{Fore.WHITE}║")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  5. {Fore.GREEN}Advanced Options{' ':<36}{Fore.WHITE}║")
        print(f"{Fore.WHITE}║{Fore.YELLOW}  6. {Fore.GREEN}Exit{' ':<47}{Fore.WHITE}║")
        print(f"{Fore.WHITE}╚{'═'*50}╝\n")
        
        while True:
            try:
                choice = input(f"{Fore.CYAN}Select option (1-6): {Fore.WHITE}")
                
                if choice == '6':
                    print(f"\n{Fore.YELLOW}Thank you for using SQL MAP PRO!{Fore.WHITE}")
                    break
                elif choice in ['1','2','3','4','5']:
                    print(f"\n{Fore.GREEN}Option {choice} selected. This feature is under development.{Fore.WHITE}")
                    print(f"{Fore.CYAN}Press Enter to continue...{Fore.WHITE}")
                    input()
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.print_banner()
                    self.loading_animation()
                    # Re-print menu
                    print(f"{Fore.WHITE}╔{'═'*50}╗")
                    print(f"{Fore.WHITE}║{Fore.CYAN}{'SQL MAP PRO - Main Menu':^50}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}╠{'═'*50}╣")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  1. {Fore.GREEN}Scan Target URL{' ':<36}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  2. {Fore.GREEN}Database Detection{' ':<34}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  3. {Fore.GREEN}Table Extraction{' ':<35}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  4. {Fore.GREEN}Data Dump{' ':<42}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  5. {Fore.GREEN}Advanced Options{' ':<36}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}║{Fore.YELLOW}  6. {Fore.GREEN}Exit{' ':<47}{Fore.WHITE}║")
                    print(f"{Fore.WHITE}╚{'═'*50}╝\n")
                else:
                    print(f"{Fore.RED}Invalid option. Please try again.{Fore.WHITE}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting SQL MAP PRO...{Fore.WHITE}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Fore.WHITE}")

if __name__ == "__main__":
    app = SQLMapPro()
    app.run()
EOF
        echo -e "${GREEN}✓ Created src/sql-map-pro${NC}"
    else:
        echo -e "${GREEN}✓ src/sql-map-pro already exists${NC}"
    fi

    chmod +x src/sql-map-pro

    # Installation complete
    echo -e "\n${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    type_animation "✨ SQL MAP PRO INSTALLATION COMPLETE! ✨" "${GREEN}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}\n"
    
    # Show loading bar
    loading_bar
    
    # Auto-run the application
    type_animation "🚀 Auto-starting SQL MAP PRO in 3 seconds..." "${YELLOW}"
    sleep 3
    
    echo -e "\n${CYAN}Starting SQL MAP PRO...${NC}\n"
    sleep 1
    
    # Run the main application
    python src/sql-map-pro
}

# Trap Ctrl+C
trap 'echo -e "\n${RED}Installation cancelled${NC}"; exit 1' INT

# Run main function
main