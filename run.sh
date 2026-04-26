#!/bin/bash
#                     INJECTOR-X - Dependency Installer                          
#                     Version: 1.0 - Bootstrap Script                           
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
BLINK='\033[5m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"
MAIN_SCRIPT="$SRC_DIR/injector-x.sh"
LOG_FILE="$SCRIPT_DIR/install.log"

# Function to clear screen
clear_screen() {
    clear
}

# Loading spinner animation
spinner() {
    local pid=$1
    local message="$2"
    local spinstr='◐◓◑◒'
    local delay=0.1
    
    while kill -0 "$pid" 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r${CYAN}[%c]${NC} ${WHITE}%s${NC}" "$spinstr" "$message"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
    done
    printf "\r${GREEN}[✓]${NC} ${WHITE}%s${NC} - ${GREEN}Done!${NC}                \n" "$message"
}

# Progress bar animation
progress_bar() {
    local duration=$1
    local message="$2"
    local width=50
    local progress=0
    
    echo -ne "${CYAN}[*]${NC} ${WHITE}$message${NC}\n"
    
    while [ $progress -le 100 ]; do
        local filled=$((progress * width / 100))
        local empty=$((width - filled))
        
        printf "\r${CYAN}[${NC}"
        printf "%${filled}s" | tr ' ' '█'
        printf "${DIM}%${empty}s${NC}" | tr ' ' '░'
        printf "${CYAN}]${NC} ${YELLOW}%d%%${NC}" "$progress"
        
        progress=$((progress + 2))
        sleep $(echo "scale=2; $duration / 50" | bc)
    done
    echo ""
}

# Matrix rain effect
matrix_effect() {
    clear_screen
    local columns=$(tput cols)
    local lines=$(tput lines)
    local chars=("0" "1")
    
    echo -e "${GREEN}"
    for (( i=0; i<30; i++ )); do
        for (( j=0; j<columns; j+=2 )); do
            if [ $((RANDOM % 3)) -eq 0 ]; then
                local y=$((RANDOM % lines))
                local char=${chars[$((RANDOM % 2))]}
                echo -ne "\033[${y};${j}H$char"
            fi
        done
    done
    sleep 0.5
    echo -e "${NC}"
}

# Cool ASCII Banner
show_banner() {
    clear_screen
    echo -e "${PURPLE}"
    cat << "EOF"
                                                                                 
        ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗        
        ██║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗       
        ██║██╔██╗ ██║     ██║█████╗  ██║        ██║   ██║   ██║██████╔╝       
        ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   ██║   ██║██╔══██╗       
        ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║       
        ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝       
                                                                              
                              ██╗  ██╗                                       
                              ╚██╗██╔╝                                       
                               ╚███╔╝                                        
                               ██╔██╗                                         
                              ██╔╝ ██╗                                        
                              ╚═╝  ╚═╝                                                                                                                     
              ⚡ Dependency Installer & Setup Wizard ⚡                   

    
EOF
    echo -e "${NC}"

    echo -e "${CYAN}║${NC}  ${BOLD}${PURPLE}Tool:${NC} ${GREEN}INJECTOR-X${NC}  ${DIM}►${NC} ${BOLD}${PURPLE}Version:${NC} ${GREEN}3.0${NC}  ${DIM}►${NC} ${BOLD}${PURPLE}Type:${NC} ${RED}Setup Wizard${NC}  ${CYAN}║${NC}"
    echo ""
}

# Function to check if a command exists
check_command() {
    command -v "$1" &> /dev/null
}

# Function to check package manager
detect_package_manager() {
    if check_command pkg; then
        PKG_MANAGER="pkg"
        INSTALL_CMD="pkg install -y"
    elif check_command apt; then
        PKG_MANAGER="apt"
        INSTALL_CMD="apt install -y"
    elif check_command apt-get; then
        PKG_MANAGER="apt-get"
        INSTALL_CMD="apt-get install -y"
    elif check_command yum; then
        PKG_MANAGER="yum"
        INSTALL_CMD="yum install -y"
    elif check_command dnf; then
        PKG_MANAGER="dnf"
        INSTALL_CMD="dnf install -y"
    elif check_command pacman; then
        PKG_MANAGER="pacman"
        INSTALL_CMD="pacman -S --noconfirm"
    else
        PKG_MANAGER="unknown"
        INSTALL_CMD=""
    fi
}

# Function to install a package
install_package() {
    local package="$1"
    local custom_name="$2"
    local display_name="${custom_name:-$package}"
    
    echo -ne "${YELLOW}[!]${NC} ${WHITE}$display_name${NC} is not installed. "
    echo -ne "${GREEN}Install? (y/n): ${NC}"
    read -r choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo -ne "${CYAN}[*]${NC} Installing ${WHITE}$display_name${NC}..."
        
        if [ "$PKG_MANAGER" == "unknown" ]; then
            echo -e "\n${RED}[✗] No package manager detected. Please install $display_name manually.${NC}"
            return 1
        fi
        
        if $INSTALL_CMD "$package" &> "$LOG_FILE"; then
            echo -e "\r${GREEN}[✓]${NC} ${WHITE}$display_name${NC} installed successfully!    "
            return 0
        else
            echo -e "\r${RED}[✗]${NC} Failed to install ${WHITE}$display_name${NC}        "
            echo -e "${YELLOW}[!] Check $LOG_FILE for details${NC}"
            return 1
        fi
    else
        echo -e "${RED}[✗]${NC} ${WHITE}$display_name${NC} is required. Installation skipped.${NC}"
        return 1
    fi
}

# Function to install Python if missing
install_python() {
    if check_command python; then
        echo -e "${GREEN}[✓]${NC} ${WHITE}Python${NC} is installed $(python --version 2>&1)"
        return 0
    elif check_command python3; then
        echo -e "${GREEN}[✓]${NC} ${WHITE}Python3${NC} is installed $(python3 --version 2>&1)"
        # Create symlink if python command doesn't exist
        if ! check_command python; then
            echo -e "${CYAN}[*]${NC} Creating python symlink..."
            if [ -f "$(which python3)" ]; then
                sudo ln -sf "$(which python3)" "$(dirname "$(which python3)")/python" 2>/dev/null
                echo -e "${GREEN}[✓]${NC} Symlink created"
            fi
        fi
        return 0
    else
        install_package "python" "Python" || install_package "python3" "Python3"
    fi
}

# Function to install Git
install_git() {
    if check_command git; then
        echo -e "${GREEN}[✓]${NC} ${WHITE}Git${NC} is installed $(git --version 2>&1 | head -n1)"
        return 0
    else
        install_package "git" "Git"
    fi
}

# Function to install Curl
install_curl() {
    if check_command curl; then
        echo -e "${GREEN}[✓]${NC} ${WHITE}Curl${NC} is installed $(curl --version 2>&1 | head -n1)"
        return 0
    else
        install_package "curl" "Curl"
    fi
}

# Function to install SQLMap
install_sqlmap() {
    local sqlmap_paths=(
        "$HOME/sqlmap/sqlmap.py"
        "/usr/share/sqlmap/sqlmap.py"
        "/opt/sqlmap/sqlmap.py"
    )
    
    for path in "${sqlmap_paths[@]}"; do
        if [ -f "$path" ]; then
            echo -e "${GREEN}[✓]${NC} ${WHITE}SQLMap${NC} is installed at: $path"
            export SQLMAP_PATH="$path"
            return 0
        fi
    done
    
    # Check if sqlmap command exists
    if check_command sqlmap; then
        echo -e "${GREEN}[✓]${NC} ${WHITE}SQLMap${NC} is installed (command available)"
        export SQLMAP_PATH="$(which sqlmap)"
        return 0
    fi
    
    echo -e "${YELLOW}[!]${NC} ${WHITE}SQLMap${NC} is not installed."
    echo -ne "${GREEN}[?]${NC} Install SQLMap? (y/n): "
    read -r choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}[*]${NC} Installing SQLMap..."
        
        # Try to install via package manager first
        if [ "$PKG_MANAGER" != "unknown" ]; then
            echo -ne "${CYAN}[*]${NC} Trying package manager installation..."
            if $INSTALL_CMD "sqlmap" &> "$LOG_FILE"; then
                echo -e "\r${GREEN}[✓]${NC} SQLMap installed via $PKG_MANAGER        "
                export SQLMAP_PATH="$(which sqlmap)"
                return 0
            fi
        fi
        
        # Clone from GitHub
        echo -e "${CYAN}[*]${NC} Cloning SQLMap from GitHub..."
        if git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$HOME/sqlmap" &> "$LOG_FILE"; then
            echo -e "${GREEN}[✓]${NC} SQLMap cloned successfully to $HOME/sqlmap"
            export SQLMAP_PATH="$HOME/sqlmap/sqlmap.py"
            return 0
        else
            echo -e "${RED}[✗]${NC} Failed to clone SQLMap"
            return 1
        fi
    else
        echo -e "${RED}[✗]${NC} SQLMap is required. Installation skipped.${NC}"
        return 1
    fi
}

# Function to create src directory and main.sh if not exists
create_main_script() {
    if [ ! -d "$SRC_DIR" ]; then
        echo -e "${CYAN}[*]${NC} Creating src directory..."
        mkdir -p "$SRC_DIR"
    fi
    
    if [ ! -f "$MAIN_SCRIPT" ]; then
        echo -e "${YELLOW}[!]${NC} ${WHITE}main.sh${NC} not found in src directory."
        echo -ne "${GREEN}[?]${NC} Create a sample main.sh? (y/n): "
        read -r choice
        
        if [[ "$choice" =~ ^[Yy]$ ]]; then
            cat > "$MAIN_SCRIPT" << 'EOF'
#!/bin/bash

# INJECTOR-X Main Script
echo "              INJECTOR-X Main Script Executed                "
echo "              All dependencies are satisfied!                "
echo ""
echo "SQLMap Path: ${SQLMAP_PATH:-$HOME/sqlmap/sqlmap.py}"
echo ""
echo "You can now add your main functionality here."
EOF
            chmod +x "$MAIN_SCRIPT"
            echo -e "${GREEN}[✓]${NC} Sample main.sh created at $MAIN_SCRIPT"
        else
            echo -e "${RED}[✗]${NC} main.sh is required to continue.${NC}"
            return 1
        fi
    fi
    
    # Make sure main.sh is executable
    chmod +x "$MAIN_SCRIPT" 2>/dev/null
    return 0
}

# Function to check all dependencies
check_all_dependencies() {
    local all_ok=true
    echo -e "${CYAN}${NC}              ${BOLD}🔍 CHECKING DEPENDENCIES 🔍${NC}                     ${CYAN}${NC}"
    echo ""
    # Check Python
    echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}[1/5]${NC} Checking Python..."
    if ! install_python; then
        all_ok=false
    fi
    
    # Check Git
    echo -e "\n${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}[2/5]${NC} Checking Git..."
    if ! install_git; then
        all_ok=false
    fi
    
    # Check Curl
    echo -e "\n${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}[3/5]${NC} Checking Curl..."
    if ! install_curl; then
        all_ok=false
    fi
    
    echo -e "${BOLD}[4/5]${NC} Checking SQLMap..."
    if ! install_sqlmap; then
        all_ok=false
    fi
    
    echo -e "${BOLD}[5/5]${NC} Checking ..."
    if ! create_main_script; then
        all_ok=false
    fi
    

    
    if [ "$all_ok" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to show summary
show_summary() {

    echo -e "${GREEN}${NC}       ${BOLD}✅ DEPENDENCY CHECK SUMMARY ✅${NC}       ${GREEN}${NC}"
    echo ""
    if check_command python || check_command python3; then
        echo -e "  ${GREEN}[✓]${NC} Python:        ${GREEN}Installed${NC}"
    else
        echo -e "  ${RED}[✗]${NC} Python:        ${RED}Missing${NC}"
    fi

    if check_command git; then
        echo -e "  ${GREEN}[✓]${NC} Git:           ${GREEN}Installed${NC}"
    else
        echo -e "  ${RED}[✗]${NC} Git:           ${RED}Missing${NC}"
    fi
    if check_command curl; then
        echo -e "  ${GREEN}[✓]${NC} Curl:          ${GREEN}Installed${NC}"
    else
        echo -e "  ${RED}[✗]${NC} Curl:          ${RED}Missing${NC}"
    fi
    
    if [ -f "${SQLMAP_PATH}" ] || check_command sqlmap; then
        echo -e "  ${GREEN}[✓]${NC} SQLMap:        ${GREEN}Installed${NC} (${SQLMAP_PATH:-$(which sqlmap)})"
    else
        echo -e "  ${RED}[✗]${NC} SQLMap:        ${RED}Missing${NC}"
    fi
    if [ -f "$MAIN_SCRIPT" ]; then
        echo -e "  ${GREEN}[✓]${NC} Main Script:   ${GREEN}Found${NC} ($MAIN_SCRIPT)"
    else
        echo -e "  ${RED}[✗]${NC} Main Script:   ${RED}Missing${NC}"
    fi
    echo ""
    echo -e "  ${YELLOW}Package Manager:${NC} ${PKG_MANAGER:-Unknown}"
    echo -e "  ${YELLOW}Log File:${NC} ${LOG_FILE}"
    echo ""
}

# Function to execute main script
execute_main() {

    echo -e "${CYAN}${NC}         ${BOLD}🚀 LAUNCHING INJECTOR-X 🚀${NC}                       ${CYAN}${NC}"
    echo ""
    
    progress_bar 2 "Initializing..."
    
    if [ -f "$MAIN_SCRIPT" ]; then
        echo -e "${GREEN}[✓]${NC} Executing..."

        echo ""
        
        # Export variables for main.sh
        export SQLMAP_PATH
        export TOOL_NAME="INJECTOR-X"
        export VERSION="3.0"
        
        # Execute main.sh
        bash "$MAIN_SCRIPT"
        
        # Check exit status
        if [ $? -eq 0 ]; then
            echo ""

            echo -e "${GREEN}[✓]${NC} Main script executed successfully"
        else
            echo ""
            echo -e "${RED}[✗]${NC} Main script exited with errors"
        fi
    else
        echo -e "${RED}[✗]${NC} Main script not found: $MAIN_SCRIPT"
        echo -e "${YELLOW}[!]${NC} Cannot continue without main.sh"
        return 1
    fi
}
main() {
    matrix_effect
    show_banner
    echo "INJECTOR-X Dependency Check Log - $(date)" > "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
    
    detect_package_manager
    echo -e "${CYAN}[*]${NC} Detected Package Manager: ${GREEN}${PKG_MANAGER:-Unknown}${NC}"
    echo "Package Manager: $PKG_MANAGER" >> "$LOG_FILE"
    if check_all_dependencies; then
        show_summary
        echo -e "${GREEN}${NC}         ${BOLD}✅ ALL DEPENDENCIES SATISFIED ✅${NC}                  ${GREEN}${NC}"
        echo -e "${GREEN}${NC}         ${WHITE}System is ready to launch INJECTOR-X${NC}              ${GREEN}${NC}"
        echo ""
        
        echo -ne "${GREEN}[?]${NC} ${BOLD}Launch INJECTOR-X now?${NC} ${DIM}(Y/n)${NC}: "
        read -r launch_choice
        if [[ ! "$launch_choice" =~ ^[Nn]$ ]]; then
            execute_main
        else
            echo -e "${YELLOW}[!]${NC} You can launch later with: ${GREEN}bash $MAIN_SCRIPT${NC}"
        fi   
    else
        show_summary
        echo -e "${RED}${NC}         ${BOLD}⚠️  SOME DEPENDENCIES ARE MISSING ⚠️${NC}              ${RED}${NC}"
        echo -e "${RED}${NC}         ${WHITE}Please install missing dependencies and retry${NC}      ${RED}${NC}"
        echo ""
        echo -e "${YELLOW}[!]${NC} Check the log file: ${GREEN}$LOG_FILE${NC}"
        echo -e "${YELLOW}[!]${NC} Run this script again after installing dependencies${NC}"
        exit 1
    fi
}
trap 'echo -e "\n\n${RED}[!]${NC} Installation interrupted by user"; exit 1' INT
main
exit 0