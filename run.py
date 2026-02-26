#!/usr/bin/env python3
import os
import sys
import subprocess

# ASCII Banner for ReconPro
BANNER = """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                           Reconnaissance Pro
"""

# Path to src/main directory
SRC_MAIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "main")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Print the main menu"""
    clear_screen()
    print(BANNER)
    print("\n" + "="*60)
    print("MAIN MENU")
    print("="*60)
    print("1. Run Tool")
    print("2. About")
    print("3. Exit")
    print("="*60)

def run_tool():
    """Option 1: Automatically run the main tool from src/main directory"""
    clear_screen()
    print(BANNER)
    print("\n" + "="*60)
    print("RUNNING TOOL")
    print("="*60)
    
    # Check if src/main directory exists
    if not os.path.exists(SRC_MAIN_DIR):
        print(f"\n[ERROR] Directory '{SRC_MAIN_DIR}' not found!")
        print("Please make sure the src/main directory exists.")
        input("\nPress Enter to return to main menu...")
        return
    
    # Look for tool script (assuming it's named tool.py or main.py)
    tool_script = None
    possible_names = ['ReconPro.py']
    
    for name in possible_names:
        script_path = os.path.join(SRC_MAIN_DIR, name)
        if os.path.isfile(script_path):
            tool_script = script_path
            break
    
    # If no specific tool found, try to find any Python script
    if not tool_script:
        scripts = [f for f in os.listdir(SRC_MAIN_DIR) 
                  if f.endswith('.py') and os.path.isfile(os.path.join(SRC_MAIN_DIR, f))]
        
        if scripts:
            # Use the first Python script found
            tool_script = os.path.join(SRC_MAIN_DIR, scripts[0])
    
    if not tool_script:
        print(f"\n[ERROR] No Python scripts found in {SRC_MAIN_DIR}")
        input("\nPress Enter to return to main menu...")
        return
    
    print(f"\n[INFO] Running tool...")
    print("-"*60)
    
    # Run the tool script
    try:
        # Make sure the script is executable
        if os.name != 'nt':  # Not Windows
            os.chmod(tool_script, 0o755)
        
        # Run the script
        result = subprocess.run([sys.executable, tool_script], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode != 0:
            print(f"\n[ERROR] Tool exited with code {result.returncode}")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to run tool: {e}")
    
    input("\nPress Enter to return to main menu...")

def about():
    """Option 2: About section - automatically run about script"""
    clear_screen()
    print(BANNER)
    print("\n" + "="*60)
    print("ABOUT ReconPro")
    print("="*60)
    
    about_script_path = os.path.join(SRC_MAIN_DIR, "about.py")
    
    if os.path.exists(about_script_path):
        print("\n[INFO] Running about script...")
        print("-"*60)
        try:
            subprocess.run([sys.executable, about_script_path])
        except Exception as e:
            print(f"\n[ERROR] Failed to run about script: {e}")
    else:
        # Default about information if about.py doesn't exist
        print("\nReconPro - Reconnaissance Tool")
        print("Version: 1.0.0")
        print("\nDescription:")
        print("  A comprehensive reconnaissance tool for security professionals")
        print("  and penetration testers.")
        print("\nFeatures:")
        print("  - Network scanning")
        print("  - Information gathering")
        print("  - Vulnerability assessment")
        print("\nCreated by: ATHEX BLACK HAT")
        print("License: MIT")
    
    input("\nPress Enter to return to main menu...")

def main():
    """Main function to run the menu system"""
    while True:
        print_menu()
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            run_tool()
        elif choice == '2':
            about()
        elif choice == '3':
            clear_screen()
            print(BANNER)
            print("\n" + "="*60)
            print("Thank you for using ReconPro!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n[ERROR] Invalid choice! Please enter 1, 2, or 3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
        sys.exit(0)