#!/bin/bash
# SQLMAP PRO Installation Script

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'
BOLD='\033[1m'

type_animation() {
    text="$1"
    color="$2"
    for ((i=0; i<${#text}; i++)); do
        echo -en "${color}${text:$i:1}${NC}"
        sleep 0.03
    done
    echo ""
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

progress_bar() {
    local duration=$1
    local steps=20
    for ((i=0; i<=steps; i++)); do
        percentage=$((i * 100 / steps))
        filled=$((i * 40 / steps))
        empty=$((40 - filled))
        printf "\r${CYAN}[${NC}"
        printf "%${filled}s" | tr ' ' '█'
        printf "%${empty}s" | tr ' ' '░'
        printf "${CYAN}]${NC} ${GREEN}%d%%${NC}" $percentage
        sleep $duration
    done
    echo ""
}

# New function to auto-execute run.py
auto_execute_run_py() {
    echo -e "\n${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}${BOLD}              AUTO-EXECUTING RUN.PY                        ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}\n"
    
    # Check if run.py exists in src directory
    if [ -f "src/run.py" ]; then
        echo -e "${GREEN}[✓]${NC} Found run.py in src directory"
        
        # Ensure virtual environment is activated
        if [ -d "sqlmap_pro_venv" ]; then
            echo -e "${BLUE}[•]${NC} Activating virtual environment..."
            source sqlmap_pro_venv/bin/activate
            
            # Change to src directory and run the script
            echo -e "${YELLOW}[→]${NC} Launching SQLMAP PRO GUI...\n"
            sleep 1
            
            cd src
            python3 run.py
            cd ..
            
            # Deactivate virtual environment after execution
            deactivate
        else
            echo -e "${RED}[✗]${NC} Virtual environment not found!"
            echo -e "${YELLOW}[!]${NC} Attempting to run without virtual environment..."
            cd src
            python3 run.py
            cd ..
        fi
    else
        echo -e "${RED}[✗]${NC} run.py not found in src directory!"
        echo -e "${YELLOW}[!]${NC} Please ensure the file exists at: $(pwd)/src/run.py"
        
        # Ask if user wants to continue anyway
        echo -ne "\n${CYAN}Continue to launcher creation? (y/n): ${NC}"
        read -n 1 continue_choice
        echo
        if [[ ! "$continue_choice" =~ ^[Yy]$ ]]; then
            echo -e "\n${YELLOW}Exiting...${NC}"
            exit 0
        fi
    fi
}

clear
echo -e "${RED}"
cat << "EOF"
███████╗ ██████╗ ██╗     ███╗   ███╗ █████╗ ██████╗  
██╔════╝██╔═══██╗██║     ████╗ ████║██╔══██╗██╔══██╗ 
███████╗██║   ██║██║     ██╔████╔██║███████║██████╔╝ 
╚════██║██║▄▄ ██║██║     ██║╚██╔╝██║██╔══██║██╔═══╝  
███████║╚██████╔╝███████╗██║ ╚═╝ ██║██║  ██║██║      
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝      
                                               ██████╗ ██████╗  ██████╗              
                                               ██╔══██╗██╔══██╗██╔═══██╗             
                                               ██████╔╝██████╔╝██║   ██║             
                                               ██╔═══╝ ██╔══██╗██║   ██║             
                                               ██║     ██║  ██║╚██████╔╝             
                                               ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                     Advance GUI Version By ATHEX BLACK HAT             
EOF
echo -e "${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}${BOLD}                    SQLMAP PRO v2.0                          ${NC}"
echo -e "${WHITE}           Advanced SQL Injection Detection Tool                   ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}\n"

type_animation "[◇] Initializing SQLMAP PRO installation..." "${CYAN}"
sleep 1

echo -e "\n${BLUE}[•]${NC} Checking Python installation..."
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[✓]${NC} Python $python_version detected"
else
    echo -e "${RED}[✗]${NC} Python3 not found! Please install Python 3.8 or higher"
    exit 1
fi
sleep 1

echo -e "\n${BLUE}[•]${NC} Checking pip installation..."
if command -v pip3 &>/dev/null; then
    pip_version=$(pip3 --version | awk '{print $2}')
    echo -e "${GREEN}[✓]${NC} pip $pip_version detected"
else
    echo -e "${YELLOW}[!]${NC} pip3 not found, installing pip..."
    sudo apt update > /dev/null 2>&1
    sudo apt install python3-pip -y > /dev/null 2>&1
    echo -e "${GREEN}[✓]${NC} pip installed successfully"
fi
sleep 1

echo -e "\n${BLUE}[•]${NC} Creating virtual environment..."
python3 -m venv sqlmap_pro_venv > /dev/null 2>&1 &
spinner $!
echo -e "${GREEN}[✓]${NC} Virtual environment created"
sleep 1

source sqlmap_pro_venv/bin/activate

echo -e "\n${BLUE}[•]${NC} Upgrading pip..."
pip3 install --upgrade pip > /dev/null 2>&1 &
spinner $!
echo -e "${GREEN}[✓]${NC} Pip upgraded successfully"
sleep 1

declare -a modules=(
    "PyQt6>=6.4.0"
    "PyQt6-WebEngine>=6.4.0"
    "requests>=2.28.0"
    "beautifulsoup4>=4.11.0"
    "lxml>=4.9.0"
)

declare -a module_names=(
    "PyQt6"
    "PyQt6-WebEngine"
    "requests"
    "beautifulsoup4"
    "lxml"
)

echo -e "\n${PURPLE}════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}${BOLD}                INSTALLING DEPENDENCIES                     ${NC}"
echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}\n"

total_modules=${#modules[@]}
current=1

for i in "${!modules[@]}"; do
    module="${modules[$i]}"
    module_name="${module_names[$i]}"
    echo -e "${YELLOW}[${current}/${total_modules}]${NC} Installing ${WHITE}${BOLD}${module_name}${NC}..."
    
    progress_bar 0.05
    
    if pip3 install "$module" > /dev/null 2>&1; then
        echo -e "${GREEN}[✓]${NC} ${module_name} installed successfully!\n"
    else
        echo -e "${RED}[✗]${NC} Failed to install ${module_name}"
        echo -e "${YELLOW}[!]${NC} Retrying with alternative method..."
        
        if pip3 install "${module_name,,}" > /dev/null 2>&1; then
            echo -e "${GREEN}[✓]${NC} ${module_name} installed successfully!\n"
        else
            echo -e "${RED}[✗]${NC} Critical error installing ${module_name}"
            exit 1
        fi
    fi
    
    ((current++))
    sleep 0.5
done

echo -e "\n${PURPLE}════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}${BOLD}                VERIFYING INSTALLATIONS                     ${NC}"
echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}\n"

verification_passed=true

for module_name in "${module_names[@]}"; do
    echo -ne "${BLUE}[•]${NC} Checking ${module_name}... "
    if python3 -c "import ${module_name%%-*}" 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
        
        version=$(python3 -c "import ${module_name%%-*}; print(${module_name%%-*}.__version__)" 2>/dev/null)
        if [ -n "$version" ]; then
            echo -e "    └─ ${CYAN}Version: ${version}${NC}"
        fi
    else
        echo -e "${RED}FAILED${NC}"
        verification_passed=false
    fi
done

echo -e "\n${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}${BOLD}                    INSTALLATION COMPLETE!                    ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}\n"

for i in {1..10}; do
    echo -en "${CYAN}✦${NC} "
    sleep 0.1
done
echo -e "\n"

if [ "$verification_passed" = true ]; then
    echo -e "${GREEN}"
    cat << "EOF"
    ╔══════════════════════════════════════════════════════════╗
    ║     🚀 ALL SYSTEMS READY! SQLMAP PRO IS NOW ACTIVE 🚀    ║
    ╚══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo -e "${WHITE}Installation Directory:${NC} $(pwd)/sqlmap_pro"
    echo -e "${WHITE}Virtual Environment:${NC} $(pwd)/sqlmap_pro_venv"
    echo -e "${WHITE}Python Version:${NC} $python_version"
    echo -e "${WHITE}Total Modules:${NC} ${#modules[@]}\n"
    
    echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}${BOLD}                    HOW TO USE                              ${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}1.${NC} Activate virtual environment: ${WHITE}source sqlmap_pro_venv/bin/activate${NC}"
    echo -e "${CYAN}2.${NC} Run SQLMAP PRO: ${WHITE}python3 src/run.py${NC}"
    echo -e "${CYAN}3.${NC} Deactivate when done: ${WHITE}deactivate${NC}\n"
    
    # Create launcher script
    cat > sqlmap_pro_launcher.sh << 'EOF'
#!/bin/bash
# SQLMAP PRO Launcher Script
source "$(dirname "$0")/sqlmap_pro_venv/bin/activate"
cd src
python3 run.py
cd ..
deactivate
EOF
    chmod +x sqlmap_pro_launcher.sh
    echo -e "${GREEN}[✓]${NC} Launcher script created: ${WHITE}./sqlmap_pro_launcher.sh${NC}"
    
    # Create desktop entry for easy access
    cat > sqlmap-pro.desktop << EOF
[Desktop Entry]
Name=SQLMAP PRO
Comment=Advanced SQL Injection Detection Tool
Exec=$(pwd)/sqlmap_pro_launcher.sh
Icon=$(pwd)/icon.png
Terminal=true
Type=Application
Categories=Development;Security;
EOF
    echo -e "${GREEN}[✓]${NC} Desktop entry created: ${WHITE}sqlmap-pro.desktop${NC}"
    
    # Ask user if they want to auto-execute run.py
    echo -e "\n${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}${BOLD}              LAUNCH SQLMAP PRO NOW?                        ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -ne "\n${CYAN}Would you like to launch SQLMAP PRO now? (y/n): ${NC}"
    read -n 1 launch_choice
    echo
    
    if [[ "$launch_choice" =~ ^[Yy]$ ]]; then
        auto_execute_run_py
    else
        echo -e "\n${YELLOW}[!]${NC} You can launch SQLMAP PRO later using:"
        echo -e "    ${WHITE}./sqlmap_pro_launcher.sh${NC}"
        echo -e "    ${WHITE}python3 src/run.py${NC} (after activating virtual environment)\n"
    fi
    
    echo -e "${PURPLE}Thanks for installing SQLMAP PRO! Happy Hacking! 🎯${NC}\n"
    
else
    echo -e "${RED}[✗]${NC} Some modules failed to install properly."
    echo -e "${YELLOW}[!]${NC} Please check the errors above and try again."
fi

echo -e "\n${BLUE}Press any key to exit...${NC}"
read -n 1
clear