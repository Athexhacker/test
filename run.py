#!/usr/bin/env python3
# SQLMAP PRO Launcher

import sys
import time
import os
import subprocess
import platform
from threading import Thread
from queue import Queue

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
    """Display animated ASCII banner with typewriter effect"""
    os.system('clear' if os.name == 'posix' else 'cls')
    banner_lines = [
        (f"{Colors.RED}    ", 0.02),
        (f"{Colors.RED}    {Colors.YELLOW}     ███████╗ ██████╗ ██╗     ███╗   ███╗ █████╗ ██████╗ {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.YELLOW}     ██╔════╝██╔═══██╗██║     ████╗ ████║██╔══██╗██╔══██╗{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.YELLOW}     ███████╗██║   ██║██║     ██╔████╔██║███████║██████╔╝{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.YELLOW}     ╚════██║██║▄▄ ██║██║     ██║╚██╔╝██║██╔══██║██╔═══╝ {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.YELLOW}     ███████║╚██████╔╝███████╗██║ ╚═╝ ██║██║  ██║██║     {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.YELLOW}     ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ██████╗ ██████╗  ██████╗ {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ██╔══██╗██╔══██╗██╔═══██╗{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ██████╔╝██████╔╝██║   ██║{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ██╔═══╝ ██╔══██╗██║   ██║{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ██║     ██║  ██║╚██████╔╝{Colors.RED}  ", 0.01),
        (f"{Colors.RED}    {Colors.CYAN}                                  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ {Colors.RED}  ", 0.01),
        (f"{Colors.RED}    ", 0.02)
    ]
    for line, speed in banner_lines:
        typewriter(line, speed, newline=True)
        time.sleep(0.05)
    time.sleep(0.3)
    print()
    typewriter(f"{Colors.PURPLE}    //////////////////////////////////////////////////////////////", 0.02)
    version_text = "                     S Q L M A P   P R O   v 2 . 0"
    for i, char in enumerate(version_text):
        color = Colors.GREEN if i % 2 == 0 else Colors.CYAN
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(0.02)
    print()
    typewriter(f"{Colors.PURPLE}    ///////////////////////////////////////////////////////////////", 0.02)
    print()
    time.sleep(0.2)
    typewriter(f"{Colors.YELLOW}    ⚡ Advanced SQL Injection Detection Tool ⚡", 0.03, Colors.YELLOW)
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
    """Check if the main tool script exists"""
    if os.path.exists('sql-map-pro.py'):
        return True
    elif os.path.exists('sql-map-pro.py'):
        return True
    else:
        return False
def run_tool():
    """Execute the SQLMAP PRO tool"""
    print(f"\n{Colors.CYAN}┌─[ Starting SQLMAP PRO ]")
    print(f"├─{Colors.PURPLE} Initializing modules...{Colors.END}")
    filename = 'sql-map-pro.py' if os.path.exists('sql-map-pro.py') else 'sql-map-pro.py'
    try:
        in_venv = os.environ.get('VIRTUAL_ENV') is not None
        if not in_venv:
            print(f"{Colors.YELLOW}├─[!] Not in virtual environment{Colors.END}")
            print(f"{Colors.YELLOW}├─[!] Attempting to activate venv...{Colors.END}")
            if os.path.exists('sqlmap_pro_launcher.sh'):
                print(f"{Colors.GREEN}├─[✓] Launcher found, using it...{Colors.END}")
                subprocess.call(['./sqlmap_pro.sh'])
                return
            else:
                print(f"{Colors.YELLOW}├─[!] No launcher found, running directly...{Colors.END}")
        result = subprocess.run(['python3', filename], capture_output=False)
        if result.returncode != 0:
            print(f"{Colors.RED}└─[✗] Tool exited with error code: {result.returncode}{Colors.END}")
        else:
            print(f"{Colors.GREEN}└─[✓] Tool execution completed{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}└─[✗] Error: Could not find Python or the tool file{Colors.END}")
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
    print(f"\n{Colors.BOLD}{Colors.YELLOW}  {Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}    {Colors.WHITE}      M A I N   M E N U               {Colors.YELLOW}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}    {Colors.END}")
    
    for i, (icon, text, color) in enumerate(menu_options, 1):
        spaces = " " * (28 - len(text))
        print(f"{Colors.BOLD}{Colors.YELLOW}    {Colors.END}  {color}{icon} {i}. {text}{spaces}{Colors.DIM}{Colors.YELLOW}║{Colors.END}")
    
    print(f"{Colors.BOLD}{Colors.YELLOW}    {Colors.END}")
    print()
def animate_selection(choice):
    """Animate the selection process"""
    print(f"\n{Colors.CLEAR_LINE}", end='')
    print(f"{Colors.CURSOR_UP}", end='')
    
    if choice == '1':
        for i in range(3):
            print(f"\r{Colors.GREEN}Selected: Run SQLMAP PRO {'.' * (i+1)}{Colors.END}", end='', flush=True)
            time.sleep(0.3)
        print()
    else:
        for i in range(3):
            print(f"\r{Colors.RED}Selected: Exit {'.' * (i+1)}{Colors.END}", end='', flush=True)
            time.sleep(0.3)
        print()
def main():
    """Main program loop"""
    
    try:
        display_banner()
        
        print()
        loading_animation("Checking tool availability", 1)
        
        if not check_tool_exists():
            print(f"{Colors.RED}{Colors.END}")
            print(f"{Colors.RED}{Colors.YELLOW}  ⚠ WARNING: sqlmap-pro.py not found in current  ⚠  {Colors.RED}{Colors.END}")
            print(f"{Colors.RED}{Colors.YELLOW}  directory! Please ensure the tool is present.    {Colors.RED}{Colors.END}")
            print(f"{Colors.RED}{Colors.END}")
            print()
            
            response = input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower()
            if response != 'y':
                print(f"{Colors.RED}Exiting...{Colors.END}")
                time.sleep(1)
                sys.exit(0)
        
        while True:
            show_menu()
            
            print(f"{Colors.CYAN}┌─[{Colors.GREEN}SELECT OPTION{Colors.CYAN}]", end='')
            choice = input(f"{Colors.PURPLE} ➜ {Colors.END}").strip()
            animate_selection(choice)
            
            if choice == '1':
                print()
                gradient_text(" INITIALIZING SQLMAP PRO ", Colors.CYAN, Colors.GREEN)
                print()
                
                run_tool()
                
              
                print(f"\n{Colors.YELLOW}{Colors.END}")
                continue_choice = input(f"{Colors.CYAN}Run again? (y/n): {Colors.END}").lower()
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
                for i in range(3):
                    print(f"\r{Colors.YELLOW}Exiting{'.' * (i+1)}{Colors.END}", end='', flush=True)
                    time.sleep(0.3)
                print(f"\n{Colors.GREEN}Goodbye! Happy Hacking! 👋{Colors.END}")
                time.sleep(1)
                break
            else:
                print(f"\r{Colors.RED}Invalid option! Please select 1 or 2{Colors.END}")
                time.sleep(1)
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
    os.system('tput cnorm') 

if __name__ == "__main__":
    os.system('tput civis')
    try:
        main()
    finally:
        cleanup()
        print()