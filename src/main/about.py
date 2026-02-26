#!/usr/bin/env python3
"""
ABOUT - REAL NETWORK SECURITY TOOLKIT
Animated about section with cool hacking vibes
"""

import time
import sys
import os
import random
import platform
import socket
from datetime import datetime

# ANSI color codes for that cool terminal vibe
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DARK = '\033[90m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;129m'

# Cool ASCII Art Banner
BANNER = f"""
{Colors.RED}
{Colors.RED}██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ {Colors.RED}
{Colors.RED}██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗{Colors.RED}
{Colors.RED}██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║{Colors.RED}
{Colors.RED}██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║{Colors.RED}
{Colors.RED}██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║  ██║╚██████╔╝{Colors.RED}
{Colors.RED}╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ {Colors.RED}
                   
             {Colors.PURPLE}⚡ REAL NETWORK SECURITY TOOLKIT ⚡{Colors.RED}                              
             {Colors.WHITE}FOR AUTHORIZED TESTING ONLY{Colors.RED}                                      {Colors.ENDC}
"""

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, delay=0.03, color=Colors.WHITE):
    """Typewriter effect with color"""
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(message="Loading", duration=2):
    """Cool loading animation"""
    symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.CYAN}{message} {symbols[i % len(symbols)]}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()

def progress_bar(current, total, bar_length=40, prefix="Progress"):
    """Display progress bar"""
    percent = float(current) * 100 / total
    arrow = '█' * int(percent/100 * bar_length)
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\r{Colors.GREEN}{prefix}: [{arrow}{spaces}] {percent:.1f}%{Colors.ENDC}")
    sys.stdout.flush()

def matrix_rain_effect(lines=3):
    """Matrix-style digital rain effect"""
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    for _ in range(lines):
        line = ""
        for i in range(80):
            if random.random() > 0.5:
                line += random.choice(chars)
            else:
                line += " "
        print(f"{Colors.GREEN}{line}{Colors.ENDC}")
        time.sleep(0.1)

def glitch_text(text, iterations=3):
    """Create glitch effect for text"""
    glitch_chars = "!@#$%&*<>?"
    for _ in range(iterations):
        glitched = list(text)
        for i in range(min(3, len(glitched))):
            pos = random.randint(0, len(glitched)-1)
            glitched[pos] = random.choice(glitch_chars)
        sys.stdout.write(f"\r{Colors.RED}{''.join(glitched)}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r{Colors.GREEN}{text}{Colors.ENDC}\n")
    sys.stdout.flush()

def display_system_info():
    """Display system information with cool formatting"""
    info = [
        ("🔐 SECURITY LEVEL", f"{random.choice(['MAXIMUM', 'HEIGHTENED', 'ELEVATED'])}"),
        ("🖥️  PLATFORM", f"{platform.system()} {platform.release()}"),
        ("🐍 PYTHON", f"{platform.python_version()}"),
        ("🌐 HOSTNAME", f"{socket.gethostname()}"),
        ("⏰ TIME", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
        ("🆔 SESSION", f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"),
    ]
    
    print(f"\n{Colors.CYAN}┌─[ SYSTEM INFORMATION {Colors.ENDC}")
    for key, value in info:
        print(f"{Colors.CYAN}│{Colors.ENDC} {Colors.YELLOW}{key:<20}{Colors.ENDC} {Colors.WHITE}{value:<30}{Colors.CYAN}│{Colors.ENDC}")
    print(f"{Colors.CYAN}........................................{Colors.ENDC}")

def display_security_modules():
    """Display security modules with status"""
    modules = [
        ("Network Scanner", "ACTIVE", Colors.GREEN),
        ("Port Scanner", "ACTIVE", Colors.GREEN),
        ("OSINT Tools", "ACTIVE", Colors.GREEN),
        ("Vuln Scanner", "ACTIVE", Colors.GREEN),
        ("Packet Sniffer", "READY", Colors.YELLOW),
        ("Threat Detection", "ACTIVE", Colors.GREEN),
        ("Exploit Framework", "STANDBY", Colors.YELLOW),
        ("Report Generator", "ACTIVE", Colors.GREEN),
    ]
    
    print(f"\n{Colors.MAGENTA}┌─[ SECURITY MODULES {Colors.ENDC}")
    for module, status, color in modules:
        status_color = color if status == "ACTIVE" else Colors.YELLOW
        print(f"{Colors.MAGENTA}│{Colors.ENDC} {Colors.CYAN}⚡{Colors.ENDC} {module:<30} {status_color}[{status}]{Colors.ENDC}{' ' * (15 - len(status))}{Colors.MAGENTA}│{Colors.ENDC}")
    print(f"{Colors.MAGENTA}...........................................{Colors.ENDC}")

def display_development_team():
    """Display development team"""
    team = [
        ("👨‍💻 LEAD DEVELOPER", "ATHEX BLACK HAT"),
        ("🔧 CORE ARCHITECT", "ATHEX BLACK HAT"),
        ("🛡️ SECURITY EXPERT", "ATHEX BLACK HAT"),
        ("📡 NETWORK GURU", "ATHEX BLACK HAT"),
        ("🎨 UI DESIGNER", "ATHEX BLACK HAT"),
        ("🧪 QA ENGINEER", "ATHEX BLACK HAT"),
    ]
    
    print(f"\n{Colors.YELLOW}┌─[ DEVELOPMENT TEAM ]////////////////////////////{Colors.ENDC}")
    for role, name in team:
        print(f"{Colors.YELLOW}│{Colors.ENDC} {Colors.WHITE}{role:<20}{Colors.ENDC} {Colors.CYAN}→{Colors.ENDC} {Colors.GREEN}{name:<25}{Colors.YELLOW}│{Colors.ENDC}")
    print(f"{Colors.YELLOW}....................................................{Colors.ENDC}")

def display_features():
    """Display toolkit features"""
    features = [
        ("🌐 Network Discovery", "ARP scanning, ICMP ping sweep", 100),
        ("🔌 Port Scanning", "TCP/UDP, SYN stealth, service detection", 98),
        ("🌍 OSINT Gathering", "Geolocation, WHOIS, DNS recon", 95),
        ("⚠️ Vulnerability Scan", "SSL checks, header analysis", 92),
        ("📡 Packet Analysis", "Real-time traffic capture", 90),
        ("📊 Report Generation", "Comprehensive security reports", 95),
        ("👁️ Continuous Monitoring", "24/7 network surveillance", 88),
    ]
    
    print(f"\n{Colors.GREEN}┌─[ FEATURE MATRIX ]/////////////////////////////////{Colors.ENDC}")
    for feature, desc, progress in features:
        bar_length = int(progress / 2.5)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"{Colors.GREEN}│{Colors.ENDC} {Colors.CYAN}{feature:<15}{Colors.ENDC} {Colors.WHITE}{desc:<30}{Colors.ENDC}")
        print(f"{Colors.GREEN}│{Colors.ENDC}     {Colors.MAGENTA}[{bar}]{Colors.ENDC} {Colors.YELLOW}{progress}%{Colors.ENDC}{' ' * (23)}{Colors.GREEN}│{Colors.ENDC}")
    print(f"{Colors.GREEN}└.....................................................{Colors.ENDC}")

def display_security_stats():
    """Display security statistics"""
    stats = [
        ("Lines of Code", f"{random.randint(15000, 25000):,}", "📝"),
        ("Security Checks", f"{random.randint(150, 300)}", "🔍"),
        ("Detection Rules", f"{random.randint(500, 1000)}", "📋"),
        ("Active Users", f"{random.randint(1000, 5000):,}", "👥"),
        ("Zero-Days Found", f"{random.randint(1, 5)}", "💀"),
        ("Updates per Week", f"{random.randint(0 , 1)}", "🔄"),
    ]
    
    print(f"\n{Colors.BLUE}┌─[ SECURITY STATISTICS ]/////////////////////////////{Colors.ENDC}")
    for icon, value, label in stats:
        print(f"{Colors.BLUE}│{Colors.ENDC} {icon} {Colors.YELLOW}{label:<15}{Colors.ENDC} {Colors.WHITE}{value:>12}{Colors.ENDC}{' ' * (25)}{Colors.BLUE}│{Colors.ENDC}")
    print(f"{Colors.BLUE}└...........................................................{Colors.ENDC}")

def display_hacker_quote():
    """Display random hacker quote"""
    quotes = [
        ("The quieter you become, the more you can hear.", "― Kevin Mitnick"),
        ("Hacking is about curiosity, not destruction.", "― Anonymous"),
        ("In security, we don't patch humans.", "― Bruce Schneier"),
        ("The only secure system is the one that's powered off.", "― Gene Spafford"),
        ("Security is a process, not a product.", "― Bruce Schneier"),
        ("There are two types of companies: those that have been hacked, and those who don't know it.", "― John Chambers"),
        ("The best defense is a good offense.", "― Sun Tzu"),
        ("Know your network, know your enemy.", "― Ancient Hacker Proverb"),
    ]
    
    quote, author = random.choice(quotes)
    print(f"\n{Colors.ORANGE}/////////////////////////////////////////////////////////////{Colors.ENDC}")
    print(f"{Colors.ORANGE}{Colors.ENDC} {Colors.YELLOW}💭 \"{quote}\"{Colors.ENDC}")
    print(f"{Colors.ORANGE}{Colors.ENDC} {Colors.CYAN}   {author}{Colors.ENDC}{' ' * (45 - len(author))}{Colors.ORANGE}║{Colors.ENDC}")
    print(f"{Colors.ORANGE}//////////////////////////////////////////////////////////////{Colors.ENDC}")

def display_legal_warning():
    """Display legal warning with animation"""
    warning_lines = [
        "⚠️  LEGAL WARNING  ⚠️",
        "",
        "THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY!",
        "",
        "Using this tool against networks/systems without",
        "explicit written permission is ILLEGAL and may",
        "violate computer fraud and abuse laws.",
        "",
        "You MUST have written authorization from the owner",
        "before scanning any system or network.",
    ]
    
    print(f"\n{Colors.RED}///////////////////////////////////////////////////////////////{Colors.ENDC}")
    for line in warning_lines:
        padding = (56 - len(line)) // 2
        print(f"{Colors.RED}║{Colors.ENDC}{' ' * padding}{Colors.YELLOW}{line}{Colors.ENDC}{' ' * (56 - len(line) - padding)}{Colors.RED}║{Colors.ENDC}")
        time.sleep(0.2)
    print(f"{Colors.RED}//////////////////////////////////////////////////////////////////{Colors.ENDC}")

def display_version_info():
    """Display version information"""
    versions = [
        ("Core Engine", "v3.2.1"),
        ("Network Module", "v2.5.0"),
        ("Security Module", "v3.0.2"),
        ("OSINT Module", "v1.8.4"),
        ("Report Module", "v2.1.3"),
    ]
    
    print(f"\n{Colors.PURPLE}┌─[ VERSION INFORMATION ]///////////////////////////////{Colors.ENDC}")
    for module, version in versions:
        print(f"{Colors.PURPLE}│{Colors.ENDC} {Colors.WHITE}{module:<20}{Colors.ENDC} {Colors.GREEN}{version:>10}{Colors.ENDC}{' ' * (20)}{Colors.PURPLE}│{Colors.ENDC}")
    print(f"{Colors.PURPLE}...............................................................{Colors.ENDC}")

def display_thank_you():
    """Display thank you message"""
    message = "THANK YOU FOR USING ReconPro NETWORK SECURITY TOOLKIT"
    border = "═" * (len(message) + 4)
    
    print(f"\n{Colors.GREEN}╔{border}╗{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}  {Colors.YELLOW}{message}{Colors.ENDC}  {Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}╚{border}╝{Colors.ENDC}")

def main():
    """Main about function"""
    try:
        clear_screen()
        
        # Initial loading sequence
        print(f"{Colors.DARK}Initializing secure connection...{Colors.ENDC}")
        loading_animation("Establishing secure channel", 1)
        
        # Show banner with glitch effect
        clear_screen()
        for line in BANNER.split('\n'):
            print(line)
            time.sleep(0.05)
        
        # Matrix rain effect
        matrix_rain_effect(2)
        time.sleep(0.5)
        
        # System info with type effect
        display_system_info()
        time.sleep(1)
        
        # Loading security modules
        print(f"\n{Colors.CYAN}[*] Loading security modules...{Colors.ENDC}")
        for i in range(101):
            progress_bar(i, 100, prefix="Loading")
            time.sleep(0.01)
        print("\n")
        
        # Display main sections
        display_security_modules()
        time.sleep(1)
        
        display_features()
        time.sleep(1)
        
        display_development_team()
        time.sleep(1)
        
        display_security_stats()
        time.sleep(1)
        
        display_version_info()
        time.sleep(1)
        
        # Random quote
        display_hacker_quote()
        time.sleep(1)
        
        # Legal warning with emphasis
        display_legal_warning()
        time.sleep(1)
        
        # Final message
        display_thank_you()
        
        # Exit sequence
        print(f"\n{Colors.DARK}[*] Disconnecting...{Colors.ENDC}")
        loading_animation("Cleaning up", 0.5)
        
        # Wait for user
        input(f"\n{Colors.CYAN}[?] Press Enter to return to main menu...{Colors.ENDC}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Connection terminated{Colors.ENDC}")
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Colors.RED}[!] Error: {e}{Colors.ENDC}")
        time.sleep(2)
        input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()