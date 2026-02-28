#!/usr/bin/env python3
# SQLMAP PRO Launcher - Fixed version with src directory support

import sys
import time
import os
import subprocess
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent  # Go up one level from src to root
TOOL_PATH = PROJECT_ROOT / 'sql-map-pro.py'
LAUNCHER_PATH = PROJECT_ROOT / 'sqlmap_pro_launcher.sh'

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    END = '\033[0m'
    CLEAR_LINE = '\033[2K'
    CURSOR_UP = '\033[1A'

def typewriter(text, delay=0.03, color=Colors.WHITE, newline=True):
    """Print text with typewriter effect"""
    for char in text:
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(delay)
    if newline:
        print()

def display_banner():
    """Display animated ASCII banner - FIXED VERSION"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Fixed banner with proper borders - Print instantly for better visibility
    banner_lines = [
        (f"{Colors.RED}    ╔══════════════════════════════════════════════════════════╗", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ███████╗ ██████╗ ██╗     ███╗   ███╗ █████╗ ██████╗ {Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ██╔════╝██╔═══██╗██║     ████╗ ████║██╔══██╗██╔══██╗{Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ███████╗██║   ██║██║     ██╔████╔██║███████║██████╔╝{Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ╚════██║██║▄▄ ██║██║     ██║╚██╔╝██║██╔══██║██╔═══╝ {Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ███████║╚██████╔╝███████╗██║ ╚═╝ ██║██║  ██║██║     {Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.YELLOW}     ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     {Colors.RED}  ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ██████╗ ██████╗  ██████╗ {Colors.RED}              ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ██╔══██╗██╔══██╗██╔═══██╗{Colors.RED}              ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ██████╔╝██████╔╝██║   ██║{Colors.RED}              ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ██╔═══╝ ██╔══██╗██║   ██║{Colors.RED}              ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ██║     ██║  ██║╚██████╔╝{Colors.RED}              ║", 0),
        (f"{Colors.RED}    ║{Colors.CYAN}                     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ {Colors.RED}               ║", 0),
        (f"{Colors.RED}    ╚══════════════════════════════════════════════════════════╝", 0)
    ]
    
    # Print banner instantly (no delay) for clean display
    for line, _ in banner_lines:
        print(line)
        time.sleep(0.03)  # Small delay between lines for visual effect
    
    time.sleep(0.3)
    print()
    print(f"{Colors.PURPLE}    ════════════════════════════════════════════════════════════{Colors.END}")
    
    # Gradient version text - keep the animation for the version
    version_text = "                     S Q L M A P   P R O   v 2 . 0"
    for i, char in enumerate(version_text):
        color = Colors.GREEN if i % 2 == 0 else Colors.CYAN
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(0.02)
    print()
    
    print(f"{Colors.PURPLE}    ════════════════════════════════════════════════════════════{Colors.END}")
    print()
    time.sleep(0.2)
    
    # Animated tagline with typewriter effect
    typewriter(f"{Colors.YELLOW}    ⚡ Advanced SQL Injection Detection Tool ⚡{Colors.END}", 0.03)
    print()

def loading_animation(text, duration=1.5):
    """Display loading animation"""
    animation = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.BLUE}{text}{Colors.END} {Colors.CYAN}{animation[i % len(animation)]}{Colors.END}", end='', flush=True)
        i += 1
        time.sleep(0.1)
    print(f"\r{Colors.GREEN}{text} ✓{Colors.END}   ")

def gradient_text(text, start_color, end_color):
    """Print text with gradient effect"""
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(0.01)
    print()

def check_tool_exists():
    """Check if the main tool script exists in the root directory"""
    return TOOL_PATH.exists()

def run_tool():
    """Execute the SQLMAP PRO tool"""
    print(f"\n{Colors.CYAN}┌─[ Starting SQLMAP PRO ]")
    print(f"├─{Colors.PURPLE} Initializing modules...{Colors.END}")
    
    try:
        # Check if we're in a virtual environment
        in_venv = os.environ.get('VIRTUAL_ENV') is not None
        
        if not in_venv:
            print(f"{Colors.YELLOW}├─[!] Not in virtual environment{Colors.END}")
            print(f"{Colors.YELLOW}├─[!] Attempting to activate venv...{Colors.END}")
            
            # Try to use the launcher if it exists
            if LAUNCHER_PATH.exists():
                print(f"{Colors.GREEN}├─[✓] Launcher found, using it...{Colors.END}")
                # Change to project root before running launcher
                os.chdir(PROJECT_ROOT)
                subprocess.call([str(LAUNCHER_PATH)], shell=True)
                return
            else:
                print(f"{Colors.YELLOW}├─[!] No launcher found, running directly...{Colors.END}")
        
        # Change to project root before running the tool
        os.chdir(PROJECT_ROOT)
        
        # Run the Python script
        result = subprocess.run(['python3', str(TOOL_PATH)], capture_output=False)
        
        if result.returncode != 0:
            print(f"{Colors.RED}└─[✗] Tool exited with error code: {result.returncode}{Colors.END}")
        else:
            print(f"{Colors.GREEN}└─[✓] Tool execution completed{Colors.END}")
            
    except FileNotFoundError:
        print(f"{Colors.RED}└─[✗] Error: Could not find Python or the tool file{Colors.END}")
        print(f"{Colors.YELLOW}   Expected location: {TOOL_PATH}{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}└─[!] Tool execution interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}└─[✗] Unexpected error: {str(e)}{Colors.END}")

def show_menu():
    """Display interactive menu with animations"""
    menu_options = [
        ("🚀", "Run SQLMAP PRO", Colors.GREEN),
        ("❌", "Exit", Colors.RED)
    ]
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}    ╔════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}    ║{Colors.WHITE}             M A I N   M E N U               {Colors.YELLOW}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}    ╠════════════════════════════════════════════╣{Colors.END}")
    
    for i, (icon, text, color) in enumerate(menu_options, 1):
        spaces = " " * (32 - len(text))
        print(f"{Colors.BOLD}{Colors.YELLOW}    ║{Colors.END}  {color}{icon} {i}. {text}{spaces}{Colors.YELLOW}║{Colors.END}")
    
    print(f"{Colors.BOLD}{Colors.YELLOW}    ╚════════════════════════════════════════════╝{Colors.END}")
    print()

def animate_selection(choice):
    """Animate the selection process"""
    print(f"\r{Colors.CLEAR_LINE}", end='')
    
    if choice == '1':
        for i in range(3):
            print(f"\r{Colors.GREEN}Selected: Run SQLMAP PRO {'.' * (i+1)}{Colors.END}", end='', flush=True)
            time.sleep(0.3)
        print()
    elif choice == '2':
        for i in range(3):
            print(f"\r{Colors.RED}Selected: Exit {'.' * (i+1)}{Colors.END}", end='', flush=True)
            time.sleep(0.3)
        print()

def main():
    """Main program loop"""
    
    try:
        display_banner()
        
        # Show current directory info
        print(f"{Colors.DIM}Script location: {SCRIPT_DIR}{Colors.END}")
        print(f"{Colors.DIM}Tool location: {TOOL_PATH}{Colors.END}")
        print()
        
        loading_animation("Checking tool availability", 1)
        
        if not check_tool_exists():
            print(f"\n{Colors.RED}╔════════════════════════════════════════════════════╗{Colors.END}")
            print(f"{Colors.RED}║{Colors.YELLOW}  ⚠ WARNING: sql-map-pro.py not found!            ⚠  {Colors.RED}║{Colors.END}")
            print(f"{Colors.RED}║{Colors.YELLOW}  Expected location: {Colors.END}")
            print(f"{Colors.RED}║{Colors.CYAN}  {TOOL_PATH}{Colors.END}")
            print(f"{Colors.RED}║{Colors.YELLOW}  Please ensure the tool is present.                {Colors.RED}║{Colors.END}")
            print(f"{Colors.RED}╚════════════════════════════════════════════════════╝{Colors.END}")
            print()
            
            response = input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower().strip()
            if response != 'y':
                print(f"{Colors.RED}Exiting...{Colors.END}")
                time.sleep(1)
                sys.exit(0)
        
        while True:
            show_menu()
            
            choice = input(f"{Colors.CYAN}┌─[{Colors.GREEN}SELECT OPTION{Colors.CYAN}]{Colors.PURPLE} ➜ {Colors.END}").strip()
            
            animate_selection(choice)
            
            if choice == '1':
                print()
                gradient_text(" INITIALIZING SQLMAP PRO ", Colors.CYAN, Colors.GREEN)
                print()
                
                run_tool()
                
                print(f"\n{Colors.YELLOW}════════════════════════════════════════════════════{Colors.END}")
                continue_choice = input(f"{Colors.CYAN}Run again? (y/n): {Colors.END}").lower().strip()
                
                if continue_choice != 'y':
                    print()
                    typewriter(f"{Colors.GREEN}Thank you for using SQLMAP PRO!{Colors.END}", 0.05)
                    time.sleep(1)
                    break
                else:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    display_banner()
                    continue
                    
            elif choice == '2':
                print()
                # Exit animation
                for i in range(3):
                    print(f"\r{Colors.YELLOW}Exiting{'.' * (i+1)}{Colors.END}", end='', flush=True)
                    time.sleep(0.3)
                print(f"\n{Colors.GREEN}Goodbye! Happy Hacking! 👋{Colors.END}")
                time.sleep(1)
                break
            else:
                print(f"\r{Colors.RED}Invalid option! Please select 1 or 2{Colors.END}")
                time.sleep(1)
                # Clear the invalid message
                print(f"\r{Colors.CLEAR_LINE}", end='')
                print(f"{Colors.CURSOR_UP}", end='')
                print(f"\r{Colors.CLEAR_LINE}", end='')
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠ Interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}Goodbye!{Colors.END}")
        time.sleep(1)
        sys.exit(0)
    
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        time.sleep(2)
        sys.exit(1)

def cleanup():
    """Clean up before exit"""
    print(f"{Colors.END}", end='')
    # Show cursor again
    try:
        os.system('tput cnorm 2>/dev/null')
    except:
        pass

if __name__ == "__main__":
    # Hide cursor for better animation
    try:
        os.system('tput civis 2>/dev/null')
    except:
        pass
    
    try:
        main()
    finally:
        cleanup()
        print()