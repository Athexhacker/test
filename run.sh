#!/usr/bin/env bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BLACK='\033[0;30m'
ORANGE='\033[0;33m'
MAGENTA='\033[0;35m'
LIGHT_RED='\033[1;31m'
LIGHT_GREEN='\033[1;32m'
LIGHT_BLUE='\033[1;34m'
LIGHT_PURPLE='\033[1;35m'
LIGHT_CYAN='\033[1;36m'
BOLD='\033[1m'
NC='\033[0m' 
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_BLUE='\033[44m'
BG_PURPLE='\033[45m'
BG_CYAN='\033[46m'
BG_YELLOW='\033[43m'


clear

print_banner() {
    local frame=$1
    local colors=($RED $GREEN $YELLOW $BLUE $PURPLE $CYAN $WHITE)
    case $frame in
        0|6)
            echo -e "${colors[$frame]}"
            cat << "EOF"

          ██╗   ██╗███╗   ██╗██╗███████╗██╗███████╗██████╗            
          ██║   ██║████╗  ██║██║██╔════╝██║██╔════╝██╔══██╗           
          ██║   ██║██╔██╗ ██║██║█████╗  ██║█████╗  ██║  ██║           
          ██║   ██║██║╚██╗██║██║██╔══╝  ██║██╔══╝  ██║  ██║           
          ╚██████╔╝██║ ╚████║██║██║     ██║███████╗██████╔╝           
           ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚══════╝╚═════╝                     
    
EOF
            ;;
        1|7)
            echo -e "${colors[$frame]}"
            cat << "EOF"

                          🔐 SECURITY ANALYZER 🔐                       
                             PROFESSIONAL EDITION                       
///═════════════════════════════════════════════════════════════════///
                                                                       
          ⚡ Network Monitoring    |    🕷️  Deep Web Crawler            
          🧩 Extension Analysis    |    🌐 Web App Scanner             
          📊 Live Progress         |    🎯 Real-time Detection         
                                                                       
                     🚀 Version 3.0 Professional                  
    
EOF
            ;;
        2|8)
            echo -e "${colors[$frame]}"
            cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
    ║     ░█▀▀░█▀█░█▀▄░█▀▀░█░█░░░█▀▄░█▀█░█▀▀░█░█░░░█▀▀░█▀█░█▀▄░░        ║
    ║     ░█░░░█░█░█░█░█▀▀░▄▀▄░░░█░█░█░█░█▀▀░█▄█░░░█░░░█░█░█░█░░        ║
    ║     ░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀░░░        ║
    ║     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
    ║                                                                   ║
    ║              🔥 PROFESSIONAL SECURITY SUITE 🔥                    ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
            ;;
        3|9)
            echo -e "${colors[$frame]}"
            cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ╔═╗╦ ╦╔╦╗╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╔═╗╔═╗╔╦╗╔═╗╦ ╦╔╗╔╔╦╗╔═╗            ║
    ║     ╠═╣║ ║ ║ ╠═╣ ║ ║╣ ║║║ ║   ║  ║ ║║║║╠═╣║ ║║║║ ║ ╚═╗            ║
    ║     ╩ ╩╚═╝ ╩ ╩ ╩ ╩ ╚═╝╝╚╝ ╩   ╚═╝╚═╝╩ ╩╩ ╩╚═╝╝╚╝ ╩ ╚═╝            ║
    ║                                                                   ║
    ║                    🛡️  ZERO TRUST READY  🛡️                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
            ;;
        4|10)
            echo -e "${colors[$frame]}"
            cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    🌐 WEB SCANNER    │    📡 NETWORK MONITOR    │    🧩 EXTENSION  ║
    ║    ─────────────────────────────────────────────────────────────   ║
    ║    ✓ SQL Injection   │    ✓ API Key Detection │    ✓ Hardcoded    ║
    ║    ✓ XSS Testing     │    ✓ Traffic Analysis  │    ✓ Permissions  ║
    ║    ✓ Path Traversal  │    ✓ Live Statistics   │    ✓ Obfuscation  ║
    ║    ✓ CSRF Checks     │    ✓ Packet Capture    │    ✓ External API ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
            ;;
        5|11)
            echo -e "${colors[$frame]}"
            cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ████████╗ ██████╗  ██████╗ ██╗     ███████╗████████╗          ║
    ║     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝╚══██╔══╝          ║
    ║        ██║   ██║   ██║██║   ██║██║     █████╗     ██║             ║
    ║        ██║   ██║   ██║██║   ██║██║     ██╔══╝     ██║             ║
    ║        ██║   ╚██████╔╝╚██████╔╝███████╗███████╗   ██║             ║
    ║        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝             ║
    ║                                                                   ║
    ║                     🔧 INSTALLATION SCRIPT 🔧                     ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
            ;;
    esac
}

loading_animation() {
    local pid=$1
    local message=$2
    local spinstr='|/-\'
    local temp
    
    echo -ne "${CYAN}$message ${NC}"
    
    while ps -p $pid > /dev/null 2>&1; do
        temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        spinstr=$temp${spinstr%"$temp"}
        sleep 0.1
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
    echo -e "${GREEN}✓ Done!${NC}"
}

animate_banner() {
    for i in {0..5}; do
        clear
        print_banner $i
        sleep 0.3
    done
}

glitch_effect() {
    local text=$1
    local glitch_chars='!@#$%&*<>?/\\|'
    
    for i in {1..3}; do
        echo -ne "\r${RED}${text:0:${#text}-$i}${glitch_chars:RANDOM%${#glitch_chars}:1}${NC}"
        sleep 0.1
    done
    echo -ne "\r${GREEN}${text}${NC}\n"
}

matrix_effect() {
    local chars="01アイウエオカキクケコサシスセソタチツテト"
    local lines=5
    
    for ((l=0; l<lines; l++)); do
        for ((i=0; i<40; i++)); do
            echo -ne "\e[32m${chars:RANDOM%${#chars}:1}\e[0m"
        done
        echo
        sleep 0.1
    done
}

print_step() {
    echo -e "\n${BOLD}${BLUE}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}   ⚡ $1${NC}"
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 found"
        return 0
    else
        print_warning "$1 not found"
        return 1
    fi
}

progress_bar() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    printf "\r${CYAN}[${NC}"
    printf "%${completed}s" | tr ' ' '█'
    printf "%${remaining}s" | tr ' ' '░'
    printf "${CYAN}]${NC} ${GREEN}%3d%%${NC}" $percentage
}


animate_banner

echo -e "\n${GREEN}Initializing security protocols...${NC}\n"
matrix_effect
sleep 1

echo -e "\n${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}                    🔐 LEGAL NOTICE & DISCLAIMER                     ${NC}"
echo -e "${BOLD}${RED}///═══════════════════════════════════════════════════════════════════///${NC}"
echo -e "${BOLD}${RED}${NC}                                                                   ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}  ${YELLOW}Unified Security Analysis Tool is for AUTHORIZED testing ONLY!${NC}   ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}                                                                   ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}  • Only scan systems you own or have permission to test           ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}  • Network monitoring may be subject to local laws                 ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}  • The user assumes all responsibility for compliance              ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}  • Handle all findings confidentially                               ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}                                                                   ${BOLD}${RED}${NC}"
echo -e "${BOLD}${RED}${NC}\n"

echo -ne "${BOLD}${YELLOW}Do you accept these terms and wish to continue? (y/N): ${NC}"
read -r agreement

if [[ ! "$agreement" =~ ^[Yy]$ ]]; then
    echo -e "\n${RED}Installation cancelled.${NC}"
    exit 0
fi

echo -e "\n${GREEN}✓ Terms accepted. Starting installation...${NC}\n"
sleep 1

print_step "🔍 SYSTEM CHECK"

echo -ne "${CYAN}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
if [[ $(echo "$python_version" | cut -d. -f1) -ge 3 ]] && [[ $(echo "$python_version" | cut -d. -f2) -ge 6 ]]; then
    echo -e "\r${GREEN}✅ Python $python_version found${NC}"
else
    echo -e "\r${RED}❌ Python 3.6+ required (found $python_version)${NC}"
    exit 1
fi

echo -ne "${CYAN}Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "\r${GREEN}✅ pip3 found${NC}"
else
    echo -e "\r${RED}❌ pip3 not found${NC}"
    exit 1
fi

echo -ne "${CYAN}Checking permissions...${NC}"
if [[ $EUID -eq 0 ]]; then
    echo -e "\r${GREEN}✅ Running as root (network monitoring enabled)${NC}"
else
    echo -e "\r${YELLOW}⚠️  Not running as root (network monitoring may be limited)${NC}"
    print_warning "Network monitoring requires root privileges"
    print_info "You can run: sudo -E python3 install.py after installation"
fi
sleep 1

print_step "📦 CREATING VIRTUAL ENVIRONMENT"

echo -ne "${CYAN}Creating venv...${NC}"
python3 -m venv venv > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "\r${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "\r${YELLOW}⚠️  Could not create virtual environment${NC}"
    print_warning "Installing globally instead"
fi

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Virtual environment activated"
fi

print_step "📥 INSTALLING DEPENDENCIES"

DEPENDENCIES=(
    "requests"
    "beautifulsoup4"
    "scapy"
    "cryptography"
    "dnspython"
    "lxml"
    "colorama"
)

TOTAL=${#DEPENDENCIES[@]}
CURRENT=0

for dep in "${DEPENDENCIES[@]}"; do
    ((CURRENT++))
    progress_bar $CURRENT $TOTAL
    echo -ne " ${CYAN}Installing $dep...${NC}"
    
    pip3 install --quiet $dep 2>&1 &
    PID=$!
    wait $PID
    
    if [ $? -eq 0 ]; then
        echo -e "\r${GREEN}✅ $dep installed${NC}                    "
    else
        echo -e "\r${RED}❌ Failed to install $dep${NC}                "
    fi
done

echo -e "\n${GREEN}✓ Dependencies installed${NC}"
sleep 1

print_step "📝 CREATING INSTALLATION FILE"

cat > install.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil
from datetime import datetime

BANNER = """
\033[1;36m
           ╔═══════════════════════════════════════════════════════════════╗
           ║  ██╗   ██╗███╗   ██╗██╗███████╗██╗███████╗██████╗   ╔══════╗  ║
           ║  ██║   ██║████╗  ██║██║██╔════╝██║██╔════╝██╔══██╗  ║ CYBER║  ║
           ║  ██║   ██║██╔██╗ ██║██║█████╗  ██║█████╗  ██║  ██║  ║  ═════╝  ║
           ║  ██║   ██║██║╚██╗██║██║██╔══╝  ██║██╔══╝  ██║  ██║  ║ ELITE  ║
           ║  ╚██████╔╝██║ ╚████║██║██║     ██║███████╗██████╔╝  ║  ═════╗  ║
           ║   ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚══════╝╚═════╝   ║ TOOL  ║  ║
           ╚═══════════════════════════════════════════════════════════════╝
\033[0m
"""
SKULL = """
\033[1;31m
                     ▄▄▄▄▄▄▄▄▄▄▄
                  ▄█████████████████▄
                ███████████████████████
               █████████████████████████
               █████████████████████████
               ████████████▀▀███████████
               ███████████   ███████████
               ███████████   ███████████
               ███████████   ███████████
               █████████████████████████
               █████████████████████████
               █████████████████████████
                ███████████████████████
                  ▀█████████████████▀
                      ▀▀▀▀▀▀▀▀▀
\033[0m
"""

SRC_MAIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "main")

def clear_screen():
    """Clear the terminal screen with style"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_animated(text, delay=0.03):
    """Print text with typewriter animation"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(message="Loading", duration=1):
    """Show a loading animation"""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    for i in range(int(duration * 10)):
        sys.stdout.write(f'\r\033[1;36m{message} {chars[i % len(chars)]}\033[0m')
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def print_progress_bar(current, total, bar_length=50, title="Progress"):
    """Display a progress bar"""
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    sys.stdout.write(f"\r\033[1;33m{title}: [{arrow}{spaces}] {percent:.1f}%\033[0m")
    sys.stdout.flush()

def print_menu():
    """Print the main menu with animations"""
    clear_screen()
    print(BANNER)
    
    print("\033[1;35m" + "▓" * 70 + "\033[0m")
    print("\033[1;33m██\033[0m" + " " * 30 + "\033[1;32mMAIN CONTROL PANEL\033[0m" + " " * 30 + "\033[1;33m██\033[0m")
    print("\033[1;35m" + "▓" * 70 + "\033[0m")
    
    print("\n\033[1;36m    ⚡ [1]\033[0m \033[1;37mRUN TOOL\033[0m          \033[1;90m- Execute unified security suite\033[0m")
    print("\033[1;36m    🔍 [2]\033[0m \033[1;37mABOUT\033[0m            \033[1;90m- View tool information and credits\033[0m")
    print("\033[1;36m    🚪 [3]\033[0m \033[1;37mEXIT\033[0m             \033[1;90m- Leave the matrix\033[0m")
    
    print("\n\033[1;35m" + "─" * 70 + "\033[0m")
    
    terminal_size = shutil.get_terminal_size().columns
    print(f"\033[1;90m    System: {sys.platform.upper()} | Time: {datetime.now().strftime('%H:%M:%S')} | Terminal: {terminal_size} cols\033[0m")
    print("\033[1;35m" + "─" * 70 + "\033[0m")

def run_tool():
    """Option 1: Automatically run the main tool with enhanced visualization"""
    clear_screen()
    print(BANNER)
    print("\n\033[1;33m" + "="*70 + "\033[0m")
    print("\033[1;32m🚀 LAUNCHING UNIFIED\033[0m".center(70))
    print("\033[1;33m" + "="*70 + "\033[0m\n")
    
    print_animated("\033[1;36m[SYSTEM] Initializing security protocols...\033[0m")
    time.sleep(0.5)
    
    if not os.path.exists(SRC_MAIN_DIR):
        print(f"\n\033[1;31m[✗] CRITICAL ERROR: Directory '{SRC_MAIN_DIR}' not found!\033[0m")
        print("\033[1;33m[!] Please ensure the src/main directory exists and try again.\033[0m")
        input("\n\033[1;33mPress Enter to return to main menu...\033[0m")
        return
    
    loading_animation("Scanning directory", 1)
    
    tool_script = None
    possible_names = ['unified.py']
    
    for name in possible_names:
        script_path = os.path.join(SRC_MAIN_DIR, name)
        if os.path.isfile(script_path):
            tool_script = script_path
            print(f"\033[1;32m[✓] Found tool: {name}\033[0m")
            time.sleep(0.3)
            break
    
    if not tool_script:
        scripts = [f for f in os.listdir(SRC_MAIN_DIR) 
                  if f.endswith('.py') and os.path.isfile(os.path.join(SRC_MAIN_DIR, f))]
        if scripts:
            tool_script = os.path.join(SRC_MAIN_DIR, scripts[0])
            print(f"\033[1;33m[!] Using first available script: {scripts[0]}\033[0m")
            time.sleep(0.3)
    
    if not tool_script:
        print(f"\n\033[1;31m[✗] No Python scripts found in {SRC_MAIN_DIR}\033[0m")
        input("\n\033[1;33mPress Enter to return to main menu...\033[0m")
        return
    
    print("\n\033[1;36m[INFO] Initializing tool components...\033[0m")
    for i in range(101):
        print_progress_bar(i, 100, title="\033[1;32mLoading")
        time.sleep(0.01)
    print("\n")
    
    print(f"\033[1;32m[✓] Tool loaded successfully!\033[0m")
    print("\033[1;33m" + "─"*70 + "\033[0m")
    print(f"\033[1;36m[EXECUTING] {os.path.basename(tool_script)}\033[0m")
    print("\033[1;33m" + "─"*70 + "\033[0m\n")
    
    try:
        if os.name != 'nt':  
            os.chmod(tool_script, 0o755)
        
        result = subprocess.run([sys.executable, tool_script], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode != 0:
            print(f"\n\033[1;31m[✗] Tool exited with code {result.returncode}\033[0m")
        else:
            print(f"\n\033[1;32m[✓] Tool execution completed successfully!\033[0m")
            
    except Exception as e:
        print(f"\n\033[1;31m[✗] Failed to run tool: {e}\033[0m")
    
    input("\n\033[1;33mPress Enter to return to main menu...\033[0m")

def about():
    """Enhanced about section with detailed information"""
    clear_screen()
    print(BANNER)
    print("\n\033[1;35m" + "★"*70 + "\033[0m")
    print("\033[1;33m📋 ABOUT UNIFIED SECURITY TOOL\033[0m".center(70))
    print("\033[1;35m" + "★"*70 + "\033[0m\n")

    about_script_path = os.path.join(SRC_MAIN_DIR, "about.py")
    
    if os.path.exists(about_script_path):
        print_animated("\033[1;36m[INFO] Loading detailed information...\033[0m")
        time.sleep(0.5)
        print("\033[1;33m" + "─"*70 + "\033[0m\n")
        
        try:
            subprocess.run([sys.executable, about_script_path])
        except Exception as e:
            print(f"\n\033[1;31m[ERROR] Failed to run about script: {e}\033[0m")
    else:
        print(SKULL)
        time.sleep(0.5)
        
        print("\033[1;36m╔══════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[1;36m║                    TOOL INFORMATION                          ║\033[0m")
        print("\033[1;36m╚══════════════════════════════════════════════════════════════╝\033[0m\n")
        
        print("\033[1;33m📌 NAME:\033[0m \033[1;37mUNIFIED - Advanced Security Testing Framework\033[0m")
        print("\033[1;33m📌 VERSION:\033[0m \033[1;37m2.0.0 (Quantum Edition)\033[0m")
        print("\033[1;33m📌 RELEASE:\033[0m \033[1;37m2026\033[0m\n")
        
        print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
        
        print("\033[1;32m🔷 DESCRIPTION:\033[0m")
        print_animated("  A cutting-edge, all-in-one security assessment platform designed")
        print_animated("  for elite penetration testers and security professionals. UNIFIED")
        print_animated("  combines multiple security testing methodologies into a single,")
        print_animated("  powerful interface with advanced automation capabilities.\n")
        
        print("\033[1;32m🔷 CORE FEATURES:\033[0m")
        features = [
            "⚡ Advanced Vulnerability Assessment & Scanning",
            "🕸️ Web Application Security Testing",
            "📊 Professional Report Generation",
            "🤖 AI-Powered Threat Detection",
        ]
        
        for feature in features:
            print(f"  \033[1;37m{feature}\033[0m")
            time.sleep(0.1)
        
        print("\n\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
        
        print("\033[1;32m🔷 TECHNICAL SPECIFICATIONS:\033[0m")
        print("  \033[1;37m├─ Language:\033[0m Python 3.8+")
        print("  \033[1;37m├─ Architecture:\033[0m Modular Plugin-Based")
        print("  \033[1;37m├─ Database:\033[0m SQLite/PostgreSQL Support")
        print("  \033[1;37m├─ API Support:\033[0m RESTful & GraphQL")
        print("  \033[1;37m└─ Platforms:\033[0m Linux, macOS, Windows\n")
        
        print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
        
        print("\033[1;32m🔷 REQUIREMENTS:\033[0m")
        print("  \033[1;37m• Python 3.8 or higher\033[0m")
        print("  \033[1;37m• 4GB RAM minimum (8GB recommended)\033[0m")
        print("  \033[1;37m• 1GB free disk space\033[0m")
        print("  \033[1;37m• Root/Admin privileges for某些功能\033[0m\n")
        
        print("\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
        
        print("\033[1;32m🔷 CREATED BY:\033[0m")
        print("  \033[1;35m\033[0m")
        print("  \033[1;35m\033[0m  \033[1;33mMarkhor (TEAM ATHEX)\033[0m                        \033[1;35m\033[0m")
        print("  \033[1;35m \033[0m      Fixed and Maintained by TEAM ATHEX Leader ATHEX BLACK HAT\033[1;35m\033[0m")
        print("  \033[1;35m\033[0m  \033[1;34mhttps://github.com/Athexhacker\033[0m                \033[1;35m\033[0m")
        print("  \033[1;35m\033[0m\n")
        
        print("\033[1;32m🔷 LICENSE:\033[0m")
        print("  \033[1;37mMIT License - Copyright (c) 2026 TEAM ATHEX BLACK HAT\033[0m")
        print("  \033[1;90mFree to use, modify, and distribute with attribution\033[0m\n")
        
        print("\033[1;32m🔷 DISCLAIMER:\033[0m")
        print("  \033[1;31m⚠️  This tool is for authorized security testing only!\033[0m")
        print("  \033[1;31m   Users are responsible for compliance with applicable laws.\033[0m")
    
    print("\n\033[1;35m" + "★"*70 + "\033[0m")
    input("\n\033[1;33mPress Enter to return to main menu...\033[0m")

def exit_animation():
    """Show exit animation"""
    clear_screen()
    print(BANNER)
    print("\n\033[1;35m" + "="*70 + "\033[0m")
    print("\033[1;33mThank you for using UNIFIED Security Tool!\033[0m".center(70))
    print("\033[1;35m" + "="*70 + "\033[0m\n")
    
    messages = [
        "\033[1;36m[•] Clearing security protocols...\033[0m",
        "\033[1;36m[•] Closing connections...\033[0m",
        "\033[1;36m[•] Wiping temporary data...\033[0m",
        "\033[1;32m[✓] System secured. Goodbye!\033[0m"
    ]
    
    for msg in messages:
        print_animated(msg, 0.02)
        time.sleep(0.3)
    
    print("\n\033[1;35m" + "▄"*70 + "\033[0m")
    time.sleep(1)

def main():
    """Main function with enhanced error handling"""
    try:
        clear_screen()
        print(BANNER)
        loading_animation("Initializing UNIFIED system", 2)
        
        while True:
            print_menu()
            
            try:
                choice = input("\n\033[1;36m[?] Enter your choice (1-3): \033[0m").strip()
                
                if choice == '1':
                    run_tool()
                elif choice == '2':
                    about()
                elif choice == '3':
                    exit_animation()
                    sys.exit(0)
                else:
                    print("\n\033[1;31m[✗] Invalid choice! Please enter 1, 2, or 3.\033[0m")
                    time.sleep(1)
                    
            except (EOFError, KeyboardInterrupt):
                print("\n\n\033[1;33m[!] Returning to main menu...\033[0m")
                time.sleep(1)
                continue
                
    except KeyboardInterrupt:
        exit_animation()
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[1;31m[CRITICAL ERROR] {e}\033[0m")
        print("\033[1;33mPlease report this issue to the developer.\033[0m")
        time.sleep(3)
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x install.py
print_success "install.py created"

print_step "🚀 FINAL INSTALLATION"

echo -e "${CYAN}Running Python installation script...${NC}\n"
python3 install.py

if [ ! -f "install.py" ] && [ ! -f "install.py" ]; then
    print_warning "Main tool file not found in current directory"
    print_info "Please ensure your install.py Python file is in this directory"
    print_info "Expected filename: install.py"
    
    echo -ne "\n${YELLOW}Enter the filename of your security tool (or press Enter to skip): ${NC}"
    read -r tool_file
    
    if [ -n "$tool_file" ] && [ -f "$tool_file" ]; then
        print_success "Found $tool_file"
        chmod +x "$tool_file"
    fi
fi

# Final ASCII art
clear
echo -e "${GREEN}"
cat << "EOF"
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║      ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗            ║
    ║      ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║            ║
    ║      ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║            ║
    ║      ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║            ║
    ║      ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗       ║
    ║      ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝       ║
    ║                                                                   ║
    ║                      🎉 INSTALLATION COMPLETE! 🎉                ║
    ║                                                                   ║
    ╠═══════════════════════════════════════════════════════════════════╣
EOF
echo -e "${NC}"

# Show dependency status
print_step "📊 DEPENDENCY STATUS"

deps_ok=0
deps_total=5

# Check each dependency
check_command "python3" && ((deps_ok++))
python3 -c "import requests" 2>/dev/null && print_success "requests installed" && ((deps_ok++))
python3 -c "import bs4" 2>/dev/null && print_success "beautifulsoup4 installed" && ((deps_ok++))
python3 -c "import scapy" 2>/dev/null && print_success "scapy installed" && ((deps_ok++))
python3 -c "import cryptography" 2>/dev/null && print_success "cryptography installed" && ((deps_ok++))

echo
if [ $deps_ok -eq $deps_total ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some dependencies are missing ($deps_ok/$deps_total)${NC}"
    print_info "Run: pip install -r requirements.txt"
fi

# Create requirements.txt for future reference
cat > requirements.txt << 'EOF'
requests>=2.26.0
beautifulsoup4>=4.10.0
scapy>=2.4.5
cryptography>=3.4.8
dnspython>=2.1.0
lxml>=4.6.3
colorama>=0.4.4
EOF

print_success "Created requirements.txt"

# Glitch effect for fun
echo -e "\n"
glitch_effect "SYSTEM READY"
echo -e "\n"

# Final countdown
echo -ne "${CYAN}Launching tool in ${NC}"
for i in 3 2 1; do
    echo -ne "${GREEN}$i${NC} "
    sleep 0.5
done
echo -e "${GREEN}GO!${NC}\n"
sleep 0.5

# Check for main tool file and run it
if [ -f "install.py" ]; then
    python3 install.py
elif [ -f "install.py" ]; then
    python3 install.py
else
    # Save the provided Python code
    echo -e "${YELLOW}Main tool file not found. Creating from provided code...${NC}"
    
    cat > install.py << 'PYTHON_CODE'
#!/usr/bin/env python3
"""
Unified Security Analysis Tool - Professional Edition
Paste your provided Python code here
"""
PYTHON_CODE
    
    echo -e "${YELLOW}Please paste your Python tool code into install.py${NC}"
    echo -e "${GREEN}Installation complete! Run: python3 install.py${NC}"
    
    # Open in editor if possible
    if command -v nano &> /dev/null; then
        echo -ne "\n${CYAN}Open in nano editor now? (y/N): ${NC}"
        read -r open_editor
        if [[ "$open_editor" =~ ^[Yy]$ ]]; then
            nano install.py
        fi
    fi
fi
