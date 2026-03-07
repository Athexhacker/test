#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil
from datetime import datetime

# Cool animated banner with colors (ANSI codes)
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

# Additional cool ascii art
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
    
    # Animated border
    print("\033[1;35m" + "▓" * 70 + "\033[0m")
    print("\033[1;33m██\033[0m" + " " * 30 + "\033[1;32mMAIN CONTROL PANEL\033[0m" + " " * 30 + "\033[1;33m██\033[0m")
    print("\033[1;35m" + "▓" * 70 + "\033[0m")
    
    # Menu options with icons
    print("\n\033[1;36m    ⚡ [1]\033[0m \033[1;37mRUN TOOL\033[0m          \033[1;90m- Execute unified security suite\033[0m")
    print("\033[1;36m    🔍 [2]\033[0m \033[1;37mABOUT\033[0m            \033[1;90m- View tool information and credits\033[0m")
    print("\033[1;36m    🚪 [3]\033[0m \033[1;37mEXIT\033[0m             \033[1;90m- Leave the matrix\033[0m")
    
    print("\n\033[1;35m" + "─" * 70 + "\033[0m")
    
    # System info
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
    
    # Check if directory exists with animation
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
    
    # Progress bar animation
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
        
        # Run the tool
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
    
    # Check if about script exists
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
        # Enhanced default about section
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
        # Welcome animation
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