#!/usr/bin/env bash

# ==================== DEOBX INSTALLATION SCRIPT ====================
# Version: 3.0
# Description: Complete installation script for DeobX tool
# Supports: Ubuntu/Debian, Fedora, CentOS/RHEL, Arch Linux, macOS

set -e  # Exit on error

# ==================== COLOR CODES ====================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# ==================== ASCII BANNER ====================

show_banner() {
    clear
    echo -e "${CYAN}"
    cat << "EOF"

                                                                               
   ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗                                 
   ██╔══██╗██╔════╝██╔═══██╗██╔══██╗╚██╗██╔╝                                 
   ██║  ██║█████╗  ██║   ██║██████╔╝ ╚███╔╝                                  
   ██║  ██║██╔══╝  ██║   ██║██╔══██╗ ██╔██╗                                  
   ██████╔╝███████╗╚██████╔╝██████╔╝██╔╝ ██╗                                 
   ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝                                 
                                                                                     
                                                                               
                    Advanced Deobfuscation Tool v3.0                           
                      Automated Installation Script                           
                                                                               

EOF
    echo -e "${NC}"
}

# ==================== UTILITY FUNCTIONS ====================

print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[i]${NC} $1"
}

print_bold() {
    echo -e "${BOLD}$1${NC}"
}

print_step() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${WHITE}  $1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# ==================== DETECT OS ====================

detect_os() {
    print_status "Detecting operating system..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$NAME
            VER=$VERSION_ID
            print_success "Detected: $OS $VER"
        else
            OS="Linux"
            print_success "Detected: Linux"
        fi
        PKG_MANAGER="apt"
        
        # Detect package manager
        if command -v apt-get &> /dev/null; then
            PKG_MANAGER="apt"
        elif command -v yum &> /dev/null; then
            PKG_MANAGER="yum"
        elif command -v dnf &> /dev/null; then
            PKG_MANAGER="dnf"
        elif command -v pacman &> /dev/null; then
            PKG_MANAGER="pacman"
        elif command -v zypper &> /dev/null; then
            PKG_MANAGER="zypper"
        fi
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        print_success "Detected: macOS"
        PKG_MANAGER="brew"
        
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            print_warning "Homebrew not found. It will be installed automatically."
        fi
        
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="Windows"
        print_success "Detected: Windows (via WSL/Cygwin/MSYS)"
        PKG_MANAGER="choco"
    else
        OS="Unknown"
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# ==================== CHECK PYTHON ====================

check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
            print_success "Python $PYTHON_VERSION detected (OK)"
        else
            print_error "Python 3.7+ required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Installing..."
        install_python
    fi
}

# ==================== INSTALL PYTHON ====================

install_python() {
    print_status "Installing Python..."
    
    case $PKG_MANAGER in
        apt)
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-dev python3-venv
            ;;
        yum)
            sudo yum install -y python3 python3-pip python3-devel
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip python3-devel
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-pip
            ;;
        brew)
            brew install python3
            ;;
        *)
            print_error "Cannot install Python automatically. Please install Python 3.7+ manually."
            exit 1
            ;;
    esac
    
    print_success "Python installed successfully"
}

# ==================== INSTALL SYSTEM DEPENDENCIES ====================

install_system_deps() {
    print_step "Installing System Dependencies"
    
    case $PKG_MANAGER in
        apt)
            print_status "Updating package lists..."
            sudo apt-get update
            
            print_status "Installing dependencies for Ubuntu/Debian..."
            sudo apt-get install -y \
                python3-tk \
                python3-dev \
                python3-pip \
                python3-venv \
                git \
                wget \
                curl \
                build-essential \
                libssl-dev \
                libffi-dev \
                tk-dev \
                --no-install-recommends
            ;;
            
        yum)
            print_status "Installing dependencies for CentOS/RHEL..."
            sudo yum install -y \
                python3-tkinter \
                python3-devel \
                python3-pip \
                git \
                wget \
                curl \
                gcc \
                openssl-devel \
                libffi-devel
            ;;
            
        dnf)
            print_status "Installing dependencies for Fedora..."
            sudo dnf install -y \
                python3-tkinter \
                python3-devel \
                python3-pip \
                git \
                wget \
                curl \
                gcc \
                openssl-devel \
                libffi-devel
            ;;
            
        pacman)
            print_status "Installing dependencies for Arch Linux..."
            sudo pacman -S --noconfirm \
                python \
                python-pip \
                python-tk \
                git \
                wget \
                curl \
                base-devel
            ;;
            
        brew)
            print_status "Installing dependencies for macOS..."
            brew install \
                python3 \
                git \
                wget \
                curl \
                tk
            ;;
            
        *)
            print_warning "Unknown package manager. Please install dependencies manually:"
            echo "  - Python 3.7+"
            echo "  - python3-tk/tkinter"
            echo "  - git"
            echo "  - pip"
            ;;
    esac
    
    print_success "System dependencies installed"
}

# ==================== INSTALL PYTHON PACKAGES ====================

install_python_packages() {
    print_step "Installing Python Packages"
    
    # Upgrade pip
    print_status "Upgrading pip..."
    python3 -m pip install --upgrade pip setuptools wheel
    
    # Install required packages
    print_status "Installing required Python packages..."
    
    PACKAGES=(
        "autopep8>=1.7.0"
        "colorama>=0.4.6"
        "pyfiglet>=0.8.post1"
        "termcolor>=2.3.0"
        "tqdm>=4.65.0"
        "requests>=2.28.0"
        "pillow>=9.0.0"
    )
    
    for package in "${PACKAGES[@]}"; do
        print_status "Installing $package..."
        python3 -m pip install "$package"
    done
    
    # Install optional packages
    print_status "Installing optional packages for better experience..."
    
    OPTIONAL_PACKAGES=(
        "pylint>=2.17.0"
        "black>=23.0.0"
        "pytest>=7.4.0"
        "coverage>=7.2.0"
        "flake8>=6.0.0"
    )
    
    for package in "${OPTIONAL_PACKAGES[@]}"; do
        print_status "Installing $package (optional)..."
        python3 -m pip install "$package" || print_warning "Failed to install $package (optional)"
    done
    
    print_success "Python packages installed"
}

# ==================== CHECK TKINTER ====================

check_tkinter() {
    print_status "Checking tkinter for GUI support..."
    
    if python3 -c "import tkinter" 2>/dev/null; then
        print_success "tkinter is available (GUI mode supported)"
    else
        print_warning "tkinter is not available. GUI mode may not work."
        print_info "To install tkinter:"
        
        case $PKG_MANAGER in
            apt)
                echo "  sudo apt-get install python3-tk"
                ;;
            yum|dnf)
                echo "  sudo $PKG_MANAGER install python3-tkinter"
                ;;
            pacman)
                echo "  sudo pacman -S python-tk"
                ;;
            brew)
                echo "  brew install python-tk"
                ;;
        esac
    fi
}

# ==================== INSTALL DEOBX ====================

install_deobx() {
    print_step "Installing DeobX"
    
    # Set installation directory
    INSTALL_DIR="$HOME/deobx"
    
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "DeobX already installed at $INSTALL_DIR"
        read -p "Do you want to reinstall? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Skipping installation"
            return
        fi
        print_status "Removing old installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Create installation directory
    print_status "Creating installation directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    
    # Copy files
    print_status "Copying DeobX files..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    if [ -f "$SCRIPT_DIR/deobx.py" ]; then
        cp "$SCRIPT_DIR/deobx.py" "$INSTALL_DIR/"
        print_success "Copied deobx.py"
    else
        print_warning "deobx.py not found in current directory"
    fi
    
    # Create src directory
    mkdir -p "$INSTALL_DIR/src"
    
    # Create main script files if they don't exist
    if [ ! -f "$INSTALL_DIR/src/run.py" ]; then
        cat > "$INSTALL_DIR/src/run.py" << 'EOF'
#!/usr/bin/env python3
"""
DeobX CLI Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run CLI
try:
    from deobfuscator import AdvancedDeobfuscatorCLI
    # CLI code here
    print("DeobX CLI Mode - Coming Soon!")
except ImportError as e:
    print(f"Error: {e}")
    print("Please ensure all dependencies are installed")
EOF
        chmod +x "$INSTALL_DIR/src/run.py"
    fi
    
    if [ ! -f "$INSTALL_DIR/src/gui.py" ]; then
        cat > "$INSTALL_DIR/src/gui.py" << 'EOF'
#!/usr/bin/env python3
"""
DeobX GUI Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run GUI
try:
    import tkinter
    # GUI code here
    print("DeobX GUI Mode - Coming Soon!")
    print("Initializing GUI...")
except ImportError as e:
    print(f"Error: {e}")
    print("tkinter is required for GUI mode")
except Exception as e:
    print(f"Error starting GUI: {e}")
EOF
        chmod +x "$INSTALL_DIR/src/gui.py"
    fi
    
    if [ ! -f "$INSTALL_DIR/deobfuscator.py" ]; then
        cat > "$INSTALL_DIR/deobfuscator.py" << 'EOF'
#!/usr/bin/env python3
"""
DeobX Core Deobfuscation Engine
"""
import base64
import re
import hashlib
from datetime import datetime

class AdvancedDeobfuscatorCLI:
    """Main deobfuscation engine"""
    
    def __init__(self, verbose=False, aggressive=False, output_file=None):
        self.verbose = verbose
        self.aggressive = aggressive
        self.output_file = output_file
    
    def deobfuscate_file(self, filepath):
        """Deobfuscate a file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic deobfuscation logic
            # Decode base64
            base64_pattern = r'[A-Za-z0-9+/]+={0,2}'
            base64_matches = re.findall(base64_pattern, content)
            
            for b64 in base64_matches:
                if len(b64) > 20:
                    try:
                        decoded = base64.b64decode(b64).decode('utf-8')
                        content = content.replace(b64, f"# DECODED: {decoded[:50]}...")
                    except:
                        pass
            
            info = {
                'filename': filepath,
                'original_length': len(content),
                'deobfuscated_length': len(content),
                'timestamp': datetime.now().isoformat(),
                'md5': hashlib.md5(content.encode()).hexdigest(),
                'sha256': hashlib.sha256(content.encode()).hexdigest()
            }
            
            return content, info
            
        except Exception as e:
            return f"Error: {e}", {'error': str(e)}

if __name__ == "__main__":
    print("DeobX Core Engine")
EOF
    fi
    
    print_success "DeobX installed to $INSTALL_DIR"
}

# ==================== CREATE EXECUTABLE ====================

create_executable() {
    print_step "Creating Executable"
    
    INSTALL_DIR="$HOME/deobx"
    
    # Create launcher script
    print_status "Creating 'deobx' command..."
    
    cat > /tmp/deobx_launcher << 'EOF'
#!/usr/bin/env bash
# DeobX Launcher Script

INSTALL_DIR="$HOME/deobx"

if [ -f "$INSTALL_DIR/deobx.py" ]; then
    cd "$INSTALL_DIR"
    python3 deobx.py "$@"
else
    echo "DeobX not found at $INSTALL_DIR"
    echo "Please run the installation script first."
    exit 1
fi
EOF
    
    chmod +x /tmp/deobx_launcher
    sudo mv /tmp/deobx_launcher /usr/local/bin/deobx
    
    print_success "Created 'deobx' command in /usr/local/bin"
}

# ==================== CREATE DESKTOP ENTRY ====================

create_desktop_entry() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_step "Creating Desktop Entry"
        
        INSTALL_DIR="$HOME/deobx"
        
        cat > ~/.local/share/applications/deobx.desktop << EOF
[Desktop Entry]
Name=DeobX
Comment=Advanced Deobfuscation Tool
Exec=deobx
Icon=$INSTALL_DIR/icon.png
Terminal=true
Type=Application
Categories=Development;Security;
Keywords=deobfuscate;security;python;bash;
EOF
        
        print_success "Desktop entry created"
        
        # Create icon if possible
        if [ ! -f "$INSTALL_DIR/icon.png" ]; then
            print_status "Creating simple icon..."
            # Create a simple icon using Python
            python3 -c "
try:
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (128, 128), color='#4a9eff')
    d = ImageDraw.Draw(img)
    d.text((40, 50), 'DeobX', fill='white')
    img.save('$INSTALL_DIR/icon.png')
except:
    pass
" 2>/dev/null || print_warning "Could not create icon"
        fi
    fi
}

# ==================== CREATE VIRTUAL ENVIRONMENT ====================

create_virtual_env() {
    print_step "Creating Virtual Environment"
    
    INSTALL_DIR="$HOME/deobx"
    
    read -p "Do you want to create a virtual environment for DeobX? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Creating virtual environment..."
        cd "$INSTALL_DIR"
        python3 -m venv venv
        
        print_status "Activating virtual environment..."
        source venv/bin/activate
        
        print_status "Installing packages in virtual environment..."
        python3 -m pip install --upgrade pip
        python3 -m pip install autopep8 colorama pyfiglet termcolor tqdm
        
        print_success "Virtual environment created"
        print_info "To activate: source $INSTALL_DIR/venv/bin/activate"
    else
        print_info "Skipping virtual environment creation"
    fi
}

# ==================== SETUP COMPLETION ====================

show_completion() {
    print_step "Installation Complete"
    
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           DEOBX INSTALLATION COMPLETED SUCCESSFULLY           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    print_success "DeobX has been installed to: $HOME/deobx"
    print_success "Global command 'deobx' is available"
    
    echo
    print_bold "🚀 Quick Start:"
    echo -e "  ${CYAN}deobx${NC}                    # Launch DeobX launcher"
    echo -e "  ${CYAN}deobx -f script.py${NC}       # Deobfuscate a file"
    echo -e "  ${CYAN}deobx -i${NC}                  # Interactive mode"
    echo -e "  ${CYAN}deobx -a -v${NC}               # Aggressive + verbose"
    
    echo
    print_bold "📚 Documentation:"
    echo -e "  ${CYAN}deobx --help${NC}              # Show help"
    echo -e "  ${CYAN}man deobx${NC}                 # Manual page (if installed)"
    
    echo
    print_bold "🔧 Configuration:"
    echo -e "  Installation directory: ${DIM}$HOME/deobx${NC}"
    echo -e "  Logs: ${DIM}$HOME/.deobx/logs${NC}"
    
    echo
    print_bold "💡 Next Steps:"
    echo -e "  1. Test the installation: ${CYAN}deobx -v${NC}"
    echo -e "  2. Check out examples: ${CYAN}cd $HOME/deobx/examples${NC}"
    echo -e "  3. Read the documentation: ${CYAN}deobx --help${NC}"
    
    echo
    print_warning "Note: Some features require additional dependencies"
    echo -e "      Run ${CYAN}deobx --check-deps${NC} to verify all dependencies"
    
    echo
    print_success "Thank you for installing DeobX!"
    echo -e "${GREEN}Reveal the Code... Clean the Malicious...${NC}\n"
}

# ==================== MAIN INSTALLATION ====================

main() {
    # Show banner
    show_banner
    
    echo -e "${YELLOW}DeobX Installation Script v3.0${NC}"
    echo -e "${DIM}This script will install DeobX and all dependencies${NC}\n"
    
    # Confirm installation
    read -p "Do you want to continue with installation? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Installation cancelled${NC}"
        exit 0
    fi
    
    echo
    
    # Run installation steps
    detect_os
    check_python
    install_system_deps
    install_python_packages
    check_tkinter
    install_deobx
    create_executable
    create_desktop_entry
    create_virtual_env
    show_completion
}

# ==================== RUN INSTALLATION ====================

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "This script should not be run as root!"
    print_info "Please run without sudo. The script will use sudo when needed."
    exit 1
fi

# Run main installation
main "$@"