#!/bin/bash
# Written in Bash
# "ONLY FOR EDUCATIONAL PURPOSE"

current_version=2.32

# Color codes
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
BLUE='\033[0;94m'
PURPLE='\033[0;95m'
CYAN='\033[0;96m'
WHITE='\033[0;97m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Animation functions
loading_animation() {
    local message=$1
    local chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    
    echo -ne "${CYAN}${BOLD}$message ${NC}"
    for i in {1..20}; do
        for char in $(echo $chars | grep -o .); do
            echo -ne "${YELLOW}${BOLD}$char${NC}"
            sleep 0.05
            echo -ne "\b"
        done
    done
    echo -e "${GREEN}${BOLD} Done! ${NC}"
}

progress_bar() {
    local duration=$1
    local message=$2
    
    echo -ne "${BLUE}${BOLD}$message ${NC}"
    for i in {1..50}; do
        echo -ne "${GREEN}${BOLD}▓${NC}"
        sleep $(echo "scale=2; $duration/50" | bc 2>/dev/null || echo "0.05")
    done
    echo -e "${GREEN}${BOLD} Complete! ${NC}"
}

pulse_message() {
    local message=$1
    local color=$2
    
    for i in {1..3}; do
        echo -ne "${color}${BOLD}$message${NC}"
        sleep 0.3
        echo -ne "\r"
        for j in $(seq 1 ${#message}); do
            echo -n " "
        done
        echo -ne "\r"
        sleep 0.3
    done
    echo -e "${color}${BOLD}$message${NC}"
}

sparkle_effect() {
    echo -ne "${YELLOW}"
    for i in {1..30}; do
        echo -ne "✦"
        sleep 0.03
    done
    echo -e "${NC}"
}

typewriter_effect() {
    local text=$1
    local color=$2
    for ((i=0; i<${#text}; i++)); do
        echo -ne "${color}${BOLD}${text:$i:1}${NC}"
        sleep 0.03
    done
    echo
}

# Banner with gradient effect
display_banner() {
    clear
    echo -e "${RED}${BOLD}"
    cat << "EOF"
 
 █████╗ ██████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████║██║  ██║██████╔╝       ██║   ██║   ██║██║   ██║██║     
██╔══██║██║  ██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
██║  ██║██████╔╝██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚═════╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
🔧 ${GREEN}ANDRO-EYE${RED} - ${CYAN}Android Security Toolkit${RED}              
 
EOF
    echo -e "${NC}"
    echo -e "${YELLOW}${BOLD}              DEVELOPED BY ${RED}${BOLD}A T H E X${NC}\n"
    sparkle_effect
}

# Main script starts here
display_banner
sleep 1

echo -e "${PURPLE}${BOLD}⚡ ADB-Toolkit Initializing...${NC}\n"
loading_animation "🔍 Checking for updates"

check_new_version() {
    if ping -q -c 1 -W 1 google.com >/dev/null 2>&1; then
        typewriter_effect "📡 Checking online for updates..." "${CYAN}"
        checked_version=$(curl -s https://raw.githubusercontent.com/Athexhacker/ANDRO-EYE/master/modules/version 2>/dev/null)
        
        if [ -n "$checked_version" ] && [ "$checked_version" != "$current_version" ]; then
            echo -e "\n${RED}${BOLD}╔════════════════════════════════════════╗"
            echo -e "║        UPDATE AVAILABLE!              ║"
            echo -e "╚════════════════════════════════════════╝${NC}"
            echo -e "${YELLOW}Current Version: ${RED}$current_version${NC}"
            echo -e "${YELLOW}New Version: ${GREEN}$checked_version${NC}"
            pulse_message "❗ PLEASE UPDATE VIA GIT PULL ❗" "${RED}"
            progress_bar 5 "⏳ Auto-continuing in"
        else
            echo -e "${GREEN}${BOLD}✓ You have the latest version${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ No internet connection - skipping update check${NC}"
    fi
}

check_new_version
echo

if [ $(id -u) -ne 0 ]; then
    pulse_message "❌ THIS SCRIPT MUST BE RUN AS ROOT ❌" "${RED}"
    exit 1
fi

echo -e "${BLUE}${BOLD}📁 Checking directory structure...${NC}"
if [ -d "$PWD/.temp/" ]; then
    echo -e "${GREEN}✓ .temp directory found${NC}"
    sleep 1
    clear
    display_banner
else
    echo -e "${RED}${BOLD}✗ .temp directory not found!${NC}"
    echo -e "${YELLOW}Creating .temp directory...${NC}"
    mkdir -p "$PWD/.temp"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ .temp directory created successfully${NC}"
    else
        echo -e "${RED}Failed to create .temp directory. Please create it manually: mkdir .temp${NC}"
        exit 1
    fi
fi

echo -e "\n${PURPLE}${BOLD}🔧 Checking dependencies...${NC}\n"

# Check ADB
progress_bar 2 "🔍 Checking ADB installation"
adb_check=$(which adb 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ ADB is installed${NC}"
    loading_animation "🔄 Initializing ADB"
else
    echo -e "\n${RED}✗ ADB IS NOT INSTALLED${NC}"
    echo -e "${YELLOW}Please run the installation script or install ADB manually:${NC}"
    echo -e "${CYAN}sudo apt install adb${NC}"
    exit 1
fi

# Check Fastboot
progress_bar 2 "🔍 Checking Fastboot installation"
fastboot_check=$(which fastboot 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Fastboot is installed${NC}"
    loading_animation "🔄 Initializing Fastboot"
else
    echo -e "\n${RED}✗ FASTBOOT IS NOT INSTALLED${NC}"
    echo -e "${YELLOW}Please run the installation script or install Fastboot manually:${NC}"
    echo -e "${CYAN}sudo apt install fastboot${NC}"
    exit 1
fi

echo -e "\n${PURPLE}${BOLD}⚙️  Server Configuration${NC}\n"

# Server restart prompt with animation
while true; do
    echo -ne "${YELLOW}${BOLD}❓ Do you want to kill and restart the ADB server? ${WHITE}(Y/N) ${YELLOW}: ${RED}"
    read -p "" yn
    case $yn in
        [Yy]* )
            echo -e "\n${CYAN}${BOLD}🔄 Killing previous ADB server...${NC}"
            adb kill-server >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ Server killed successfully${NC}"
            fi
            
            loading_animation "🔄 Starting new ADB server"
            adb start-server >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ New server started${NC}"
            fi
            sparkle_effect
            break;;
        [Nn]* )
            echo -e "${BLUE}${BOLD}⏭️  Keeping existing ADB server${NC}"
            break;;
        * )
            pulse_message "Please answer with Y or N" "${RED}"
            ;;
    esac
done

clear
display_banner

# Load functions
echo -e "${PURPLE}${BOLD}📦 Loading modules...${NC}\n"
if [ -f "modules/funtion.sh" ]; then
    progress_bar 2 "🔧 Loading functions"
    source modules/funtion.sh
    echo -e "${GREEN}✓ Modules loaded successfully${NC}"
else
    echo -e "${RED}✗ modules/funtion.sh not found!${NC}"
    exit 1
fi

echo -e "\n${GREEN}${BOLD}✅ Ready to use!${NC}\n"
sleep 1