#!/usr/bin/env python3
"""
REAL NETWORK SECURITY TOOLKIT
Comprehensive network scanning and monitoring tool.
FOR AUTHORIZED TESTING ONLY - Use on networks you own or have permission to test
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import json
import os
import sys
import time
import socket
import requests
import datetime
import platform
import ipaddress
from ping3 import ping
import whois
import dns.resolver
import dns.reversename
import nmap

# Try to import Scapy - might need installation
try:
    from scapy.all import ARP, Ether, srp, sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Scapy not available. Some features will be limited.")

class RealNetworkToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 NETWORK SECURITY TOOLKIT - REAL SCANNER")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Set style
        self.setup_styles()
        
        # Data storage
        self.targets = []
        self.scan_results = {}
        self.monitoring_active = False
        self.previous_results = {}
        self.network_interfaces = self.get_network_interfaces()
        
        # Build GUI
        self.create_menu()
        self.create_main_dashboard()
        
        # Show legal warning
        self.show_legal_warning()
    
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2d2d2d')
        style.configure('TNotebook.Tab', background='#3d3d3d', foreground='white', padding=[10, 2])
        style.map('TNotebook.Tab', background=[('selected', '#007acc')])
    
    def show_legal_warning(self):
        """Display legal disclaimer"""
        warning = tk.Toplevel(self.root)
        warning.title("⚠️ LEGAL WARNING")
        warning.geometry("600x300")
        warning.configure(bg='#2d2d2d')
        warning.transient(self.root)
        warning.grab_set()
        
        tk.Label(warning, text="LEGAL NOTICE", 
                bg='#2d2d2d', fg='#ff4444', 
                font=('Arial', 20, 'bold')).pack(pady=20)
        
        warning_text = """
        THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY!
        
        Scanning networks, systems, or devices without explicit 
        written permission is ILLEGAL and may violate:
        
        • Computer Fraud and Abuse Act (CFAA)
        • Various state and international laws
        • Terms of service agreements
        • Privacy regulations
        
        By using this tool, you certify that you have:
        ✓ Written permission to test ALL target systems
        ✓ Authority from the network owner
        ✓ Proper authorization documentation
        
        Use only on networks you own or have written authorization to test.
        """
        
        tk.Label(warning, text=warning_text, 
                bg='#2d2d2d', fg='white', 
                font=('Arial', 11), justify=tk.LEFT).pack(pady=10, padx=20)
        
        tk.Button(warning, text="I AGREE - I HAVE AUTHORIZATION", 
                 command=warning.destroy,
                 bg='#007acc', fg='white', 
                 font=('Arial', 12, 'bold')).pack(pady=20)
    
    def get_network_interfaces(self):
        """Get available network interfaces"""
        interfaces = []
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'adapter' in line.lower():
                        interfaces.append(line.strip().replace('adapter', '').strip(':'))
            except:
                interfaces = ["Ethernet", "Wi-Fi"]
        else:
            try:
                result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if ': <' in line:
                        interface = line.split(':')[1].strip()
                        interfaces.append(interface)
            except:
                interfaces = ["eth0", "wlan0"]
        return interfaces
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        menubar.configure(bg='#2d2d2d', fg='white')
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white')
        file_menu.add_command(label="New Session", command=self.new_session)
        file_menu.add_command(label="Load Targets", command=self.load_targets)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white')
        tools_menu.add_command(label="Network Scanner", command=lambda: self.notebook.select(0))
        tools_menu.add_command(label="Port Scanner", command=lambda: self.notebook.select(1))
        tools_menu.add_command(label="OSINT Tools", command=lambda: self.notebook.select(2))
        tools_menu.add_command(label="Vulnerability Scanner", command=lambda: self.notebook.select(3))
        tools_menu.add_command(label="Packet Sniffer", command=lambda: self.notebook.select(4))
        tools_menu.add_separator()
        tools_menu.add_command(label="Run All Scans", command=self.full_scan)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Monitor menu
        monitor_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white')
        monitor_menu.add_command(label="Start Monitoring", command=self.start_monitoring)
        monitor_menu.add_command(label="Stop Monitoring", command=self.stop_monitoring)
        monitor_menu.add_command(label="Set Alerts", command=self.set_alerts)
        menubar.add_cascade(label="Monitoring", menu=monitor_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white')
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_dashboard(self):
        """Create main GUI dashboard"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top control panel
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', height=80)
        control_frame.pack(fill=tk.X, pady=2)
        control_frame.pack_propagate(False)
        
        # Target input
        tk.Label(control_frame, text="Target IP/Domain:", 
                bg='#2d2d2d', fg='white', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        
        self.target_entry = tk.Entry(control_frame, width=30, bg='#3d3d3d', fg='lime',
                                     insertbackground='white', font=('Arial', 11))
        self.target_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Add Target", command=self.add_target,
                 bg='#007acc', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Clear All", command=self.clear_targets,
                 bg='#ff4444', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
        
        # Interface selection
        tk.Label(control_frame, text="Interface:", 
                bg='#2d2d2d', fg='white', font=('Arial', 11)).pack(side=tk.LEFT, padx=(20,5))
        
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(control_frame, textvariable=self.interface_var,
                                           values=self.network_interfaces, width=15)
        self.interface_combo.pack(side=tk.LEFT, padx=5)
        if self.network_interfaces:
            self.interface_combo.current(0)
        
        # Status
        self.status_label = tk.Label(control_frame, text="Ready", 
                                     bg='#2d2d2d', fg='#00ff00', font=('Arial', 10))
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Target list
        target_frame = tk.Frame(main_frame, bg='#2d2d2d', height=60)
        target_frame.pack(fill=tk.X, pady=2)
        target_frame.pack_propagate(False)
        
        tk.Label(target_frame, text="Targets:", bg='#2d2d2d', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.target_listbox = tk.Listbox(target_frame, height=2, bg='#3d3d3d', fg='white')
        self.target_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create tabs
        self.create_network_scanner_tab()
        self.create_port_scanner_tab()
        self.create_osint_tab()
        self.create_vuln_scanner_tab()
        self.create_packet_sniffer_tab()
        self.create_results_tab()
        
        # Status bar
        status_bar = tk.Frame(main_frame, bg='#2d2d2d', height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_detail = tk.Label(status_bar, text="Ready for operation", 
                                      bg='#2d2d2d', fg='#aaa', font=('Arial', 9))
        self.status_detail.pack(side=tk.LEFT, padx=10)
        
        tk.Label(status_bar, text="Authorized Use Only", 
                bg='#2d2d2d', fg='#ffaa00', font=('Arial', 9, 'bold')).pack(side=tk.RIGHT, padx=10)
    
    def create_network_scanner_tab(self):
        """Network discovery tab using ARP/ICMP"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="🌐 Network Scanner")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        tk.Label(control, text="Network Range:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.network_range = tk.Entry(control, width=20, bg='#3d3d3d', fg='white')
        self.network_range.insert(0, "192.168.1.0/24")
        self.network_range.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="🔍 ARP Scan", command=self.run_arp_scan,
                 bg='#007acc', fg='white').pack(side=tk.LEFT, padx=2)
        
        tk.Button(control, text="📡 ICMP Ping Sweep", command=self.run_ping_sweep,
                 bg='#007acc', fg='white').pack(side=tk.LEFT, padx=2)
        
        # Progress
        self.network_progress = ttk.Progressbar(control, length=200, mode='indeterminate')
        self.network_progress.pack(side=tk.RIGHT, padx=10)
        
        # Output area
        self.network_output = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                        font=('Courier', 10), height=20)
        self.network_output.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def create_port_scanner_tab(self):
        """Port scanning tab using python-nmap"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="🔌 Port Scanner")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        tk.Label(control, text="Port Range:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.port_start = tk.Entry(control, width=6, bg='#3d3d3d', fg='white')
        self.port_start.insert(0, "1")
        self.port_start.pack(side=tk.LEFT, padx=2)
        
        tk.Label(control, text="-", bg='#2d2d2d', fg='white').pack(side=tk.LEFT)
        
        self.port_end = tk.Entry(control, width=6, bg='#3d3d3d', fg='white')
        self.port_end.insert(0, "1024")
        self.port_end.pack(side=tk.LEFT, padx=2)
        
        tk.Label(control, text="Scan Type:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=(10,5))
        
        self.scan_type = ttk.Combobox(control, values=[
            "TCP Connect Scan (-sT)",
            "SYN Stealth Scan (-sS)",
            "UDP Scan (-sU)",
            "Service Version (-sV)",
            "OS Detection (-O)",
            "Aggressive Scan (-A)"
        ], width=20)
        self.scan_type.set("TCP Connect Scan (-sT)")
        self.scan_type.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="▶ Start Scan", command=self.run_port_scan,
                 bg='#007acc', fg='white').pack(side=tk.LEFT, padx=10)
        
        # Progress
        self.port_progress = ttk.Progressbar(control, length=200, mode='indeterminate')
        self.port_progress.pack(side=tk.RIGHT, padx=10)
        
        # Output area
        self.port_output = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                     font=('Courier', 10), height=20)
        self.port_output.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def create_osint_tab(self):
        """OSINT tools tab with real data"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="🌍 OSINT Tools")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        # Checkboxes for OSINT options
        self.osint_ip = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="IP Geolocation", variable=self.osint_ip,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        self.osint_whois = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="WHOIS", variable=self.osint_whois,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        self.osint_dns = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="DNS Records", variable=self.osint_dns,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        self.osint_reverse = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="Reverse DNS", variable=self.osint_reverse,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="🔍 Gather OSINT", command=self.run_osint,
                 bg='#007acc', fg='white').pack(side=tk.RIGHT, padx=10)
        
        # Output area
        self.osint_output = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                      font=('Courier', 10), height=20)
        self.osint_output.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def create_vuln_scanner_tab(self):
        """Vulnerability scanner tab"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="⚠️ Vuln Scanner")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        tk.Label(control, text="Check for:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.vuln_ssl = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="SSL/TLS Issues", variable=self.vuln_ssl,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        self.vuln_headers = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="Security Headers", variable=self.vuln_headers,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        self.vuln_ports = tk.BooleanVar(value=True)
        tk.Checkbutton(control, text="Open Ports Risk", variable=self.vuln_ports,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="🔓 Scan Vulnerabilities", command=self.run_vuln_scan,
                 bg='#007acc', fg='white').pack(side=tk.RIGHT, padx=10)
        
        # Output area
        self.vuln_output = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                     font=('Courier', 10), height=20)
        self.vuln_output.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def create_packet_sniffer_tab(self):
        """Packet sniffer tab"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="📡 Packet Sniffer")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        tk.Label(control, text="Filter:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.sniffer_filter = tk.Entry(control, width=30, bg='#3d3d3d', fg='white')
        self.sniffer_filter.insert(0, "tcp or udp")
        self.sniffer_filter.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control, text="Count:", bg='#2d2d2d', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.sniffer_count = tk.Entry(control, width=6, bg='#3d3d3d', fg='white')
        self.sniffer_count.insert(0, "10")
        self.sniffer_count.pack(side=tk.LEFT, padx=2)
        
        self.sniffing_active = False
        self.sniff_button = tk.Button(control, text="▶ Start Sniffing", command=self.toggle_sniffer,
                                      bg='#007acc', fg='white')
        self.sniff_button.pack(side=tk.LEFT, padx=10)
        
        # Output area
        self.sniffer_output = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                        font=('Courier', 10), height=20)
        self.sniffer_output.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def create_results_tab(self):
        """Combined results tab"""
        tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(tab, text="📊 Results")
        
        # Control frame
        control = tk.Frame(tab, bg='#2d2d2d')
        control.pack(fill=tk.X, pady=2)
        
        tk.Button(control, text="📄 Generate Report", command=self.generate_report,
                 bg='#007acc', fg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="💾 Save All Results", command=self.save_results,
                 bg='#007acc', fg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="🗑️ Clear", command=lambda: self.results_text.delete(1.0, tk.END),
                 bg='#ff4444', fg='white').pack(side=tk.RIGHT, padx=5)
        
        # Results area
        self.results_text = scrolledtext.ScrolledText(tab, bg='#1e1e1e', fg='#00ff00',
                                                      font=('Courier', 10), height=25)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def add_target(self):
        """Add target to list"""
        target = self.target_entry.get().strip()
        if target:
            try:
                # Validate target (IP or domain)
                try:
                    ipaddress.ip_address(target)
                except:
                    # Check if it's a valid domain (simple check)
                    if '.' not in target:
                        raise ValueError("Invalid target")
                
                self.targets.append(target)
                self.target_listbox.insert(tk.END, f" {target}")
                self.target_entry.delete(0, tk.END)
                self.update_status(f"Target {target} added")
            except:
                messagebox.showerror("Error", "Invalid target format")
    
    def clear_targets(self):
        """Clear all targets"""
        self.targets.clear()
        self.target_listbox.delete(0, tk.END)
        self.update_status("Targets cleared")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_detail.config(text=f"Status: {message}")
        self.root.update()
    
    def run_arp_scan(self):
        """Run real ARP scan"""
        if not SCAPY_AVAILABLE:
            messagebox.showerror("Error", "Scapy not installed. Please install: pip install scapy")
            return
        
        network = self.network_range.get()
        self.network_output.delete(1.0, tk.END)
        self.network_progress.start()
        
        def scan():
            try:
                self.network_output.insert(tk.END, f"Starting ARP scan on {network}...\n")
                self.network_output.insert(tk.END, "-" * 50 + "\n")
                
                # Create ARP request
                arp = ARP(pdst=network)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                packet = ether / arp
                
                # Send packet and receive response
                result = srp(packet, timeout=3, verbose=0)[0]
                
                devices = []
                for sent, received in result:
                    devices.append({'ip': received.psrc, 'mac': received.hwsrc})
                
                if devices:
                    self.network_output.insert(tk.END, f"\nFound {len(devices)} devices:\n")
                    self.network_output.insert(tk.END, "IP Address\t\tMAC Address\n")
                    self.network_output.insert(tk.END, "-" * 40 + "\n")
                    for device in devices:
                        self.network_output.insert(tk.END, f"{device['ip']}\t\t{device['mac']}\n")
                        
                        # Try to get hostname
                        try:
                            hostname = socket.gethostbyaddr(device['ip'])[0]
                            self.network_output.insert(tk.END, f"  └─ Hostname: {hostname}\n")
                        except:
                            pass
                else:
                    self.network_output.insert(tk.END, "No devices found\n")
                
                self.scan_results['arp_scan'] = devices
                
            except Exception as e:
                self.network_output.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                self.network_progress.stop()
                self.update_status("ARP scan completed")
        
        threading.Thread(target=scan, daemon=True).start()
    
    def run_ping_sweep(self):
        """Run ICMP ping sweep"""
        network = self.network_range.get()
        self.network_output.delete(1.0, tk.END)
        self.network_progress.start()
        
        def sweep():
            try:
                self.network_output.insert(tk.END, f"Starting ping sweep on {network}...\n")
                self.network_output.insert(tk.END, "-" * 50 + "\n")
                
                # Parse network
                ip_net = ipaddress.ip_network(network, strict=False)
                
                live_hosts = []
                for ip in ip_net.hosts():
                    ip_str = str(ip)
                    self.network_output.insert(tk.END, f"Pinging {ip_str}... ")
                    
                    response_time = ping(ip_str, timeout=1)
                    
                    if response_time:
                        live_hosts.append(ip_str)
                        self.network_output.insert(tk.END, f"Online ({response_time*1000:.1f}ms)\n")
                    else:
                        self.network_output.insert(tk.END, "Timeout\n")
                    
                    # Limit to first 50 hosts for demo
                    if len(live_hosts) >= 50:
                        break
                
                self.network_output.insert(tk.END, f"\nFound {len(live_hosts)} live hosts\n")
                self.scan_results['ping_sweep'] = live_hosts
                
            except Exception as e:
                self.network_output.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                self.network_progress.stop()
                self.update_status("Ping sweep completed")
        
        threading.Thread(target=sweep, daemon=True).start()
    
    def run_port_scan(self):
        """Run real port scan using nmap"""
        if not self.targets:
            messagebox.showwarning("No Target", "Please add a target first!")
            return
        
        self.port_output.delete(1.0, tk.END)
        self.port_progress.start()
        
        def scan():
            try:
                nm = nmap.PortScanner()
                
                start_port = int(self.port_start.get())
                end_port = int(self.port_end.get())
                ports = f"{start_port}-{end_port}"
                
                # Map scan type to nmap arguments
                scan_args = {
                    "TCP Connect Scan (-sT)": "-sT",
                    "SYN Stealth Scan (-sS)": "-sS",
                    "UDP Scan (-sU)": "-sU",
                    "Service Version (-sV)": "-sV",
                    "OS Detection (-O)": "-O",
                    "Aggressive Scan (-A)": "-A"
                }
                
                scan_type = self.scan_type.get()
                args = scan_args.get(scan_type, "-sT")
                
                for target in self.targets:
                    self.port_output.insert(tk.END, f"Scanning {target} ({scan_type})...\n")
                    self.port_output.insert(tk.END, f"Ports: {ports}\n")
                    self.port_output.insert(tk.END, "-" * 50 + "\n")
                    
                    # Run nmap scan
                    nm.scan(target, ports, arguments=args)
                    
                    for host in nm.all_hosts():
                        self.port_output.insert(tk.END, f"\nHost: {host} ({nm[host].hostname()})\n")
                        self.port_output.insert(tk.END, f"State: {nm[host].state()}\n")
                        
                        for proto in nm[host].all_protocols():
                            self.port_output.insert(tk.END, f"\nProtocol: {proto}\n")
                            ports = nm[host][proto].keys()
                            
                            for port in sorted(ports):
                                state = nm[host][proto][port]['state']
                                name = nm[host][proto][port].get('name', 'unknown')
                                product = nm[host][proto][port].get('product', '')
                                version = nm[host][proto][port].get('version', '')
                                
                                self.port_output.insert(tk.END, 
                                    f"  {port}/{proto}\t{state}\t{name}")
                                if product or version:
                                    self.port_output.insert(tk.END, f" ({product} {version})")
                                self.port_output.insert(tk.END, "\n")
                    
                    self.port_output.insert(tk.END, "\n" + "=" * 50 + "\n")
                    
            except Exception as e:
                self.port_output.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                self.port_progress.stop()
                self.update_status("Port scan completed")
        
        threading.Thread(target=scan, daemon=True).start()
    
    def run_osint(self):
        """Run real OSINT gathering"""
        if not self.targets:
            messagebox.showwarning("No Target", "Please add a target first!")
            return
        
        self.osint_output.delete(1.0, tk.END)
        
        def gather():
            for target in self.targets:
                self.osint_output.insert(tk.END, f"\n{'='*50}\n")
                self.osint_output.insert(tk.END, f"OSINT Report for: {target}\n")
                self.osint_output.insert(tk.END, f"{'='*50}\n\n")
                
                # IP Geolocation
                if self.osint_ip.get():
                    self.osint_output.insert(tk.END, "📍 IP GEOLOCATION:\n")
                    try:
                        # Try to resolve domain to IP if needed
                        ip = target
                        try:
                            ipaddress.ip_address(target)
                        except:
                            ip = socket.gethostbyname(target)
                        
                        # Query ip-api.com
                        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                        if response.status_code == 200:
                            data = response.json()
                            if data['status'] == 'success':
                                self.osint_output.insert(tk.END, 
                                    f"  Country: {data.get('country', 'N/A')}\n")
                                self.osint_output.insert(tk.END, 
                                    f"  Region: {data.get('regionName', 'N/A')}\n")
                                self.osint_output.insert(tk.END, 
                                    f"  City: {data.get('city', 'N/A')}\n")
                                self.osint_output.insert(tk.END, 
                                    f"  ISP: {data.get('isp', 'N/A')}\n")
                                self.osint_output.insert(tk.END, 
                                    f"  Organization: {data.get('org', 'N/A')}\n")
                                self.osint_output.insert(tk.END, 
                                    f"  Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n")
                            else:
                                self.osint_output.insert(tk.END, f"  {data.get('message', 'Unknown error')}\n")
                        else:
                            self.osint_output.insert(tk.END, "  Geolocation service unavailable\n")
                    except Exception as e:
                        self.osint_output.insert(tk.END, f"  Error: {str(e)}\n")
                    self.osint_output.insert(tk.END, "\n")
                
                # WHOIS Lookup
                if self.osint_whois.get():
                    self.osint_output.insert(tk.END, "📋 WHOIS INFORMATION:\n")
                    try:
                        w = whois.whois(target)
                        if w.name:
                            self.osint_output.insert(tk.END, f"  Registrar: {w.registrar}\n")
                            self.osint_output.insert(tk.END, f"  Creation Date: {w.creation_date}\n")
                            self.osint_output.insert(tk.END, f"  Expiration Date: {w.expiration_date}\n")
                            self.osint_output.insert(tk.END, f"  Name Servers: {', '.join(w.name_servers[:3])}\n")
                        else:
                            self.osint_output.insert(tk.END, "  No WHOIS information available\n")
                    except Exception as e:
                        self.osint_output.insert(tk.END, f"  Error: {str(e)}\n")
                    self.osint_output.insert(tk.END, "\n")
                
                # DNS Records
                if self.osint_dns.get():
                    self.osint_output.insert(tk.END, "🔍 DNS RECORDS:\n")
                    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']
                    
                    for record in record_types:
                        try:
                            answers = dns.resolver.resolve(target, record, raise_on_no_answer=False)
                            if answers:
                                self.osint_output.insert(tk.END, f"  {record} Records:\n")
                                for answer in answers:
                                    self.osint_output.insert(tk.END, f"    {answer}\n")
                        except:
                            pass
                    self.osint_output.insert(tk.END, "\n")
                
                # Reverse DNS
                if self.osint_reverse.get():
                    self.osint_output.insert(tk.END, "🔄 REVERSE DNS:\n")
                    try:
                        # Try to get IP first
                        ip = target
                        try:
                            ipaddress.ip_address(target)
                        except:
                            ip = socket.gethostbyname(target)
                        
                        rev_name = dns.reversename.from_address(ip)
                        answers = dns.resolver.resolve(rev_name, 'PTR')
                        for answer in answers:
                            self.osint_output.insert(tk.END, f"  {answer}\n")
                    except:
                        self.osint_output.insert(tk.END, "  No reverse DNS record found\n")
                    self.osint_output.insert(tk.END, "\n")
            
            self.update_status("OSINT gathering completed")
        
        threading.Thread(target=gather, daemon=True).start()
    
    def run_vuln_scan(self):
        """Run vulnerability scan"""
        if not self.targets:
            messagebox.showwarning("No Target", "Please add a target first!")
            return
        
        self.vuln_output.delete(1.0, tk.END)
        
        def scan():
            for target in self.targets:
                self.vuln_output.insert(tk.END, f"\n{'='*50}\n")
                self.vuln_output.insert(tk.END, f"Vulnerability Scan for: {target}\n")
                self.vuln_output.insert(tk.END, f"{'='*50}\n\n")
                
                if self.vuln_ssl.get():
                    self.vuln_output.insert(tk.END, "🔐 SSL/TLS Security Check:\n")
                    try:
                        # Check HTTPS on port 443
                        response = requests.get(f"https://{target}", timeout=5, verify=False)
                        self.vuln_output.insert(tk.END, f"  HTTPS Status: {response.status_code}\n")
                        
                        # Check security headers
                        headers = response.headers
                        security_headers = {
                            'Strict-Transport-Security': 'HSTS',
                            'Content-Security-Policy': 'CSP',
                            'X-Frame-Options': 'Clickjacking Protection',
                            'X-Content-Type-Options': 'MIME Sniffing Prevention',
                            'X-XSS-Protection': 'XSS Protection'
                        }
                        
                        for header, desc in security_headers.items():
                            if header in headers:
                                self.vuln_output.insert(tk.END, f"  ✓ {desc}: Present\n")
                            else:
                                self.vuln_output.insert(tk.END, f"  ✗ {desc}: Missing\n")
                    except Exception as e:
                        self.vuln_output.insert(tk.END, f"  Error checking SSL: {str(e)}\n")
                    self.vuln_output.insert(tk.END, "\n")
                
                if self.vuln_headers.get():
                    self.vuln_output.insert(tk.END, "📋 Security Headers Analysis:\n")
                    try:
                        # Check HTTP on port 80
                        response = requests.get(f"http://{target}", timeout=5)
                        
                        # Check for information disclosure
                        server = response.headers.get('Server', '')
                        if server:
                            self.vuln_output.insert(tk.END, f"  Server Info Disclosure: {server}\n")
                        
                        # Check for directory listing
                        if 'Index of' in response.text:
                            self.vuln_output.insert(tk.END, "  ⚠️ Possible directory listing enabled\n")
                        
                        # Check for common admin panels
                        admin_paths = ['/admin', '/login', '/wp-admin', '/phpmyadmin']
                        for path in admin_paths:
                            try:
                                r = requests.get(f"http://{target}{path}", timeout=2)
                                if r.status_code == 200:
                                    self.vuln_output.insert(tk.END, f"  ⚠️ Exposed admin path: {path}\n")
                            except:
                                pass
                    except Exception as e:
                        self.vuln_output.insert(tk.END, f"  Error checking headers: {str(e)}\n")
                    self.vuln_output.insert(tk.END, "\n")
                
                if self.vuln_ports.get():
                    self.vuln_output.insert(tk.END, "🔌 Open Ports Risk Assessment:\n")
                    try:
                        # Quick port scan of common ports
                        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                                      443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
                        
                        open_ports = []
                        for port in common_ports:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            result = sock.connect_ex((target, port))
                            if result == 0:
                                open_ports.append(port)
                                service = socket.getservbyport(port, 'tcp') if port in dir(socket) else 'unknown'
                                risk = self.assess_port_risk(port)
                                self.vuln_output.insert(tk.END, f"  Port {port}/{service}: {risk}\n")
                            sock.close()
                        
                        if not open_ports:
                            self.vuln_output.insert(tk.END, "  No common ports open\n")
                    except Exception as e:
                        self.vuln_output.insert(tk.END, f"  Error scanning ports: {str(e)}\n")
                
                self.vuln_output.insert(tk.END, "\n" + "=" * 50 + "\n")
            
            self.update_status("Vulnerability scan completed")
        
        threading.Thread(target=scan, daemon=True).start()
    
    def assess_port_risk(self, port):
        """Assess risk level of open port"""
        high_risk = [21, 23, 445, 3389, 5900]  # FTP, Telnet, SMB, RDP, VNC
        medium_risk = [22, 25, 110, 143, 3306]  # SSH, SMTP, POP3, IMAP, MySQL
        low_risk = [80, 443, 53, 8080]  # HTTP, HTTPS, DNS, HTTP-Alt
        
        if port in high_risk:
            return "HIGH RISK - Common attack vector"
        elif port in medium_risk:
            return "MEDIUM RISK - Requires monitoring"
        elif port in low_risk:
            return "LOW RISK - Standard service"
        else:
            return "UNKNOWN RISK - Investigate further"
    
    def toggle_sniffer(self):
        """Toggle packet sniffer"""
        if not SCAPY_AVAILABLE:
            messagebox.showerror("Error", "Scapy not installed. Please install: pip install scapy")
            return
        
        if not self.sniffing_active:
            self.sniffing_active = True
            self.sniff_button.config(text="⏹ Stop Sniffing", bg='#ff4444')
            self.sniffer_output.delete(1.0, tk.END)
            self.start_sniffer()
        else:
            self.sniffing_active = False
            self.sniff_button.config(text="▶ Start Sniffing", bg='#007acc')
    
    def start_sniffer(self):
        """Start packet sniffing"""
        def packet_handler(pkt):
            if not self.sniffing_active:
                return
            
            try:
                output = ""
                if IP in pkt:
                    src_ip = pkt[IP].src
                    dst_ip = pkt[IP].dst
                    
                    if TCP in pkt:
                        output = f"TCP: {src_ip}:{pkt[TCP].sport} -> {dst_ip}:{pkt[TCP].dport}"
                    elif UDP in pkt:
                        output = f"UDP: {src_ip}:{pkt[UDP].sport} -> {dst_ip}:{pkt[UDP].dport}"
                    elif ICMP in pkt:
                        output = f"ICMP: {src_ip} -> {dst_ip} (Type: {pkt[ICMP].type})"
                    else:
                        output = f"IP: {src_ip} -> {dst_ip} (Protocol: {pkt[IP].proto})"
                    
                    # Add to output
                    self.sniffer_output.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {output}\n")
                    self.sniffer_output.see(tk.END)
            except:
                pass
        
        def sniff_thread():
            try:
                count = int(self.sniffer_count.get())
                interface = self.interface_var.get() if self.interface_var.get() else None
                filter_str = self.sniffer_filter.get() if self.sniffer_filter.get() else None
                
                sniff(prn=packet_handler, count=count, iface=interface, 
                      filter=filter_str, store=0)
            except Exception as e:
                self.sniffer_output.insert(tk.END, f"Sniffer error: {str(e)}\n")
            finally:
                self.sniffing_active = False
                self.sniff_button.config(text="▶ Start Sniffing", bg='#007acc')
        
        threading.Thread(target=sniff_thread, daemon=True).start()
    
    def full_scan(self):
        """Run all scans on all targets"""
        if not self.targets:
            messagebox.showwarning("No Target", "Please add a target first!")
            return
        
        self.notebook.select(5)  # Results tab
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "🔍 FULL SECURITY SCAN INITIATED\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        self.results_text.insert(tk.END, f"Targets: {', '.join(self.targets)}\n")
        self.results_text.insert(tk.END, f"Start Time: {datetime.datetime.now()}\n\n")
        
        def scan_all():
            for target in self.targets:
                self.results_text.insert(tk.END, f"\n{'#'*60}\n")
                self.results_text.insert(tk.END, f"COMPREHENSIVE REPORT FOR: {target}\n")
                self.results_text.insert(tk.END, f"{'#'*60}\n\n")
                
                # Basic connectivity check
                self.results_text.insert(tk.END, "📡 Connectivity Check:\n")
                response_time = ping(target, timeout=2)
                if response_time:
                    self.results_text.insert(tk.END, f"  ✓ Host is online ({response_time*1000:.1f}ms)\n")
                else:
                    self.results_text.insert(tk.END, "  ✗ Host is offline or unreachable\n")
                
                # DNS resolution
                try:
                    ip = socket.gethostbyname(target)
                    self.results_text.insert(tk.END, f"  ✓ Resolves to: {ip}\n")
                except:
                    self.results_text.insert(tk.END, "  ✗ DNS resolution failed\n")
                
                # Port scan summary
                self.results_text.insert(tk.END, "\n🔌 Port Scan Summary:\n")
                try:
                    nm = nmap.PortScanner()
                    nm.scan(target, '1-1000', arguments='-sT --open')
                    
                    for host in nm.all_hosts():
                        for proto in nm[host].all_protocols():
                            ports = nm[host][proto].keys()
                            if ports:
                                for port in sorted(ports):
                                    service = nm[host][proto][port].get('name', 'unknown')
                                    self.results_text.insert(tk.END, 
                                        f"  Port {port}/{proto}: {service} (open)\n")
                            else:
                                self.results_text.insert(tk.END, "  No open ports found in range 1-1000\n")
                except Exception as e:
                    self.results_text.insert(tk.END, f"  Port scan error: {str(e)}\n")
                
                # OSINT Summary
                self.results_text.insert(tk.END, "\n🌍 OSINT Summary:\n")
                try:
                    # Geolocation
                    ip_to_check = target
                    try:
                        ipaddress.ip_address(target)
                    except:
                        ip_to_check = socket.gethostbyname(target)
                    
                    response = requests.get(f"http://ip-api.com/json/{ip_to_check}", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            self.results_text.insert(tk.END, 
                                f"  Location: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}\n")
                            self.results_text.insert(tk.END, f"  ISP: {data.get('isp', 'N/A')}\n")
                except:
                    pass
                
                # Vulnerability Summary
                self.results_text.insert(tk.END, "\n⚠️ Vulnerability Summary:\n")
                
                # Check for HTTP service
                try:
                    response = requests.get(f"http://{target}", timeout=5)
                    if 'Server' in response.headers:
                        server = response.headers['Server']
                        self.results_text.insert(tk.END, f"  Server info: {server}\n")
                        
                        # Check for outdated software
                        if 'Apache/2.2' in server or 'IIS/6' in server:
                            self.results_text.insert(tk.END, "  ⚠️ Potentially outdated web server\n")
                except:
                    pass
                
                # Check HTTPS
                try:
                    response = requests.get(f"https://{target}", timeout=5, verify=False)
                    self.results_text.insert(tk.END, "  ✓ HTTPS is available\n")
                except:
                    self.results_text.insert(tk.END, "  ✗ HTTPS not available\n")
                
                self.results_text.insert(tk.END, "\n" + "-" * 40 + "\n")
            
            self.results_text.insert(tk.END, f"\n✅ FULL SCAN COMPLETED: {datetime.datetime.now()}\n")
            self.update_status("Full scan completed")
        
        threading.Thread(target=scan_all, daemon=True).start()
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if not self.targets:
            messagebox.showwarning("No Target", "Please add a target first!")
            return
        
        if not self.monitoring_active:
            self.monitoring_active = True
            self.update_status("Monitoring started")
            
            def monitor():
                while self.monitoring_active:
                    for target in self.targets:
                        try:
                            # Check if host is up
                            response_time = ping(target, timeout=2)
                            current_status = "online" if response_time else "offline"
                            
                            # Check for changes
                            if target in self.previous_results:
                                if self.previous_results[target] != current_status:
                                    self.trigger_alert(f"{target} changed status to {current_status}")
                            
                            self.previous_results[target] = current_status
                            
                        except Exception as e:
                            print(f"Monitoring error: {e}")
                    
                    time.sleep(30)  # Check every 30 seconds
            
            threading.Thread(target=monitor, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        self.update_status("Monitoring stopped")
    
    def trigger_alert(self, message):
        """Trigger an alert"""
        # Create alert window
        alert = tk.Toplevel(self.root)
        alert.title("⚠️ ALERT")
        alert.geometry("400x150")
        alert.configure(bg='#ff4444')
        alert.transient(self.root)
        
        tk.Label(alert, text="🚨 CHANGE DETECTED", 
                bg='#ff4444', fg='white', font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(alert, text=message, 
                bg='#ff4444', fg='white', font=('Arial', 12)).pack(pady=10)
        
        tk.Button(alert, text="OK", command=alert.destroy,
                 bg='white', fg='#ff4444').pack(pady=10)
    
    def set_alerts(self):
        """Configure alerts"""
        alert_window = tk.Toplevel(self.root)
        alert_window.title("Alert Configuration")
        alert_window.geometry("300x200")
        alert_window.configure(bg='#2d2d2d')
        
        tk.Label(alert_window, text="Alert Settings", 
                bg='#2d2d2d', fg='white', font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Alert options
        self.alert_host_down = tk.BooleanVar(value=True)
        tk.Checkbutton(alert_window, text="Host goes down", variable=self.alert_host_down,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack()
        
        self.alert_host_up = tk.BooleanVar(value=True)
        tk.Checkbutton(alert_window, text="Host comes up", variable=self.alert_host_up,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack()
        
        self.alert_new_port = tk.BooleanVar(value=True)
        tk.Checkbutton(alert_window, text="New port opens", variable=self.alert_new_port,
                      bg='#2d2d2d', fg='white', selectcolor='#3d3d3d').pack()
        
        tk.Button(alert_window, text="Save", command=alert_window.destroy,
                 bg='#007acc', fg='white').pack(pady=20)
    
    def generate_report(self):
        """Generate comprehensive report"""
        if not self.targets:
            messagebox.showwarning("No Target", "No targets to report!")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Security Report")
        report_window.geometry("800x600")
        report_window.configure(bg='#1e1e1e')
        
        report_text = scrolledtext.ScrolledText(report_window, bg='#1e1e1e', fg='#00ff00',
                                               font=('Courier', 10))
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generate report
        report_text.insert(tk.END, "=" * 80 + "\n")
        report_text.insert(tk.END, "NETWORK SECURITY ASSESSMENT REPORT\n")
        report_text.insert(tk.END, "=" * 80 + "\n\n")
        
        report_text.insert(tk.END, f"Report Generated: {datetime.datetime.now()}\n")
        report_text.insert(tk.END, f"Targets Assessed: {len(self.targets)}\n\n")
        
        for i, target in enumerate(self.targets, 1):
            report_text.insert(tk.END, f"\n{'-'*40}\n")
            report_text.insert(tk.END, f"TARGET {i}: {target}\n")
            report_text.insert(tk.END, f"{'-'*40}\n")
            
            # Add scan results if available
            if target in self.scan_results:
                for scan_type, results in self.scan_results[target].items():
                    report_text.insert(tk.END, f"\n{scan_type}:\n")
                    report_text.insert(tk.END, f"{results}\n")
            
            report_text.insert(tk.END, "\n")
        
        report_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        report_text.insert(tk.END, "END OF REPORT\n")
        report_text.insert(tk.END, "=" * 80 + "\n")
        
        # Save button
        tk.Button(report_window, text="Save Report", 
                 command=lambda: self.save_report(report_text.get(1.0, tk.END)),
                 bg='#007acc', fg='white').pack(pady=5)
    
    def save_report(self, content):
        """Save report to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"security_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Report saved to {filename}")
    
    def save_results(self):
        """Save all results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.scan_results, f, indent=2, default=str)
            messagebox.showinfo("Success", f"Results saved to {filename}")
    
    def load_targets(self):
        """Load targets from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r') as f:
                targets = f.read().strip().split('\n')
                for target in targets:
                    if target.strip():
                        self.targets.append(target.strip())
                        self.target_listbox.insert(tk.END, f" {target.strip()}")
            self.update_status(f"Loaded {len(targets)} targets")
    
    def new_session(self):
        """Start new session"""
        if messagebox.askyesno("New Session", "Clear all current data?"):
            self.targets.clear()
            self.target_listbox.delete(0, tk.END)
            self.scan_results.clear()
            self.previous_results.clear()
            
            # Clear all outputs
            self.network_output.delete(1.0, tk.END)
            self.port_output.delete(1.0, tk.END)
            self.osint_output.delete(1.0, tk.END)
            self.vuln_output.delete(1.0, tk.END)
            self.sniffer_output.delete(1.0, tk.END)
            self.results_text.delete(1.0, tk.END)
            
            self.update_status("New session started")
    
    def export_report(self):
        """Export report in different formats"""
        formats = ["PDF", "HTML", "CSV"]
        format_window = tk.Toplevel(self.root)
        format_window.title("Export Report")
        format_window.geometry("300x200")
        format_window.configure(bg='#2d2d2d')
        
        tk.Label(format_window, text="Select Export Format", 
                bg='#2d2d2d', fg='white', font=('Arial', 12, 'bold')).pack(pady=20)
        
        for fmt in formats:
            tk.Button(format_window, text=fmt, 
                     command=lambda f=fmt: self.export_format(f, format_window),
                     bg='#007acc', fg='white', width=15).pack(pady=5)
    
    def export_format(self, format_type, window):
        """Export in specified format"""
        window.destroy()
        messagebox.showinfo("Export", f"Exporting as {format_type}...\n(This feature requires additional libraries)")
        # You would implement actual export logic here
    
    def show_docs(self):
        """Show documentation"""
        docs = """
        NETWORK SECURITY TOOLKIT - DOCUMENTATION
        
        QUICK START:
        1. Add targets (IPs or domains)
        2. Select a tool tab
        3. Configure options
        4. Run scans
        
        TOOLS:
        • Network Scanner - Find live hosts using ARP/ICMP
        • Port Scanner - Scan for open ports with Nmap
        • OSINT Tools - Gather information from public sources
        • Vuln Scanner - Check for common vulnerabilities
        • Packet Sniffer - Capture and analyze network traffic
        
        REQUIREMENTS:
        • Python 3.6+
        • Nmap installed on system
        • Scapy (optional, for packet features)
        
        For detailed help, visit the project documentation.
        """
        
        messagebox.showinfo("Documentation", docs)
    
    def show_about(self):
        """Show about dialog"""
        about = """
        NETWORK SECURITY TOOLKIT
        Version 1.0
        
        A comprehensive network scanning and monitoring tool
        for authorized security testing.
        
        Features:
        • Real ARP/ICMP network discovery
        • Nmap integration for port scanning
        • OSINT gathering from public sources
        • Vulnerability assessment
        • Packet capture and analysis
        
        Created with Python, Tkinter, Scapy, and Nmap
        
        FOR AUTHORIZED USE ONLY
        """
        
        messagebox.showinfo("About", about)

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Check Python version
    if sys.version_info[0] < 3:
        print("Python 3 required")
        sys.exit(1)
    
    # Check for required libraries
    missing_libs = []
    try:
        import nmap
    except ImportError:
        missing_libs.append("python-nmap")
    
    try:
        import whois
    except ImportError:
        missing_libs.append("python-whois")
    
    try:
        import dns.resolver
    except ImportError:
        missing_libs.append("dnspython")
    
    try:
        from ping3 import ping
    except ImportError:
        missing_libs.append("ping3")
    
    if missing_libs:
        print("Missing required libraries:")
        for lib in missing_libs:
            print(f"  • {lib}")
        print("\nInstall with: pip install " + " ".join(missing_libs))
        
        # Still continue, but warn
        if not messagebox.askyesno("Missing Libraries", 
                                   f"Missing: {', '.join(missing_libs)}\n\nSome features may not work.\nContinue anyway?"):
            sys.exit(1)
    
    # Check if running as admin (warn but don't require)
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
    else:
        is_admin = os.geteuid() == 0
    
    if not is_admin:
        warning = tk.Tk()
        warning.withdraw()
        messagebox.showwarning("Limited Privileges", 
                              "Not running with administrator/root privileges.\n"
                              "Some features (like ARP scanning) may not work properly.")
    
    # Create main application
    root = tk.Tk()
    app = RealNetworkToolkit(root)
    
    # Set icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Run application
    root.mainloop()