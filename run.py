#!/usr/bin/env python3
"""
Comprehensive Installation Tool
Author: System Administrator
Description: Automated installation and management tool with visual enhancements
"""

import os
import sys
import subprocess
import time
import shutil
from pathlib import Path
import importlib.metadata
from typing import List, Tuple

# ANSI color codes for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'
    YELLOW = '\033[33m'
    RED = '\033[31m'

# Cool ASCII Banner
ASCII_BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ██████╗ 
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝   ██╔═══██╗██╔══██╗
██║  ███╗███████║██║   ██║███████╗   ██║█████╗██║   ██║██████╔╝
██║   ██║██╔══██║██║   ██║╚════██║   ██║╚════╝██║▄▄ ██║██╔══██╗
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ╚██████╔╝██║  ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚══▀▀═╝ ╚═╝  ╚═╝
                                                               
               POWERED BY ATHEX BLACK HAT   
{Colors.ENDC}
"""

def animate_loading(message: str, duration: float = 1.5):
    """Display an animated loading indicator"""
    animation_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.CYAN}{animation_chars[i % len(animation_chars)]} {message}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r✓ {message}{' ' * 20}\n")
    sys.stdout.flush()

def animate_progress(description: str, total_steps: int = 10):
    """Display a progress bar animation"""
    for i in range(total_steps + 1):
        progress = int(50 * i / total_steps)
        bar = "█" * progress + "░" * (50 - progress)
        sys.stdout.write(f"\r{Colors.GREEN}{description}: [{bar}] {int(100 * i / total_steps)}%{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def print_status(message: str, status: str = "INFO"):
    """Print formatted status messages"""
    status_colors = {
        "INFO": Colors.BLUE,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.FAIL
    }
    color = status_colors.get(status, Colors.CYAN)
    symbol = {
        "INFO": "ℹ",
        "SUCCESS": "✓",
        "WARNING": "⚠",
        "ERROR": "✗"
    }.get(status, "•")
    
    print(f"{color}[{symbol}] {message}{Colors.ENDC}")

def check_root() -> bool:
    """Check if script is running with root privileges"""
    if os.geteuid() != 0:
        print_status("This script must be run as root/sudo!", "ERROR")
        print(f"{Colors.YELLOW}Please run: sudo python3 {sys.argv[0]}{Colors.ENDC}")
        return False
    print_status("Root privileges confirmed", "SUCCESS")
    return True

def read_requirements(file_path: str = "requirements.txt") -> List[str]:
    """Read and parse requirements.txt file"""
    if not Path(file_path).exists():
        print_status(f"{file_path} not found. Skipping dependency check.", "WARNING")
        return []
    
    with open(file_path, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return requirements

def check_installed_packages() -> Tuple[List[str], List[str]]:
    """Check which packages from requirements are installed"""
    try:
        installed = [dist.metadata['Name'].lower() for dist in importlib.metadata.distributions()]
    except Exception:
        # Fallback to pip list if importlib fails
        result = subprocess.run(['pip', 'list', '--format=freeze'], capture_output=True, text=True)
        installed = [line.split('==')[0].lower() for line in result.stdout.splitlines()]
    
    return installed

def install_package(package: str) -> bool:
    """Install a single package using pip"""
    try:
        animate_loading(f"Installing {package}...", 0.5)
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                      capture_output=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_dependencies():
    """Check and install missing dependencies"""
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}📦 DEPENDENCY CHECK{Colors.ENDC}\n")
    
    requirements = read_requirements()
    if not requirements:
        return
    
    animate_loading("Checking installed packages...", 0.8)
    installed_packages = check_installed_packages()
    
    missing = []
    for req in requirements:
        # Handle packages with version specifiers
        package_name = req.split('>')[0].split('<')[0].split('=')[0].split('[')[0].strip()
        if package_name.lower() not in installed_packages:
            missing.append(req)
    
    if not missing:
        print_status("All dependencies are already installed!", "SUCCESS")
        return
    
    print_status(f"Found {len(missing)} missing dependencies", "INFO")
    
    animate_progress("Installing missing dependencies", len(missing))
    
    failed = []
    for i, package in enumerate(missing):
        print_status(f"Installing: {package}", "INFO")
        if install_package(package):
            print_status(f"Successfully installed {package}", "SUCCESS")
        else:
            print_status(f"Failed to install {package}", "ERROR")
            failed.append(package)
    
    if failed:
        print_status(f"Failed to install: {', '.join(failed)}", "WARNING")
        print_status("Please install manually or check your internet connection", "INFO")
    else:
        print_status("All dependencies installed successfully!", "SUCCESS")

def run_script(script_path: str, description: str):
    """Execute a Python script"""
    if not Path(script_path).exists():
        print_status(f"{script_path} not found!", "ERROR")
        print_status(f"Please ensure {script_path} exists in the correct location", "INFO")
        return
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}▶ Running {description}...{Colors.ENDC}\n")
    animate_loading(f"Launching {description}", 1)
    
    try:
        result = subprocess.run([sys.executable, script_path])
        if result.returncode == 0:
            print_status(f"{description} completed successfully", "SUCCESS")
        else:
            print_status(f"{description} exited with code {result.returncode}", "WARNING")
    except KeyboardInterrupt:
        print_status(f"{description} interrupted by user", "WARNING")
    except Exception as e:
        print_status(f"Error running {description}: {str(e)}", "ERROR")

def view_documentation():
    """Display documentation from README or help file"""
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}📚 DOCUMENTATION{Colors.ENDC}\n")
    
    doc_files = ['README.md', 'README.txt', 'docs/README.md', 'DOCS.md']
    doc_content = None
    
    for doc_file in doc_files:
        if Path(doc_file).exists():
            with open(doc_file, 'r') as f:
                doc_content = f.read()
            break
    
    if doc_content:
        # Truncate if too long
        if len(doc_content) > 2000:
            doc_content = doc_content[:2000] + "\n\n... (truncated, see full documentation in README.md)"
        print(f"{Colors.CYAN}{doc_content}{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}No documentation file found.{Colors.ENDC}")
        print("Available options:")
        print("  • Telegram-Based")
        print("  • Web-Based")
        print("  • View Documentation: Display this help")
        print("  • Exit: Close the application")
        print("\nFor more information, please check the project's README or documentation files.")
    
    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

def display_menu():
    """Display the main menu with options"""
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}🎮 MAIN MENU{Colors.ENDC}\n")
    print(f"{Colors.GREEN}1.{Colors.ENDC} Telegram-Based")
    print(f"{Colors.GREEN}2.{Colors.ENDC}  Web-Based")
    print(f"{Colors.GREEN}3.{Colors.ENDC} View Documentation")
    print(f"{Colors.GREEN}4.{Colors.ENDC} Exit")
    print()

def main():
    """Main function to run the installation tool"""
    # Clear screen for better visual experience
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Display ASCII banner
    print(ASCII_BANNER)
    
    # Check root privileges
    if not check_root():
        sys.exit(1)
    
    # Animated welcome
    animate_loading("Initializing installation tool", 1.5)
    animate_progress("Loading components", 10)
    
    # Check and install dependencies
    install_dependencies()
    
    # Create src directory if it doesn't exist
    if not Path("Src").exists():
        Path("src").mkdir()
        print_status("Created 'Src' directory", "SUCCESS")
        
        # Create example files if they don't exist
        if not Path("Src/run.py").exists():
            with open("Src/run.py", 'w') as f:
                f.write('#!/usr/bin/env python3\nprint("Hello from run.py!")')
            print_status("Created example Src/run.py", "INFO")
        
        if not Path("Src/main.py").exists():
            with open("Src/main.py", 'w') as f:
                f.write('#!/usr/bin/env python3\nprint("Hello from main.py!")')
            print_status("Created example Src/main.py", "INFO")
    
    # Create example requirements.txt if not exists
    if not Path("requirements.txt").exists():
        with open("requirements.txt", 'w') as f:
            f.write("# Example requirements\nrequests>=2.25.0\ncolorama\n")
        print_status("Created example requirements.txt", "INFO")
    
    # Main menu loop
    while True:
        display_menu()
        choice = input(f"{Colors.BOLD}Select an option [1-4]: {Colors.ENDC}").strip()
        
        if choice == '1':
            run_script("Src/telegram-based", "First Option")
        elif choice == '2':
            run_script("Src/ghostqr", "Second Option")
        elif choice == '3':
            view_documentation()
        elif choice == '4':
            animate_loading("Shutting down", 1)
            print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using the Installation Tool!{Colors.ENDC}\n")
            sys.exit(0)
        else:
            print_status("Invalid option. Please choose 1-4.", "WARNING")
            time.sleep(1)
        
        if choice != '3':  # Don't wait twice if viewing docs
            input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_status(f"Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)
