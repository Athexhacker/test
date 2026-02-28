#!/bin/bash

# ASCII Banner for ReconPro
BANNER='
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔═══╝ ██╔══██╗██║   ██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                           A   T  H  E  X'

# Path to src/main directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_MAIN_DIR="${SCRIPT_DIR}/src/main"

clear_screen() {
    clear
}

print_menu() {
    clear_screen
    echo "$BANNER"
    echo -e "\n============================================================"
    echo "MAIN MENU"
    echo "============================================================"
    echo "1. Run Tool"
    echo "2. About"
    echo "3. Exit"
    echo "============================================================"
}

run_tool() {
    clear_screen
    echo "$BANNER"
    echo -e "\n============================================================"
    echo "RUNNING TOOL"
    echo "============================================================"
    
    # Check if src/main directory exists
    if [ ! -d "$SRC_MAIN_DIR" ]; then
        echo -e "\n[ERROR] Directory '$SRC_MAIN_DIR' not found!"
        echo "Please make sure the src/main directory exists."
        read -p $'\nPress Enter to return to main menu...'
        return
    fi
    
    # Look for tool script (assuming it's named ReconPro.py)
    tool_script=""
    possible_names=('sql-map-pro.py')
    
    for name in "${possible_names[@]}"; do
        script_path="${SRC_MAIN_DIR}/${name}"
        if [ -f "$script_path" ]; then
            tool_script="$script_path"
            break
        fi
    done
    
    # If no specific tool found, try to find any Python script
    if [ -z "$tool_script" ]; then
        scripts=($(find "$SRC_MAIN_DIR" -maxdepth 1 -name "*.py" -type f))
        if [ ${#scripts[@]} -gt 0 ]; then
            # Use the first Python script found
            tool_script="${scripts[0]}"
        fi
    fi
    
    if [ -z "$tool_script" ]; then
        echo -e "\n[ERROR] No Python scripts found in $SRC_MAIN_DIR"
        read -p $'\nPress Enter to return to main menu...'
        return
    fi
    
    echo -e "\n[INFO] Running tool..."
    echo "------------------------------------------------------------"
    
    # Make sure the script is executable (not on Windows)
    if [[ "$OSTYPE" != "msys" ]] && [[ "$OSTYPE" != "win32" ]]; then
        chmod 755 "$tool_script" 2>/dev/null
    fi
    
    # Run the script
    python3 "$tool_script"
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n[ERROR] Tool exited with code $exit_code"
    fi
    
    read -p $'\nPress Enter to return to main menu...'
}

about() {
    clear_screen
    echo "$BANNER"
    echo -e "\n============================================================"
    echo "ABOUT SQLMAP-Pro"
    echo "============================================================"
    
    about_script_path="${SRC_MAIN_DIR}/about.py"
    
    if [ -f "$about_script_path" ]; then
        echo -e "\n[INFO] Running about script..."
        echo "------------------------------------------------------------"
        python3 "$about_script_path"
    else
        
        echo -e "\nSQLMAP-Pro - Web Pentesting Tool"
        echo "Version: 2.0"
        echo -e "\nDescription:"
        echo "  A comprehensive SQL Injection Detection tool for security professionals"
        echo "  and penetration testers."
        echo -e "\nCreated by: ATHEX BLACK HAT"
        echo "License: MIT"
    fi
    
    read -p $'\nPress Enter to return to main menu...'
}

main() {
    while true; do
        print_menu
        
        read -p $'\nEnter your choice (1-3): ' choice
        
        case $choice in
            1)
                run_tool
                ;;
            2)
                about
                ;;
            3)
                clear_screen
                echo "$BANNER"
                echo -e "\n============================================================"
                echo "Thank you for using SQLMAP-Pro!"
                echo "============================================================"
                echo ""
                exit 0
                ;;
            *)
                echo -e "\n[ERROR] Invalid choice! Please enter 1, 2, or 3."
                read -p "Press Enter to continue..."
                ;;
        esac
    done
}

# Handle Ctrl+C
trap 'echo -e "\n\n[!] Program interrupted by user"; exit 0' INT

# Run main function
main