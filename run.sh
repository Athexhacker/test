#!/data/data/com.termux/files/usr/bin/bash
# Termux Personalizer Pro - Advanced Terminal Customization Suite
# Version: 1.0.0
# Developer: CyberForge Studios

set -e

# Configuration directories
CONFIG_DIR="$HOME/.config/termux-personalizer"
BACKUP_DIR="$CONFIG_DIR/backups"
THEME_DIR="$CONFIG_DIR/themes"
SCRIPT_DIR="$CONFIG_DIR/scripts"
mkdir -p "$CONFIG_DIR" "$BACKUP_DIR" "$THEME_DIR" "$SCRIPT_DIR"

# Configuration file
CONFIG_FILE="$CONFIG_DIR/config.cfg"
PASSWORD_FILE="$CONFIG_DIR/.secure_auth"
SETTINGS_FILE="$CONFIG_DIR/settings.conf"

# Color codes and themes
declare -A THEMES
THEMES=(
    ["hacker"]="\e[32m\e[40m\e[92m"  # Classic green hacker
    ["midnight"]="\e[34m\e[40m\e[94m" # Midnight blue
    ["crimson"]="\e[31m\e[40m\e[91m"  # Crimson red
    ["cyberpunk"]="\e[35m\e[45m\e[95m" # Cyberpunk purple
    ["ocean"]="\e[36m\e[44m\e[96m"    # Ocean cyan
    ["forest"]="\e[32m\e[42m\e[92m"   # Forest green
    ["sunset"]="\e[33m\e[43m\e[93m"   # Sunset orange
    ["ice"]="\e[37m\e[46m\e[97m"     # Ice white
)

# Prompt styles
declare -A PROMPTS
PROMPTS=(
    ["default"]='\[\e[1;32m\]\u\[\e[0m\]@\[\e[1;34m\]\h\[\e[0m\]:\[\e[1;33m\]\w\[\e[0m\]\$ '
    ["minimal"]='\[\e[1;36m\]➜ \[\e[0m\]'
    ["detailed"]='\[\e[1;31m\][\[\e[1;33m\]\t\[\e[1;31m\]] \[\e[1;32m\]\u\[\e[0m\]@\[\e[1;34m\]\h\[\e[0m\]:\[\e[1;35m\]\w\[\e[0m\]\$ '
    ["powerline"]='\[\e[48;5;238m\e[38;5;15m\] \u@\h \[\e[48;5;31m\e[38;5;238m\]\[\e[38;5;15m\] \w \[\e[0m\e[38;5;31m\]\[\e[0m\] '
    ["terminal"]='\[\e[1;37m\]> \[\e[0m\]'
    ["matrix"]='\[\e[1;32m\][\[\e[1;33m\]\T\[\e[1;32m\]] \[\e[1;36m\]\w\[\e[0m\]\$ '
)

# ASCII Art Banners
declare -A BANNERS
BANNERS[hacker]='
\e[32m    ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
          ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
             ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ 
             ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ 
             ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
             ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝\e[0m
\e[92m                      PERSONALIZER PRO
                    By ATHEX BLACK HAT\e[0m
'

BANNERS[minimal]='
\e[34m    ┳┳┓         ┓•       
          ┃┃┃┏┓┏┓┏┏┓┏┓  ┣┓┓┏┓┏┓╋
          ┛ ┗┗┛┛┗┻┛┗┗   ┛┗┗┛┗┗┻┛\e[0m
\e[94m        Termux Suite\e[0m
'

BANNERS[cyber]='
\e[35m    
            ░█▀▀░█░█░█▀█░█▀▀░█▀▄░▀█▀░█▀█░█  
            ░█░░░▀▄▀░█▀▀░█▀▀░█▀▄░░█░░█▀█░▀  
            ░▀▀▀░░▀░░▀░░░▀▀▀░▀▀░░▀▀▀░▀░▀░▀  
                                      \e[0m
'

# Load saved settings
load_settings() {
    if [ -f "$SETTINGS_FILE" ]; then
        source "$SETTINGS_FILE"
    else
        CURRENT_THEME="hacker"
        CURRENT_PROMPT="default"
        CURRENT_BANNER="hacker"
    fi
}

# Save settings
save_settings() {
    cat > "$SETTINGS_FILE" << EOF
CURRENT_THEME="$CURRENT_THEME"
CURRENT_PROMPT="$CURRENT_PROMPT"
CURRENT_BANNER="$CURRENT_BANNER"
EOF
}

# Password hashing function
hash_password() {
    echo -n "$1" | sha256sum | awk '{print $1}'
}

# Secure password storage
setup_password() {
    clear
    echo -e "\e[1;33m"
    echo -e "     INITIAL SECURITY SETUP        "
    echo -e "\e[0m"
    echo ""
    
    while true; do
        read -s -p "Enter new password: " PASSWORD1
        echo ""
        read -s -p "Confirm password: " PASSWORD2
        echo ""
        
        if [ "$PASSWORD1" = "$PASSWORD2" ] && [ ${#PASSWORD1} -ge 4 ]; then
            HASH=$(hash_password "$PASSWORD1")
            echo "$HASH" > "$PASSWORD_FILE"
            chmod 600 "$PASSWORD_FILE"
            echo -e "\e[32m✓ Password set successfully!\e[0m"
            sleep 1
            break
        else
            echo -e "\e[31m✗ Passwords don't match or too short (min 4 chars)\e[0m"
        fi
    done
}

# Password verification
verify_password() {
    if [ ! -f "$PASSWORD_FILE" ]; then
        setup_password
        return 0
    fi
    
    STORED_HASH=$(cat "$PASSWORD_FILE")
    ATTEMPTS=0
    
    while [ $ATTEMPTS -lt 3 ]; do
        clear
        echo -e "\e[1;35m"
        echo -e "       TERMUX PERSONALIZER         "
        echo -e "       AUTHENTICATION REQUIRED     "
        echo -e "\e[0m"
        echo ""
        read -s -p "Enter password: " INPUT_PASSWORD
        echo ""
        
        INPUT_HASH=$(hash_password "$INPUT_PASSWORD")
        
        if [ "$INPUT_HASH" = "$STORED_HASH" ]; then
            return 0
        else
            ATTEMPTS=$((ATTEMPTS + 1))
            echo -e "\e[31m✗ Incorrect password! Attempts remaining: $((3 - ATTEMPTS))\e[0m"
            sleep 1
        fi
    done
    
    echo -e "\e[31m✗ Too many failed attempts. Exiting.\e[0m"
    exit 1
}

# Apply the selected theme
apply_theme() {
    IFS=';' read -r C1 C2 C3 <<< "${THEMES[$CURRENT_THEME]}"
    
    # Apply to Termux
    echo -e "${C2}${C1}" > "$HOME/.termux/colors.properties"
    
    # Export for current session
    export PS1=$(echo -e "${THEMES[$CURRENT_THEME]%%;*}")
    clear
}

# Apply prompt
apply_prompt() {
    PROMPT_COMMAND=""
    PS1="${PROMPTS[$CURRENT_PROMPT]}"
}

# Animated typing effect for banner
type_banner() {
    local text="$1"
    local delay=0.001
    
    while IFS= read -r line; do
        echo -e "$line"
        sleep 0.05
    done <<< "$text"
}

# Advanced loading animation
show_loading() {
    local frames=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    local loading_text="INITIALIZING SYSTEM"
    
    echo ""
    for i in {1..20}; do
        local frame=${frames[$((i % 10))]}
        printf "\r\e[32m${frame} ${loading_text:0:$((i % 20))}...\e[0m"
        sleep 0.1
    done
    echo -e "\r\e[32m✓ SYSTEM READY                    \e[0m"
    sleep 0.5
    clear
}

# Display welcome banner
show_welcome() {
    clear
    case $CURRENT_BANNER in
        "hacker") echo -e "${BANNERS[hacker]}" ;;
        "minimal") echo -e "${BANNERS[minimal]}" ;;
        "cyber") echo -e "${BANNERS[cyber]}" ;;
        *) echo -e "${BANNERS[hacker]}" ;;
    esac
    echo ""
}

# Main customization menu
customization_menu() {
    while true; do
        clear
        echo -e "\e[1;36m"
        echo -e "        TERMUX PERSONALIZER PRO           "
        echo -e "           CUSTOMIZATION MENU             "
        echo -e "\e[0m"
        echo ""
        echo -e "\e[1;33m[1]\e[0m Change Color Theme"
        echo -e "\e[1;33m[2]\e[0m Change Prompt Style"
        echo -e "\e[1;33m[3]\e[0m Change Banner Style"
        echo -e "\e[1;33m[4]\e[0m Preview Current Settings"
        echo -e "\e[1;33m[5]\e[0m Reset to Default"
        echo -e "\e[1;33m[6]\e[0m Exit to Termux"
        echo ""
        echo -e "\e[1;37mCurrent Theme: \e[92m$CURRENT_THEME\e[0m"
        echo -e "\e[1;37mCurrent Prompt: \e[92m$CURRENT_PROMPT\e[0m"
        echo -e "\e[1;37mCurrent Banner: \e[92m$CURRENT_BANNER\e[0m"
        echo ""
        read -p "Select option [1-6]: " choice
        
        case $choice in
            1) change_theme ;;
            2) change_prompt ;;
            3) change_banner ;;
            4) preview_settings ;;
            5) reset_defaults ;;
            6) break ;;
            *) echo -e "\e[31mInvalid option!\e[0m"; sleep 1 ;;
        esac
    done
}

# Change theme
change_theme() {
    clear
    echo -e "\e[1;34m"
    echo -e "           SELECT COLOR THEME             "
    echo -e "\e[0m"
    echo ""
    echo -e "\e[32m[1] Hacker (Classic Green)\e[0m"
    echo -e "\e[34m[2] Midnight Blue\e[0m"
    echo -e "\e[91m[3] Crimson Red\e[0m"
    echo -e "\e[95m[4] Cyberpunk Purple\e[0m"
    echo -e "\e[96m[5] Ocean Cyan\e[0m"
    echo -e "\e[92m[6] Forest Green\e[0m"
    echo -e "\e[93m[7] Sunset Orange\e[0m"
    echo -e "\e[97m[8] Ice White\e[0m"
    echo ""
    read -p "Select theme [1-8]: " theme_choice
    
    case $theme_choice in
        1) CURRENT_THEME="hacker" ;;
        2) CURRENT_THEME="midnight" ;;
        3) CURRENT_THEME="crimson" ;;
        4) CURRENT_THEME="cyberpunk" ;;
        5) CURRENT_THEME="ocean" ;;
        6) CURRENT_THEME="forest" ;;
        7) CURRENT_THEME="sunset" ;;
        8) CURRENT_THEME="ice" ;;
        *) echo -e "\e[31mInvalid choice!\e[0m"; sleep 1; return ;;
    esac
    
    save_settings
    apply_theme
    echo -e "\e[32m✓ Theme applied successfully!\e[0m"
    sleep 1
}

# Change prompt
change_prompt() {
    clear
    echo -e "\e[1;34m"
    echo -e "           SELECT PROMPT STYLE            "
    echo -e "\e[0m"
    echo ""
    echo -e "[1] Default (user@host:path$)"
    echo -e "[2] Minimal (➜)"
    echo -e "[3] Detailed (with timestamp)"
    echo -e "[4] Powerline Style"
    echo -e "[5] Terminal (>)"
    echo -e "[6] Matrix Style"
    echo ""
    read -p "Select prompt [1-6]: " prompt_choice
    
    case $prompt_choice in
        1) CURRENT_PROMPT="default" ;;
        2) CURRENT_PROMPT="minimal" ;;
        3) CURRENT_PROMPT="detailed" ;;
        4) CURRENT_PROMPT="powerline" ;;
        5) CURRENT_PROMPT="terminal" ;;
        6) CURRENT_PROMPT="matrix" ;;
        *) echo -e "\e[31mInvalid choice!\e[0m"; sleep 1; return ;;
    esac
    
    save_settings
    apply_prompt
    echo -e "\e[32m✓ Prompt applied successfully!\e[0m"
    sleep 1
}

# Change banner
change_banner() {
    clear
    echo -e "\e[1;34m"
    echo -e "           SELECT BANNER STYLE            "
    echo -e "\e[0m"
    echo ""
    echo -e "[1] Hacker Style"
    echo -e "[2] Minimal Style"
    echo -e "[3] Cyber Style"
    echo ""
    read -p "Select banner [1-3]: " banner_choice
    
    case $banner_choice in
        1) CURRENT_BANNER="hacker" ;;
        2) CURRENT_BANNER="minimal" ;;
        3) CURRENT_BANNER="cyber" ;;
        *) echo -e "\e[31mInvalid choice!\e[0m"; sleep 1; return ;;
    esac
    
    save_settings
    echo -e "\e[32m✓ Banner selected successfully!\e[0m"
    sleep 1
}

# Preview current settings
preview_settings() {
    clear
    echo -e "\e[1;34m"
    echo -e "           CURRENT SETTINGS               "
    echo -e "\e[0m"
    echo ""
    echo -e "\e[1;33mActive Theme: \e[0m$CURRENT_THEME"
    echo -e "\e[1;33mActive Prompt: \e[0m$CURRENT_PROMPT"
    echo -e "\e[1;33mActive Banner: \e[0m$CURRENT_BANNER"
    echo ""
    echo -e "\e[1;33mBanner Preview:\e[0m"
    case $CURRENT_BANNER in
        "hacker") echo -e "${BANNERS[hacker]}" ;;
        "minimal") echo -e "${BANNERS[minimal]}" ;;
        "cyber") echo -e "${BANNERS[cyber]}" ;;
    esac
    echo ""
    echo -e "\e[1;33mPromt Example:\e[0m"
    echo -e "${PROMPTS[$CURRENT_PROMPT]}command_example"
    echo ""
    read -p "Press enter to continue..."
}
reset_defaults() {
    CURRENT_THEME="hacker"
    CURRENT_PROMPT="default"
    CURRENT_BANNER="hacker"
    save_settings
    apply_theme
    apply_prompt
    echo -e "\e[32m✓ Settings reset to default!\e[0m"
    sleep 1
}
backup_bashrc() {
    if [ -f "$HOME/.bashrc" ]; then
        cp "$HOME/.bashrc" "$BACKUP_DIR/bashrc.backup.$(date +%Y%m%d_%H%M%S)"
    fi
}
main() {
    load_settings
    if [ ! -f "$PASSWORD_FILE" ]; then
        show_welcome
        setup_password
    fi
    verify_password
    show_loading
    show_welcome
    apply_theme
    apply_prompt
    customization_menu
    backup_bashrc
    if ! grep -q "termux-personalizer" "$HOME/.bashrc" 2>/dev/null; then
        cat >> "$HOME/.bashrc" << 'EOF'

# Termux Personalizer Pro - Auto-load
if [ -f "$HOME/.config/termux-personalizer/settings.conf" ]; then
    source "$HOME/.config/termux-personalizer/settings.conf"
fi
EOF
    fi
    
    clear
    echo -e "\e[32m"
    echo -e "     TERMUX PERSONALIZER PRO ACTIVE      "
    echo -e "....................................\e[0m"
    echo ""
    echo -e "\e[1;33mWelcome to your personalized Termux!\e[0m"
    echo -e "\e[1;37mSettings will persist across sessions\e[0m"
    echo ""
}

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "This script must be run in Termux!"
    exit 1
fi

# Run main
main

# Exit to shell
exit 0