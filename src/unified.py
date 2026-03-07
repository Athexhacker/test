#!/usr/bin/env python3
"""
Unified Security Analysis Tool - Professional Edition
Combines Network Monitoring, Deep Web Crawling, Chrome Extension Analysis, and Web App Scanning
For authorized security testing and research ONLY
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import queue
import time
import json
import re
import hashlib
import socket
import ssl
import os
import zipfile
import tempfile
import shutil
import base64
import sys
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote, unquote, parse_qs
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# Optional imports with graceful fallback
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from scapy.all import *
    from scapy.layers import http
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# DNS is optional
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

# ============================================================================
# PROFESSIONAL COLOR SCHEME
# ============================================================================

class Colors:
    BG_PRIMARY = "#0a0c0f"
    BG_SECONDARY = "#1a1d24"
    BG_TERTIARY = "#2d333b"
    FG_PRIMARY = "#e6edf3"
    FG_SECONDARY = "#848d97"
    ACCENT_RED = "#f85149"
    ACCENT_GREEN = "#3fb950"
    ACCENT_BLUE = "#58a6ff"
    ACCENT_ORANGE = "#db6d28"
    ACCENT_PURPLE = "#bc8cff"
    ACCENT_YELLOW = "#FFD700"
    ACCENT_CYAN = "#79c0ff"
    CRITICAL = "#f85149"
    HIGH = "#db6d28"
    MEDIUM = "#f7d44a"
    LOW = "#3fb950"
    INFO = "#58a6ff"
    BORDER = "#30363d"
    PROGRESS_BG = "#1a1d24"
    PROGRESS_FG = "#58a6ff"

# ============================================================================
# ANIMATION AND PROGRESS MANAGER
# ============================================================================

class ProgressManager:
    """Manages live progress updates and animations"""
    
    def __init__(self, root, progress_bar, progress_label, percentage_label):
        self.root = root
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.percentage_label = percentage_label
        self.current_value = 0
        self.is_running = False
        self.animation_id = None
        
    def start_pulse(self):
        """Start pulsing animation when progress is indeterminate"""
        self.is_running = True
        self._pulse(0)
        
    def _pulse(self, step):
        """Pulse animation loop"""
        if not self.is_running:
            return
            
        # Create pulsing effect by varying the progress bar style
        colors = [Colors.PROGRESS_FG, Colors.ACCENT_CYAN, Colors.ACCENT_BLUE, Colors.ACCENT_PURPLE]
        style = ttk.Style()
        style.configure("color.Horizontal.TProgressbar", 
                       background=colors[step % len(colors)],
                       troughcolor=Colors.PROGRESS_BG)
        self.progress_bar.configure(style="color.Horizontal.TProgressbar")
        
        self.animation_id = self.root.after(300, lambda: self._pulse(step + 1))
        
    def stop_pulse(self):
        """Stop pulsing animation"""
        self.is_running = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
            
    def update_progress(self, value, message):
        """Update progress with percentage"""
        self.current_value = value
        self.progress_bar['value'] = value
        self.progress_label.config(text=message)
        self.percentage_label.config(text=f"{value}%")
        self.root.update_idletasks()
        
    def increment(self, amount=1, message=None):
        """Increment progress by amount"""
        new_value = min(100, self.current_value + amount)
        self.update_progress(new_value, message or self.progress_label.cget('text'))
        
    def reset(self):
        """Reset progress to zero"""
        self.current_value = 0
        self.progress_bar['value'] = 0
        self.percentage_label.config(text="0%")
        self.progress_label.config(text="Ready")
        self.stop_pulse()

# ============================================================================
# ENUMS AND DATA CLASSES
# ============================================================================

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class SourceType(Enum):
    NETWORK = "Network Traffic"
    DEEP_SCAN = "Deep Web Crawl"
    EXTENSION = "Chrome Extension"
    WEB_APP = "Web Application"

@dataclass
class ChromeExtension:
    id: str
    name: str
    version: str
    description: str
    author: str
    rating: float
    users: int
    permissions: List[str]
    host_permissions: List[str]
    download_url: str
    crx_url: str
    last_updated: str

@dataclass
class Vulnerability:
    type: str
    description: str
    file: str
    line_number: int
    severity: Severity
    remediation: str
    source_type: SourceType
    url: str = ""
    cwe: Optional[str] = None
    owasp: Optional[str] = None
    poc: Optional[str] = None
    impact: Optional[str] = None
    timestamp: str = ""

# ============================================================================
# COMPREHENSIVE API KEY PATTERNS
# ============================================================================

API_PATTERNS = {
    # Cloud Providers
    'AWS Access Key': {
        'pattern': r'AKIA[0-9A-Z]{16}',
        'confidence': 0.95,
        'category': 'Cloud',
        'risk': 'High',
        'description': 'AWS Access Key ID',
        'cwe': 'CWE-798'
    },
    'AWS Secret Key': {
        'pattern': r'(?i)aws_secret.?access.?key[=:]["\']?[0-9a-zA-Z/+]{40}',
        'confidence': 0.90,
        'category': 'Cloud',
        'risk': 'Critical',
        'description': 'AWS Secret Access Key',
        'cwe': 'CWE-798'
    },
    'Google API Key': {
        'pattern': r'AIza[0-9A-Za-z\-_]{35}',
        'confidence': 0.90,
        'category': 'Cloud',
        'risk': 'High',
        'description': 'Google Cloud API Key',
        'cwe': 'CWE-798'
    },
    'Google OAuth': {
        'pattern': r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com',
        'confidence': 0.95,
        'category': 'Cloud',
        'risk': 'High',
        'description': 'Google OAuth Client ID',
        'cwe': 'CWE-798'
    },
    
    # AI Services
    'OpenAI API': {
        'pattern': r'sk-[a-zA-Z0-9]{48,}|sk-proj-[a-zA-Z0-9]{50,}',
        'confidence': 0.98,
        'category': 'AI',
        'risk': 'Critical',
        'description': 'OpenAI API Key',
        'cwe': 'CWE-798'
    },
    'Anthropic API': {
        'pattern': r'sk-ant-[a-zA-Z0-9_-]{30,50}',
        'confidence': 0.95,
        'category': 'AI',
        'risk': 'Critical',
        'description': 'Anthropic Claude API Key',
        'cwe': 'CWE-798'
    },
    
    # Payment Processors
    'Stripe Live': {
        'pattern': r'sk_live_[0-9a-zA-Z]{24,}|rk_live_[0-9a-zA-Z]{24,}',
        'confidence': 0.98,
        'category': 'Payment',
        'risk': 'Critical',
        'description': 'Stripe Live Secret Key',
        'cwe': 'CWE-798'
    },
    'PayPal': {
        'pattern': r'access_token\$production\$[0-9a-zA-Z]{20,}\$[0-9a-f]{32}',
        'confidence': 0.95,
        'category': 'Payment',
        'risk': 'Critical',
        'description': 'PayPal Access Token',
        'cwe': 'CWE-798'
    },
    
    # DevOps
    'GitHub Token': {
        'pattern': r'gh[pousr]_[a-zA-Z0-9]{36,}',
        'confidence': 0.95,
        'category': 'DevOps',
        'risk': 'High',
        'description': 'GitHub Personal Access Token',
        'cwe': 'CWE-798'
    },
    
    # Communication
    'Discord Token': {
        'pattern': r'[MN][A-Za-z\d]{23,25}\.[A-Za-z\d]{6}\.[A-Za-z\d\-_]{27,}',
        'confidence': 0.90,
        'category': 'Communication',
        'risk': 'High',
        'description': 'Discord Bot Token',
        'cwe': 'CWE-798'
    },
    'Telegram Bot': {
        'pattern': r'[0-9]{8,10}:[a-zA-Z0-9_-]{35,40}',
        'confidence': 0.95,
        'category': 'Communication',
        'risk': 'High',
        'description': 'Telegram Bot Token',
        'cwe': 'CWE-798'
    },
    
    # Database
    'MongoDB URI': {
        'pattern': r'mongodb(\+srv)?:\/\/[^\s<>"\'(){}|\\^`\[\]]+',
        'confidence': 0.85,
        'category': 'Database',
        'risk': 'Critical',
        'description': 'MongoDB Connection String',
        'cwe': 'CWE-798'
    },
    
    # Authentication
    'JWT Token': {
        'pattern': r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
        'confidence': 0.75,
        'category': 'Auth',
        'risk': 'Medium',
        'description': 'JSON Web Token',
        'cwe': 'CWE-312'
    },
    'Firebase URL': {
        'pattern': r'https?://[a-zA-Z0-9-]+\.firebaseio\.com',
        'confidence': 0.85,
        'category': 'Database',
        'risk': 'Medium',
        'description': 'Firebase Database URL',
        'cwe': 'CWE-200'
    }
}

# ============================================================================
# VULNERABILITY PATTERNS FOR EXTENSION ANALYSIS
# ============================================================================

VULNERABILITY_PATTERNS = [
    # Hardcoded credentials
    ('hardcoded_api_key', r'api[_-]?key[\s]*[:=][\s]*[\'"]([^\'"]+)[\'"]', Severity.CRITICAL, 'CWE-798', 'OWASP API3:2019'),
    ('hardcoded_password', r'password[\s]*[:=][\s]*[\'"]([^\'"]+)[\'"]', Severity.CRITICAL, 'CWE-798', 'OWASP API3:2019'),
    ('hardcoded_token', r'token[\s]*[:=][\s]*[\'"]([^\'"]+)[\'"]', Severity.HIGH, 'CWE-798', 'OWASP API3:2019'),
    ('hardcoded_secret', r'secret[\s]*[:=][\s]*[\'"]([^\'"]+)[\'"]', Severity.CRITICAL, 'CWE-798', 'OWASP API3:2019'),
    
    # Dangerous JavaScript
    ('eval_usage', r'eval\(', Severity.CRITICAL, 'CWE-95', 'OWASP API7:2019'),
    ('innerHTML_usage', r'\.innerHTML\s*=', Severity.HIGH, 'CWE-79', 'OWASP API7:2019'),
    ('document_write', r'document\.write\(', Severity.HIGH, 'CWE-79', 'OWASP API7:2019'),
    ('setTimeout_string', r'setTimeout\s*\(\s*[\'"]', Severity.MEDIUM, 'CWE-95', 'OWASP API7:2019'),
    ('Function_constructor', r'new\s+Function\s*\(', Severity.HIGH, 'CWE-95', 'OWASP API7:2019'),
    
    # Storage of sensitive data
    ('localStorage_sensitive', r'localStorage\.setItem\s*\(\s*[\'"]?(token|key|secret|password|auth)', Severity.HIGH, 'CWE-312', 'OWASP API4:2019'),
    ('sessionStorage_sensitive', r'sessionStorage\.setItem\s*\(\s*[\'"]?(token|key|secret|password|auth)', Severity.MEDIUM, 'CWE-312', 'OWASP API4:2019'),
    ('cookie_sensitive', r'document\.cookie\s*=\s*[\'"]?[^;]*(token|key|secret|password|auth)', Severity.HIGH, 'CWE-312', 'OWASP API4:2019'),
    
    # Insecure communication
    ('http_url', r'http://[^\s"\'<>]+', Severity.HIGH, 'CWE-319', 'OWASP API8:2019'),
    ('mixed_content', r'https?://[^\s"\'<>]*\.(jpg|png|gif|css|js)[\'"]?', Severity.MEDIUM, 'CWE-319', 'OWASP API8:2019'),
    
    # Extension-specific vulnerabilities
    ('wildcard_permission', r'\*://\*/\*|\<all_urls\>', Severity.CRITICAL, 'CWE-265', 'OWASP API1:2019'),
    ('unsafe_eval_in_manifest', r'"content_security_policy".*?(unsafe-eval|unsafe-inline)', Severity.CRITICAL, 'CWE-265', 'OWASP API7:2019'),
    ('external_script', r'<script\s+src=[\'"]https?://[^\'"]+[\'"]', Severity.MEDIUM, 'CWE-829', 'OWASP API6:2019'),
    
    # Information disclosure
    ('internal_ip', r'(192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+)', Severity.MEDIUM, 'CWE-200', 'OWASP API5:2019'),
    ('email_address', r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', Severity.LOW, 'CWE-200', 'OWASP API5:2019'),
]

# ============================================================================
# SQL INJECTION PAYLOADS
# ============================================================================

SQL_PAYLOADS = [
    "'", "\"", "';--", "\" --", "' OR '1'='1", "' OR '1'='1' --",
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
    "' AND SLEEP(5)--", "' WAITFOR DELAY '00:00:05'--",
    "admin'--", "1' ORDER BY 1--", "1' ORDER BY 100--"
]

# ============================================================================
# XSS PAYLOADS
# ============================================================================

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "\"><script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<svg onload=alert('XSS')>",
    "'-alert('XSS')-'",
    "\"-alert('XSS')-\"",
    "{{7*7}}",
    "${7*7}",
    "<%= 7*7 %>"
]

# ============================================================================
# PATH TRAVERSAL PAYLOADS
# ============================================================================

PATH_TRAVERSAL = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\win.ini",
    "%2e%2e%2fetc%2fpasswd",
    "....//....//....//etc/passwd",
    "..;/etc/passwd"
]

# ============================================================================
# COMMON DIRECTORIES FOR ENUMERATION
# ============================================================================

COMMON_PATHS = [
    # Admin panels
    'admin', 'administrator', 'adminarea', 'admin-panel', 'dashboard',
    'cms-admin', 'wp-admin', 'joomla-admin', 'drupal-admin',
    
    # API endpoints
    'api', 'api/v1', 'api/v2', 'api/v3', 'rest', 'graphql', 'swagger', 'docs',
    
    # Backup directories
    'backup', 'backups', 'bak', 'old', 'temp', 'tmp', 'test',
    
    # Upload directories
    'uploads', 'upload', 'files', 'media', 'images', 'assets',
    
    # Configuration
    'config', 'configuration', 'settings', 'setup', 'install',
    
    # Development
    'dev', 'development', 'staging', 'test', 'testing', 'debug',
    
    # Common CMS paths
    'wp-content', 'wp-includes', 'wp-json',
    'includes', 'modules', 'components', 'templates',
    
    # Authentication
    'login', 'signin', 'auth', 'oauth', 'authenticate',
    'register', 'signup', 'forgot-password', 'reset-password',
    
    # User areas
    'user', 'users', 'profile', 'account', 'my-account', 'my-profile',
    
    # File managers
    'filemanager', 'file-manager', 'elfinder', 'ckfinder',
    
    # Database interfaces
    'phpmyadmin', 'pma', 'adminer', 'phpPgAdmin', 'phpMyAdmin',
    
    # Logs
    'logs', 'log', 'error_log', 'access_log', 'debug_log',
    
    # Source code
    'src', 'source', 'lib', 'vendor', 'node_modules'
]

# ============================================================================
# SENSITIVE FILES
# ============================================================================

SENSITIVE_FILES = [
    '.env', '.git/config', '.git/HEAD', '.svn/entries', '.svn/wc.db',
    'wp-config.php', 'wp-config.bak', 'config.php', 'config.bak',
    'database.yml', 'application.yml', 'secrets.yml',
    'backup.sql', 'dump.sql', 'db_backup.sql',
    'phpinfo.php', 'info.php', 'test.php',
    'robots.txt', 'sitemap.xml', 'crossdomain.xml',
    'README.md', 'CHANGELOG.md', 'composer.json', 'package.json',
    'web.config', '.htaccess', '.htpasswd',
    'error_log', 'debug.log', 'install.php', 'setup.php'
]

# ============================================================================
# CHROME EXTENSION ANALYZER WITH PROGRESS
# ============================================================================

class ChromeExtensionAnalyzer:
    """Advanced Chrome Extension analyzer with deep security analysis and progress tracking"""
    
    def __init__(self, callback=None, progress_callback=None):
        self.callback = callback
        self.progress_callback = progress_callback
        self.stop_flag = False
        self.temp_dir = None
        self.results = {
            'metadata': {},
            'permissions': [],
            'host_permissions': [],
            'content_scripts': [],
            'background_scripts': [],
            'apis': [],
            'vulnerabilities': [],
            'external_domains': [],
            'obfuscated_code': [],
            'storage_usage': [],
            'message_passing': [],
            'web_accessible_resources': [],
            'analysis_summary': {}
        }
        
        # Chrome Web Store API endpoints
        self.CWS_API = "https://chrome.google.com/webstore/detail/"
        self.CWS_DETAILS_API = "https://chrome.google.com/webstore/ajax/detail"
        self.CWS_CRX_URL = "https://clients2.google.com/service/update2/crx"
        
    def analyze_extension(self, extension_id: str, deep_scan: bool = True):
        """Analyze Chrome extension by ID with live progress"""
        try:
            self._log(f"🔍 Starting Chrome extension analysis for ID: {extension_id}")
            self._update_progress(5, "Fetching extension metadata...")
            
            # Step 1: Fetch extension metadata (5-15%)
            metadata = self._fetch_extension_metadata(extension_id)
            if not metadata:
                self._log("❌ Failed to fetch extension metadata", "ERROR")
                return None
                
            self.results['metadata'] = metadata
            self._log(f"📦 Extension: {metadata.get('name', 'Unknown')} v{metadata.get('version', 'Unknown')}")
            self._update_progress(15, "Metadata fetched, downloading extension...")
            
            # Step 2: Download CRX file (15-25%)
            crx_data = self._download_extension(extension_id)
            if not crx_data:
                self._log("❌ Failed to download extension", "ERROR")
                return None
            self._update_progress(25, "Extension downloaded, extracting...")
                
            # Step 3: Extract and analyze (25-35%)
            self.temp_dir = tempfile.mkdtemp(prefix="chrome_ext_")
            
            if self._extract_extension(crx_data):
                self._update_progress(35, "Extraction complete, analyzing manifest...")
                
                # Step 4: Analyze manifest (35-45%)
                self._analyze_manifest()
                self._update_progress(45, "Manifest analyzed, discovering JavaScript files...")
                
                # Step 5: Find all JavaScript files (45-55%)
                js_files = self._find_javascript_files()
                total_files = len(js_files)
                self._update_progress(55, f"Found {total_files} JavaScript files, analyzing...")
                
                # Step 6: Deep JavaScript analysis (55-70%)
                for idx, js_file in enumerate(js_files):
                    if self.stop_flag:
                        break
                    self._analyze_javascript_file(js_file)
                    # Update progress based on file count
                    progress = 55 + int((idx + 1) / total_files * 15)
                    self._update_progress(progress, f"Analyzing JavaScript {idx+1}/{total_files}")
                
                if self.stop_flag:
                    self._cleanup()
                    return None
                    
                # Step 7: Security vulnerability scan (70-85%)
                self._update_progress(70, "Scanning for vulnerabilities...")
                self._scan_vulnerabilities(js_files)
                self._update_progress(85, "Vulnerability scan complete")
                
                # Step 8: External resource analysis (85-90%)
                self._update_progress(85, "Analyzing external resources...")
                self._analyze_external_resources(js_files)
                self._update_progress(90, "External resource analysis complete")
                
                # Step 9: Generate summary (90-100%)
                self._update_progress(90, "Generating analysis summary...")
                self._generate_summary()
                
                # Step 10: Cleanup
                self._update_progress(100, "Analysis complete!")
                self._cleanup()
                
                self._log(f"✅ Extension analysis complete. Found {len(self.results['vulnerabilities'])} vulnerabilities")
                return self.results
            else:
                self._log("❌ Failed to extract extension", "ERROR")
                self._cleanup()
                return None
                
        except Exception as e:
            self._log(f"❌ Analysis failed: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            self._cleanup()
            return None
            
    def analyze_by_url(self, url: str):
        """Analyze extension from Chrome Web Store URL"""
        patterns = [
            r'/detail/[^/]+/([a-z]{32})',
            r'id=([a-z]{32})',
            r'webstore/detail/[^/]+/([a-z]{32})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return self.analyze_extension(match.group(1))
                
        self._log("❌ Could not extract extension ID from URL", "ERROR")
        return None
        
    def _fetch_extension_metadata(self, extension_id: str) -> Dict:
        """Fetch extension metadata from Chrome Web Store"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            url = f"{self.CWS_API}{extension_id}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                metadata = {
                    'id': extension_id,
                    'name': self._extract_text(soup, 'h1', 'Unknown'),
                    'version': self._extract_text(soup, 'span[class*="version"]', 'Unknown'),
                    'description': self._extract_text(soup, 'meta[name="description"]', '', 'content'),
                    'author': self._extract_text(soup, 'div[class*="author"]', 'Unknown'),
                    'rating': self._extract_rating(soup),
                    'users': self._extract_users(soup),
                    'last_updated': self._extract_text(soup, 'div[class*="last-updated"]', 'Unknown'),
                    'permissions': self._extract_permissions(soup),
                    'host_permissions': self._extract_host_permissions(soup),
                    'category': self._extract_category(soup),
                    'size': self._extract_size(soup),
                    'languages': self._extract_languages(soup)
                }
                
                return metadata
                
        except Exception as e:
            self._log(f"Metadata fetch error: {str(e)}", "WARNING")
            
        return {
            'id': extension_id,
            'name': extension_id,
            'version': 'Unknown',
            'description': 'Could not fetch metadata',
            'author': 'Unknown',
            'rating': 0.0,
            'users': 0,
            'permissions': [],
            'host_permissions': []
        }
        
    def _extract_text(self, soup, selector, default, attr=None):
        """Extract text from BeautifulSoup element"""
        try:
            element = soup.select_one(selector)
            if element:
                if attr:
                    return element.get(attr, default)
                return element.get_text(strip=True)
        except:
            pass
        return default
        
    def _extract_rating(self, soup):
        """Extract rating from page"""
        try:
            rating_elem = soup.select_one('meta[itemprop="ratingValue"]')
            if rating_elem:
                return float(rating_elem.get('content', '0'))
        except:
            pass
        return 0.0
        
    def _extract_users(self, soup):
        """Extract user count"""
        try:
            users_elem = soup.select_one('span[class*="users"]')
            if users_elem:
                text = users_elem.get_text()
                numbers = re.findall(r'[\d,]+', text)
                if numbers:
                    return int(numbers[0].replace(',', ''))
        except:
            pass
        return 0
        
    def _extract_permissions(self, soup):
        """Extract permissions"""
        permissions = []
        try:
            perm_elements = soup.select('ul[class*="permissions"] li')
            for elem in perm_elements:
                permissions.append(elem.get_text(strip=True))
        except:
            pass
        return permissions
        
    def _extract_host_permissions(self, soup):
        """Extract host permissions"""
        return []
        
    def _extract_category(self, soup):
        """Extract category"""
        try:
            cat_elem = soup.select_one('a[href*="/category/"]')
            if cat_elem:
                return cat_elem.get_text(strip=True)
        except:
            pass
        return 'Unknown'
        
    def _extract_size(self, soup):
        """Extract extension size"""
        try:
            size_elem = soup.select_one('dd:contains("Size")')
            if size_elem:
                return size_elem.get_text(strip=True)
        except:
            pass
        return 'Unknown'
        
    def _extract_languages(self, soup):
        """Extract supported languages"""
        try:
            lang_elem = soup.select_one('dd:contains("Language")')
            if lang_elem:
                text = lang_elem.get_text()
                return [lang.strip() for lang in text.split(',')]
        except:
            pass
        return ['en']
        
    def _download_extension(self, extension_id: str) -> Optional[bytes]:
        """Download CRX file from Chrome Web Store"""
        try:
            params = {
                'response': 'redirect',
                'os': 'win',
                'arch': 'x64',
                'nacl_arch': 'x86-64',
                'prod': 'chromium',
                'prodchannel': 'stable',
                'prodversion': '100.0.4896.127',
                'acceptformat': 'crx2,crx3',
                'x': f'id={extension_id}&uc'
            }
            
            response = requests.get(self.CWS_CRX_URL, params=params, timeout=30)
            if response.status_code == 200:
                return response.content
                
        except Exception as e:
            self._log(f"Download error: {str(e)}", "ERROR")
            
        return None
        
    def _extract_extension(self, crx_data: bytes) -> bool:
        """Extract CRX file"""
        try:
            if crx_data.startswith(b'Cr24'):
                magic = crx_data[0:4]
                version = int.from_bytes(crx_data[4:8], byteorder='little')
                header_len = int.from_bytes(crx_data[8:12], byteorder='little')
                
                zip_data = crx_data[12 + header_len:]
                
                zip_path = os.path.join(self.temp_dir, 'extension.zip')
                with open(zip_path, 'wb') as f:
                    f.write(zip_data)
                    
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.temp_dir)
                    
                return True
                
        except Exception as e:
            self._log(f"Extraction error: {str(e)}", "ERROR")
            
        return False
        
    def _analyze_manifest(self):
        """Analyze manifest.json"""
        manifest_path = os.path.join(self.temp_dir, 'manifest.json')
        if not os.path.exists(manifest_path):
            self._log("⚠️ No manifest.json found", "WARNING")
            return
            
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                
            self.results['permissions'] = manifest.get('permissions', [])
            self.results['host_permissions'] = manifest.get('host_permissions', [])
            
            content_scripts = manifest.get('content_scripts', [])
            for script in content_scripts:
                self.results['content_scripts'].extend(script.get('js', []))
                
            background = manifest.get('background', {})
            if 'scripts' in background:
                self.results['background_scripts'].extend(background['scripts'])
            if 'service_worker' in background:
                self.results['background_scripts'].append(background['service_worker'])
                
            self.results['web_accessible_resources'] = manifest.get('web_accessible_resources', [])
            
            csp = manifest.get('content_security_policy', {})
            if isinstance(csp, dict):
                csp = csp.get('extension_pages', '')
            if 'unsafe-eval' in csp or 'unsafe-inline' in csp:
                self._add_vulnerability(
                    'unsafe_eval_in_manifest',
                    'Unsafe CSP policy allowing eval/inline scripts',
                    'manifest.json',
                    0,
                    Severity.CRITICAL,
                    'Remove unsafe-eval and unsafe-inline from CSP',
                    'CWE-265',
                    'OWASP API7:2019'
                )
                
        except Exception as e:
            self._log(f"Manifest analysis error: {str(e)}", "ERROR")
            
    def _find_javascript_files(self) -> List[str]:
        """Find all JavaScript files"""
        js_files = []
        extensions = ['.js', '.jsx', '.ts', '.tsx']
        
        for root, dirs, files in os.walk(self.temp_dir):
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', 'build']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    rel_path = os.path.relpath(os.path.join(root, file), self.temp_dir)
                    js_files.append(rel_path)
                    
        return js_files
        
    def _analyze_javascript_file(self, js_file: str):
        """Analyze a single JavaScript file"""
        file_path = os.path.join(self.temp_dir, js_file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            if self._is_obfuscated(content):
                self.results['obfuscated_code'].append({
                    'file': js_file,
                    'obfuscation_type': self._detect_obfuscation_type(content)
                })
                
            self._extract_api_endpoints(content, js_file)
            self._check_storage_usage(content, js_file)
            self._check_message_passing(content, js_file)
            self._extract_external_domains(content, js_file)
                
        except Exception as e:
            self._log(f"Error analyzing {js_file}: {str(e)}", "WARNING")
                
    def _is_obfuscated(self, content: str) -> bool:
        """Check if code is obfuscated"""
        indicators = [
            r'eval\(function\(p,a,c,k,e,d\)',
            r'\\x[0-9a-f]{2}',
            r'String\.fromCharCode',
            r'atob\(',
            r'\[[0-9A-F]{2,}\]',
            len(re.findall(r'[_$][a-zA-Z0-9]{1,2}', content)) > 100,
        ]
        
        score = sum(1 for indicator in indicators if isinstance(indicator, bool) and indicator or 
                   isinstance(indicator, str) and re.search(indicator, content))
                   
        return score >= 2
        
    def _detect_obfuscation_type(self, content: str) -> str:
        """Detect obfuscation technique"""
        if re.search(r'eval\(function\(p,a,c,k,e,d\)', content):
            return 'Packer Obfuscation'
        elif re.search(r'\\x[0-9a-f]{2}', content):
            return 'Hex Encoding'
        elif re.search(r'atob\(', content):
            return 'Base64 Encoding'
        elif re.search(r'String\.fromCharCode', content):
            return 'CharCode Obfuscation'
        else:
            return 'Minified/Unknown'
            
    def _extract_api_endpoints(self, content: str, js_file: str):
        """Extract API endpoints from JavaScript"""
        patterns = [
            (r'fetch\([\'"]([^\'"]+)[\'"]', 'fetch'),
            (r'axios\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', 'axios'),
            (r'\$\.(get|post|ajax)\([\'"]([^\'"]+)[\'"]', 'jquery'),
            (r'XMLHttpRequest\([^)]*\)[^;]*open\([\'"](\w+)[\'"],\s*[\'"]([^\'"]+)[\'"]', 'xhr'),
            (r'chrome\.runtime\.sendMessage\([^,]*,\s*[\'"]([^\'"]+)[\'"]', 'extension_message'),
            (r'chrome\.tabs\.(sendMessage|executeScript)\([^,]*,\s*[\'"]([^\'"]+)[\'"]', 'tabs_api'),
            (r'https?://[^\s"\'<>]+', 'url'),
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern, api_type in patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        if api_type == 'xhr' and len(match) >= 2:
                            url = match[1]
                            method = match[0]
                        elif api_type == 'axios' and len(match) == 2:
                            method, url = match[0], match[1]
                        else:
                            url = match[0]
                            method = 'GET'
                    else:
                        url = match
                        method = 'GET'
                        
                    if self._is_valid_url(url):
                        self._check_api_keys_in_url(url, js_file, line_num)
                        
                        self.results['apis'].append({
                            'url': url,
                            'method': method.upper() if isinstance(method, str) else 'GET',
                            'file': js_file,
                            'line_number': line_num,
                            'type': api_type
                        })
                        
    def _check_api_keys_in_url(self, url: str, js_file: str, line_num: int):
        """Check if URL contains API keys"""
        for key_type, config in API_PATTERNS.items():
            if re.search(config['pattern'], url):
                self._add_vulnerability(
                    'api_key_in_url',
                    f'API key ({key_type}) exposed in URL',
                    js_file,
                    line_num,
                    Severity.CRITICAL,
                    'Remove API keys from URLs, use headers instead',
                    config.get('cwe', 'CWE-200'),
                    'OWASP API3:2019'
                )
                
    def _check_storage_usage(self, content: str, js_file: str):
        """Check storage usage patterns"""
        patterns = [
            (r'localStorage\.setItem\s*\(\s*[\'"]([^\'"]+)[\'"]', 'localStorage'),
            (r'sessionStorage\.setItem\s*\(\s*[\'"]([^\'"]+)[\'"]', 'sessionStorage'),
            (r'chrome\.storage\.local\.set\s*\(', 'chrome.storage.local'),
            (r'chrome\.storage\.sync\.set\s*\(', 'chrome.storage.sync'),
            (r'indexedDB\.open\s*\(', 'IndexedDB'),
        ]
        
        for pattern, storage_type in patterns:
            if re.search(pattern, content):
                self.results['storage_usage'].append({
                    'type': storage_type,
                    'file': js_file
                })
                
    def _check_message_passing(self, content: str, js_file: str):
        """Check message passing patterns"""
        patterns = [
            (r'chrome\.runtime\.(onMessage|onMessageExternal)\.addListener', 'message_listener'),
            (r'chrome\.runtime\.sendMessage', 'send_message'),
            (r'chrome\.runtime\.connect', 'port_connection'),
            (r'port\.(postMessage|onMessage)', 'port_communication'),
            (r'window\.addEventListener\s*\(\s*[\'"]message[\'"]', 'window_message'),
        ]
        
        for pattern, msg_type in patterns:
            if re.search(pattern, content):
                self.results['message_passing'].append({
                    'type': msg_type,
                    'file': js_file
                })
                
    def _extract_external_domains(self, content: str, js_file: str):
        """Extract external domains from JavaScript"""
        domain_pattern = r'https?://([a-zA-Z0-9.-]+)'
        domains = re.findall(domain_pattern, content)
        
        for domain in set(domains):
            if domain not in ['localhost', '127.0.0.1'] and '.' in domain:
                self.results['external_domains'].append({
                    'domain': domain,
                    'file': js_file
                })
                
    def _scan_vulnerabilities(self, js_files: List[str]):
        """Scan for vulnerabilities"""
        for js_file in js_files:
            if self.stop_flag:
                break
                
            file_path = os.path.join(self.temp_dir, js_file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for line_num, line in enumerate(lines, 1):
                    for vuln_name, pattern, severity, cwe, owasp in VULNERABILITY_PATTERNS:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            if self._is_false_positive(line, vuln_name):
                                continue
                                
                            start = max(0, match.start() - 50)
                            end = min(len(line), match.end() + 50)
                            context = line[start:end].strip()
                            
                            self._add_vulnerability(
                                vuln_name,
                                self._get_vuln_description(vuln_name),
                                js_file,
                                line_num,
                                severity,
                                self._get_remediation(vuln_name),
                                cwe,
                                owasp,
                                context
                            )
                            
            except Exception as e:
                self._log(f"Error scanning {js_file}: {str(e)}", "WARNING")
                
    def _is_false_positive(self, line: str, vuln_name: str) -> bool:
        """Check if finding is a false positive"""
        false_positives = {
            'hardcoded_api_key': ['example.com', 'test.com', 'localhost', '127.0.0.1'],
            'http_url': ['http://localhost', 'http://127.0.0.1', 'http://0.0.0.0'],
        }
        
        if vuln_name in false_positives:
            for fp in false_positives[vuln_name]:
                if fp in line.lower():
                    return True
                    
        return False
        
    def _get_vuln_description(self, vuln_name: str) -> str:
        """Get vulnerability description"""
        descriptions = {
            'hardcoded_api_key': 'Hardcoded API key found in source code',
            'hardcoded_password': 'Hardcoded password found in source code',
            'hardcoded_token': 'Hardcoded authentication token found',
            'hardcoded_secret': 'Hardcoded secret key found',
            'eval_usage': 'Use of eval() which can lead to code injection',
            'innerHTML_usage': 'Use of innerHTML which can lead to XSS',
            'document_write': 'Use of document.write() which can lead to XSS',
            'setTimeout_string': 'Use of setTimeout with string argument (like eval)',
            'Function_constructor': 'Use of Function constructor (like eval)',
            'localStorage_sensitive': 'Sensitive data stored in localStorage',
            'sessionStorage_sensitive': 'Sensitive data stored in sessionStorage',
            'cookie_sensitive': 'Sensitive data stored in cookies',
            'http_url': 'Insecure HTTP URL used',
            'wildcard_permission': 'Wildcard permission grants excessive access',
            'unsafe_eval_in_manifest': 'Unsafe CSP allowing eval/inline scripts',
            'external_script': 'External script loaded from third-party domain',
            'internal_ip': 'Internal IP address disclosed',
            'email_address': 'Email address disclosed',
        }
        return descriptions.get(vuln_name, f'Found {vuln_name} pattern')
        
    def _get_remediation(self, vuln_name: str) -> str:
        """Get remediation advice"""
        remediations = {
            'hardcoded_api_key': 'Use environment variables or secure storage',
            'hardcoded_password': 'Never hardcode passwords - use credential managers',
            'hardcoded_token': 'Store tokens securely, use secure session management',
            'hardcoded_secret': 'Use secret management services',
            'eval_usage': 'Avoid eval() - use JSON.parse() or Function constructor safely',
            'innerHTML_usage': 'Use textContent or createElement() with proper escaping',
            'document_write': 'Use DOM manipulation methods with proper encoding',
            'setTimeout_string': 'Use function references instead of strings',
            'Function_constructor': 'Avoid dynamic code generation',
            'localStorage_sensitive': 'Avoid storing sensitive data in localStorage',
            'sessionStorage_sensitive': 'Use secure session management',
            'cookie_sensitive': 'Set HttpOnly and Secure flags, use encryption',
            'http_url': 'Use HTTPS for all external communications',
            'wildcard_permission': 'Request only specific domains needed',
            'unsafe_eval_in_manifest': 'Use strict CSP without unsafe-eval/unsafe-inline',
            'external_script': 'Use SRI hashes and verify third-party scripts',
            'internal_ip': 'Remove internal IP addresses from code',
            'email_address': 'Remove email addresses or use contact forms',
        }
        return remediations.get(vuln_name, 'Review and fix this security issue')
        
    def _add_vulnerability(self, vuln_type: str, description: str, file: str, 
                          line_num: int, severity: Severity, remediation: str,
                          cwe: str = None, owasp: str = None, context: str = None):
        """Add vulnerability to results"""
        self.results['vulnerabilities'].append({
            'type': vuln_type,
            'description': description,
            'file': file,
            'line_number': line_num,
            'severity': severity.value,
            'remediation': remediation,
            'cwe': cwe,
            'owasp': owasp,
            'context': context,
            'source_type': SourceType.EXTENSION.value
        })
        
    def _analyze_external_resources(self, js_files: List[str]):
        """Analyze external resources for security issues"""
        external_resources = []
        
        for js_file in js_files:
            file_path = os.path.join(self.temp_dir, js_file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                script_pattern = r'<script\s+src=[\'"](https?://[^\'"]+)[\'"]'
                scripts = re.findall(script_pattern, content, re.IGNORECASE)
                
                for script in scripts:
                    external_resources.append({
                        'url': script,
                        'file': js_file,
                        'type': 'script'
                    })
                    
                css_pattern = r'<link\s+[^>]*href=[\'"](https?://[^\'"]+\.css)[\'"]'
                css = re.findall(css_pattern, content, re.IGNORECASE)
                
                for stylesheet in css:
                    external_resources.append({
                        'url': stylesheet,
                        'file': js_file,
                        'type': 'stylesheet'
                    })
                    
                iframe_pattern = r'<iframe\s+[^>]*src=[\'"](https?://[^\'"]+)[\'"]'
                iframes = re.findall(iframe_pattern, content, re.IGNORECASE)
                
                for iframe in iframes:
                    external_resources.append({
                        'url': iframe,
                        'file': js_file,
                        'type': 'iframe'
                    })
                    
            except Exception:
                pass
                
        self.results['external_resources'] = external_resources
        
    def _generate_summary(self):
        """Generate analysis summary"""
        vulns_by_severity = defaultdict(int)
        for vuln in self.results['vulnerabilities']:
            vulns_by_severity[vuln['severity']] += 1
            
        self.results['analysis_summary'] = {
            'total_files': len(self._find_javascript_files()),
            'total_apis': len(self.results['apis']),
            'total_vulnerabilities': len(self.results['vulnerabilities']),
            'vulnerabilities_by_severity': dict(vulns_by_severity),
            'risk_score': self._calculate_risk_score(vulns_by_severity),
            'obfuscated_files': len(self.results['obfuscated_code']),
            'external_domains': len(set(d['domain'] for d in self.results['external_domains']))
        }
        
    def _calculate_risk_score(self, vulns_by_severity: Dict) -> int:
        """Calculate overall risk score (0-100)"""
        weights = {
            'CRITICAL': 25,
            'HIGH': 10,
            'MEDIUM': 5,
            'LOW': 1,
            'INFO': 0
        }
        
        score = 0
        for severity, count in vulns_by_severity.items():
            score += count * weights.get(severity, 0)
            
        return min(100, score)
        
    def _is_valid_url(self, url: str) -> bool:
        """Check if string is a valid URL"""
        try:
            if isinstance(url, str):
                url_lower = url.lower()
                if url_lower.startswith(('http://', 'https://', '/api', 'api.', 'wss://', 'ws://')):
                    return True
                if '://' in url_lower and not url_lower.startswith(('data:', 'blob:', 'chrome-extension://')):
                    return True
        except:
            pass
        return False
        
    def _cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass
                
    def stop(self):
        """Stop analysis"""
        self.stop_flag = True
        
    def _log(self, message: str, level: str = "INFO"):
        """Log message via callback"""
        if self.callback:
            self.callback(f"[{level}] {message}")
            
    def _update_progress(self, value: int, message: str):
        """Update progress via callback"""
        if self.progress_callback:
            self.progress_callback(value, message)

# ============================================================================
# NETWORK MONITORING ENGINE WITH LIVE STATS
# ============================================================================

class NetworkMonitor:
    """Passive network traffic monitor for API key discovery with live stats"""
    
    def __init__(self, callback=None, stats_callback=None):
        self.callback = callback
        self.stats_callback = stats_callback
        self.is_monitoring = False
        self.sniffer_thread = None
        self.results = []
        self.stats = {
            'packets_captured': 0,
            'http_requests': 0,
            'https_connections': 0,
            'keys_found': 0
        }
        
    def start_monitoring(self, interface=None):
        """Start passive network monitoring"""
        if not SCAPY_AVAILABLE:
            self._log("ERROR: Scapy not installed. Install with: pip install scapy")
            return False
            
        self.is_monitoring = True
        self.interface = interface or conf.iface
        
        self._log(f"🚀 Starting network monitoring on {self.interface}")
        
        self.sniffer_thread = threading.Thread(target=self._sniff_packets)
        self.sniffer_thread.daemon = True
        self.sniffer_thread.start()
        return True
        
    def stop_monitoring(self):
        """Stop network monitoring"""
        self.is_monitoring = False
        self._log("⏹️ Network monitoring stopped")
        
    def _sniff_packets(self):
        """Sniff packets and analyze"""
        try:
            sniff(iface=self.interface, 
                  prn=self._process_packet,
                  store=False,
                  stop_filter=lambda x: not self.is_monitoring)
        except Exception as e:
            self._log(f"❌ Sniffing error: {str(e)}")
            
    def _process_packet(self, packet):
        """Process captured packet"""
        if not self.is_monitoring:
            return
            
        self.stats['packets_captured'] += 1
        
        # Update stats via callback
        if self.stats_callback:
            self.stats_callback(self.stats)
        
        try:
            if packet.haslayer(TCP) and packet.haslayer(Raw):
                ip_layer = packet.getlayer(IP)
                tcp_layer = packet.getlayer(TCP)
                
                if tcp_layer.sport == 80 or tcp_layer.dport == 80:
                    self._analyze_http_packet(packet)
                elif tcp_layer.sport == 443 or tcp_layer.dport == 443:
                    self.stats['https_connections'] += 1
                    
        except Exception:
            pass
            
    def _analyze_http_packet(self, packet):
        """Analyze HTTP packet for API keys"""
        self.stats['http_requests'] += 1
        
        try:
            raw_data = packet[Raw].load.decode('utf-8', errors='ignore')
            
            if '\r\n\r\n' in raw_data:
                headers_part, body_part = raw_data.split('\r\n\r\n', 1)
            else:
                headers_part = raw_data
                body_part = ''
                
            self._scan_for_keys(headers_part, "HTTP Headers", packet)
            self._scan_for_keys(body_part, "HTTP Body", packet)
            
            if 'Authorization:' in headers_part:
                auth_line = [l for l in headers_part.split('\n') if 'Authorization:' in l]
                if auth_line:
                    self._scan_for_keys(auth_line[0], "Authorization Header", packet)
                    
        except Exception:
            pass
            
    def _scan_for_keys(self, data, source, packet):
        """Scan data for API keys"""
        for key_type, config in API_PATTERNS.items():
            try:
                matches = re.finditer(config['pattern'], data, re.IGNORECASE)
                for match in matches:
                    key = match.group()
                    
                    if len(key) < 10 or key in ['example', 'test', 'xxxx']:
                        continue
                        
                    start = max(0, match.start() - 50)
                    end = min(len(data), match.end() + 50)
                    context = data[start:end].strip()
                    
                    packet_info = {
                        'timestamp': datetime.now().isoformat(),
                        'source_ip': packet[IP].src if packet.haslayer(IP) else 'Unknown',
                        'dest_ip': packet[IP].dst if packet.haslayer(IP) else 'Unknown',
                        'source_port': packet[TCP].sport if packet.haslayer(TCP) else 'Unknown',
                        'dest_port': packet[TCP].dport if packet.haslayer(TCP) else 'Unknown',
                        'protocol': 'TCP'
                    }
                    
                    result = {
                        'key': key,
                        'type': key_type,
                        'category': config['category'],
                        'risk': config['risk'],
                        'confidence': config['confidence'],
                        'source': source,
                        'source_type': SourceType.NETWORK.value,
                        'context': context,
                        'packet_info': packet_info,
                        'timestamp': datetime.now().isoformat(),
                        'hash': hashlib.md5(key.encode()).hexdigest()[:8]
                    }
                    
                    self.results.append(result)
                    self.stats['keys_found'] += 1
                    
                    if self.stats_callback:
                        self.stats_callback(self.stats)
                    
                    self._log(f"🔑 Network: Found {key_type} in {source}")
                    self._log(f"   From: {packet_info['source_ip']}:{packet_info['source_port']}")
                    
            except Exception:
                pass
                
    def _log(self, message):
        """Log message via callback"""
        if self.callback:
            self.callback(message)

# ============================================================================
# DEEP WEB CRAWLER WITH PROGRESS
# ============================================================================

class DeepWebCrawler:
    """Deep website crawler with JavaScript analysis and live progress"""
    
    def __init__(self, callback=None, progress_callback=None):
        self.callback = callback
        self.progress_callback = progress_callback
        self.visited_urls = set()
        self.js_files = set()
        self.results = []
        self.stop_flag = False
        
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            })
        
    def crawl(self, start_url, max_depth=3, max_pages=100):
        """Deep crawl website with live progress"""
        if not REQUESTS_AVAILABLE:
            self._log("ERROR: Requests library not installed")
            return []
            
        self.results = []
        self.visited_urls.clear()
        self.js_files.clear()
        self.stop_flag = False
        
        self._log(f"🚀 Starting deep crawl of {start_url}")
        self._update_progress(5, "Initializing crawler...")
        
        # Calculate total estimated work
        estimated_pages = min(max_pages, 50)  # Cap for demo
        self._update_progress(10, f"Planning to crawl up to {estimated_pages} pages...")
        
        # Start crawling
        pages_crawled = self._crawl_recursive(start_url, depth=0, max_depth=max_depth, max_pages=estimated_pages)
        
        # Update progress for JS scanning
        self._update_progress(60, f"Crawled {pages_crawled} pages, scanning JavaScript...")
        
        # Scan all discovered JS files
        if self.js_files:
            self._log(f"📜 Scanning {len(self.js_files)} JavaScript files...")
            js_count = len(self.js_files)
            for idx, js_url in enumerate(self.js_files):
                if self.stop_flag:
                    break
                self._scan_js_file(js_url)
                # Update progress based on JS files
                progress = 60 + int((idx + 1) / js_count * 30)
                self._update_progress(progress, f"Scanning JavaScript {idx+1}/{js_count}")
        
        self._update_progress(100, "Crawl complete!")
        self._log(f"✅ Deep crawl complete. Found {len(self.results)} keys")
        return self.results
        
    def stop(self):
        """Stop crawling"""
        self.stop_flag = True
        
    def _crawl_recursive(self, url, depth, max_depth, max_pages):
        """Recursive crawling with progress"""
        if depth > max_depth or len(self.visited_urls) >= max_pages or url in self.visited_urls or self.stop_flag:
            return len(self.visited_urls)
            
        self.visited_urls.add(url)
        
        # Calculate progress for crawling phase (10-60%)
        progress = 10 + int(len(self.visited_urls) / max_pages * 50)
        self._update_progress(progress, f"Crawling page {len(self.visited_urls)}/{max_pages} at depth {depth}")
        
        self._log(f"📡 Crawling [{depth}/{max_depth}]: {url}")
        
        try:
            response = self.session.get(url, timeout=10, verify=False)
            
            if response.status_code == 200:
                self._scan_content(response.text, url, "HTML")
                
                if BEAUTIFULSOUP_AVAILABLE:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for script in soup.find_all('script', src=True):
                        js_url = urljoin(url, script['src'])
                        if js_url not in self.js_files:
                            self.js_files.add(js_url)
                            
                    if depth < max_depth:
                        base_domain = urlparse(url).netloc
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            if href and not href.startswith('#') and not href.startswith('javascript:'):
                                full_url = urljoin(url, href)
                                if urlparse(full_url).netloc == base_domain:
                                    self._crawl_recursive(full_url, depth + 1, max_depth, max_pages)
                                
        except Exception as e:
            self._log(f"❌ Error crawling {url}: {str(e)[:50]}")
            
        return len(self.visited_urls)
            
    def _scan_js_file(self, js_url):
        """Scan JavaScript file for API keys"""
        try:
            response = self.session.get(js_url, timeout=10, verify=False)
            if response.status_code == 200:
                self._scan_content(response.text, js_url, "JavaScript")
        except Exception:
            pass
            
    def _scan_content(self, content, source, source_type):
        """Scan content for API keys"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for key_type, config in API_PATTERNS.items():
                try:
                    matches = re.finditer(config['pattern'], line)
                    for match in matches:
                        key = match.group()
                        
                        if len(key) < 10:
                            continue
                            
                        start = max(0, match.start() - 75)
                        end = min(len(line), match.end() + 75)
                        context = line[start:end].strip()
                        
                        confidence = config['confidence']
                        context_lower = context.lower()
                        keywords = ['api', 'key', 'token', 'secret', 'auth']
                        if any(kw in context_lower for kw in keywords):
                            confidence = min(1.0, confidence + 0.1)
                            
                        result = {
                            'key': key,
                            'type': key_type,
                            'category': config['category'],
                            'risk': config['risk'],
                            'confidence': confidence,
                            'source': source,
                            'source_type': source_type,
                            'line': i,
                            'context': context,
                            'timestamp': datetime.now().isoformat(),
                            'hash': hashlib.md5(key.encode()).hexdigest()[:8],
                            'cwe': config.get('cwe', 'CWE-200')
                        }
                        
                        self.results.append(result)
                        
                        self._log(f"🔑 Found {key_type} in {source_type}")
                        
                except Exception:
                    pass
                    
    def _log(self, message):
        """Log message via callback"""
        if self.callback:
            self.callback(message)
            
    def _update_progress(self, value, message):
        """Update progress via callback"""
        if self.progress_callback:
            self.progress_callback(value, message)

# ============================================================================
# WEB APPLICATION SCANNER WITH PROGRESS
# ============================================================================

class WebAppScanner:
    """Web application security scanner with live progress tracking"""
    
    def __init__(self, target_url, callback=None, progress_callback=None):
        self.target_url = target_url.rstrip('/')
        self.parsed_url = urlparse(self.target_url)
        self.base_domain = self.parsed_url.netloc
        self.callback = callback
        self.progress_callback = progress_callback
        self.stop_flag = False
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.results = {
            'target_info': {},
            'technologies': [],
            'crawled_urls': [],
            'discovered_paths': [],
            'vulnerabilities': [],
            'forms': [],
            'api_endpoints': [],
            'headers': {},
            'cookies': [],
            'sensitive_files': []
        }
        
        self.total_steps = 8  # Total number of major steps
        self.current_step = 0
        
    def log(self, message, level="INFO"):
        """Log message via callback"""
        if self.callback:
            self.callback(f"[{level}] {message}")
            
    def update_progress(self, value, message):
        """Update progress via callback"""
        if self.progress_callback:
            self.progress_callback(value, message)
            
    def stop(self):
        """Stop the scan"""
        self.stop_flag = True
        self.log("Scan stopped by user", "WARNING")
        
    def _step_progress(self, step_name, step_weight=12.5):
        """Update progress for a major step"""
        self.current_step += 1
        progress = int(self.current_step * step_weight)
        self.update_progress(progress, step_name)
        
    def validate_target(self):
        """Validate target URL and gather basic information"""
        self.log("Step 1: Validating target...")
        self._step_progress("Validating target...")
        
        try:
            response = self.session.get(self.target_url, timeout=10, verify=False)
            
            try:
                ip_address = socket.gethostbyname(self.base_domain)
            except:
                ip_address = "Could not resolve"
            
            server = response.headers.get('Server', 'Unknown')
            
            self.results['target_info'] = {
                'url': self.target_url,
                'domain': self.base_domain,
                'ip_address': ip_address,
                'server': server,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            self.log(f"✓ Target validated: {self.target_url}")
            self.log(f"  IP: {ip_address}")
            self.log(f"  Server: {server}")
            self.log(f"  Status: {response.status_code}")
            
            return True
            
        except requests.exceptions.ConnectionError:
            self.log("✗ Target unreachable - Connection failed", "ERROR")
            return False
        except Exception as e:
            self.log(f"✗ Target validation failed: {str(e)}", "ERROR")
            return False
            
    def fingerprint_technologies(self):
        """Perform technology fingerprinting"""
        self.log("\nStep 2: Technology Fingerprinting...")
        self._step_progress("Fingerprinting technologies...")
        
        try:
            response = self.session.get(self.target_url, timeout=10, verify=False)
            content = response.text
            
            self._analyze_headers(response.headers)
            self._analyze_cookies(response.cookies)
            self._detect_frameworks(content)
            self._detect_analytics(content)
            
            self.log(f"✓ Found {len(self.results['technologies'])} technologies:")
            for tech in self.results['technologies'][:10]:
                self.log(f"  • {tech.get('name')} ({tech.get('category')})")
                
        except Exception as e:
            self.log(f"✗ Technology fingerprinting failed: {str(e)}", "ERROR")
            
    def _analyze_headers(self, headers):
        """Analyze HTTP headers for security information"""
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Content-Type-Options': 'X-Content-Type-Options',
            'X-Frame-Options': 'X-Frame-Options',
            'X-XSS-Protection': 'X-XSS-Protection',
            'Referrer-Policy': 'Referrer-Policy',
        }
        
        present_headers = []
        missing_headers = []
        
        for header, name in security_headers.items():
            if header in headers:
                present_headers.append(name)
            else:
                missing_headers.append(name)
                
        self.results['headers'] = {
            'present': present_headers,
            'missing': missing_headers,
            'all': dict(headers)
        }
        
        # Check for missing security headers
        for header, name in security_headers.items():
            if header not in headers:
                self._add_vulnerability(
                    name=f"Missing Security Header: {header}",
                    severity=Severity.MEDIUM,
                    url=self.target_url,
                    description=f"Missing {name} security header",
                    impact="Could expose users to various attacks",
                    remediation=f"Add {header} header"
                )
        
    def _analyze_cookies(self, cookies):
        """Analyze cookies for security attributes"""
        cookie_list = []
        
        for cookie in cookies:
            cookie_info = {
                'name': cookie.name,
                'value': cookie.value[:20] + '...' if len(cookie.value) > 20 else cookie.value,
                'secure': cookie.secure if hasattr(cookie, 'secure') else False,
                'httponly': cookie.has_nonstandard_attr('HttpOnly') if hasattr(cookie, 'has_nonstandard_attr') else False,
                'samesite': cookie.get_nonstandard_attr('SameSite', 'Not Set') if hasattr(cookie, 'get_nonstandard_attr') else 'Not Set'
            }
            cookie_list.append(cookie_info)
            
            if hasattr(cookie, 'secure') and not cookie.secure:
                self._add_vulnerability(
                    name="Insecure Cookie",
                    severity=Severity.MEDIUM,
                    url=self.target_url,
                    description=f"Cookie '{cookie.name}' missing Secure flag",
                    impact="Cookie may be transmitted over unencrypted connections",
                    remediation="Set Secure flag for all cookies"
                )
            
        self.results['cookies'] = cookie_list
        
    def _detect_frameworks(self, content):
        """Detect JavaScript frameworks"""
        frameworks = {
            'React': ['react', 'ReactDOM', 'create-react-app'],
            'Angular': ['ng-', 'angular', 'ngVersion'],
            'Vue.js': ['vue', 'Vue.', 'v-bind', 'v-model'],
            'jQuery': ['jquery', 'jQuery', '$('],
            'Bootstrap': ['bootstrap', 'col-md-', 'container-fluid'],
            'Tailwind': ['tailwind', 'w-', 'h-', 'bg-', 'text-'],
            'Laravel': ['laravel', 'csrf-token', 'Laravel'],
            'Django': ['csrfmiddlewaretoken', 'django'],
        }
        
        content_lower = content.lower()
        
        for framework, signatures in frameworks.items():
            for signature in signatures:
                if signature.lower() in content_lower:
                    self.results['technologies'].append({
                        'name': framework,
                        'category': 'Framework',
                        'signature': signature
                    })
                    break
                    
    def _detect_analytics(self, content):
        """Detect analytics and tracking services"""
        analytics = {
            'Google Analytics': ['google-analytics', 'ga(', 'gtag('],
            'Google Tag Manager': ['googletagmanager'],
            'Facebook Pixel': ['facebook.com/tr', 'fbq('],
            'Hotjar': ['hotjar'],
        }
        
        content_lower = content.lower()
        
        for service, signatures in analytics.items():
            for signature in signatures:
                if signature in content_lower:
                    self.results['technologies'].append({
                        'name': service,
                        'category': 'Analytics'
                    })
                    break
                    
    def crawl_website(self, max_pages=50):
        """Crawl website to discover pages"""
        self.log("\nStep 3: Crawling website...")
        self._step_progress("Crawling website...")
        
        visited = set()
        to_visit = [self.target_url]
        forms_found = []
        apis_found = []
        
        page_count = 0
        while to_visit and len(visited) < max_pages and not self.stop_flag:
            url = to_visit.pop(0)
            if url in visited:
                continue
                
            try:
                self.log(f"  Crawling: {url}")
                response = self.session.get(url, timeout=10, verify=False)
                visited.add(url)
                page_count += 1
                
                # Update progress during crawl (25-40%)
                crawl_progress = 25 + int(page_count / max_pages * 15)
                self.update_progress(crawl_progress, f"Crawling page {page_count}/{max_pages}")
                
                if BEAUTIFULSOUP_AVAILABLE and 'text/html' in response.headers.get('Content-Type', ''):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href and not href.startswith('#') and not href.startswith('javascript:'):
                            full_url = urljoin(url, href)
                            if urlparse(full_url).netloc == self.base_domain:
                                if full_url not in visited and full_url not in to_visit:
                                    to_visit.append(full_url)
                                    
                    forms = soup.find_all('form')
                    for form in forms:
                        form_info = self._extract_form_info(form, url)
                        forms_found.append(form_info)
                        
                    scripts = soup.find_all('script', src=True)
                    for script in scripts:
                        src = script['src']
                        if src and ('api' in src.lower() or 'rest' in src.lower()):
                            api_url = urljoin(url, src)
                            apis_found.append(api_url)
                            
            except Exception as e:
                self.log(f"  Error crawling {url}: {str(e)[:50]}", "WARNING")
                
        self.results['crawled_urls'] = list(visited)
        self.results['forms'] = forms_found
        self.results['api_endpoints'] = apis_found
        
        self.log(f"✓ Crawled {len(visited)} pages")
        self.log(f"✓ Found {len(forms_found)} forms")
        self.log(f"✓ Found {len(apis_found)} API endpoints")
        
    def _extract_form_info(self, form, page_url):
        """Extract information from HTML form"""
        form_info = {
            'page': page_url,
            'action': form.get('action', ''),
            'method': form.get('method', 'get').upper(),
            'inputs': []
        }
        
        if form_info['action']:
            form_info['action_url'] = urljoin(page_url, form_info['action'])
        else:
            form_info['action_url'] = page_url
            
        for input_tag in form.find_all(['input', 'textarea', 'select']):
            input_info = {
                'type': input_tag.get('type', 'text'),
                'name': input_tag.get('name', ''),
                'value': input_tag.get('value', '')
            }
            if input_info['name']:
                form_info['inputs'].append(input_info)
                
        return form_info
        
    def discover_paths(self):
        """Discover hidden directories and endpoints"""
        self.log("\nStep 4: Discovering hidden paths...")
        self._step_progress("Discovering paths...")
        
        discovered = []
        sensitive_found = []
        
        total_paths = len(COMMON_PATHS)
        for i, path in enumerate(COMMON_PATHS):
            if self.stop_flag:
                break
                
            url = f"{self.target_url}/{path}"
            try:
                response = self.session.get(url, timeout=3, verify=False, allow_redirects=False)
                
                if response.status_code in [200, 401, 403, 500]:
                    discovered.append({
                        'url': url,
                        'status': response.status_code,
                        'size': len(response.content)
                    })
                    self.log(f"  Found: {url} ({response.status_code})")
                    
            except:
                pass
                
            # Update progress during path discovery (40-45%)
            if i % 10 == 0:
                progress = 40 + int(i / total_paths * 5)
                self.update_progress(progress, f"Discovering paths... ({i}/{total_paths})")
                
        self.log("\n  Checking for sensitive files...")
        total_files = len(SENSITIVE_FILES)
        for i, file in enumerate(SENSITIVE_FILES):
            if self.stop_flag:
                break
                
            url = f"{self.target_url}/{file}"
            try:
                response = self.session.get(url, timeout=3, verify=False)
                
                if response.status_code == 200:
                    sensitive_found.append({
                        'url': url,
                        'file': file,
                        'size': len(response.content)
                    })
                    self.log(f"  ⚠ Sensitive file found: {url}")
                    
                    self._add_vulnerability(
                        name="Sensitive File Exposure",
                        severity=Severity.HIGH,
                        url=url,
                        description=f"Sensitive file exposed: {file}",
                        impact="Attackers can access sensitive information",
                        remediation="Remove or restrict access to sensitive files"
                    )
                    
            except:
                pass
                
            # Update progress during file checking (45-50%)
            if i % 5 == 0:
                progress = 45 + int(i / total_files * 5)
                self.update_progress(progress, f"Checking sensitive files... ({i}/{total_files})")
                
        self.results['discovered_paths'] = discovered
        self.results['sensitive_files'] = sensitive_found
        
        self.log(f"✓ Discovered {len(discovered)} paths")
        self.log(f"✓ Found {len(sensitive_found)} sensitive files")
        
    def check_misconfigurations(self):
        """Check for security misconfigurations"""
        self.log("\nStep 5: Checking security misconfigurations...")
        self._step_progress("Checking misconfigurations...")
        
        try:
            response = self.session.get(self.target_url, timeout=10, verify=False)
            
            self._check_directory_listing()
            self._check_information_disclosure(response.text)
            self._check_debug_modes(response.text)
            
        except Exception as e:
            self.log(f"✗ Misconfiguration check failed: {str(e)}", "ERROR")
            
        self.update_progress(55, "Misconfiguration checks complete")
            
    def _check_directory_listing(self):
        """Check for directory listing vulnerabilities"""
        test_dirs = ['/images/', '/css/', '/js/', '/uploads/', '/assets/']
        
        for dir_path in test_dirs:
            url = f"{self.target_url}{dir_path}"
            try:
                response = self.session.get(url, timeout=3, verify=False)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'index of' in content or 'parent directory' in content:
                        self._add_vulnerability(
                            name="Directory Listing Enabled",
                            severity=Severity.MEDIUM,
                            url=url,
                            description="Directory listing is enabled",
                            impact="Attackers can browse directory contents",
                            remediation="Disable directory listing in web server configuration"
                        )
                        
            except:
                pass
                
    def _check_information_disclosure(self, content):
        """Check for information disclosure"""
        patterns = {
            r'email["\']?\s*:\s*["\']([^"\']+@[^"\']+)': 'Email addresses',
            r'password["\']?\s*:\s*["\']([^"\']+)': 'Passwords',
            r'api[_-]?key["\']?\s*:\s*["\']([^"\']+)': 'API keys',
            r'token["\']?\s*:\s*["\']([^"\']+)': 'Tokens',
            r'SQL syntax.*MySQL': 'SQL errors',
            r'Fatal error': 'PHP errors',
            r'stack trace': 'Stack traces',
        }
        
        for pattern, desc in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                self._add_vulnerability(
                    name="Information Disclosure",
                    severity=Severity.HIGH,
                    url=self.target_url,
                    description=f"Sensitive information disclosed: {desc}",
                    impact="Exposed sensitive data could aid attackers",
                    remediation="Remove sensitive data from client-side code"
                )
                
    def _check_debug_modes(self, content):
        """Check for debug mode indicators"""
        debug_indicators = [
            'debug mode', 'development mode', 'debug=True',
            'enable_debug', 'APP_DEBUG', 'WP_DEBUG',
            'laravel-debugbar', 'werkzeug', 'django debug'
        ]
        
        content_lower = content.lower()
        for indicator in debug_indicators:
            if indicator in content_lower:
                self._add_vulnerability(
                    name="Debug Mode Enabled",
                    severity=Severity.HIGH,
                    url=self.target_url,
                    description=f"Debug mode enabled: {indicator}",
                    impact="Debug information can reveal sensitive details",
                    remediation="Disable debug mode in production"
                )
                break
                
    def test_sql_injection(self):
        """Test for SQL injection vulnerabilities"""
        self.log("\nStep 6.1: Testing for SQL Injection...")
        self.update_progress(60, "Testing SQL injection...")
        
        test_urls = self.results['crawled_urls'][:10]
        total_tests = len(test_urls)
        
        for idx, url in enumerate(test_urls):
            if self.stop_flag:
                break
                
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            if params:
                for param, values in params.items():
                    original_value = values[0]
                    
                    for payload in SQL_PAYLOADS[:3]:
                        test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                        
                        try:
                            response = self.session.get(test_url, timeout=3, verify=False)
                            content = response.text.lower()
                            
                            error_patterns = [
                                'sql syntax', 'mysql_fetch', 'ora-', 'postgresql error',
                                'unclosed quotation mark', 'you have an error in your sql',
                            ]
                            
                            for pattern in error_patterns:
                                if pattern in content:
                                    self._add_vulnerability(
                                        name="SQL Injection",
                                        severity=Severity.CRITICAL,
                                        url=test_url,
                                        description=f"Potential SQL injection in parameter '{param}'",
                                        poc=f"Payload: {payload}",
                                        impact="Attackers can read/modify database data",
                                        remediation="Use parameterized queries/prepared statements"
                                    )
                                    break
                                    
                        except:
                            pass
                            
            # Update progress
            progress = 60 + int((idx + 1) / total_tests * 5)
            self.update_progress(progress, f"SQL injection tests ({idx+1}/{total_tests})")
                            
    def test_xss(self):
        """Test for Cross-Site Scripting (XSS) vulnerabilities"""
        self.log("\nStep 6.2: Testing for XSS...")
        self.update_progress(65, "Testing XSS...")
        
        test_forms = self.results['forms'][:5]
        total_forms = len(test_forms)
        
        for idx, form in enumerate(test_forms):
            if self.stop_flag:
                break
                
            for payload in XSS_PAYLOADS[:2]:
                form_data = {}
                for input_field in form['inputs']:
                    if input_field['type'] in ['text', 'search', 'textarea']:
                        form_data[input_field['name']] = payload
                    else:
                        form_data[input_field['name']] = input_field['value']
                        
                try:
                    if form['method'] == 'GET':
                        response = self.session.get(form['action_url'], params=form_data, timeout=3)
                    else:
                        response = self.session.post(form['action_url'], data=form_data, timeout=3)
                        
                    if payload in response.text and len(payload) > 10:
                        self._add_vulnerability(
                            name="Cross-Site Scripting (XSS)",
                            severity=Severity.HIGH,
                            url=form['action_url'],
                            description="Reflected XSS vulnerability detected",
                            poc=f"Payload: {payload}",
                            impact="Attackers can execute JavaScript in victims' browsers",
                            remediation="Implement proper output encoding and input validation"
                        )
                        break
                        
                except:
                    pass
                    
            # Update progress
            progress = 65 + int((idx + 1) / total_forms * 5)
            self.update_progress(progress, f"XSS tests ({idx+1}/{total_forms})")
                    
    def test_csrf(self):
        """Test for Cross-Site Request Forgery (CSRF)"""
        self.log("\nStep 6.3: Testing for CSRF...")
        self.update_progress(70, "Testing CSRF...")
        
        for idx, form in enumerate(self.results['forms']):
            if form['method'] == 'POST':
                has_csrf = False
                
                csrf_indicators = ['csrf', 'token', 'authenticity_token', '_token']
                
                for input_field in form['inputs']:
                    input_name = input_field['name'].lower()
                    if any(indicator in input_name for indicator in csrf_indicators):
                        has_csrf = True
                        break
                        
                if not has_csrf:
                    self._add_vulnerability(
                        name="Missing CSRF Protection",
                        severity=Severity.MEDIUM,
                        url=form['action_url'],
                        description="Form lacks CSRF protection tokens",
                        impact="Attackers can trick users into submitting unwanted requests",
                        remediation="Implement CSRF tokens for all state-changing operations"
                    )
                    
        self.update_progress(75, "CSRF tests complete")
                    
    def test_path_traversal(self):
        """Test for path traversal vulnerabilities"""
        self.log("\nStep 6.4: Testing for Path Traversal...")
        self.update_progress(75, "Testing path traversal...")
        
        traversal_params = ['file', 'document', 'folder', 'path', 'page', 'include']
        test_urls = self.results['crawled_urls'][:10]
        total_tests = len(test_urls)
        
        for idx, url in enumerate(test_urls):
            if self.stop_flag:
                break
                
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param in params:
                if param.lower() in traversal_params:
                    for payload in PATH_TRAVERSAL[:2]:
                        test_url = url.replace(f"{param}={params[param][0]}", f"{param}={payload}")
                        
                        try:
                            response = self.session.get(test_url, timeout=3, verify=False)
                            
                            if 'root:' in response.text or '[extensions]' in response.text:
                                self._add_vulnerability(
                                    name="Path Traversal",
                                    severity=Severity.CRITICAL,
                                    url=test_url,
                                    description=f"Path traversal in parameter '{param}'",
                                    poc=f"Payload: {payload}",
                                    impact="Attackers can read arbitrary files",
                                    remediation="Validate and sanitize file paths"
                                )
                                break
                                
                        except:
                            pass
                            
            # Update progress
            progress = 75 + int((idx + 1) / total_tests * 5)
            self.update_progress(progress, f"Path traversal tests ({idx+1}/{total_tests})")
                            
    def _add_vulnerability(self, name, severity, url, description, poc=None, 
                          impact=None, remediation=None):
        """Add vulnerability to results"""
        vuln = {
            'name': name,
            'severity': severity.value if isinstance(severity, Severity) else severity,
            'url': url,
            'description': description,
            'poc': poc,
            'impact': impact,
            'remediation': remediation,
            'timestamp': datetime.now().isoformat(),
            'source_type': SourceType.WEB_APP.value
        }
        
        self.results['vulnerabilities'].append(vuln)
        
        severity_colors = {
            'CRITICAL': "🔴",
            'HIGH': "🟠",
            'MEDIUM': "🟡",
            'LOW': "🟢",
            'INFO': "🔵"
        }
        
        self.log(f"  {severity_colors.get(vuln['severity'], '⚪')} Found: {name} [{vuln['severity']}]")
        
    def run_full_scan(self):
        """Run complete security scan with live progress"""
        start_time = time.time()
        
        if not self.validate_target():
            return self.results
            
        self.fingerprint_technologies()
        self.crawl_website()
        self.discover_paths()
        self.check_misconfigurations()
        self.test_sql_injection()
        self.test_xss()
        self.test_csrf()
        self.test_path_traversal()
        
        self.results['scan_time'] = time.time() - start_time
        self.update_progress(100, "Scan complete!")
        
        return self.results

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class UnifiedSecurityTool:
    """Main unified application combining all security tools with live progress"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Security Analysis Tool - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg=Colors.BG_PRIMARY)
        
        # Initialize progress manager
        self.progress_manager = None
        
        # Initialize components
        self.network_monitor = NetworkMonitor(
            callback=self.log_message,
            stats_callback=self.update_network_stats
        )
        self.deep_crawler = None
        self.extension_analyzer = None
        self.web_scanner = None
        
        # Threading
        self.scan_thread = None
        self.monitor_thread = None
        self.is_scanning = False
        
        # Data storage
        self.network_results = []
        self.crawl_results = []
        self.extension_results = None
        self.web_results = None
        
        # Queue for thread-safe GUI updates
        self.queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        self.center_window()
        
        # Check dependencies
        self.check_dependencies()
        
        # Start queue processor
        self.process_queue()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def check_dependencies(self):
        """Check and report missing dependencies"""
        deps_status = []
        
        if not SCAPY_AVAILABLE:
            deps_status.append("⚠️ Scapy missing - Network monitoring disabled")
        if not BEAUTIFULSOUP_AVAILABLE:
            deps_status.append("⚠️ BeautifulSoup4 missing - HTML parsing limited")
        if not REQUESTS_AVAILABLE:
            deps_status.append("⚠️ Requests missing - Scanning disabled")
        if not CRYPTO_AVAILABLE:
            deps_status.append("⚠️ Cryptography missing - Some decryption disabled")
        if not DNS_AVAILABLE:
            deps_status.append("⚠️ DNS python missing - DNS lookups disabled")
            
        if deps_status:
            self.log_message("📦 Dependency Status:")
            for status in deps_status:
                self.log_message(f"  {status}")
            self.log_message("  Run: pip install requests beautifulsoup4 scapy cryptography dnspython")
            
    def setup_ui(self):
        """Setup the user interface with live progress indicators"""
        
        # ==================== HEADER ====================
        header = tk.Frame(self.root, bg=Colors.BG_SECONDARY, height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=Colors.BG_SECONDARY)
        title_frame.pack(side='left', padx=20, pady=15)
        
        tk.Label(title_frame, text="🔐 UNIFIED SECURITY ANALYZER",
                font=('Segoe UI', 20, 'bold'),
                bg=Colors.BG_SECONDARY, fg=Colors.ACCENT_BLUE).pack(anchor='w')
        
        tk.Label(title_frame, text="Professional Edition - Live Progress Tracking",
                font=('Segoe UI', 11),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(anchor='w')
        
        # Status indicator
        self.status_indicator = tk.Canvas(header, width=20, height=20, bg=Colors.BG_SECONDARY, highlightthickness=0)
        self.status_indicator.pack(side='right', padx=20, pady=30)
        self.status_indicator.create_oval(5, 5, 15, 15, fill=Colors.ACCENT_GREEN, outline='')
        
        # ==================== GLOBAL PROGRESS BAR ====================
        progress_container = tk.Frame(self.root, bg=Colors.BG_PRIMARY)
        progress_container.pack(fill='x', padx=20, pady=(10, 0))
        
        # Main progress bar
        self.progress_bar = ttk.Progressbar(progress_container, length=400, mode='determinate')
        self.progress_bar.pack(side='left', fill='x', expand=True)
        
        # Percentage label
        self.percentage_label = tk.Label(progress_container, text="0%", 
                                         bg=Colors.BG_PRIMARY, fg=Colors.ACCENT_CYAN,
                                         font=('Segoe UI', 10, 'bold'), width=5)
        self.percentage_label.pack(side='left', padx=(10, 0))
        
        # Status label
        self.progress_label = tk.Label(self.root, text="Ready",
                                       bg=Colors.BG_PRIMARY, fg=Colors.FG_SECONDARY,
                                       font=('Segoe UI', 10))
        self.progress_label.pack(anchor='w', padx=20, pady=(0, 10))
        
        # Initialize progress manager
        self.progress_manager = ProgressManager(self.root, self.progress_bar, 
                                               self.progress_label, self.percentage_label)
        
        # ==================== MAIN NOTEBOOK ====================
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Style notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=Colors.BG_PRIMARY)
        style.configure('TNotebook.Tab', 
                       background=Colors.BG_SECONDARY,
                       foreground=Colors.FG_PRIMARY,
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', Colors.BG_TERTIARY)],
                 foreground=[('selected', Colors.ACCENT_CYAN)])
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_web_scanner_tab()
        self.create_extension_tab()
        self.create_network_tab()
        self.create_crawler_tab()
        self.create_remediation_tab()
        self.create_logs_tab()
        
    def create_dashboard_tab(self):
        """Create dashboard tab with summary"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='📊 DASHBOARD')
        
        # Welcome message
        welcome_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        welcome_frame.pack(fill='x', padx=20, pady=20)
        
        welcome_text = tk.Text(welcome_frame, height=5, bg=Colors.BG_SECONDARY,
                               fg=Colors.ACCENT_CYAN, font=('Segoe UI', 12),
                               wrap='word', bd=0, highlightthickness=0)
        welcome_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        welcome_msg = """Welcome to Unified Security Analyzer Professional Edition

This tool combines multiple security analysis capabilities with LIVE PROGRESS TRACKING:
• Web Application Scanning (OWASP Top 10)
• Chrome Extension Security Analysis
• Network Traffic Monitoring
• Deep Web Crawling

Select a tab above to begin your security assessment. All scans show real-time progress!"""
        
        welcome_text.insert('1.0', welcome_msg)
        welcome_text.config(state='disabled')
        
        # Quick actions
        actions_frame = tk.LabelFrame(frame, text="Quick Actions",
                                      bg=Colors.BG_SECONDARY, fg=Colors.ACCENT_CYAN,
                                      font=('Segoe UI', 12, 'bold'))
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        button_frame = tk.Frame(actions_frame, bg=Colors.BG_SECONDARY)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🌐 Scan Website",
                 bg=Colors.ACCENT_BLUE, fg='white',
                 font=('Segoe UI', 11),
                 padx=20, pady=10,
                 command=lambda: self.notebook.select(1)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🧩 Analyze Extension",
                 bg=Colors.ACCENT_ORANGE, fg='white',
                 font=('Segoe UI', 11),
                 padx=20, pady=10,
                 command=lambda: self.notebook.select(2)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🌐 Monitor Network",
                 bg=Colors.ACCENT_PURPLE, fg='white',
                 font=('Segoe UI', 11),
                 padx=20, pady=10,
                 command=lambda: self.notebook.select(3)).pack(side='left', padx=5)
        
        # Stats cards
        stats_frame = tk.Frame(frame, bg=Colors.BG_TERTIARY)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self.stats_labels = {}
        stats = [
            ('Web Vulns', '0', Colors.ACCENT_RED),
            ('Extension Vulns', '0', Colors.ACCENT_ORANGE),
            ('API Keys', '0', Colors.ACCENT_GREEN),
            ('Pages', '0', Colors.ACCENT_BLUE),
        ]
        
        for title, value, color in stats:
            card = tk.Frame(stats_frame, bg=Colors.BG_SECONDARY, relief='flat', bd=1)
            card.pack(side='left', padx=5, fill='both', expand=True)
            
            tk.Label(card, text=title,
                    font=('Segoe UI', 11),
                    bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(pady=(10, 0))
            
            label = tk.Label(card, text=value,
                            font=('Segoe UI', 24, 'bold'),
                            bg=Colors.BG_SECONDARY, fg=color)
            label.pack(pady=(0, 10))
            
            self.stats_labels[title.lower().replace(' ', '_')] = label
            
    def create_web_scanner_tab(self):
        """Create web application scanner tab with live progress"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='🌐 WEB SCANNER')
        
        # Control panel
        control_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        control_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(control_frame, text="Target URL:",
                font=('Segoe UI', 11, 'bold'),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=10)
        
        self.web_url_var = tk.StringVar(value="https://example.com")
        url_entry = tk.Entry(control_frame, textvariable=self.web_url_var,
                            font=('Segoe UI', 11), width=50,
                            bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY,
                            insertbackground=Colors.ACCENT_BLUE)
        url_entry.pack(side='left', padx=10, fill='x', expand=True)
        
        # Scan button with progress
        self.web_scan_btn = tk.Button(control_frame, text="▶ START SCAN",
                                      bg=Colors.ACCENT_GREEN, fg='white',
                                      font=('Segoe UI', 11, 'bold'),
                                      padx=20, command=self.start_web_scan)
        self.web_scan_btn.pack(side='right', padx=10)
        
        # Local progress for this tab
        self.web_progress_var = tk.IntVar(value=0)
        self.web_progress = ttk.Progressbar(control_frame, variable=self.web_progress_var,
                                            length=200, mode='determinate')
        self.web_progress.pack(side='right', padx=10)
        
        # Results area
        results_frame = tk.Frame(frame, bg=Colors.BG_TERTIARY)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create sub-notebook for results
        web_notebook = ttk.Notebook(results_frame)
        web_notebook.pack(fill='both', expand=True)
        
        # Vulnerabilities tab
        vuln_frame = tk.Frame(web_notebook, bg=Colors.BG_TERTIARY)
        web_notebook.add(vuln_frame, text='Vulnerabilities')
        
        columns = ('Severity', 'Name', 'URL', 'Description')
        self.web_vuln_tree = ttk.Treeview(vuln_frame, columns=columns, show='headings', height=15)
        self.web_vuln_tree.heading('Severity', text='Severity')
        self.web_vuln_tree.heading('Name', text='Vulnerability')
        self.web_vuln_tree.heading('URL', text='URL')
        self.web_vuln_tree.heading('Description', text='Description')
        
        self.web_vuln_tree.column('Severity', width=100)
        self.web_vuln_tree.column('Name', width=200)
        self.web_vuln_tree.column('URL', width=300)
        self.web_vuln_tree.column('Description', width=400)
        
        self.web_vuln_tree.tag_configure('CRITICAL', background='#5a1e1e')
        self.web_vuln_tree.tag_configure('HIGH', background='#5a3e1e')
        self.web_vuln_tree.tag_configure('MEDIUM', background='#5a5a1e')
        self.web_vuln_tree.tag_configure('LOW', background='#1e5a1e')
        
        self._add_tree_scrollbars(vuln_frame, self.web_vuln_tree)
        
        # Bind double-click to show details
        self.web_vuln_tree.bind('<Double-Button-1>', self.show_web_vuln_details)
        
        # Discovered paths tab
        paths_frame = tk.Frame(web_notebook, bg=Colors.BG_TERTIARY)
        web_notebook.add(paths_frame, text='Discovered Paths')
        
        self.web_paths_list = tk.Listbox(paths_frame, bg=Colors.BG_SECONDARY,
                                         fg=Colors.FG_PRIMARY, font=('Consolas', 10))
        self.web_paths_list.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Technologies tab
        tech_frame = tk.Frame(web_notebook, bg=Colors.BG_TERTIARY)
        web_notebook.add(tech_frame, text='Technologies')
        
        columns = ('Name', 'Category', 'Version')
        self.web_tech_tree = ttk.Treeview(tech_frame, columns=columns, show='headings', height=15)
        self.web_tech_tree.heading('Name', text='Technology')
        self.web_tech_tree.heading('Category', text='Category')
        self.web_tech_tree.heading('Version', text='Version')
        
        self.web_tech_tree.column('Name', width=200)
        self.web_tech_tree.column('Category', width=150)
        self.web_tech_tree.column('Version', width=150)
        
        self._add_tree_scrollbars(tech_frame, self.web_tech_tree)
        
    def create_extension_tab(self):
        """Create Chrome extension analyzer tab with progress"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='🧩 EXTENSION ANALYZER')
        
        # Control panel
        control_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        control_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(control_frame, text="Extension ID/URL:",
                font=('Segoe UI', 11, 'bold'),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=10)
        
        self.ext_input_var = tk.StringVar()
        ext_entry = tk.Entry(control_frame, textvariable=self.ext_input_var,
                            font=('Segoe UI', 11), width=50,
                            bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY,
                            insertbackground=Colors.ACCENT_BLUE)
        ext_entry.pack(side='left', padx=10, fill='x', expand=True)
        
        # Quick examples
        examples_frame = tk.Frame(control_frame, bg=Colors.BG_SECONDARY)
        examples_frame.pack(side='bottom', pady=5)
        
        tk.Label(examples_frame, text="Popular:",
                bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(side='left')
        
        examples = [
            ("uBlock", "gighmmpiobklfepjocnamgkkbiglidom"),
            ("LastPass", "hdokiejnpimakedhajhdlcegeplioahd"),
            ("Grammarly", "kbfnbcaeplbcioakkpcpgfkobkghlhen"),
        ]
        
        for name, ext_id in examples:
            tk.Button(examples_frame, text=name,
                     bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY,
                     command=lambda eid=ext_id: self.ext_input_var.set(eid)).pack(side='left', padx=2)
        
        # Analyze button
        self.ext_scan_btn = tk.Button(control_frame, text="🔍 ANALYZE",
                                      bg=Colors.ACCENT_ORANGE, fg='white',
                                      font=('Segoe UI', 11, 'bold'),
                                      padx=20, command=self.analyze_extension)
        self.ext_scan_btn.pack(side='right', padx=10)
        
        # Local progress
        self.ext_progress_var = tk.IntVar(value=0)
        self.ext_progress = ttk.Progressbar(control_frame, variable=self.ext_progress_var,
                                            length=200, mode='determinate')
        self.ext_progress.pack(side='right', padx=10)
        
        # Results area
        results_frame = tk.Frame(frame, bg=Colors.BG_TERTIARY)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ext_notebook = ttk.Notebook(results_frame)
        ext_notebook.pack(fill='both', expand=True)
        
        # Metadata tab
        meta_frame = tk.Frame(ext_notebook, bg=Colors.BG_TERTIARY)
        ext_notebook.add(meta_frame, text='Metadata')
        
        self.metadata_text = scrolledtext.ScrolledText(meta_frame,
                                                       bg=Colors.BG_SECONDARY,
                                                       fg=Colors.FG_PRIMARY,
                                                       font=('Consolas', 10),
                                                       height=15)
        self.metadata_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Vulnerabilities tab
        vuln_frame = tk.Frame(ext_notebook, bg=Colors.BG_TERTIARY)
        ext_notebook.add(vuln_frame, text='Vulnerabilities')
        
        columns = ('Severity', 'Type', 'File', 'Line', 'Description')
        self.ext_vuln_tree = ttk.Treeview(vuln_frame, columns=columns, show='headings', height=15)
        self.ext_vuln_tree.heading('Severity', text='Severity')
        self.ext_vuln_tree.heading('Type', text='Type')
        self.ext_vuln_tree.heading('File', text='File')
        self.ext_vuln_tree.heading('Line', text='Line')
        self.ext_vuln_tree.heading('Description', text='Description')
        
        self.ext_vuln_tree.column('Severity', width=100)
        self.ext_vuln_tree.column('Type', width=150)
        self.ext_vuln_tree.column('File', width=250)
        self.ext_vuln_tree.column('Line', width=60)
        self.ext_vuln_tree.column('Description', width=300)
        
        self.ext_vuln_tree.tag_configure('CRITICAL', background='#5a1e1e')
        self.ext_vuln_tree.tag_configure('HIGH', background='#5a3e1e')
        self.ext_vuln_tree.tag_configure('MEDIUM', background='#5a5a1e')
        
        self._add_tree_scrollbars(vuln_frame, self.ext_vuln_tree)
        self.ext_vuln_tree.bind('<Double-Button-1>', self.show_ext_vuln_details)
        
        # Permissions tab
        perm_frame = tk.Frame(ext_notebook, bg=Colors.BG_TERTIARY)
        ext_notebook.add(perm_frame, text='Permissions')
        
        self.perm_listbox = tk.Listbox(perm_frame, bg=Colors.BG_SECONDARY,
                                       fg=Colors.FG_PRIMARY, font=('Consolas', 10))
        self.perm_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # APIs tab
        api_frame = tk.Frame(ext_notebook, bg=Colors.BG_TERTIARY)
        ext_notebook.add(api_frame, text='APIs')
        
        columns = ('URL', 'Method', 'File', 'Line')
        self.ext_api_tree = ttk.Treeview(api_frame, columns=columns, show='headings', height=15)
        self.ext_api_tree.heading('URL', text='URL')
        self.ext_api_tree.heading('Method', text='Method')
        self.ext_api_tree.heading('File', text='File')
        self.ext_api_tree.heading('Line', text='Line')
        
        self.ext_api_tree.column('URL', width=400)
        self.ext_api_tree.column('Method', width=80)
        self.ext_api_tree.column('File', width=250)
        self.ext_api_tree.column('Line', width=60)
        
        self._add_tree_scrollbars(api_frame, self.ext_api_tree)
        
    def create_network_tab(self):
        """Create network monitoring tab with live stats"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='🌐 NETWORK MONITOR')
        
        # Control panel
        control_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        control_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(control_frame, text="Interface:",
                font=('Segoe UI', 11, 'bold'),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=10)
        
        self.interface_var = tk.StringVar(value="eth0")
        iface_entry = tk.Entry(control_frame, textvariable=self.interface_var,
                              font=('Segoe UI', 11), width=20,
                              bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY)
        iface_entry.pack(side='left', padx=10)
        
        tk.Label(control_frame, text="(use 'Wi-Fi' on Windows)",
                font=('Segoe UI', 9),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(side='left')
        
        self.network_btn = tk.Button(control_frame, text="▶ START MONITOR",
                                     bg=Colors.ACCENT_PURPLE, fg='white',
                                     font=('Segoe UI', 11, 'bold'),
                                     padx=20, command=self.toggle_network_monitor)
        self.network_btn.pack(side='right', padx=10)
        
        # Stats frame with live updates
        stats_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.net_stats_label = tk.Label(stats_frame,
                                        text="Packets: 0 | HTTP: 0 | HTTPS: 0 | Keys: 0",
                                        bg=Colors.BG_SECONDARY, fg=Colors.ACCENT_CYAN,
                                        font=('Consolas', 11, 'bold'))
        self.net_stats_label.pack(pady=5)
        
        # Results tree
        tree_frame = tk.Frame(frame, bg=Colors.BG_TERTIARY)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Time', 'Source', 'Destination', 'Key Type', 'Risk', 'Key')
        self.network_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        self.network_tree.heading('Time', text='Time')
        self.network_tree.heading('Source', text='Source')
        self.network_tree.heading('Destination', text='Destination')
        self.network_tree.heading('Key Type', text='Key Type')
        self.network_tree.heading('Risk', text='Risk')
        self.network_tree.heading('Key', text='Key Preview')
        
        self.network_tree.column('Time', width=80)
        self.network_tree.column('Source', width=150)
        self.network_tree.column('Destination', width=150)
        self.network_tree.column('Key Type', width=120)
        self.network_tree.column('Risk', width=80)
        self.network_tree.column('Key', width=200)
        
        self._add_tree_scrollbars(tree_frame, self.network_tree)
        
    def create_crawler_tab(self):
        """Create deep web crawler tab with progress"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='🔍 DEEP CRAWLER')
        
        # Control panel
        control_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        control_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(control_frame, text="Start URL:",
                font=('Segoe UI', 11, 'bold'),
                bg=Colors.BG_SECONDARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=10)
        
        self.crawl_url_var = tk.StringVar(value="https://example.com")
        url_entry = tk.Entry(control_frame, textvariable=self.crawl_url_var,
                            font=('Segoe UI', 11), width=50,
                            bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY)
        url_entry.pack(side='left', padx=10, fill='x', expand=True)
        
        # Options
        options_frame = tk.Frame(control_frame, bg=Colors.BG_SECONDARY)
        options_frame.pack(side='bottom', pady=5)
        
        tk.Label(options_frame, text="Depth:",
                bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(side='left')
        
        self.depth_var = tk.IntVar(value=2)
        tk.Spinbox(options_frame, from_=1, to=5, width=5,
                  textvariable=self.depth_var,
                  bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=5)
        
        tk.Label(options_frame, text="Max Pages:",
                bg=Colors.BG_SECONDARY, fg=Colors.FG_SECONDARY).pack(side='left', padx=(10,0))
        
        self.pages_var = tk.IntVar(value=50)
        tk.Spinbox(options_frame, from_=10, to=500, width=6,
                  textvariable=self.pages_var,
                  bg=Colors.BG_TERTIARY, fg=Colors.FG_PRIMARY).pack(side='left', padx=5)
        
        self.crawl_btn = tk.Button(control_frame, text="▶ START CRAWL",
                                   bg=Colors.ACCENT_GREEN, fg='white',
                                   font=('Segoe UI', 11, 'bold'),
                                   padx=20, command=self.start_deep_crawl)
        self.crawl_btn.pack(side='right', padx=10)
        
        # Local progress
        self.crawl_progress_var = tk.IntVar(value=0)
        self.crawl_progress = ttk.Progressbar(control_frame, variable=self.crawl_progress_var,
                                              length=200, mode='determinate')
        self.crawl_progress.pack(side='right', padx=10)
        
        # Results list
        results_frame = tk.Frame(frame, bg=Colors.BG_TERTIARY)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Risk', 'Type', 'URL', 'Key')
        self.crawl_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=20)
        self.crawl_tree.heading('Risk', text='Risk')
        self.crawl_tree.heading('Type', text='Key Type')
        self.crawl_tree.heading('URL', text='Source URL')
        self.crawl_tree.heading('Key', text='Key Preview')
        
        self.crawl_tree.column('Risk', width=80)
        self.crawl_tree.column('Type', width=150)
        self.crawl_tree.column('URL', width=400)
        self.crawl_tree.column('Key', width=300)
        
        self._add_tree_scrollbars(results_frame, self.crawl_tree)
        
    def create_remediation_tab(self):
        """Create remediation guide tab"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='🔧 REMEDIATION')
        
        # Create notebook for different remediation categories
        rem_notebook = ttk.Notebook(frame)
        rem_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # OWASP Top 10
        owasp_frame = tk.Frame(rem_notebook, bg=Colors.BG_TERTIARY)
        rem_notebook.add(owasp_frame, text='OWASP Top 10')
        
        owasp_text = scrolledtext.ScrolledText(owasp_frame,
                                               bg=Colors.BG_SECONDARY,
                                               fg=Colors.FG_PRIMARY,
                                               font=('Consolas', 11),
                                               wrap='word')
        owasp_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        owasp_content = """
OWASP TOP 10 REMEDIATION GUIDE
═══════════════════════════════════════════════════════════════

1. A01: Broken Access Control
   • Implement proper access control checks
   • Deny by default
   • Use role-based access control (RBAC)
   • Log access control failures

2. A02: Cryptographic Failures
   • Use strong encryption (AES-256, TLS 1.3)
   • Encrypt all sensitive data at rest and in transit
   • Use secure key management
   • Disable outdated protocols

3. A03: Injection
   • Use parameterized queries/prepared statements
   • Implement input validation
   • Use safe APIs
   • Escape special characters

4. A04: Insecure Design
   • Implement secure design patterns
   • Threat modeling
   • Security requirements in design phase
   • Use security libraries/frameworks

5. A05: Security Misconfiguration
   • Use secure defaults
   • Regular security audits
   • Minimal platform features
   • Separate environments

6. A06: Vulnerable Components
   • Regular dependency updates
   • Use SBOM (Software Bill of Materials)
   • Remove unused dependencies
   • Monitor CVE databases

7. A07: Identification/Authentication Failures
   • Implement MFA
   • Secure password policies
   • Rate limiting
   • Session management

8. A08: Software/Data Integrity Failures
   • Use CI/CD security checks
   • Code signing
   • Integrity checks
   • Secure update mechanisms

9. A09: Security Logging/Monitoring Failures
   • Centralized logging
   • Real-time monitoring
   • Alert on suspicious activity
   • Log retention policies

10. A10: Server-Side Request Forgery (SSRF)
    • Validate/sanitize URLs
    • Network segmentation
    • Deny list of internal addresses
    • Use allow lists
"""
        owasp_text.insert('1.0', owasp_content)
        owasp_text.config(state='disabled')
        
        # API Security
        api_frame = tk.Frame(rem_notebook, bg=Colors.BG_TERTIARY)
        rem_notebook.add(api_frame, text='API Security')
        
        api_text = scrolledtext.ScrolledText(api_frame,
                                             bg=Colors.BG_SECONDARY,
                                             fg=Colors.FG_PRIMARY,
                                             font=('Consolas', 11),
                                             wrap='word')
        api_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        api_content = """
API SECURITY BEST PRACTICES
═══════════════════════════════════════════════════════════════

AUTHENTICATION & AUTHORIZATION
───────────────────────────────────────────────────────────────
• Use OAuth 2.0 / OIDC for authentication
• Implement proper scope validation
• Use short-lived tokens
• Rotate API keys regularly
• Never expose keys in URLs

INPUT VALIDATION
───────────────────────────────────────────────────────────────
• Validate all input parameters
• Use strict schema validation
• Implement rate limiting
• Sanitize special characters
• Content-Type validation

RATE LIMITING
───────────────────────────────────────────────────────────────
• Implement per-user/IP rate limits
• Use token bucket algorithms
• Return proper 429 status codes
• Queue excessive requests
• Monitor usage patterns

ERROR HANDLING
────────────────────────────────────────────────────────────────
• Don't expose stack traces
• Use generic error messages
• Log detailed errors internally
• Return appropriate HTTP status codes
• Implement global error handlers

DATA PROTECTION
────────────────────────────────────────────────────────────────
• Encrypt sensitive data
• Use HTTPS exclusively
• Implement CORS properly
• Remove sensitive data from responses
• Audit data access

MONITORING
────────────────────────────────────────────────────────────────
• Log all API access
• Monitor for abuse patterns
• Set up alerts
• Regular security audits
• Track API version usage
"""
        api_text.insert('1.0', api_content)
        api_text.config(state='disabled')
        
        # Extension Security
        ext_rem_frame = tk.Frame(rem_notebook, bg=Colors.BG_TERTIARY)
        rem_notebook.add(ext_rem_frame, text='Extension Security')
        
        ext_rem_text = scrolledtext.ScrolledText(ext_rem_frame,
                                                 bg=Colors.BG_SECONDARY,
                                                 fg=Colors.FG_PRIMARY,
                                                 font=('Consolas', 11),
                                                 wrap='word')
        ext_rem_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        ext_rem_content = """
CHROME EXTENSION SECURITY BEST PRACTICES
═══════════════════════════════════════════════════════════════

MANIFEST SECURITY
───────────────────────────────────────────────────────────────
• Use manifest V3
• Request minimal permissions
• Avoid wildcard permissions (*://*/*)
• Use host_permissions specifically
• Implement strict CSP

CONTENT SECURITY POLICY (CSP)
───────────────────────────────────────────────────────────────
• Avoid 'unsafe-eval' and 'unsafe-inline'
• Use nonces or hashes for inline scripts
• Restrict script sources
• Implement object-src 'none'
• Regular CSP audits

DATA STORAGE
───────────────────────────────────────────────────────────────
• Never hardcode secrets
• Use chrome.storage with encryption
• Avoid localStorage for sensitive data
• Clear sensitive data on logout
• Implement secure defaults

MESSAGE PASSING
───────────────────────────────────────────────────────────────
• Validate message origins
• Use strict message schemas
• Avoid eval() on received data
• Implement timeout mechanisms
• Log suspicious messages

EXTERNAL COMMUNICATION
───────────────────────────────────────────────────────────────
• Use HTTPS exclusively
• Validate external responses
• Implement timeout handling
• Avoid mixed content
• Use fetch() with credentials: 'omit'

CODE QUALITY
───────────────────────────────────────────────────────────────
• Regular security audits
• Use ESLint security plugins
• Minimize third-party dependencies
• Keep dependencies updated
• Use Subresource Integrity (SRI) for external scripts

PERMISSIONS
───────────────────────────────────────────────────────────────
• Request permissions only when needed
• Use optional permissions when possible
• Explain why permissions are needed
• Regularly audit permission usage
• Remove unused permissions

BACKGROUND SCRIPTS
───────────────────────────────────────────────────────────────
• Use service workers (MV3)
• Keep background scripts minimal
• Implement proper error handling
• Avoid memory leaks
• Use alarms for periodic tasks

WEB ACCESSIBLE RESOURCES
───────────────────────────────────────────────────────────────
• Restrict web accessible resources
• Avoid exposing internal files
• Use content security headers
• Validate resource requests
• Implement origin checks
"""
        ext_rem_text.insert('1.0', ext_rem_content)
        ext_rem_text.config(state='disabled')
        
        # Network Security
        net_frame = tk.Frame(rem_notebook, bg=Colors.BG_TERTIARY)
        rem_notebook.add(net_frame, text='Network Security')
        
        net_text = scrolledtext.ScrolledText(net_frame,
                                             bg=Colors.BG_SECONDARY,
                                             fg=Colors.FG_PRIMARY,
                                             font=('Consolas', 11),
                                             wrap='word')
        net_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        net_content = """
NETWORK SECURITY BEST PRACTICES
═══════════════════════════════════════════════════════════════

ENCRYPTION
───────────────────────────────────────────────────────────────
• Use TLS 1.3 minimum
• Implement HSTS
• Use strong cipher suites
• Regular certificate rotation
• Disable weak protocols (SSLv3, TLS 1.0/1.1)

AUTHENTICATION
───────────────────────────────────────────────────────────────
• Implement mutual TLS where applicable
• Use certificate pinning for mobile apps
• Secure API key storage
• Rotate credentials regularly
• Implement proper session management

MONITORING
───────────────────────────────────────────────────────────────
• Network intrusion detection (IDS/IPS)
• Real-time traffic analysis
• Anomaly detection
• Log all network events
• Regular penetration testing

FIREWALL CONFIGURATION
───────────────────────────────────────────────────────────────
• Default deny policy
• Allow only necessary ports
• Rate limiting on all endpoints
• DDoS protection
• Regular rule audits

DNS SECURITY
───────────────────────────────────────────────────────────────
• Use DNSSEC
• Implement DNS filtering
• Monitor for DNS tunneling
• Use secure DNS resolvers
• Regular DNS audits

SEGMENTATION
───────────────────────────────────────────────────────────────
• Network segmentation
• DMZ for public services
• Micro-segmentation for cloud
• VLAN separation
• Regular network mapping

INCIDENT RESPONSE
───────────────────────────────────────────────────────────────
• Documented response plan
• Regular drills
• Clear communication channels
• Forensic readiness
• Post-incident analysis
"""
        net_text.insert('1.0', net_content)
        net_text.config(state='disabled')
        
    def create_logs_tab(self):
        """Create logs tab"""
        frame = tk.Frame(self.notebook, bg=Colors.BG_TERTIARY)
        self.notebook.add(frame, text='📝 LOGS')
        
        self.log_text = scrolledtext.ScrolledText(frame,
                                                  bg=Colors.BG_SECONDARY,
                                                  fg=Colors.FG_PRIMARY,
                                                  font=('Consolas', 10),
                                                  wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=20, pady=20)
        
    def _add_tree_scrollbars(self, parent, tree):
        """Add scrollbars to treeview"""
        v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
    # ==================== UTILITY METHODS ====================
    
    def log_message(self, message):
        """Queue log message"""
        self.queue.put(('log', message))
        
    def update_progress(self, value, message):
        """Queue progress update for main progress"""
        self.queue.put(('progress', value, message))
        
    def update_web_progress(self, value):
        """Update web scanner progress"""
        self.web_progress_var.set(value)
        
    def update_ext_progress(self, value):
        """Update extension analyzer progress"""
        self.ext_progress_var.set(value)
        
    def update_crawl_progress(self, value):
        """Update crawler progress"""
        self.crawl_progress_var.set(value)
        
    def process_queue(self):
        """Process queued updates in GUI thread"""
        try:
            while True:
                item = self.queue.get_nowait()
                
                if item[0] == 'log':
                    self._add_log(item[1])
                elif item[0] == 'progress':
                    self.progress_manager.update_progress(item[1], item[2])
                elif item[0] == 'web_progress':
                    self.update_web_progress(item[1])
                elif item[0] == 'ext_progress':
                    self.update_ext_progress(item[1])
                elif item[0] == 'crawl_progress':
                    self.update_crawl_progress(item[1])
                elif item[0] == 'network_result':
                    self._add_network_result(item[1])
                elif item[0] == 'crawl_result':
                    self._add_crawl_result(item[1])
                elif item[0] == 'extension_result':
                    self._display_extension_results(item[1])
                elif item[0] == 'web_result':
                    self._display_web_results(item[1])
                    
        except queue.Empty:
            pass
            
        self.root.after(100, self.process_queue)
        
    def _add_log(self, message):
        """Add message to log widget"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        
    # ==================== WEB SCANNER METHODS ====================
    
    def start_web_scan(self):
        """Start web application scan with live progress"""
        url = self.web_url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a target URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.web_url_var.set(url)
            
        # Legal disclaimer
        if not messagebox.askyesno("Legal Notice", 
                                   "You must own this website or have explicit permission to test it.\n\n"
                                   "Do you have permission to test this target?"):
            return
            
        self.is_scanning = True
        self.web_scan_btn.config(state='disabled', text="⏳ SCANNING...")
        self.web_progress_var.set(0)
        
        # Start pulsing animation for indeterminate parts
        self.progress_manager.start_pulse()
        
        # Clear previous results
        for item in self.web_vuln_tree.get_children():
            self.web_vuln_tree.delete(item)
        self.web_paths_list.delete(0, tk.END)
        for item in self.web_tech_tree.get_children():
            self.web_tech_tree.delete(item)
            
        # Create scanner with progress callbacks
        self.web_scanner = WebAppScanner(
            target_url=url,
            callback=self.log_message,
            progress_callback=lambda v, m: self.queue.put(('progress', v, m))
        )
        
        # Start scan in thread
        self.scan_thread = threading.Thread(target=self._run_web_scan)
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        self.log_message(f"🚀 Starting web application scan of {url}")
        
    def _run_web_scan(self):
        """Run web scan in thread"""
        results = self.web_scanner.run_full_scan()
        self.queue.put(('web_result', results))
        self.root.after(0, self._web_scan_complete)
        
    def _web_scan_complete(self):
        """Handle web scan completion"""
        self.is_scanning = False
        self.web_scan_btn.config(state='normal', text="▶ START SCAN")
        self.progress_manager.stop_pulse()
        
    def _display_web_results(self, results):
        """Display web scan results"""
        self.web_results = results
        
        # Display vulnerabilities
        for vuln in results.get('vulnerabilities', []):
            severity = vuln.get('severity', 'INFO')
            self.web_vuln_tree.insert('', 'end', values=(
                severity,
                vuln.get('name', ''),
                vuln.get('url', '')[:80] + '...' if len(vuln.get('url', '')) > 80 else vuln.get('url', ''),
                vuln.get('description', '')[:100] + '...' if len(vuln.get('description', '')) > 100 else vuln.get('description', '')
            ), tags=(severity,))
            
        # Display discovered paths
        for path in results.get('discovered_paths', []):
            self.web_paths_list.insert('end', f"{path['url']} ({path['status']})")
            
        # Display technologies
        for tech in results.get('technologies', []):
            self.web_tech_tree.insert('', 'end', values=(
                tech.get('name', ''),
                tech.get('category', ''),
                tech.get('version', '')
            ))
            
        # Update stats
        vuln_count = len(results.get('vulnerabilities', []))
        self.stats_labels['web_vulns'].config(text=str(vuln_count))
        
        self.log_message(f"✅ Web scan complete. Found {vuln_count} vulnerabilities")
        
    def show_web_vuln_details(self, event):
        """Show web vulnerability details"""
        selection = self.web_vuln_tree.selection()
        if not selection or not self.web_results:
            return
            
        item = self.web_vuln_tree.item(selection[0])
        values = item['values']
        
        # Find the vulnerability
        for vuln in self.web_results.get('vulnerabilities', []):
            if vuln.get('name') == values[1]:
                self._show_vuln_detail_window(vuln)
                break
                
    # ==================== EXTENSION ANALYSIS METHODS ====================
    
    def analyze_extension(self):
        """Analyze Chrome extension by ID or URL with live progress"""
        input_text = self.ext_input_var.get().strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter an Extension ID or URL")
            return
            
        # Extract extension ID from URL if needed
        if 'chrome.google.com' in input_text or 'webstore' in input_text:
            extension_id = self._extract_id_from_url(input_text)
        else:
            extension_id = input_text
            
        if not extension_id or not re.match(r'^[a-z]{32}$', extension_id):
            messagebox.showerror("Error", "Invalid Extension ID format")
            return
            
        self.is_scanning = True
        self.ext_scan_btn.config(state='disabled', text="⏳ ANALYZING...")
        self.ext_progress_var.set(0)
        
        # Start pulsing animation
        self.progress_manager.start_pulse()
        
        # Clear previous results
        self.metadata_text.delete(1.0, tk.END)
        for item in self.ext_vuln_tree.get_children():
            self.ext_vuln_tree.delete(item)
        for item in self.ext_api_tree.get_children():
            self.ext_api_tree.delete(item)
        self.perm_listbox.delete(0, tk.END)
        
        # Start analysis thread
        self.scan_thread = threading.Thread(target=self._run_extension_analysis,
                                            args=(extension_id,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        self.log_message(f"🔍 Starting Chrome extension analysis for ID: {extension_id}")
        
    def _extract_id_from_url(self, url):
        """Extract extension ID from Chrome Web Store URL"""
        patterns = [
            r'/detail/[^/]+/([a-z]{32})',
            r'id=([a-z]{32})',
            r'webstore/detail/[^/]+/([a-z]{32})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
        
    def _run_extension_analysis(self, extension_id):
        """Run extension analysis in thread"""
        self.extension_analyzer = ChromeExtensionAnalyzer(
            callback=self.log_message,
            progress_callback=lambda v, m: self.queue.put(('ext_progress', v))
        )
        
        results = self.extension_analyzer.analyze_extension(extension_id)
        
        if results:
            self.queue.put(('extension_result', results))
            
        self.root.after(0, self._extension_analysis_complete)
        
    def _extension_analysis_complete(self):
        """Handle extension analysis completion"""
        self.is_scanning = False
        self.ext_scan_btn.config(state='normal', text="🔍 ANALYZE")
        self.progress_manager.stop_pulse()
        
    def _display_extension_results(self, results):
        """Display extension analysis results"""
        self.extension_results = results
        
        # Display metadata
        metadata = results.get('metadata', {})
        meta_display = f"""
╔══════════════════════════════════════════════════════════════╗
║                    EXTENSION METADATA                         ║
╚══════════════════════════════════════════════════════════════╝

📦 Name: {metadata.get('name', 'Unknown')}
🔖 ID: {metadata.get('id', 'Unknown')}
📌 Version: {metadata.get('version', 'Unknown')}
👤 Author: {metadata.get('author', 'Unknown')}
⭐ Rating: {metadata.get('rating', 0)} / 5
👥 Users: {metadata.get('users', 0):,}
📅 Last Updated: {metadata.get('last_updated', 'Unknown')}
📂 Category: {metadata.get('category', 'Unknown')}
📏 Size: {metadata.get('size', 'Unknown')}
🌐 Languages: {', '.join(metadata.get('languages', ['en']))}

📝 Description:
{metadata.get('description', 'No description available')}
"""
        self.metadata_text.insert('1.0', meta_display)
        
        # Display vulnerabilities
        for vuln in results.get('vulnerabilities', []):
            severity = vuln.get('severity', 'INFO')
            self.ext_vuln_tree.insert('', 'end', values=(
                severity,
                vuln.get('type', ''),
                vuln.get('file', ''),
                vuln.get('line_number', ''),
                vuln.get('description', '')[:100]
            ), tags=(severity,))
        
        # Display APIs
        for api in results.get('apis', []):
            self.ext_api_tree.insert('', 'end', values=(
                api.get('url', '')[:100],
                api.get('method', 'GET'),
                api.get('file', ''),
                api.get('line_number', '')
            ))
        
        # Display permissions
        for perm in results.get('permissions', []):
            self.perm_listbox.insert('end', perm)
            
        # Update stats
        vuln_count = len(results.get('vulnerabilities', []))
        self.stats_labels['extension_vulns'].config(text=str(vuln_count))
        self.stats_labels['api_keys'].config(text=str(len(results.get('apis', [])) + len(self.network_results) + len(self.crawl_results)))
        
        self.log_message(f"✅ Extension analysis complete. Found {vuln_count} vulnerabilities")
        
    def show_ext_vuln_details(self, event):
        """Show extension vulnerability details"""
        selection = self.ext_vuln_tree.selection()
        if not selection or not self.extension_results:
            return
            
        item = self.ext_vuln_tree.item(selection[0])
        values = item['values']
        
        # Find the vulnerability
        for vuln in self.extension_results.get('vulnerabilities', []):
            if (vuln.get('type') == values[1] and 
                vuln.get('file') == values[2]):
                
                details = f"""
VULNERABILITY DETAILS
═══════════════════════════════════════════════════════════════

Type: {vuln.get('type')}
Severity: {vuln.get('severity')}
CWE: {vuln.get('cwe', 'N/A')}
OWASP: {vuln.get('owasp', 'N/A')}
File: {vuln.get('file')}
Line: {vuln.get('line_number')}

Description:
{vuln.get('description')}

Context:
{vuln.get('context', 'No context available')}

Remediation:
{vuln.get('remediation')}
"""
                
                self._show_vuln_detail_window({'description': details, 'severity': vuln.get('severity')})
                break
                
    # ==================== NETWORK MONITOR METHODS ====================
    
    def toggle_network_monitor(self):
        """Toggle network monitoring"""
        if not SCAPY_AVAILABLE:
            messagebox.showerror("Error", "Scapy not installed.\nInstall with: pip install scapy")
            return
            
        if not self.network_monitor.is_monitoring:
            interface = self.interface_var.get()
            if self.network_monitor.start_monitoring(interface):
                self.network_btn.config(text="⏹ STOP MONITOR", bg=Colors.ACCENT_RED)
                self.log_message(f"🌐 Network monitoring started on {interface}")
                self.update_network_stats()
        else:
            self.network_monitor.stop_monitoring()
            self.network_btn.config(text="▶ START MONITOR", bg=Colors.ACCENT_PURPLE)
            
    def update_network_stats(self, stats=None):
        """Update network statistics in real-time"""
        if stats:
            self.net_stats_label.config(
                text=f"Packets: {stats['packets_captured']} | "
                     f"HTTP: {stats['http_requests']} | "
                     f"HTTPS: {stats['https_connections']} | "
                     f"Keys: {stats['keys_found']}"
            )
        else:
            # Update with current stats
            stats = self.network_monitor.stats
            self.net_stats_label.config(
                text=f"Packets: {stats['packets_captured']} | "
                     f"HTTP: {stats['http_requests']} | "
                     f"HTTPS: {stats['https_connections']} | "
                     f"Keys: {stats['keys_found']}"
            )
            
    def _add_network_result(self, result):
        """Add network result to GUI"""
        self.network_results.append(result)
        
        packet_info = result.get('packet_info', {})
        self.network_tree.insert('', 'end', values=(
            result['timestamp'][11:19],
            f"{packet_info.get('source_ip', 'Unknown')}:{packet_info.get('source_port', '')}",
            f"{packet_info.get('dest_ip', 'Unknown')}:{packet_info.get('dest_port', '')}",
            result['type'],
            result['risk'],
            result['key'][:50] + '...' if len(result['key']) > 50 else result['key']
        ))
        
        # Update stats
        total_keys = len(self.network_results) + len(self.crawl_results)
        if self.extension_results:
            total_keys += len(self.extension_results.get('apis', []))
        self.stats_labels['api_keys'].config(text=str(total_keys))
        
    # ==================== DEEP CRAWL METHODS ====================
    
    def start_deep_crawl(self):
        """Start deep website crawl with live progress"""
        url = self.crawl_url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.crawl_url_var.set(url)
            
        # Legal disclaimer
        if not messagebox.askyesno("Confirm", 
                                   f"Start deep crawl of {url}?\n\nOnly scan systems you own or have permission to test!"):
            return
            
        self.is_scanning = True
        self.crawl_btn.config(state='disabled', text="⏳ CRAWLING...")
        self.crawl_progress_var.set(0)
        
        # Start pulsing animation
        self.progress_manager.start_pulse()
        
        # Clear previous results
        for item in self.crawl_tree.get_children():
            self.crawl_tree.delete(item)
            
        depth = self.depth_var.get()
        max_pages = self.pages_var.get()
        
        self.scan_thread = threading.Thread(target=self._run_deep_crawl,
                                            args=(url, depth, max_pages))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        self.log_message(f"🔍 Starting deep crawl of {url}")
        
    def _run_deep_crawl(self, url, depth, max_pages):
        """Run deep crawl in thread"""
        crawler = DeepWebCrawler(
            callback=self.log_message,
            progress_callback=lambda v, m: self.queue.put(('crawl_progress', v))
        )
        results = crawler.crawl(url, depth, max_pages)
        
        for result in results:
            self.queue.put(('crawl_result', result))
            
        self.root.after(0, self._crawl_complete)
        
    def _crawl_complete(self):
        """Handle crawl completion"""
        self.is_scanning = False
        self.crawl_btn.config(state='normal', text="▶ START CRAWL")
        self.progress_manager.stop_pulse()
        
    def _add_crawl_result(self, result):
        """Add crawl result to GUI"""
        self.crawl_results.append(result)
        
        risk_emoji = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }.get(result['risk'], '⚪')
        
        self.crawl_tree.insert('', 'end', values=(
            f"{risk_emoji} {result['risk']}",
            result['type'],
            result['source'][:80] + '...' if len(result['source']) > 80 else result['source'],
            result['key'][:50] + '...' if len(result['key']) > 50 else result['key']
        ))
        
        # Update stats
        self.stats_labels['pages'].config(text=str(len(self.crawl_results)))
        total_keys = len(self.network_results) + len(self.crawl_results)
        if self.extension_results:
            total_keys += len(self.extension_results.get('apis', []))
        self.stats_labels['api_keys'].config(text=str(total_keys))
        
    # ==================== UTILITY METHODS ====================
    
    def _show_vuln_detail_window(self, vuln):
        """Show vulnerability details in new window"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Vulnerability Details")
        detail_window.geometry("700x500")
        detail_window.configure(bg=Colors.BG_PRIMARY)
        
        # Color based on severity
        severity = vuln.get('severity', 'INFO')
        color_map = {
            'CRITICAL': Colors.ACCENT_RED,
            'HIGH': Colors.ACCENT_ORANGE,
            'MEDIUM': Colors.ACCENT_YELLOW,
            'LOW': Colors.ACCENT_GREEN,
        }
        border_color = color_map.get(severity, Colors.ACCENT_BLUE)
        
        # Text widget
        text = tk.Text(detail_window,
                      bg=Colors.BG_SECONDARY,
                      fg=Colors.FG_PRIMARY,
                      font=('Consolas', 11),
                      wrap='word',
                      padx=20,
                      pady=20)
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add border
        text.config(highlightbackground=border_color, highlightcolor=border_color, highlightthickness=2)
        
        text.insert('1.0', vuln.get('description', 'No details available'))
        text.configure(state='disabled')
        
        # Copy button
        tk.Button(detail_window, text="📋 Copy Details",
                 bg=Colors.ACCENT_BLUE, fg='white',
                 font=('Segoe UI', 11),
                 command=lambda: self._copy_to_clipboard(vuln.get('description', ''))).pack(pady=10)
        
    def _copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Details copied to clipboard!")
        
    def stop_all(self):
        """Stop all operations"""
        if self.network_monitor.is_monitoring:
            self.network_monitor.stop_monitoring()
            self.network_btn.config(text="▶ START MONITOR", bg=Colors.ACCENT_PURPLE)
            
        if hasattr(self, 'deep_crawler') and self.deep_crawler:
            self.deep_crawler.stop()
            
        if self.extension_analyzer:
            self.extension_analyzer.stop()
            
        if self.web_scanner:
            self.web_scanner.stop()
            
        self.is_scanning = False
        self.progress_manager.stop_pulse()
        self.log_message("⏹️ All operations stopped")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    
    disclaimer = """⚠️ LEGAL NOTICE

Unified Security Analysis Tool is for AUTHORIZED security testing ONLY.

• Only scan systems and extensions you own or have permission to test
• Network monitoring may be subject to local laws
• The user assumes all responsibility for compliance
• Always handle findings confidentially

Do you accept these terms?"""
    
    root = tk.Tk()
    root.withdraw()
    
    if not messagebox.askyesno("Legal Notice", disclaimer, icon='warning'):
        root.destroy()
        return
        
    root.deiconify()
    
    try:
        app = UnifiedSecurityTool(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()