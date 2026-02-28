#!/usr/bin/env python3
"""
Advanced SQLMap GUI - Professional Penetration Testing Tool
Author: Security Researcher
Version: 2.0
"""

import sys
import os
import json
import subprocess
import threading
import re
import time
from datetime import datetime
from pathlib import Path
from queue import Queue
from typing import Optional, Dict, List, Any

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Optional imports for advanced features
try:
    import requests
    from bs4 import BeautifulSoup
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False

class ScanWorker(QThread):
    """Worker thread for running SQLMap scans without freezing GUI"""
    output_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, command: List[str]):
        super().__init__()
        self.command = command
        self.process = None
        
    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output line by line
            for line in self.process.stdout:
                self.output_signal.emit(line.strip())
                
                # Update progress based on output
                if "%" in line:
                    try:
                        progress = int(re.search(r'(\d+)%', line).group(1))
                        self.progress_signal.emit(progress)
                    except:
                        pass
            
            self.process.wait()
            success = self.process.returncode == 0
            self.finished_signal.emit(success, "Scan completed successfully" if success else "Scan failed")
            
        except Exception as e:
            self.finished_signal.emit(False, str(e))
    
    def stop(self):
        if self.process:
            self.process.terminate()

class AdvancedSQLMapGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scan_history = []
        self.current_worker = None
        self.results_data = {}
        self.tamper_scripts = self.load_tamper_scripts()
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the main user interface"""
        self.setWindowTitle("Advanced SQLMap GUI - Security Research Tool")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #363636;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ddd;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #363636;
                border-bottom: 2px solid #4CAF50;
            }
            QGroupBox {
                color: #ddd;
                border: 2px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #ddd;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background-color: #404040;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #666;
            }
            QCheckBox {
                color: #ddd;
            }
            QRadioButton {
                color: #ddd;
            }
            QListWidget {
                background-color: #404040;
                color: #ddd;
                border: 1px solid #555;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Toolbar
        self.create_toolbar()
        
        # Tab widget for different sections
        tabs = QTabWidget()
        
        # Add tabs
        tabs.addTab(self.create_target_tab(), "🎯 Target Configuration")
        tabs.addTab(self.create_injection_tab(), "💉 Injection Options")
        tabs.addTab(self.create_detection_tab(), "🔍 Detection & Enumeration")
        tabs.addTab(self.create_optimization_tab(), "⚡ Performance & Optimization")
        tabs.addTab(self.create_evasion_tab(), "🛡️ WAF Bypass & Evasion")
        tabs.addTab(self.create_automation_tab(), "🤖 Automation & Scheduling")
        tabs.addTab(self.create_results_tab(), "📊 Results & Reporting")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar in status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.hide()
        self.status_bar.addPermanentWidget(self.progress_bar)
        
    def create_toolbar(self):
        """Create main toolbar with actions"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #333;
                border: none;
                spacing: 3px;
            }
        """)
        
        # New scan action
        new_action = QAction(QIcon.fromTheme("document-new"), "New Scan", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_scan)
        toolbar.addAction(new_action)
        
        # Save results
        save_action = QAction(QIcon.fromTheme("document-save"), "Save Results", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_results)
        toolbar.addAction(save_action)
        
        # Load configuration
        load_action = QAction(QIcon.fromTheme("document-open"), "Load Config", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_config)
        toolbar.addAction(load_action)
        
        toolbar.addSeparator()
        
        # Start scan
        self.start_action = QAction(QIcon.fromTheme("media-playback-start"), "Start Scan", self)
        self.start_action.setShortcut("F5")
        self.start_action.triggered.connect(self.start_scan)
        toolbar.addAction(self.start_action)
        
        # Stop scan
        self.stop_action = QAction(QIcon.fromTheme("media-playback-stop"), "Stop Scan", self)
        self.stop_action.setShortcut("F6")
        self.stop_action.triggered.connect(self.stop_scan)
        self.stop_action.setEnabled(False)
        toolbar.addAction(self.stop_action)
        
        toolbar.addSeparator()
        
        # Settings
        settings_action = QAction(QIcon.fromTheme("preferences-system"), "Settings", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
        
        # Help
        help_action = QAction(QIcon.fromTheme("help-contents"), "Help", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
    def create_target_tab(self):
        """Create target configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Target URL group
        url_group = QGroupBox("Target URL")
        url_layout = QVBoxLayout()
        
        url_input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://example.com/page.php?id=1")
        url_input_layout.addWidget(self.url_input)
        
        # Quick target buttons
        quick_buttons = QHBoxLayout()
        quick_buttons.addWidget(QLabel("Quick targets:"))
        targets = ["localhost", "testphp.vulnweb.com", "dvwa.local"]
        for target in targets:
            btn = QPushButton(target)
            btn.clicked.connect(lambda checked, t=target: self.url_input.setText(f"http://{t}"))
            quick_buttons.addWidget(btn)
        
        url_layout.addLayout(url_input_layout)
        url_layout.addLayout(quick_buttons)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        # Request configuration
        request_group = QGroupBox("Request Configuration")
        request_layout = QGridLayout()
        
        # Method selection
        request_layout.addWidget(QLabel("Method:"), 0, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE"])
        request_layout.addWidget(self.method_combo, 0, 1)
        
        # Data for POST
        request_layout.addWidget(QLabel("POST Data:"), 1, 0)
        self.post_data = QLineEdit()
        self.post_data.setPlaceholderText("param1=value1&param2=value2")
        request_layout.addWidget(self.post_data, 1, 1)
        
        # Cookies
        request_layout.addWidget(QLabel("Cookies:"), 2, 0)
        self.cookies = QLineEdit()
        self.cookies.setPlaceholderText("PHPSESSID=abc123; security=low")
        request_layout.addWidget(self.cookies, 2, 1)
        
        # Headers
        request_layout.addWidget(QLabel("Headers:"), 3, 0)
        self.headers = QTextEdit()
        self.headers.setMaximumHeight(60)
        self.headers.setPlaceholderText("User-Agent: Mozilla/5.0\nAccept: text/html")
        request_layout.addWidget(self.headers, 3, 1)
        
        # Authentication
        request_layout.addWidget(QLabel("Auth:"), 4, 0)
        auth_layout = QHBoxLayout()
        self.auth_type = QComboBox()
        self.auth_type.addItems(["None", "Basic", "Digest", "NTLM"])
        auth_layout.addWidget(self.auth_type)
        self.auth_creds = QLineEdit()
        self.auth_creds.setPlaceholderText("username:password")
        auth_layout.addWidget(self.auth_creds)
        request_layout.addLayout(auth_layout, 4, 1)
        
        request_group.setLayout(request_layout)
        layout.addWidget(request_group)
        
        # Proxy configuration
        proxy_group = QGroupBox("Proxy Settings")
        proxy_layout = QGridLayout()
        
        proxy_layout.addWidget(QLabel("Proxy:"), 0, 0)
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://127.0.0.1:8080")
        proxy_layout.addWidget(self.proxy_input, 0, 1)
        
        self.tor_check = QCheckBox("Use Tor")
        self.tor_check.toggled.connect(lambda checked: self.proxy_input.setText("socks5://127.0.0.1:9050" if checked else ""))
        proxy_layout.addWidget(self.tor_check, 1, 0)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        layout.addStretch()
        return widget
    
    def create_injection_tab(self):
        """Create injection options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Technique selection
        tech_group = QGroupBox("Injection Techniques")
        tech_layout = QGridLayout()
        
        self.tech_be = QCheckBox("Boolean-based blind")
        self.tech_be.setChecked(True)
        tech_layout.addWidget(self.tech_be, 0, 0)
        
        self.tech_tb = QCheckBox("Time-based blind")
        self.tech_tb.setChecked(True)
        tech_layout.addWidget(self.tech_tb, 0, 1)
        
        self.tech_e = QCheckBox("Error-based")
        self.tech_e.setChecked(True)
        tech_layout.addWidget(self.tech_e, 1, 0)
        
        self.tech_u = QCheckBox("UNION query")
        self.tech_u.setChecked(True)
        tech_layout.addWidget(self.tech_u, 1, 1)
        
        self.tech_s = QCheckBox("Stacked queries")
        self.tech_s.setChecked(True)
        tech_layout.addWidget(self.tech_s, 2, 0)
        
        self.tech_o = QCheckBox("Out-of-band")
        tech_layout.addWidget(self.tech_o, 2, 1)
        
        tech_group.setLayout(tech_layout)
        layout.addWidget(tech_group)
        
        # Parameter selection
        param_group = QGroupBox("Parameter Targeting")
        param_layout = QVBoxLayout()
        
        self.skip_static = QCheckBox("Skip static parameters")
        param_layout.addWidget(self.skip_static)
        
        self.param_del = QCheckBox("Use parameter delimiter")
        param_layout.addWidget(self.param_del)
        
        self.custom_param = QLineEdit()
        self.custom_param.setPlaceholderText("Custom parameters to test (comma-separated)")
        param_layout.addWidget(self.custom_param)
        
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        
        # Database selection
        db_group = QGroupBox("Database Configuration")
        db_layout = QGridLayout()
        
        db_layout.addWidget(QLabel("Database:"), 0, 0)
        self.db_combo = QComboBox()
        self.db_combo.addItems(["Auto-detect", "MySQL", "Oracle", "PostgreSQL", "MSSQL", "SQLite", "Access"])
        db_layout.addWidget(self.db_combo, 0, 1)
        
        db_layout.addWidget(QLabel("DB User:"), 1, 0)
        self.db_user = QLineEdit()
        self.db_user.setPlaceholderText("root")
        db_layout.addWidget(self.db_user, 1, 1)
        
        db_layout.addWidget(QLabel("DB Password:"), 2, 0)
        self.db_pass = QLineEdit()
        self.db_pass.setEchoMode(QLineEdit.EchoMode.Password)
        db_layout.addWidget(self.db_pass, 2, 1)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        layout.addStretch()
        return widget
    
    def create_detection_tab(self):
        """Create detection and enumeration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Level and risk
        level_group = QGroupBox("Detection Level")
        level_layout = QGridLayout()
        
        level_layout.addWidget(QLabel("Level (1-5):"), 0, 0)
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 5)
        self.level_spin.setValue(1)
        level_layout.addWidget(self.level_spin, 0, 1)
        
        level_layout.addWidget(QLabel("Risk (1-3):"), 1, 0)
        self.risk_spin = QSpinBox()
        self.risk_spin.setRange(1, 3)
        self.risk_spin.setValue(1)
        level_layout.addWidget(self.risk_spin, 1, 1)
        
        level_group.setLayout(level_layout)
        layout.addWidget(level_group)
        
        # Enumeration options
        enum_group = QGroupBox("Enumeration Options")
        enum_layout = QVBoxLayout()
        
        self.enum_basic = QRadioButton("Basic info (banner, current user, current DB)")
        enum_layout.addWidget(self.enum_basic)
        
        self.enum_dbs = QRadioButton("Enumerate databases")
        enum_layout.addWidget(self.enum_dbs)
        
        self.enum_tables = QRadioButton("Enumerate tables")
        enum_layout.addWidget(self.enum_tables)
        
        self.enum_columns = QRadioButton("Enumerate columns")
        enum_layout.addWidget(self.enum_columns)
        
        self.enum_dump = QRadioButton("Dump data")
        enum_layout.addWidget(self.enum_dump)
        
        self.enum_all = QRadioButton("Enumerate everything")
        self.enum_all.setChecked(True)
        enum_layout.addWidget(self.enum_all)
        
        enum_group.setLayout(enum_layout)
        layout.addWidget(enum_group)
        
        # Specific target selection
        target_group = QGroupBox("Specific Targets")
        target_layout = QGridLayout()
        
        target_layout.addWidget(QLabel("Database:"), 0, 0)
        self.target_db = QLineEdit()
        target_layout.addWidget(self.target_db, 0, 1)
        
        target_layout.addWidget(QLabel("Table:"), 1, 0)
        self.target_table = QLineEdit()
        target_layout.addWidget(self.target_table, 1, 1)
        
        target_layout.addWidget(QLabel("Column:"), 2, 0)
        self.target_column = QLineEdit()
        target_layout.addWidget(self.target_column, 2, 1)
        
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        layout.addStretch()
        return widget
    
    def create_optimization_tab(self):
        """Create performance optimization tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Threading
        thread_group = QGroupBox("Threading & Concurrency")
        thread_layout = QGridLayout()
        
        thread_layout.addWidget(QLabel("Threads:"), 0, 0)
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 50)
        self.threads_spin.setValue(1)
        thread_layout.addWidget(self.threads_spin, 0, 1)
        
        self.optimize_threads = QCheckBox("Optimize thread count")
        thread_layout.addWidget(self.optimize_threads, 1, 0, 1, 2)
        
        thread_group.setLayout(thread_layout)
        layout.addWidget(thread_group)
        
        # Timeouts and delays
        timeout_group = QGroupBox("Timeouts & Delays")
        timeout_layout = QGridLayout()
        
        timeout_layout.addWidget(QLabel("Timeout (sec):"), 0, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 120)
        self.timeout_spin.setValue(30)
        timeout_layout.addWidget(self.timeout_spin, 0, 1)
        
        timeout_layout.addWidget(QLabel("Retries:"), 1, 0)
        self.retries_spin = QSpinBox()
        self.retries_spin.setRange(0, 10)
        self.retries_spin.setValue(3)
        timeout_layout.addWidget(self.retries_spin, 1, 1)
        
        timeout_layout.addWidget(QLabel("Delay (sec):"), 2, 0)
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0, 60)
        self.delay_spin.setValue(0)
        self.delay_spin.setSingleStep(0.5)
        timeout_layout.addWidget(self.delay_spin, 2, 1)
        
        timeout_group.setLayout(timeout_layout)
        layout.addWidget(timeout_group)
        
        # Performance options
        perf_group = QGroupBox("Performance Options")
        perf_layout = QVBoxLayout()
        
        self.null_conn = QCheckBox("Null connection")
        perf_layout.addWidget(self.null_conn)
        
        self.keep_alive = QCheckBox("Keep alive")
        self.keep_alive.setChecked(True)
        perf_layout.addWidget(self.keep_alive)
        
        self.text_only = QCheckBox("Text-only responses")
        perf_layout.addWidget(self.text_only)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        layout.addStretch()
        return widget
    
    def create_evasion_tab(self):
        """Create WAF bypass and evasion tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tamper scripts
        tamper_group = QGroupBox("Tamper Scripts (WAF Bypass)")
        tamper_layout = QVBoxLayout()
        
        # Search/filter for tamper scripts
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.tamper_search = QLineEdit()
        self.tamper_search.setPlaceholderText("Filter scripts...")
        self.tamper_search.textChanged.connect(self.filter_tamper_scripts)
        search_layout.addWidget(self.tamper_search)
        tamper_layout.addLayout(search_layout)
        
        # Tamper scripts list
        self.tamper_list = QListWidget()
        self.tamper_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.populate_tamper_scripts()
        tamper_layout.addWidget(self.tamper_list)
        
        # Common bypass combinations
        bypass_buttons = QHBoxLayout()
        bypass_buttons.addWidget(QLabel("Quick bypass:"))
        
        bypass_presets = [
            ("Basic", "space2comment"),
            ("MSSQL", "charencode,charunicodeencode"),
            ("MySQL", "between,bluecoat"),
            ("Aggressive", "space2comment,randomcase,base64encode")
        ]
        
        for name, scripts in bypass_presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, s=scripts: self.select_tamper_scripts(s))
            bypass_buttons.addWidget(btn)
        
        tamper_layout.addLayout(bypass_buttons)
        tamper_group.setLayout(tamper_layout)
        layout.addWidget(tamper_group)
        
        # Evasion techniques
        evade_group = QGroupBox("Additional Evasion")
        evade_layout = QVBoxLayout()
        
        self.random_agent = QCheckBox("Random User-Agent")
        evade_layout.addWidget(self.random_agent)
        
        self.mobile_agent = QCheckBox("Use mobile User-Agent")
        evade_layout.addWidget(self.mobile_agent)
        
        self.chunked = QCheckBox("Chunked transfer encoding")
        evade_layout.addWidget(self.chunked)
        
        evade_group.setLayout(evade_layout)
        layout.addWidget(evade_group)
        
        layout.addStretch()
        return widget
    
    def create_automation_tab(self):
        """Create automation and scheduling tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Batch mode
        batch_group = QGroupBox("Batch Processing")
        batch_layout = QVBoxLayout()
        
        self.batch_mode = QCheckBox("Batch mode (non-interactive)")
        self.batch_mode.setChecked(True)
        batch_layout.addWidget(self.batch_mode)
        
        self.auto_complete = QCheckBox("Auto-complete parameters")
        batch_layout.addWidget(self.auto_complete)
        
        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)
        
        # Scheduling
        schedule_group = QGroupBox("Scan Scheduling")
        schedule_layout = QGridLayout()
        
        self.schedule_enable = QCheckBox("Enable scheduling")
        schedule_layout.addWidget(self.schedule_enable, 0, 0, 1, 2)
        
        schedule_layout.addWidget(QLabel("Start time:"), 1, 0)
        self.schedule_time = QTimeEdit()
        self.schedule_time.setTime(QTime.currentTime().addSecs(3600))  # 1 hour from now
        schedule_layout.addWidget(self.schedule_time, 1, 1)
        
        schedule_layout.addWidget(QLabel("Repeat:"), 2, 0)
        self.schedule_repeat = QComboBox()
        self.schedule_repeat.addItems(["Once", "Hourly", "Daily", "Weekly"])
        schedule_layout.addWidget(self.schedule_repeat, 2, 1)
        
        schedule_group.setLayout(schedule_layout)
        layout.addWidget(schedule_group)
        
        # Multiple targets
        multi_group = QGroupBox("Multiple Targets")
        multi_layout = QVBoxLayout()
        
        self.target_file = QLineEdit()
        self.target_file.setPlaceholderText("Path to file containing targets (one per line)")
        multi_layout.addWidget(self.target_file)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_target_file)
        multi_layout.addWidget(browse_btn)
        
        multi_group.setLayout(multi_layout)
        layout.addWidget(multi_group)
        
        layout.addStretch()
        return widget
    
    def create_results_tab(self):
        """Create results and reporting tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Output console
        console_group = QGroupBox("Console Output")
        console_layout = QVBoxLayout()
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Courier New", 10))
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #444;
            }
        """)
        console_layout.addWidget(self.console)
        
        # Clear console button
        clear_btn = QPushButton("Clear Console")
        clear_btn.clicked.connect(self.console.clear)
        console_layout.addWidget(clear_btn)
        
        console_group.setLayout(console_layout)
        layout.addWidget(console_group)
        
        # Results summary
        summary_group = QGroupBox("Results Summary")
        summary_layout = QVBoxLayout()
        
        self.summary_tree = QTreeWidget()
        self.summary_tree.setHeaderLabels(["Item", "Value"])
        self.summary_tree.setMaximumHeight(150)
        summary_layout.addWidget(self.summary_tree)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # Export buttons
        export_layout = QHBoxLayout()
        
        export_json = QPushButton("Export JSON")
        export_json.clicked.connect(lambda: self.export_results("json"))
        export_layout.addWidget(export_json)
        
        export_html = QPushButton("Export HTML Report")
        export_html.clicked.connect(lambda: self.export_results("html"))
        export_layout.addWidget(export_html)
        
        export_csv = QPushButton("Export CSV")
        export_csv.clicked.connect(lambda: self.export_results("csv"))
        export_layout.addWidget(export_csv)
        
        layout.addLayout(export_layout)
        
        return widget
    
    def populate_tamper_scripts(self):
        """Populate the tamper scripts list"""
        common_tampers = [
            "apostrophemask", "apostrophenullencode", "appendnullbyte",
            "base64encode", "between", "bluecoat", "chardoubleencode",
            "charencode", "charunicodeencode", "concat2concatws",
            "equaltolike", "greatest", "halfversionedmorekeywords",
            "ifnull2ifisnull", "informationschemacomment",
            "lowercase", "modsecurityversioned", "modsecurityzeroversioned",
            "multiplespaces", "nonrecursivereplacement", "overlongutf8",
            "percentage", "randomcase", "randomcomments", "securesphere",
            "sp_password", "space2comment", "space2dash", "space2hash",
            "space2morehash", "space2mssqlblank", "space2mssqlhash",
            "space2mysqlblank", "space2mysqldash", "space2plus",
            "space2randomblank", "symboliclogical", "unionalltounion",
            "unmagicquotes", "uppercase", "varnish", "versionedkeywords",
            "versionedmorekeywords", "xforwardedfor"
        ]
        
        for tamper in common_tampers:
            item = QListWidgetItem(tamper)
            self.tamper_list.addItem(item)
    
    def filter_tamper_scripts(self):
        """Filter tamper scripts based on search text"""
        search_text = self.tamper_search.text().lower()
        
        for i in range(self.tamper_list.count()):
            item = self.tamper_list.item(i)
            item.setHidden(search_text not in item.text().lower())
    
    def select_tamper_scripts(self, scripts):
        """Select specific tamper scripts"""
        self.tamper_list.clearSelection()
        script_list = scripts.split(',')
        
        for i in range(self.tamper_list.count()):
            item = self.tamper_list.item(i)
            if item.text() in script_list:
                item.setSelected(True)
    
    def browse_target_file(self):
        """Browse for target file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Target File", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            self.target_file.setText(filename)
    
    def load_tamper_scripts(self):
        """Load available tamper scripts from SQLMap"""
        # This would actually query SQLMap for available scripts
        return []
    
    def build_command(self) -> List[str]:
        """Build SQLMap command based on GUI selections"""
        cmd = ["sqlmap"]
        
        # Target
        if self.url_input.text():
            cmd.extend(["-u", self.url_input.text()])
        
        # Method and data
        if self.method_combo.currentText() == "POST" and self.post_data.text():
            cmd.extend(["--data", self.post_data.text()])
        
        # Cookies
        if self.cookies.text():
            cmd.extend(["--cookie", self.cookies.text()])
        
        # Headers
        if self.headers.toPlainText():
            headers = self.headers.toPlainText().replace('\n', '\r\n')
            cmd.extend(["--headers", headers])
        
        # Authentication
        if self.auth_type.currentText() != "None" and self.auth_creds.text():
            auth_type = self.auth_type.currentText().lower()
            cmd.extend([f"--auth-type={auth_type}", f"--auth-cred={self.auth_creds.text()}"])
        
        # Proxy
        if self.proxy_input.text():
            cmd.extend(["--proxy", self.proxy_input.text()])
        
        # Injection techniques
        techniques = []
        if self.tech_be.isChecked(): techniques.append("B")
        if self.tech_tb.isChecked(): techniques.append("T")
        if self.tech_e.isChecked(): techniques.append("E")
        if self.tech_u.isChecked(): techniques.append("U")
        if self.tech_s.isChecked(): techniques.append("S")
        if self.tech_o.isChecked(): techniques.append("O")
        
        if techniques and len(techniques) < 6:
            cmd.extend(["--technique", ''.join(techniques)])
        
        # Level and risk
        cmd.extend(["--level", str(self.level_spin.value())])
        cmd.extend(["--risk", str(self.risk_spin.value())])
        
        # Enumeration
        if self.enum_basic.isChecked():
            cmd.append("--banner")
            cmd.append("--current-user")
            cmd.append("--current-db")
        elif self.enum_dbs.isChecked():
            cmd.append("--dbs")
        elif self.enum_tables.isChecked():
            if self.target_db.text():
                cmd.extend(["-D", self.target_db.text()])
            cmd.append("--tables")
        elif self.enum_columns.isChecked():
            if self.target_db.text() and self.target_table.text():
                cmd.extend(["-D", self.target_db.text()])
                cmd.extend(["-T", self.target_table.text()])
            cmd.append("--columns")
        elif self.enum_dump.isChecked():
            if self.target_db.text() and self.target_table.text():
                cmd.extend(["-D", self.target_db.text()])
                cmd.extend(["-T", self.target_table.text()])
                if self.target_column.text():
                    cmd.extend(["-C", self.target_column.text()])
            cmd.append("--dump")
        elif self.enum_all.isChecked():
            cmd.append("--all")
        
        # Database specific
        if self.db_combo.currentText() != "Auto-detect":
            cmd.extend(["--dbms", self.db_combo.currentText().lower()])
        
        if self.db_user.text() and self.db_pass.text():
            cmd.extend(["--dbms-cred", f"{self.db_user.text()}:{self.db_pass.text()}"])
        
        # Threading
        if self.threads_spin.value() > 1:
            cmd.extend(["--threads", str(self.threads_spin.value())])
        
        # Timeouts
        cmd.extend(["--timeout", str(self.timeout_spin.value())])
        cmd.extend(["--retries", str(self.retries_spin.value())])
        
        if self.delay_spin.value() > 0:
            cmd.extend(["--delay", str(self.delay_spin.value())])
        
        # Performance
        if self.null_conn.isChecked():
            cmd.append("--null-connection")
        if not self.keep_alive.isChecked():
            cmd.append("--disable-keepalive")
        
        # Tamper scripts
        selected_tampers = []
        for item in self.tamper_list.selectedItems():
            selected_tampers.append(item.text())
        
        if selected_tampers:
            cmd.extend(["--tamper", ",".join(selected_tampers)])
        
        # User-Agent
        if self.random_agent.isChecked():
            cmd.append("--random-agent")
        elif self.mobile_agent.isChecked():
            cmd.append("--mobile")
        
        # Batch mode
        if self.batch_mode.isChecked():
            cmd.append("--batch")
        
        # Output directory
        output_dir = f"results/sqlmap_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cmd.extend(["--output-dir", output_dir])
        
        return cmd
    
    def start_scan(self):
        """Start the SQLMap scan"""
        # Validate target
        if not self.url_input.text() and not self.target_file.text():
            QMessageBox.warning(self, "Warning", "Please specify a target URL or target file")
            return
        
        # Build command
        cmd = self.build_command()
        
        # Log command
        self.console.append(f"\n[>] Executing: {' '.join(cmd)}\n{'-'*60}\n")
        
        # Disable start button, enable stop
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)
        
        # Show progress bar
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        self.current_worker = ScanWorker(cmd)
        self.current_worker.output_signal.connect(self.update_console)
        self.current_worker.progress_signal.connect(self.progress_bar.setValue)
        self.current_worker.finished_signal.connect(self.scan_finished)
        self.current_worker.start()
        
        self.status_bar.showMessage("Scan in progress...")
    
    def stop_scan(self):
        """Stop the current scan"""
        if self.current_worker:
            reply = QMessageBox.question(
                self, "Confirm Stop",
                "Are you sure you want to stop the current scan?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_worker.stop()
                self.console.append("\n[!] Scan stopped by user\n")
                self.scan_finished(False, "Scan stopped")
    
    def update_console(self, text: str):
        """Update console with new output"""
        self.console.append(text)
        
        # Auto-scroll to bottom
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console.setTextCursor(cursor)
        
        # Parse and update summary if we find results
        self.parse_results(text)
    
    def parse_results(self, text: str):
        """Parse SQLMap output for relevant results"""
        # Look for database names
        if "available databases" in text.lower():
            self.add_to_summary("Databases Found", "Yes")
        
        # Look for table names
        if "tables" in text.lower() and "entries" in text.lower():
            self.add_to_summary("Tables Enumerated", "Yes")
        
        # Look for credentials
        if "credentials:" in text.lower():
            self.add_to_summary("Credentials Found", "Yes")
    
    def add_to_summary(self, item: str, value: str):
        """Add item to results summary"""
        # Check if item already exists
        for i in range(self.summary_tree.topLevelItemCount()):
            top_item = self.summary_tree.topLevelItem(i)
            if top_item.text(0) == item:
                top_item.setText(1, value)
                return
        
        # Add new item
        new_item = QTreeWidgetItem([item, value])
        self.summary_tree.addTopLevelItem(new_item)
    
    def scan_finished(self, success: bool, message: str):
        """Handle scan completion"""
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.progress_bar.hide()
        
        if success:
            self.status_bar.showMessage("Scan completed successfully")
            self.console.append(f"\n[✓] {message}\n")
            
            # Add to history
            self.scan_history.append({
                'timestamp': datetime.now().isoformat(),
                'target': self.url_input.text(),
                'success': True
            })
            
            QMessageBox.information(self, "Success", "Scan completed successfully!")
        else:
            self.status_bar.showMessage("Scan failed")
            self.console.append(f"\n[✗] {message}\n")
            
            QMessageBox.critical(self, "Error", f"Scan failed: {message}")
    
    def new_scan(self):
        """Reset for new scan"""
        reply = QMessageBox.question(
            self, "New Scan",
            "Clear current configuration and start new scan?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear inputs
            self.url_input.clear()
            self.post_data.clear()
            self.cookies.clear()
            self.headers.clear()
            self.proxy_input.clear()
            
            # Reset selections
            self.tech_be.setChecked(True)
            self.tech_tb.setChecked(True)
            self.tech_e.setChecked(True)
            self.tech_u.setChecked(True)
            self.tech_s.setChecked(True)
            self.tech_o.setChecked(True)
            
            self.enum_all.setChecked(True)
            
            self.level_spin.setValue(1)
            self.risk_spin.setValue(1)
            
            # Clear console and summary
            self.console.clear()
            self.summary_tree.clear()
            
            self.status_bar.showMessage("New scan configured")
    
    def save_results(self):
        """Save scan results to file"""
        if not self.console.toPlainText():
            QMessageBox.warning(self, "Warning", "No results to save")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Results", 
            f"sqlmap_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(self.console.toPlainText())
            QMessageBox.information(self, "Success", f"Results saved to {filename}")
    
    def export_results(self, format_type: str):
        """Export results in specified format"""
        if not self.console.toPlainText():
            QMessageBox.warning(self, "Warning", "No results to export")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == "json":
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export JSON", f"sqlmap_results_{timestamp}.json",
                "JSON Files (*.json)"
            )
            if filename:
                data = {
                    'timestamp': timestamp,
                    'target': self.url_input.text(),
                    'command': self.build_command(),
                    'output': self.console.toPlainText(),
                    'summary': self.get_summary_data()
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
        
        elif format_type == "html":
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export HTML Report", f"sqlmap_report_{timestamp}.html",
                "HTML Files (*.html)"
            )
            if filename:
                self.generate_html_report(filename)
        
        elif format_type == "csv":
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export CSV", f"sqlmap_results_{timestamp}.csv",
                "CSV Files (*.csv)"
            )
            if filename:
                # Simple CSV export
                with open(filename, 'w') as f:
                    f.write("Timestamp,Target,Result\n")
                    f.write(f"{timestamp},{self.url_input.text()},\"{self.console.toPlainText()[:100]}...\"\n")
        
        if filename:
            QMessageBox.information(self, "Success", f"Results exported to {filename}")
    
    def generate_html_report(self, filename: str):
        """Generate HTML report"""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SQLMap Scan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: auto; background: white; padding: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background: #e8f5e8; padding: 10px; margin: 10px 0; }}
                .output {{ background: #1e1e1e; color: #00ff00; padding: 10px; font-family: monospace; }}
                .timestamp {{ color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SQLMap Scan Report</h1>
                <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="summary">
                    <h2>Scan Summary</h2>
                    <p><strong>Target:</strong> {self.url_input.text()}</p>
                    <p><strong>Command:</strong> {' '.join(self.build_command())}</p>
                </div>
                
                <h2>Console Output</h2>
                <pre class="output">{self.console.toPlainText()}</pre>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_template)
    
    def get_summary_data(self) -> Dict:
        """Get summary data as dictionary"""
        summary = {}
        for i in range(self.summary_tree.topLevelItemCount()):
            item = self.summary_tree.topLevelItem(i)
            summary[item.text(0)] = item.text(1)
        return summary
    
    def load_config(self):
        """Load configuration from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                # Restore settings
                self.url_input.setText(config.get('target', ''))
                self.method_combo.setCurrentText(config.get('method', 'GET'))
                self.post_data.setText(config.get('data', ''))
                
                QMessageBox.information(self, "Success", "Configuration loaded")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load config: {e}")
    
    def save_settings(self):
        """Save application settings"""
        settings = QSettings("SecurityResearch", "SQLMapGUI")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
    
    def load_settings(self):
        """Load application settings"""
        settings = QSettings("SecurityResearch", "SQLMapGUI")
        self.restoreGeometry(settings.value("geometry", b""))
        self.restoreState(settings.value("windowState", b""))
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # SQLMap path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("SQLMap Path:"))
        path_input = QLineEdit()
        path_input.setText("sqlmap")
        path_layout.addWidget(path_input)
        layout.addLayout(path_layout)
        
        # Default options
        default_group = QGroupBox("Default Options")
        default_layout = QVBoxLayout()
        default_layout.addWidget(QCheckBox("Always use batch mode"))
        default_layout.addWidget(QCheckBox("Save results automatically"))
        default_layout.addWidget(QCheckBox("Enable verbose output"))
        default_group.setLayout(default_layout)
        layout.addWidget(default_group)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Save settings
            pass
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
        <h2>Advanced SQLMap GUI - Help</h2>
        
        <h3>Quick Start:</h3>
        <ol>
            <li>Enter target URL in the Target tab</li>
            <li>Configure injection techniques</li>
            <li>Set enumeration options</li>
            <li>Click Start Scan (F5)</li>
        </ol>
        
        <h3>Features:</h3>
        <ul>
            <li><b>Target Configuration:</b> URL, POST data, cookies, headers, proxy</li>
            <li><b>Injection:</b> Multiple SQL injection techniques</li>
            <li><b>Detection:</b> Level, risk, enumeration options</li>
            <li><b>Optimization:</b> Threads, timeouts, performance tuning</li>
            <li><b>Evasion:</b> Tamper scripts for WAF bypass</li>
            <li><b>Automation:</b> Batch mode, scheduling, multiple targets</li>
        </ul>
        
        <h3>Keyboard Shortcuts:</h3>
        <ul>
            <li><b>F5:</b> Start scan</li>
            <li><b>F6:</b> Stop scan</li>
            <li><b>Ctrl+N:</b> New scan</li>
            <li><b>Ctrl+S:</b> Save results</li>
            <li><b>Ctrl+O:</b> Load configuration</li>
            <li><b>F1:</b> Help</li>
        </ul>
        
        <h3>Note:</h3>
        <p><b>IMPORTANT:</b> Only use this tool on systems you own or have explicit permission to test.</p>
        """
        
        QMessageBox.information(self, "Help", help_text)
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.save_settings()
        
        if self.current_worker and self.current_worker.isRunning():
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "A scan is still running. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_worker.stop()
                self.current_worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

class ScanScheduler(QThread):
    """Thread for scheduling scans"""
    def __init__(self):
        super().__init__()
        self.scheduled_scans = Queue()
        self.running = True
    
    def add_scan(self, scan_config: Dict, schedule_time: datetime):
        """Add a scan to the schedule"""
        self.scheduled_scans.put({
            'config': scan_config,
            'time': schedule_time,
            'id': len(self.scheduled_scans.queue)
        })
    
    def run(self):
        """Run the scheduler"""
        while self.running:
            # Check scheduled scans
            # This would implement actual scheduling logic
            time.sleep(1)

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Advanced SQLMap GUI")
    app.setOrganizationName("SecurityResearch")
    
    # Set application icon
    app.setWindowIcon(QIcon.fromTheme("applications-security"))
    
    # Create and show main window
    window = AdvancedSQLMapGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()