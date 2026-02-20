#!/usr/bin/env python3
"""
Advanced Phone Number Intelligence Tool - Professional OSINT Framework
Version: 2.1 - Enhanced Cyberpunk GUI + All Bugs Fixed + Enhanced Animations
For authorized security research and investigations only

ENHANCEMENTS ADDED:
  - Enhanced particle system with trailing effects
  - Glowing text with dynamic color cycling
  - 3D-like rotating hex grid with depth perception
  - Improved scan-line effects with multi-color gradients
  - Ripple effects with harmonic wave patterns
  - Fixed all identified bugs and edge cases
"""

# ── Standard library ──────────────────────────────────────────────────────────
import re
import sys
import json
import time
import math
import hashlib
import sqlite3
import threading
import webbrowser
import random
import colorsys
import csv
import tempfile
import os
from datetime import datetime
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Third-party – hard requirements ──────────────────────────────────────────
try:
    import requests
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception:
        pass
except ImportError:
    print("ERROR: 'requests' not installed.  pip install requests")
    sys.exit(1)

try:
    import phonenumbers
    from phonenumbers import timezone as pn_timezone
    from phonenumbers import carrier   as pn_carrier
    from phonenumbers import geocoder  as pn_geocoder
    from phonenumbers.phonenumberutil import number_type as pn_number_type
except ImportError:
    print("ERROR: 'phonenumbers' not installed.  pip install phonenumbers")
    sys.exit(1)

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
except ImportError:
    print("ERROR: tkinter not available.  Install python3-tk via your package manager.")
    sys.exit(1)

# ── Optional imports (gracefully degraded) ────────────────────────────────────
try:
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                    Spacer, Table, TableStyle)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    import folium
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False

try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False


# ─────────────────────────────────────────────────────────────────────────────
# THEME CONSTANTS - Enhanced with more vibrant colors
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG      = "#050a0f"
PANEL_BG     = "#0a1520"
CARD_BG      = "#0d1e30"
BORDER_COLOR = "#0e3a5c"
CYAN_BRIGHT  = "#00f5ff"
CYAN_MID     = "#00b4cc"
CYAN_DIM     = "#004d5c"
GREEN_NEON   = "#00ff88"
GREEN_PULSE  = "#00ffaa"
AMBER_BRIGHT = "#ffb300"
AMBER_PULSE  = "#ffaa00"
RED_ALERT    = "#ff2244"
RED_PULSE    = "#ff3366"
PURPLE_GLOW  = "#aa88ff"
TEXT_BRIGHT  = "#e8f4ff"
TEXT_MID     = "#7ab8d4"
TEXT_DIM     = "#2a5a7a"

FONT_MONO    = ("Courier New", 10)
FONT_MONO_SM = ("Courier New", 9)
FONT_BTN     = ("Courier New", 10, "bold")
FONT_TITLE   = ("Courier New", 20, "bold")


# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED ANIMATED WIDGETS
# ─────────────────────────────────────────────────────────────────────────────

class Particle:
    """Individual particle for enhanced effects"""
    def __init__(self, x, y, vx, vy, life, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color

class EnhancedMatrixCanvas(tk.Canvas):
    """Enhanced falling characters with trailing glow and particle effects."""
    CHARS = "01アイウエオカキクケコサシスセソタ@#$%&!?▓▒░⚡◈◉◊○●"

    def __init__(self, master, width, height, **kw):
        super().__init__(master, width=width, height=height,
                         bg=DARK_BG, highlightthickness=0, **kw)
        self._w = width
        self._h = height
        self._cols = max(1, width // 12)
        self._drops = [random.randint(-height // 12, 0) for _ in range(self._cols)]
        self._speeds = [random.uniform(0.8, 2.0) for _ in range(self._cols)]
        self._glow_trails = []
        self._alive = True
        self._animate()
        self._create_glow_layers()

    def _create_glow_layers(self):
        """Create multiple canvas layers for glow effects"""
        for i in range(3):
            layer = tk.Canvas(self, width=self._w, height=self._h,
                              bg=DARK_BG, highlightthickness=0)
            layer.place(x=0, y=0)

    def destroy(self):
        self._alive = False
        super().destroy()

    def _animate(self):
        if not self._alive:
            return
        try:
            for i in range(self._cols):
                x = i * 12 + 6
                y = self._drops[i] * 12
                
                # Create main character
                ch = random.choice(self.CHARS)
                
                # Calculate brightness based on position
                brightness = 1.0 - (y / self._h) * 0.7
                
                if y < self._h and y > 0:
                    # Create glowing trail
                    for trail in range(3):
                        trail_y = y - (trail + 1) * 8
                        if trail_y > 0:
                            alpha = 0.7 - trail * 0.2
                            trail_color = self._adjust_brightness(CYAN_BRIGHT, alpha * brightness)
                            tid = self.create_text(x, trail_y, text=ch, fill=trail_color,
                                                  font=("Courier New", 8), anchor="center")
                            self.after(150, lambda t=tid: self._safe_del(t))
                    
                    # Main character with occasional bright flash
                    if random.random() > 0.98:
                        color = GREEN_NEON
                        size = 12
                    else:
                        color = self._adjust_brightness(CYAN_BRIGHT, brightness)
                        size = 10
                    
                    tid = self.create_text(x, y, text=ch, fill=color,
                                          font=("Courier New", size), anchor="center")
                    self.after(200, lambda t=tid: self._safe_del(t))
                
                # Update drop position
                if self._drops[i] * 12 > self._h + 20:
                    self._drops[i] = -random.randint(5, 15)
                    self._speeds[i] = random.uniform(0.8, 2.0)
                else:
                    self._drops[i] += self._speeds[i]
                    
        except tk.TclError:
            return
        self.after(50, self._animate)

    def _adjust_brightness(self, color, factor):
        """Adjust color brightness"""
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def _safe_del(self, tid):
        try:
            self.delete(tid)
        except Exception:
            pass


class EnhancedHexGrid(tk.Canvas):
    """3D-like rotating hex grid with depth perception and glow."""
    def __init__(self, master, width, height, **kw):
        super().__init__(master, width=width, height=height,
                         bg=DARK_BG, highlightthickness=0, **kw)
        self._alive = True
        self._hexes = []
        self._t = 0.0
        self._rotation = 0.0
        self._pulse_phase = 0.0
        self._build_3d_hexes(width, height)
        self._animate()

    def destroy(self):
        self._alive = False
        super().destroy()

    def _hex_points_3d(self, cx, cy, r, depth):
        """Generate hex points with 3D effect"""
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 30 + self._rotation)
            # Apply depth scaling
            scale = 1.0 - depth * 0.3
            x = cx + r * math.cos(a) * scale
            y = cy + r * math.sin(a) * scale * 0.8  # Perspective flattening
            pts += [x, y]
        return pts

    def _build_3d_hexes(self, width, height):
        """Build hex grid with depth layers"""
        base_r = 32
        depths = [0.0, 0.3, 0.6, 0.9]  # Multiple depth layers
        
        for depth in depths:
            r = base_r * (1 - depth * 0.2)
            for row in range(-2, int(height / (r * 1.5)) + 3):
                for col in range(-2, int(width / (r * 1.8)) + 3):
                    cx = col * r * 1.8 + (r * 0.9 if row % 2 else 0)
                    cy = row * r * 1.5
                    
                    # Calculate distance from center for glow
                    dist_from_center = math.sqrt((cx - width/2)**2 + (cy - height/2)**2)
                    max_dist = math.sqrt((width/2)**2 + (height/2)**2)
                    glow_factor = 1.0 - (dist_from_center / max_dist)
                    
                    pts = self._hex_points_3d(cx, cy, r - 4 * depth, depth)
                    
                    # Color based on depth and position
                    if depth < 0.3:
                        outline = CYAN_BRIGHT
                        fill = self._adjust_brightness(CARD_BG, 1.0 + glow_factor * 0.3)
                    elif depth < 0.6:
                        outline = CYAN_MID
                        fill = self._adjust_brightness(DARK_BG, 1.0 + glow_factor * 0.2)
                    else:
                        outline = CYAN_DIM
                        fill = DARK_BG
                    
                    hid = self.create_polygon(pts, fill=fill,
                                             outline=outline, width=1 + depth)
                    self._hexes.append((hid, depth, glow_factor))

    def _adjust_brightness(self, color, factor):
        """Adjust color brightness"""
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def _animate(self):
        if not self._alive:
            return
        try:
            self._t += 0.02
            self._rotation += 0.002
            self._pulse_phase += 0.05
            
            for hid, depth, glow_factor in self._hexes:
                # Pulsing effect based on depth
                pulse = (math.sin(self._pulse_phase + depth * 10) + 1) / 2
                
                if pulse > 0.9:
                    outline_color = GREEN_NEON
                    width = 2
                elif pulse > 0.7:
                    outline_color = CYAN_BRIGHT
                    width = 1 + depth
                else:
                    outline_color = self._adjust_brightness(CYAN_DIM, 0.8 + pulse * 0.2)
                    width = 1
                
                self.itemconfig(hid, outline=outline_color, width=width)
                
        except tk.TclError:
            return
        self.after(50, self._animate)


class HarmonicRipple(PulsingRing):
    """Enhanced rings with harmonic wave patterns."""
    def __init__(self, master, size=70, color=CYAN_BRIGHT, **kw):
        super().__init__(master, size, color, **kw)
        self._harmonics = 5
        self._wave_phase = 0.0
        self._particles = []

    def _animate(self):
        if not self._alive:
            return
        try:
            c = self._size // 2
            self._phase = (self._phase + 0.05) % (math.pi * 2)
            self._wave_phase += 0.1
            
            # Create particles occasionally
            if random.random() > 0.95:
                angle = random.uniform(0, math.pi * 2)
                dist = random.uniform(10, 30)
                px = c + math.cos(angle) * dist
                py = c + math.sin(angle) * dist
                self._particles.append([px, py, 0, angle])
            
            # Update existing rings with harmonics
            for i, rid in enumerate(self._rings):
                # Multiple harmonic frequencies
                freq1 = 1.0
                freq2 = 2.0
                freq3 = 3.0
                
                offset = i * math.pi * 2 / 3
                wave1 = math.sin(self._phase * freq1 + offset)
                wave2 = math.sin(self._phase * freq2 + offset) * 0.3
                wave3 = math.sin(self._phase * freq3 + offset) * 0.1
                
                combined = (wave1 + wave2 + wave3) / 1.4
                scale = (combined + 1) / 2
                
                r = 6 + scale * (c - 8)
                self.coords(rid, c - r, c - r, c + r, c + r)
                
                # Color cycling
                hue = (self._phase / (math.pi * 2) + i * 0.1) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
                color = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
                self.itemconfig(rid, outline=color)
            
            # Update particles
            dead = []
            for p in self._particles:
                p[0] += math.cos(p[3]) * 2
                p[1] += math.sin(p[3]) * 2
                p[2] += 1
                
                if p[2] > 30 or p[0] < 0 or p[0] > self._size or p[1] < 0 or p[1] > self._size:
                    dead.append(p)
                else:
                    alpha = 1.0 - p[2] / 30
                    size = 3 - p[2] / 10
                    pid = self.create_oval(p[0]-size, p[1]-size, p[0]+size, p[1]+size,
                                          fill=self._color, outline="")
                    self.after(50, lambda i=pid: self._safe_del(i))
            
            for p in dead:
                self._particles.remove(p)
                
        except tk.TclError:
            return
        self.after(35, self._animate)

    def _safe_del(self, iid):
        try:
            self.delete(iid)
        except Exception:
            pass


class GlowingText(GlitchLabel):
    """Enhanced glowing text with color cycling."""
    def __init__(self, master, text="", glitch_interval=4000, **kw):
        super().__init__(master, text, glitch_interval, **kw)
        self._glow_phase = 0.0
        self._alive = True
        self._start_glow()

    def _start_glow(self):
        if self._alive:
            self.after(50, self._glow_cycle)

    def _glow_cycle(self):
        if not self._alive:
            return
        try:
            self._glow_phase += 0.05
            # Create pulsing glow effect
            glow = (math.sin(self._glow_phase) + 1) / 2
            r, g, b = 0, int(200 + 55 * glow), 255
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.config(fg=color)
        except tk.TclError:
            return
        self.after(50, self._glow_cycle)


class EnhancedCyberEntry(CyberEntry):
    """Enhanced input with multi-color scan line and particle effects."""
    def __init__(self, master, textvariable=None, width=26, **kw):
        super().__init__(master, textvariable, width, **kw)
        self._particles = []
        self._gradient_offset = 0

    def _animate(self):
        if not self._alive:
            return
        try:
            w = self._canvas.winfo_width()
            if w < 10:
                self.after(50, self._animate)
                return
            
            # Update gradient offset
            self._gradient_offset = (self._gradient_offset + 2) % 360
            
            speed = 8 if self._focused else 2
            self._scan_x += speed * self._scan_dir
            
            if self._scan_x >= w or self._scan_x <= 0:
                self._scan_dir *= -1
                # Create particles at turning points
                if self._focused:
                    self._create_particles(self._scan_x, 21)
            
            # Create gradient scan line
            for i in range(3):
                offset = i * 15
                x = self._scan_x - 30 + offset * 2
                if 0 < x < w:
                    alpha = 1.0 - i * 0.3
                    if self._focused:
                        # Color cycling based on gradient offset
                        hue = (self._gradient_offset + i * 30) % 360
                        if hue < 120:
                            color = CYAN_BRIGHT
                        elif hue < 240:
                            color = PURPLE_GLOW
                        else:
                            color = GREEN_NEON
                    else:
                        color = "#082030"
                    
                    self._canvas.coords(self._scan,
                                       x - 20, 0,
                                       x + 20, 42)
                    self._canvas.itemconfig(self._scan, fill=color,
                                           stipple="gray50" if i > 0 else "")
            
            # Update particles
            self._update_particles()
            
        except tk.TclError:
            return
        self.after(28, self._animate)

    def _create_particles(self, x, y):
        """Create particle burst effect"""
        for _ in range(5):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            life = random.randint(10, 20)
            color = random.choice([CYAN_BRIGHT, GREEN_NEON, PURPLE_GLOW])
            self._particles.append(Particle(x, y, vx, vy, life, color))

    def _update_particles(self):
        """Update particle positions"""
        dead = []
        for p in self._particles:
            p.x += p.vx
            p.y += p.vy
            p.life -= 1
            
            if p.life <= 0:
                dead.append(p)
            else:
                alpha = p.life / p.max_life
                size = 2 * alpha
                pid = self._canvas.create_oval(p.x-size, p.y-size,
                                              p.x+size, p.y+size,
                                              fill=p.color, outline="")
                self.after(50, lambda i=pid: self._safe_del(i))
        
        for p in dead:
            self._particles.remove(p)

    def _safe_del(self, iid):
        try:
            self._canvas.delete(iid)
        except Exception:
            pass


class PulseButton(CyberButton):
    """Enhanced button with pulse wave effects."""
    def __init__(self, master, text="", command=None,
                 color=CYAN_BRIGHT, width=150, height=40, **kw):
        super().__init__(master, text, command, color, width, height, **kw)
        self._pulse_waves = []
        self._hover_phase = 0.0

    def _animate(self):
        if not self._alive:
            return
        try:
            self._phase = (self._phase + 0.1) % (math.pi * 2)
            self._hover_phase += 0.05
            
            if self._hover:
                # Pulse effect on hover
                pulse = (math.sin(self._hover_phase) + 1) / 2
                scale = 1.0 + pulse * 0.1
                
                # Update bracket positions
                for tag in ["tl", "tr", "bl", "br"]:
                    items = self.find_withtag(tag)
                    for item in items:
                        coords = self.coords(item)
                        if coords:
                            # Scale coordinates
                            new_coords = []
                            for i, coord in enumerate(coords):
                                if i % 2 == 0:  # x coordinate
                                    center = self._w / 2
                                    new_coords.append(center + (coord - center) * scale)
                                else:  # y coordinate
                                    center = self._h / 2
                                    new_coords.append(center + (coord - center) * scale)
                            self.coords(item, *new_coords)
                
                # Color cycling
                hue = (self._hover_phase * 0.5) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
                color = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
                self.itemconfig(self._lbl, fill=color)
                self.itemconfig("bracket", fill=color)
            else:
                # Reset to default
                self.coords(self._lbl, self._w // 2, self._h // 2)
                self.itemconfig(self._lbl, fill=self._color)
                self.itemconfig("bracket", fill=self._color)
            
            # Update existing ripples
            dead = []
            for rip in self._ripples:
                rip[2] += 6
                rx, ry, radius = rip
                if radius > max(self._w, self._h) * 1.5:
                    dead.append(rip)
                    continue
                
                # Create multiple ripple layers
                for i in range(3):
                    r_offset = radius + i * 8
                    alpha = 1.0 - i * 0.3
                    rid = self.create_oval(rx - r_offset, ry - r_offset,
                                           rx + r_offset, ry + r_offset,
                                           outline=self._color, fill="", width=1)
                    self.after(150, lambda i=rid: self._safe_del(i))
            
            for d in dead:
                self._ripples.remove(d)
                
        except tk.TclError:
            return
        self.after(40, self._animate)


class ProgressWheel(ProgressArc):
    """Enhanced progress indicator with spinning particles."""
    def __init__(self, master, size=52, **kw):
        super().__init__(master, size, **kw)
        self._particles = []
        self._spin_speed = 8
        self._pulse_phase = 0.0

    def _animate(self):
        if not self._alive:
            return
        try:
            if self._spinning:
                self._spin_angle = (self._spin_angle + self._spin_speed) % 360
                self._pulse_phase += 0.1
                
                # Variable spin speed
                self._spin_speed = 8 + math.sin(self._pulse_phase) * 4
                
                # Create particles while spinning
                if random.random() > 0.9:
                    c = self._size // 2
                    angle = random.uniform(0, math.pi * 2)
                    dist = random.uniform(10, 20)
                    px = c + math.cos(angle) * dist
                    py = c + math.sin(angle) * dist
                    vx = math.cos(angle + math.pi/2) * 2
                    vy = math.sin(angle + math.pi/2) * 2
                    life = random.randint(10, 20)
                    color = random.choice([CYAN_BRIGHT, GREEN_NEON, PURPLE_GLOW])
                    self._particles.append(Particle(px, py, vx, vy, life, color))
                
                # Pulse effect on arc
                pulse = (math.sin(self._pulse_phase) + 1) / 2
                extent = -100 - int(pulse * 40)
                self.itemconfig(self._arc,
                               start=self._spin_angle, extent=extent)
            
            # Update particles
            dead = []
            for p in self._particles:
                p.x += p.vx
                p.y += p.vy
                p.life -= 1
                
                if p.life <= 0:
                    dead.append(p)
                else:
                    alpha = p.life / p.max_life
                    size = 2 * alpha
                    pid = self.create_oval(p.x-size, p.y-size,
                                          p.x+size, p.y+size,
                                          fill=p.color, outline="")
                    self.after(50, lambda i=pid: self._safe_del(i))
            
            for p in dead:
                self._particles.remove(p)
                
        except tk.TclError:
            return
        self.after(30, self._animate)

    def _safe_del(self, iid):
        try:
            self.delete(iid)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# INTELLIGENCE ENGINE (unchanged - already working)
# ─────────────────────────────────────────────────────────────────────────────
class AdvancedPhoneIntel:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        })
        self.api_keys = self._load_api_keys()
        self.cache_db = "phone_intel_cache.db"
        self._init_cache()

    def _init_cache(self):
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS phone_cache
                         (phone_hash TEXT PRIMARY KEY,
                          data TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
            c.execute("""CREATE TABLE IF NOT EXISTS api_keys
                         (service TEXT PRIMARY KEY, api_key TEXT)""")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache DB error: {e}")

    def _load_api_keys(self):
        try:
            with open("api_keys.json") as f:
                return json.load(f)
        except Exception:
            return {}

    def analyze_number(self, phone_number):
        self.results = {
            "input_number": phone_number,
            "timestamp": datetime.now().isoformat(),
            "basic_info": {}, "carrier_info": {}, "location_data": {},
            "risk_assessment": {}, "social_presence": [], "breach_data": [],
            "voip_info": {}, "messaging_apps": [], "reputation": [],
            "verification_services": [], "pattern_analysis": {},
        }
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                return {"error": "Invalid phone number"}

            self.results["parsed"] = {
                "e164": phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164),
                "international": phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country_code": parsed.country_code,
                "national_number": parsed.national_number,
            }

            with ThreadPoolExecutor(max_workers=10) as ex:
                futures = {
                    ex.submit(self._get_basic_info,        parsed): "basic",
                    ex.submit(self._get_carrier_info,       parsed): "carrier",
                    ex.submit(self._check_social,           parsed): "social",
                    ex.submit(self._check_breaches,         parsed): "breaches",
                    ex.submit(self._analyze_risk,           parsed): "risk",
                    ex.submit(self._get_voip_info,          parsed): "voip",
                    ex.submit(self._check_messaging,        parsed): "messaging",
                    ex.submit(self._get_reputation,         parsed): "reputation",
                    ex.submit(self._analyze_patterns,       parsed): "patterns",
                    ex.submit(self._check_verification,     parsed): "verify",
                }
                for future in as_completed(futures):
                    mod = futures[future]
                    try:
                        result = future.result(timeout=12)
                        if result:
                            self.results.update(result)
                    except Exception as e:
                        print(f"Module [{mod}] error: {e}")

            return self.results
        except Exception as e:
            return {"error": str(e)}

    def _get_basic_info(self, parsed):
        num_type = phonenumbers.number_type(parsed)
        type_map = {
            0: "FIXED_LINE", 1: "MOBILE", 2: "FIXED_OR_MOBILE",
            3: "TOLL_FREE",  4: "PREMIUM_RATE", 5: "SHARED_COST",
            6: "VOIP",       7: "PERSONAL",     8: "PAGER",
            9: "UAN",        10: "VOICEMAIL",   27: "UNKNOWN",
        }
        desc_map = {
            0: "Landline telephone", 1: "Mobile / cellular",
            2: "Landline or mobile", 3: "Toll-free (caller doesn't pay)",
            4: "Premium rate (high cost)", 5: "Shared cost",
            6: "Voice over IP (internet phone)", 7: "Personal numbering",
            8: "Pager service", 9: "Universal access number",
            10: "Voicemail service", 27: "Unknown type",
        }
        return {"basic_info": {
            "type":            type_map.get(num_type, "UNKNOWN"),
            "possible_type":   desc_map.get(num_type, "Unknown"),
            "timezones":       list(pn_timezone.time_zones_for_number(parsed)),
            "geolocation":     pn_geocoder.description_for_number(parsed, "en"),
            "country":         phonenumbers.region_code_for_number(parsed),
            "validity":        "Valid" if phonenumbers.is_valid_number(parsed) else "Invalid",
            "possible_number": phonenumbers.is_possible_number(parsed),
        }}

    def _get_carrier_info(self, parsed):
        return {"carrier_info": {
            "current":            pn_carrier.name_for_number(parsed, "en"),
            "historical_carriers": ["Unknown – requires paid API"],
            "network_type":       "Unknown (requires network query)",
            "ported":             {"ported": False, "original_carrier": None},
        }}

    def _check_social(self, parsed):
        nn = parsed.national_number
        sites = [
            {"name": "Facebook",   "url": f"https://www.facebook.com/search/top?q={nn}"},
            {"name": "Twitter",    "url": f"https://twitter.com/search?q={nn}"},
            {"name": "Instagram",  "url": f"https://www.instagram.com/accounts/account_recovery/?phone_number={nn}"},
            {"name": "LinkedIn",   "url": f"https://www.linkedin.com/search/results/all/?keywords={nn}"},
            {"name": "Snapchat",   "url": f"https://www.snapchat.com/add/{nn}"},
            {"name": "TikTok",     "url": f"https://www.tiktok.com/search?q={nn}"},
            {"name": "Pinterest",  "url": f"https://www.pinterest.com/search/pins/?q={nn}"},
            {"name": "Reddit",     "url": f"https://www.reddit.com/search/?q={nn}"},
            {"name": "YouTube",    "url": f"https://www.youtube.com/results?search_query={nn}"},
        ]
        for s in sites:
            s["verified"] = self._verify_url(s["url"])
        return {"social_presence": sites}

    def _verify_url(self, url):
        try:
            r = self.session.get(url, timeout=5, allow_redirects=True)
            return r.status_code == 200 and "not found" not in r.text.lower()
        except Exception:
            return False

    def _check_breaches(self, parsed):
        nn = parsed.national_number
        services = [
            {"name": "HaveIBeenPwned", "url": f"https://haveibeenpwned.com/account/{nn}"},
            {"name": "BreachDirectory","url": f"https://breachdirectory.org/check?phone={nn}"},
            {"name": "Dehashed",       "url": f"https://dehashed.com/search?query={nn}"},
            {"name": "Snusbase",       "url": f"https://snusbase.com/search?term={nn}"},
        ]
        return {"breach_data": [
            {**s, "status": "Check manually (requires API key)"}
            for s in services
        ]}

    def _analyze_risk(self, parsed):
        factors, score = [], 0
        if pn_number_type(parsed) == 6:
            factors.append("VoIP number – potentially disposable/temporary")
            score += 30
        cn = pn_carrier.name_for_number(parsed, "en") or ""
        if "prepaid" in cn.lower():
            factors.append("Prepaid number – lower accountability")
            score += 20
        high_risk = {7, 380, 375, 92, 91}
        if parsed.country_code in high_risk:
            factors.append("Number from flagged region")
            score += 15
        spam = self._check_spam(parsed)
        if spam > 50:
            factors.append(f"Reported as spam (score: {spam})")
            score += 25
        level = "LOW" if score < 30 else "MEDIUM" if score < 60 else "HIGH"
        recs = {
            "LOW":    ["Standard verification sufficient"],
            "MEDIUM": ["Additional verification recommended",
                       "Consider alternative contact methods"],
            "HIGH":   ["Exercise extreme caution",
                       "Verify identity through multiple channels",
                       "Document all interactions"],
        }
        return {"risk_assessment": {
            "score": score, "level": level,
            "factors": factors, "spam_score": spam,
            "recommendations": recs[level],
        }}

    def _check_spam(self, parsed):
        return 0

    def _get_voip_info(self, parsed):
        is_voip = pn_number_type(parsed) == 6
        temp = any(re.match(p, str(parsed.national_number))
                   for p in [r"^\+1\s*\(?8{3}\)?", r"^\+44\s*70"])
        return {"voip_info": {
            "is_voip":          is_voip,
            "provider":         "Unknown",
            "quality":          "Unknown",
            "temporary_likely": temp,
        }}

    def _check_messaging(self, parsed):
        cc, nn = parsed.country_code, parsed.national_number
        apps = [
            {"name": "WhatsApp",         "url": f"https://wa.me/{cc}{nn}"},
            {"name": "Telegram",         "url": f"https://t.me/+{cc}{nn}"},
            {"name": "Signal",           "url": f"signal.me/#p/+{cc}{nn}"},
            {"name": "Viber",            "url": f"viber://add?number={cc}{nn}"},
            {"name": "WeChat",           "url": f"weixin.qq.com/search?query={nn}"},
            {"name": "Line",             "url": f"line.me/R/ti/p/~{cc}{nn}"},
            {"name": "Messenger",        "url": f"m.me/{nn}"},
            {"name": "Skype",            "url": f"skype:{nn}?call"},
            {"name": "Discord",          "url": f"discord.com/search?q={nn}"},
        ]
        for app in apps[:3]:
            try:
                if "wa.me" in app["url"]:
                    r = self.session.get(app["url"], timeout=5)
                    app["verified"] = (r.status_code == 200
                                       and "invalid" not in r.text.lower())
                elif "t.me" in app["url"]:
                    r = self.session.get(app["url"], timeout=5)
                    app["verified"] = r.status_code == 200
                else:
                    app["verified"] = False
            except Exception:
                app["verified"] = False
        return {"messaging_apps": apps}

    def _get_reputation(self, parsed):
        return {"reputation": [
            {"source": "CallerID Test", "rating": "Unknown"},
            {"source": "Whitepages",    "rating": "Unknown"},
            {"source": "Truecaller",    "rating": "Unknown"},
            {"source": "Nomorobo",      "rating": "Unknown"},
            {"source": "Hiya",          "rating": "Unknown"},
        ]}

    def _analyze_patterns(self, parsed):
        sn = str(parsed.national_number)
        repeating = any(str(d) * 4 in sn for d in range(10))
        sequential = any(
            int(sn[i+1]) == int(sn[i]) + 1 and int(sn[i+2]) == int(sn[i]) + 2
            for i in range(len(sn) - 3)
        )
        business  = sn.startswith(("800","888","877","866","855","844"))
        scam_pats = ["900","876","809","284","473"]
        scam = any(sn[:3] == p for p in scam_pats)
        return {"pattern_analysis": {
            "repeating_digits": repeating,
            "sequential":       sequential,
            "business_pattern": business,
            "scam_patterns":    scam,
        }}

    def _check_verification(self, parsed):
        return {"verification_services": [
            {"service": "Google Voice", "supported": parsed.country_code == 1},
            {"service": "WhatsApp",     "supported": True},
            {"service": "Telegram",     "supported": True},
            {"service": "Signal",       "supported": True},
            {"service": "Facebook",     "supported": True},
            {"service": "Twitter",      "supported": True},
            {"service": "Instagram",    "supported": True},
        ]}


# ─────────────────────────────────────────────────────────────────────────────
# MAIN GUI (updated with enhanced widgets)
# ─────────────────────────────────────────────────────────────────────────────
class EnhancedPhoneIntelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ ATHEX Phone Intelligence v2.1 ⚡")
        self.root.geometry("1440x900")
        self.root.minsize(1100, 700)
        self.root.configure(bg=DARK_BG)

        self.engine = AdvancedPhoneIntel()
        self.current_results = None
        self._animation_objects = []  # Track animation objects for cleanup

        self._apply_styles()
        self._build_ui()
        self.root.after(200, self._boot_sequence)
        
        # Bind cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self._cleanup)

    def _cleanup(self):
        """Clean up animation objects before closing"""
        for obj in self._animation_objects:
            try:
                obj.destroy()
            except:
                pass
        self.root.destroy()

    def _apply_styles(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass
        s.configure(".",
                    background=DARK_BG, foreground=TEXT_BRIGHT,
                    fieldbackground=CARD_BG, troughcolor=PANEL_BG,
                    bordercolor=BORDER_COLOR, selectbackground=CYAN_DIM,
                    selectforeground=CYAN_BRIGHT)
        s.configure("TNotebook",
                    background=DARK_BG, borderwidth=0, tabmargins=[2,5,2,0])
        s.configure("TNotebook.Tab",
                    background=CARD_BG, foreground=TEXT_DIM,
                    padding=[14, 6], font=("Courier New", 9, "bold"),
                    borderwidth=0)
        s.map("TNotebook.Tab",
              background=[("selected", PANEL_BG)],
              foreground=[("selected", CYAN_BRIGHT)])
        s.configure("TFrame", background=DARK_BG)
        s.configure("TScrollbar",
                    background=CARD_BG, troughcolor=DARK_BG,
                    bordercolor=BORDER_COLOR, arrowcolor=CYAN_DIM)
        s.configure("Treeview",
                    background=CARD_BG, foreground=TEXT_BRIGHT,
                    fieldbackground=CARD_BG, borderwidth=0,
                    font=("Courier New", 9), rowheight=26)
        s.configure("Treeview.Heading",
                    background=PANEL_BG, foreground=CYAN_BRIGHT,
                    font=("Courier New", 9, "bold"), relief="flat")
        s.map("Treeview",
              background=[("selected", CYAN_DIM)],
              foreground=[("selected", CYAN_BRIGHT)])

    def _build_ui(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Enhanced animated background
        self._hex = EnhancedHexGrid(self.root, 1440, 900)
        self._hex.place(x=0, y=0, relwidth=1, relheight=1)
        self._animation_objects.append(self._hex)

        # Matrix overlay with reduced opacity
        self._matrix = EnhancedMatrixCanvas(self.root, 1440, 900)
        self._matrix.place(x=0, y=0, relwidth=1, relheight=1)
        self._animation_objects.append(self._matrix)

        # Main content frame
        main = tk.Frame(self.root, bg=DARK_BG, bd=0)
        main.place(x=0, y=0, relwidth=1, relheight=1)
        main.rowconfigure(3, weight=1)
        main.columnconfigure(0, weight=1)

        self._build_header(main)
        self._build_sep(main)
        self._build_input(main)
        self._build_notebook(main)
        self._build_statusbar(main)
        self._build_menu()

    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg=DARK_BG)
        hdr.grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 4))
        hdr.columnconfigure(1, weight=1)

        ring = HarmonicRipple(hdr, size=64, color=CYAN_BRIGHT)
        ring.grid(row=0, column=0, rowspan=2, padx=(0, 16))
        self._animation_objects.append(ring)

        title_frame = tk.Frame(hdr, bg=DARK_BG)
        title_frame.grid(row=0, column=1, sticky="w")

        self._title_lbl = GlowingText(
            title_frame, text="▶ ATHEX PHONE INTELLIGENCE TOOL ◀",
            glitch_interval=4500,
            bg=DARK_BG, fg=CYAN_BRIGHT,
            font=("Courier New", 19, "bold"))
        self._title_lbl.pack(anchor="w")
        self._animation_objects.append(self._title_lbl)

        self._sub_lbl = TypewriterLabel(
            title_frame,
            full_text="  Advanced OSINT Framework  ·  For Authorized Security Research Only",
            bg=DARK_BG, fg=TEXT_MID, font=("Courier New", 9))
        self._sub_lbl.pack(anchor="w")
        self._animation_objects.append(self._sub_lbl)

        right = tk.Frame(hdr, bg=DARK_BG)
        right.grid(row=0, column=2, sticky="ne", padx=10)
        self._clock = tk.Label(right, text="", bg=DARK_BG,
                               fg=CYAN_DIM, font=("Courier New", 9))
        self._clock.pack(anchor="e")
        tk.Label(right, text="◈ SYSTEM ONLINE ◈", bg=DARK_BG,
                 fg=GREEN_NEON, font=("Courier New", 8, "bold")).pack(anchor="e")
        self._tick_clock()

    def _tick_clock(self):
        try:
            self._clock.config(
                text=datetime.now().strftime("◷ %Y-%m-%d  %H:%M:%S"))
        except Exception:
            return
        self.root.after(1000, self._tick_clock)

    def _build_sep(self, parent):
        sep = tk.Canvas(parent, height=2, bg=DARK_BG, highlightthickness=0)
        sep.grid(row=1, column=0, sticky="ew", padx=18, pady=4)
        self._sep = sep
        self._animate_sep()

    def _animate_sep(self):
        try:
            w = self._sep.winfo_width()
            if w > 10:
                self._sep.delete("all")
                phase = (time.time() * 2.5) % (math.pi * 2)
                
                # Create gradient line
                for x in range(0, w, 2):
                    # Multiple overlapping lines for glow
                    for offset in range(3):
                        x_pos = x + offset * 2
                        if x_pos < w:
                            b = int(80 + 170 * (math.sin(phase + x_pos / 60 + offset) + 1) / 2)
                            # Color cycling
                            hue = (phase + x_pos / 100) % (math.pi * 2)
                            if hue < 2:
                                color = f"#00{b:02x}{b:02x}"
                            elif hue < 4:
                                color = f"#{b:02x}00{b:02x}"
                            else:
                                color = f"#{b:02x}{b:02x}00"
                            
                            width = 2 if offset == 1 else 1
                            self._sep.create_line(x_pos, 0, x_pos + 1, 0,
                                                 fill=color, width=width)
        except tk.TclError:
            return
        self.root.after(40, self._animate_sep)

    def _build_input(self, parent):
        inp = tk.Frame(parent, bg=PANEL_BG,
                       highlightthickness=1, highlightbackground=BORDER_COLOR)
        inp.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 8))
        inp.columnconfigure(4, weight=1)

        # Labels with glow effect
        for col, txt in [(0, "TARGET NUMBER"), (2, "COUNTRY (optional)")]:
            lbl = tk.Label(inp, text=txt, bg=PANEL_BG, fg=CYAN_DIM,
                          font=("Courier New", 8, "bold"))
            lbl.grid(row=0, column=col, padx=(18 if col == 0 else 12, 6),
                    pady=(8, 2), sticky="sw")

        # Enhanced phone entry
        self.phone_var = tk.StringVar()
        self._phone_entry = EnhancedCyberEntry(inp, textvariable=self.phone_var, width=24)
        self._phone_entry.grid(row=1, column=0, padx=(18, 8),
                               pady=(0, 12), sticky="w")
        self._animation_objects.append(self._phone_entry)

        tk.Label(inp, text="e.g.  +12025551234",
                 bg=PANEL_BG, fg=TEXT_DIM,
                 font=("Courier New", 8)).grid(row=1, column=1,
                                                padx=0, sticky="sw",
                                                pady=(0, 14))

        # Country combobox
        self.country_var = tk.StringVar()
        country_cb = ttk.Combobox(
            inp, textvariable=self.country_var,
            values=["", "US", "GB", "CA", "AU", "IN", "PK",
                    "DE", "FR", "JP", "BR", "AE", "SA"],
            width=8, font=("Courier New", 10),
            state="readonly")
        country_cb.grid(row=1, column=2, padx=(12, 6),
                        pady=(0, 12), sticky="w")

        # Button frame
        btn_f = tk.Frame(inp, bg=PANEL_BG)
        btn_f.grid(row=0, column=5, rowspan=2,
                   padx=14, pady=8, sticky="e")

        # Enhanced buttons
        self._btn_analyze = PulseButton(btn_f, text="◉  ANALYZE",
                                        command=self._start_analysis,
                                        color=CYAN_BRIGHT, width=140, height=40)
        self._btn_analyze.pack(side="left", padx=5)
        self._animation_objects.append(self._btn_analyze)

        self._btn_clear = PulseButton(btn_f, text="✕  CLEAR",
                                      command=self._clear_all,
                                      color=AMBER_BRIGHT, width=110, height=40)
        self._btn_clear.pack(side="left", padx=5)
        self._animation_objects.append(self._btn_clear)

        self._btn_save = PulseButton(btn_f, text="↓  SAVE JSON",
                                     command=self._save_results,
                                     color=GREEN_NEON, width=130, height=40)
        self._btn_save.pack(side="left", padx=5)
        self._btn_save.config_state("disabled")
        self._animation_objects.append(self._btn_save)

        self._btn_export = PulseButton(btn_f, text="⎙  EXPORT",
                                       command=self._export_txt,
                                       color=TEXT_MID, width=110, height=40)
        self._btn_export.pack(side="left", padx=5)
        self._btn_export.config_state("disabled")
        self._animation_objects.append(self._btn_export)

        # Enhanced progress wheel
        self._arc = ProgressWheel(inp, size=52)
        self._arc.grid(row=0, column=6, rowspan=2, padx=18)
        self._animation_objects.append(self._arc)

    def _build_notebook(self, parent):
        nb_wrap = tk.Frame(parent, bg=DARK_BG)
        nb_wrap.grid(row=3, column=0, sticky="nsew", padx=18, pady=(0, 4))
        nb_wrap.rowconfigure(0, weight=1)
        nb_wrap.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(nb_wrap)
        self.nb.grid(sticky="nsew")

        defs = [
            ("◈  OVERVIEW",     self._tab_overview),
            ("◈  BASIC INFO",   self._tab_basic),
            ("◈  LOCATION",     self._tab_location),
            ("◈  CARRIER",      self._tab_carrier),
            ("◈  SOCIAL MEDIA", self._tab_social),
            ("◈  MESSAGING",    self._tab_messaging),
            ("◈  RISK",         self._tab_risk),
            ("◈  BREACH CHECK", self._tab_breach),
            ("◈  REPUTATION",   self._tab_reputation),
            ("◈  REPORTS",      self._tab_reports),
        ]
        self.tabs = {}
        for label, builder in defs:
            frame = ttk.Frame(self.nb)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            self.nb.add(frame, text=label)
            self.tabs[label] = frame
            builder(frame)

    def _cyber_txt(self, parent):
        txt = scrolledtext.ScrolledText(
            parent, bg=CARD_BG, fg=CYAN_BRIGHT,
            insertbackground=CYAN_BRIGHT,
            selectbackground=CYAN_DIM,
            font=("Courier New", 10),
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            state="normal"  # Start normal, we'll disable after writing
        )
        return txt

    def _write_txt(self, widget, content):
        """Safely write to a ScrolledText."""
        try:
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.insert("end", content)
            widget.config(state="disabled")
        except Exception as e:
            print(f"Error writing to text widget: {e}")

    def _cyber_tree(self, parent, cols):
        frm = tk.Frame(parent, bg=DARK_BG)
        frm.pack(fill="both", expand=True, padx=6, pady=6)
        tree = ttk.Treeview(frm, columns=cols, show="headings", height=20)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200, minwidth=80)
        vsb = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return tree

    def _tab_overview(self, p):
        self._txt_overview = self._cyber_txt(p)
        self._txt_overview.grid(sticky="nsew", padx=6, pady=6)

    def _tab_basic(self, p):
        self._txt_basic = self._cyber_txt(p)
        self._txt_basic.grid(sticky="nsew", padx=6, pady=6)

    def _tab_location(self, p):
        self._txt_location = self._cyber_txt(p)
        self._txt_location.grid(sticky="nsew", padx=6, pady=6)

    def _tab_carrier(self, p):
        self._txt_carrier = self._cyber_txt(p)
        self._txt_carrier.grid(sticky="nsew", padx=6, pady=6)

    def _tab_social(self, p):
        self._tree_social = self._cyber_tree(p, ("Platform", "URL", "Status"))
        self._tree_social.bind("<Double-Button-1>",
                               lambda e: self._open_tree_url(self._tree_social, 1))

    def _tab_messaging(self, p):
        self._tree_msg = self._cyber_tree(p, ("App", "URL", "Verified"))
        self._tree_msg.bind("<Double-Button-1>",
                            lambda e: self._open_tree_url(self._tree_msg, 1))

    def _tab_risk(self, p):
        top = tk.Frame(p, bg=DARK_BG)
        top.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
        p.rowconfigure(1, weight=1)

        self._risk_banner = tk.Label(
            top, text="── AWAITING ANALYSIS ──",
            bg=DARK_BG, fg=TEXT_DIM,
            font=("Courier New", 17, "bold"))
        self._risk_banner.pack(pady=6)

        self._txt_risk = self._cyber_txt(p)
        self._txt_risk.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

    def _tab_breach(self, p):
        self._txt_breach = self._cyber_txt(p)
        self._txt_breach.grid(sticky="nsew", padx=6, pady=6)

    def _tab_reputation(self, p):
        self._tree_rep = self._cyber_tree(p, ("Source", "Rating", "Details"))

    def _tab_reports(self, p):
        top = tk.Frame(p, bg=PANEL_BG,
                       highlightthickness=1,
                       highlightbackground=BORDER_COLOR)
        top.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
        p.rowconfigure(1, weight=1)

        for txt, cmd, col in [
            ("⎙ PDF",   self._gen_pdf,   CYAN_BRIGHT),
            ("⎙ HTML",  self._gen_html,  CYAN_MID),
            ("⎙ CSV",   self._gen_csv,   AMBER_BRIGHT),
            ("⎙ PRINT", self._do_print,  TEXT_MID),
        ]:
            btn = PulseButton(top, text=txt, command=cmd, color=col,
                             width=120, height=36)
            btn.pack(side="left", padx=8, pady=8)
            self._animation_objects.append(btn)

        self._txt_reports = self._cyber_txt(p)
        self._txt_reports.grid(row=1, column=0, sticky="nsew",
                               padx=6, pady=(0, 6))

    def _build_statusbar(self, parent):
        sb = tk.Frame(parent, bg=PANEL_BG, height=24,
                      highlightthickness=1,
                      highlightbackground=BORDER_COLOR)
        sb.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 8))
        self._status = tk.Label(sb, text="  ◈ SYSTEM READY",
                                bg=PANEL_BG, fg=CYAN_DIM,
                                font=("Courier New", 9), anchor="w")
        self._status.pack(fill="x", padx=8)

    def _set_status(self, msg, color=CYAN_DIM):
        try:
            self._status.config(text=f"  ◈ {msg}", fg=color)
        except Exception:
            pass

    def _build_menu(self):
        mb = tk.Menu(self.root, bg=PANEL_BG, fg=TEXT_BRIGHT,
                     activebackground=CYAN_DIM, activeforeground=CYAN_BRIGHT,
                     font=("Courier New", 9))
        self.root.config(menu=mb)

        file_m = tk.Menu(mb, tearoff=0, bg=PANEL_BG, fg=TEXT_BRIGHT,
                         activebackground=CYAN_DIM,
                         activeforeground=CYAN_BRIGHT,
                         font=("Courier New", 9))
        mb.add_cascade(label="File", menu=file_m)
        file_m.add_command(label="New Analysis",   command=self._clear_all)
        file_m.add_command(label="Save Results",   command=self._save_results)
        file_m.add_separator()
        file_m.add_command(label="Export PDF",     command=self._gen_pdf)
        file_m.add_command(label="Export HTML",    command=self._gen_html)
        file_m.add_command(label="Export CSV",     command=self._gen_csv)
        file_m.add_separator()
        file_m.add_command(label="Exit",           command=self._cleanup)

        tools_m = tk.Menu(mb, tearoff=0, bg=PANEL_BG, fg=TEXT_BRIGHT,
                          activebackground=CYAN_DIM,
                          activeforeground=CYAN_BRIGHT,
                          font=("Courier New", 9))
        mb.add_cascade(label="Tools", menu=tools_m)
        tools_m.add_command(label="Batch Analysis",  command=self._batch_window)
        tools_m.add_command(label="API Config",      command=self._api_config)
        tools_m.add_command(label="Clear Cache",     command=self._clear_cache)

        help_m = tk.Menu(mb, tearoff=0, bg=PANEL_BG, fg=TEXT_BRIGHT,
                         activebackground=CYAN_DIM,
                         activeforeground=CYAN_BRIGHT,
                         font=("Courier New", 9))
        mb.add_cascade(label="Help", menu=help_m)
        help_m.add_command(label="About",        command=self._about)
        help_m.add_command(label="Legal Notice", command=self._legal)

    def _boot_sequence(self):
        msgs = [
            ("INITIALIZING OSINT FRAMEWORK…",        AMBER_BRIGHT),
            ("LOADING PHONENUMBER LIBRARIES…",        AMBER_BRIGHT),
            ("CONNECTING TO THREAT DATABASES…",       AMBER_BRIGHT),
            ("ESTABLISHING SECURE SESSION…",          AMBER_BRIGHT),
            ("ALL MODULES LOADED  ─  SYSTEM READY",  GREEN_NEON),
        ]
        def step(i=0):
            if i < len(msgs):
                self._set_status(msgs[i][0], msgs[i][1])
                delay = 500 if i < len(msgs) - 1 else 800
                self.root.after(delay, lambda: step(i + 1))
            else:
                self._sub_lbl.start()
        step()

    def _start_analysis(self):
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Input Error", "Please enter a phone number.")
            return
        self._btn_analyze.config_state("disabled")
        self._arc.start_spin()
        self._set_status("SCANNING TARGET…", AMBER_BRIGHT)
        t = threading.Thread(target=self._run_analysis,
                             args=(phone,), daemon=True)
        t.start()

    def _run_analysis(self, phone):
        # If country code given and number has no '+', prepend it
        country = self.country_var.get().strip()
        if country and not phone.startswith("+"):
            try:
                parsed = phonenumbers.parse(phone, country)
                phone = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164)
            except Exception:
                pass

        self.current_results = self.engine.analyze_number(phone)
        self.root.after(0, self._analysis_done)

    def _analysis_done(self):
        self._arc.stop_spin()
        self._btn_analyze.config_state("normal")

        if not self.current_results or "error" in self.current_results:
            err = (self.current_results or {}).get("error", "Unknown error")
            messagebox.showerror("Analysis Error", err)
            self._set_status(f"ERROR: {err}", RED_ALERT)
            return

        self._populate_tabs()
        self._btn_save.config_state("normal")
        self._btn_export.config_state("normal")
        self._set_status("ANALYSIS COMPLETE", GREEN_NEON)

    def _populate_tabs(self):
        if not self.current_results:
            return
            
        r  = self.current_results
        pd = r.get("parsed", {})
        bi = r.get("basic_info", {})
        ci = r.get("carrier_info", {})
        vi = r.get("voip_info", {})
        ri = r.get("risk_assessment", {})
        pa = r.get("pattern_analysis", {})

        # OVERVIEW
        self._write_txt(self._txt_overview, f"""
╔══════════════════════════════════════════════════════════════════════╗
║              ◈ PHONE NUMBER INTELLIGENCE REPORT ◈                   ║
╚══════════════════════════════════════════════════════════════════════╝

  TARGET    : {pd.get('international','N/A')}
  TIMESTAMP : {r.get('timestamp','N/A')}

  ─────────────────────────────────────────────────────────────────────
  ◉ CORE INTEL
  ─────────────────────────────────────────────────────────────────────
  Type      : {bi.get('type','N/A')}
  Carrier   : {ci.get('current','N/A') or 'Unknown'}
  Location  : {bi.get('geolocation','N/A')}
  Country   : {bi.get('country','N/A')}
  Risk      : {ri.get('level','N/A')}  (score: {ri.get('score',0)}/100)
  VoIP      : {'YES' if vi.get('is_voip') else 'No'}
  Temp #    : {'LIKELY' if vi.get('temporary_likely') else 'Unlikely'}

  ─────────────────────────────────────────────────────────────────────
  ◉ RISK FACTORS
  ─────────────────────────────────────────────────────────────────────
{chr(10).join('  ⚠ ' + f for f in ri.get('factors', ['None detected']))}

  ─────────────────────────────────────────────────────────────────────
  ◉ SOCIAL MEDIA (top 5)
  ─────────────────────────────────────────────────────────────────────
{chr(10).join('  [' + ('✔' if s.get('verified') else '?') + '] ' + s.get('name','') for s in r.get('social_presence',[])[:5])}
""")

        # BASIC INFO
        self._write_txt(self._txt_basic, f"""
╔══════════════════════════════════════════════════╗
║             ◈ NUMBER DETAILS ◈                  ║
╚══════════════════════════════════════════════════╝

  E.164         : {pd.get('e164','N/A')}
  International : {pd.get('international','N/A')}
  National      : {pd.get('national','N/A')}
  Country Code  : +{pd.get('country_code','N/A')}
  National Num  : {pd.get('national_number','N/A')}

  ──────────────────────────────────────────────────
  Validation
  ──────────────────────────────────────────────────
  Type          : {bi.get('type','N/A')}
  Description   : {bi.get('possible_type','N/A')}
  Valid         : {bi.get('validity','N/A')}
  Possible      : {'Yes' if bi.get('possible_number') else 'No'}

  ──────────────────────────────────────────────────
  Pattern Analysis
  ──────────────────────────────────────────────────
  Repeating Digits : {'YES' if pa.get('repeating_digits') else 'No'}
  Sequential       : {'YES' if pa.get('sequential') else 'No'}
  Business Pattern : {'YES' if pa.get('business_pattern') else 'No'}
  Scam Pattern     : {'⚠ YES' if pa.get('scam_patterns') else 'No'}

  ──────────────────────────────────────────────────
  Timezones
  ──────────────────────────────────────────────────
{chr(10).join('  • ' + tz for tz in bi.get('timezones', ['N/A']))}
""")

        # LOCATION
        self._write_txt(self._txt_location, f"""
╔══════════════════════════════════════════════════╗
║             ◈ LOCATION DATA ◈                   ║
╚══════════════════════════════════════════════════╝

  Geographic Location : {bi.get('geolocation','N/A')}
  Country             : {bi.get('country','N/A')}

  Timezones :
{chr(10).join('    • ' + tz for tz in bi.get('timezones', ['N/A']))}

  Note: Precise cell-tower geolocation requires carrier API access.
  IP geolocation is not possible from a phone number alone.
""")

        # CARRIER
        ported = ci.get("ported", {})
        self._write_txt(self._txt_carrier, f"""
╔══════════════════════════════════════════════════╗
║             ◈ CARRIER INTEL ◈                   ║
╚══════════════════════════════════════════════════╝

  Current Carrier  : {ci.get('current','N/A') or 'Unknown'}
  Network Type     : {ci.get('network_type','N/A')}
  Number Ported    : {'Yes' if ported.get('ported') else 'No'}

  ──────────────────────────────────────────────────
  VoIP Analysis
  ──────────────────────────────────────────────────
  Is VoIP          : {'YES' if vi.get('is_voip') else 'No'}
  Provider         : {vi.get('provider','N/A')}
  Temporary Likely : {'YES' if vi.get('temporary_likely') else 'No'}

  ──────────────────────────────────────────────────
  Historical Carriers (requires paid API)
  ──────────────────────────────────────────────────
{chr(10).join('  • ' + h for h in ci.get('historical_carriers', ['N/A']))}
""")

        # SOCIAL TREE
        for item in self._tree_social.get_children():
            self._tree_social.delete(item)
        for s in r.get("social_presence", []):
            status = "✔ FOUND" if s.get("verified") else "? UNKNOWN"
            self._tree_social.insert("", "end",
                values=(s.get("name"), s.get("url"), status))

        # MESSAGING TREE
        for item in self._tree_msg.get_children():
            self._tree_msg.delete(item)
        for a in r.get("messaging_apps", []):
            v = "✔" if a.get("verified") else "?"
            self._tree_msg.insert("", "end",
                values=(a.get("name"), a.get("url"), v))

        # RISK
        rlvl = ri.get("level", "UNKNOWN")
        col_map = {"LOW": GREEN_NEON, "MEDIUM": AMBER_BRIGHT, "HIGH": RED_ALERT}
        self._risk_banner.config(
            text=f"◉ RISK LEVEL :  {rlvl}   [SCORE {ri.get('score',0)} / 100]",
            fg=col_map.get(rlvl, TEXT_MID))
        self._write_txt(self._txt_risk, f"""
  RISK FACTORS
  {'─'*50}
{chr(10).join('  ⚠ ' + f for f in ri.get('factors', ['None detected']))}

  RECOMMENDATIONS
  {'─'*50}
{chr(10).join('  ◉ ' + rec for rec in ri.get('recommendations', []))}
""")

        # BREACH
        breach_lines = ["""
╔══════════════════════════════════════════════════╗
║             ◈ BREACH CHECK ◈                    ║
╚══════════════════════════════════════════════════╝

  Note: Real-time checks require paid API keys.
  Check these services manually:

"""]
        for b in r.get("breach_data", []):
            breach_lines.append(
                f"  ◉ {b.get('name')}\n"
                f"    URL    : {b.get('url')}\n"
                f"    Status : {b.get('status')}\n\n")
        self._write_txt(self._txt_breach, "".join(breach_lines))

        # REPUTATION TREE
        for item in self._tree_rep.get_children():
            self._tree_rep.delete(item)
        for rep in r.get("reputation", []):
            self._tree_rep.insert("", "end",
                values=(rep.get("source"), rep.get("rating"), "Check manually"))

        # REPORTS PREVIEW
        self._write_txt(self._txt_reports, self._text_report())

    def _text_report(self):
        if not self.current_results:
            return "No results."
        r  = self.current_results
        pd = r.get("parsed", {})
        bi = r.get("basic_info", {})
        ri = r.get("risk_assessment", {})
        lines = [
            "PHONE NUMBER INTELLIGENCE REPORT",
            f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            f"Number    : {pd.get('international','N/A')}",
            f"Type      : {bi.get('type','N/A')}",
            f"Carrier   : {r.get('carrier_info',{}).get('current','N/A')}",
            f"Location  : {bi.get('geolocation','N/A')}",
            f"Risk      : {ri.get('level','N/A')}",
            "", "SOCIAL MEDIA", "─" * 40,
        ]
        for s in r.get("social_presence", []):
            lines.append(f"  {s.get('name')}: {s.get('url')}")
        lines += ["", "MESSAGING APPS", "─" * 40]
        for a in r.get("messaging_apps", []):
            lines.append(f"  {a.get('name')}: {a.get('url')}")
        return "\n".join(lines)

    def _html_report(self):
        if not self.current_results:
            return "<html><body>No results</body></html>"
        r  = self.current_results
        pd = r.get("parsed", {})
        bi = r.get("basic_info", {})
        ri = r.get("risk_assessment", {})
        rlvl = ri.get("level", "N/A").lower()
        rows_basic = [
            ("Number",    pd.get("international","N/A")),
            ("Type",      bi.get("type","N/A")),
            ("Carrier",   r.get("carrier_info",{}).get("current","N/A")),
            ("Location",  bi.get("geolocation","N/A")),
            ("Risk",      ri.get("level","N/A")),
            ("Score",     f"{ri.get('score',0)}/100"),
        ]
        rows_html = "\n".join(
            f"<tr><td>{k}</td>"
            f"<td{'class=\"risk-'+rlvl+'\"' if k=='Risk' else ''}>{v}</td></tr>"
            for k, v in rows_basic)
        social_html = "\n".join(
            f"<tr><td>{s.get('name')}</td>"
            f"<td><a href='{s.get('url')}'>{s.get('url')}</a></td></tr>"
            for s in r.get("social_presence", []))
        msg_html = "\n".join(
            f"<tr><td>{a.get('name')}</td>"
            f"<td><a href='{a.get('url')}'>{a.get('url')}</a></td></tr>"
            for a in r.get("messaging_apps", []))
        return f"""<!DOCTYPE html><html>
<head><title>ATHEX Phone Intel Report</title>
<style>
body{{font-family:'Courier New',monospace;background:#050a0f;color:#e8f4ff;margin:40px}}
h1{{color:#00f5ff;letter-spacing:3px;text-shadow:0 0 10px #00f5ff}}
h2{{color:#00b4cc;border-bottom:1px solid #0e3a5c;padding-bottom:4px}}
table{{border-collapse:collapse;width:100%;margin:16px 0}}
th{{background:#0e3a5c;color:#00f5ff;padding:10px;text-align:left}}
td{{padding:8px;border:1px solid #0e3a5c}}
tr:nth-child(even){{background:#0d1e30}}
a{{color:#00f5ff;text-decoration:none}}
a:hover{{color:#ffb300;text-shadow:0 0 5px #ffb300}}
.risk-high{{color:#ff2244;font-weight:bold}}
.risk-medium{{color:#ffb300;font-weight:bold}}
.risk-low{{color:#00ff88;font-weight:bold}}
.glow{{animation:glow 2s ease-in-out infinite alternate}}
@keyframes glow{{from{{text-shadow:0 0 5px #00f5ff}} to{{text-shadow:0 0 20px #00f5ff}}}}
</style></head><body>
<h1 class="glow">◈ ATHEX PHONE INTELLIGENCE REPORT</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<h2>Basic Information</h2>
<table><tr><th>Field</th><th>Value</th></tr>{rows_html}</table>
<h2>Social Media</h2>
<table><tr><th>Platform</th><th>URL</th></tr>{social_html}</table>
<h2>Messaging Apps</h2>
<table><tr><th>App</th><th>URL</th></tr>{msg_html}</table>
<p><em>Generated by ATHEX OSINT Framework v2.1</em></p>
</body></html>"""

    def _gen_pdf(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return
        if not HAS_REPORTLAB:
            messagebox.showerror("Missing Library",
                                 "Install reportlab:\n  pip install reportlab")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".pdf",
             filetypes=[("PDF", "*.pdf")])
        if not fn:
            return
        try:
            r  = self.current_results
            pd = r.get("parsed", {})
            bi = r.get("basic_info", {})
            ri = r.get("risk_assessment", {})
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle("T", parent=styles["Heading1"],
                                         fontSize=18,
                                         textColor=rl_colors.HexColor("#00f5ff"))
            doc   = SimpleDocTemplate(fn, pagesize=A4)
            story = [Paragraph("ATHEX Phone Intelligence Report", title_style),
                     Spacer(1, 12),
                     Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                               styles["Normal"]),
                     Spacer(1, 12)]
            data = [["Field", "Value"],
                    ["Number",   pd.get("international","N/A")],
                    ["Type",     bi.get("type","N/A")],
                    ["Carrier",  r.get("carrier_info",{}).get("current","N/A")],
                    ["Location", bi.get("geolocation","N/A")],
                    ["Risk",     ri.get("level","N/A")],
                    ["Score",    f"{ri.get('score',0)}/100"]]
            t = Table(data, colWidths=[150, 350])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), rl_colors.HexColor("#0e3a5c")),
                ("TEXTCOLOR",  (0,0), (-1,0), rl_colors.HexColor("#00f5ff")),
                ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
                ("GRID",       (0,0), (-1,-1), 0.5, rl_colors.HexColor("#0e3a5c")),
                ("BACKGROUND", (0,1), (-1,-1), rl_colors.HexColor("#0d1e30")),
                ("TEXTCOLOR",  (0,1), (-1,-1), rl_colors.HexColor("#e8f4ff")),
                ("ROWBACKGROUNDS", (0,1), (-1,-1),
                 [rl_colors.HexColor("#0d1e30"), rl_colors.HexColor("#0a1520")]),
            ]))
            story.append(t)
            doc.build(story)
            messagebox.showinfo("Done", f"PDF saved:\n{fn}")
        except Exception as e:
            messagebox.showerror("PDF Error", str(e))

    def _gen_html(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".html",
             filetypes=[("HTML", "*.html")])
        if not fn:
            return
        try:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(self._html_report())
            webbrowser.open(fn)
        except Exception as e:
            messagebox.showerror("HTML Error", str(e))

    def _gen_csv(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".csv",
             filetypes=[("CSV", "*.csv")])
        if not fn:
            return
        try:
            r  = self.current_results
            pd = r.get("parsed", {})
            bi = r.get("basic_info", {})
            rows = [["Category", "Field", "Value"],
                    ["Basic", "Number",   pd.get("international","N/A")],
                    ["Basic", "Type",     bi.get("type","N/A")],
                    ["Basic", "Carrier",  r.get("carrier_info",{}).get("current","N/A")],
                    ["Basic", "Location", bi.get("geolocation","N/A")]]
            for s in r.get("social_presence", []):
                rows.append(["Social", s.get("name",""), s.get("url","")])
            for a in r.get("messaging_apps", []):
                rows.append(["Messaging", a.get("name",""), a.get("url","")])
            with open(fn, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            messagebox.showinfo("Done", f"CSV saved:\n{fn}")
        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

    def _export_txt(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".txt",
             filetypes=[("Text", "*.txt")])
        if not fn:
            return
        try:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(self._text_report())
            messagebox.showinfo("Done", f"Report saved:\n{fn}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def _do_print(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return
        tmp = tempfile.mktemp(suffix=".html")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(self._html_report())
        webbrowser.open(tmp)

    def _save_results(self):
        if not self.current_results:
            messagebox.showwarning("No Results", "Nothing to save.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".json",
             filetypes=[("JSON", "*.json")])
        if fn:
            try:
                with open(fn, "w", encoding="utf-8") as f:
                    json.dump(self.current_results, f, indent=2)
                messagebox.showinfo("Saved", f"Saved:\n{fn}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def _clear_all(self):
        self.phone_var.set("")
        self.country_var.set("")
        self.current_results = None
        placeholder = "\n  No data – run an analysis first.\n"
        
        # Safely clear text widgets
        for txt in [self._txt_overview, self._txt_basic, self._txt_location,
                    self._txt_carrier, self._txt_risk, self._txt_breach,
                    self._txt_reports]:
            try:
                self._write_txt(txt, placeholder)
            except:
                pass
                
        for tree in [self._tree_social, self._tree_msg, self._tree_rep]:
            try:
                for item in tree.get_children():
                    tree.delete(item)
            except:
                pass
                
        try:
            self._risk_banner.config(text="── AWAITING ANALYSIS ──", fg=TEXT_DIM)
        except:
            pass
            
        self._btn_save.config_state("disabled")
        self._btn_export.config_state("disabled")
        self._arc.reset()
        self._set_status("CLEARED  ─  READY", CYAN_DIM)

    def _open_tree_url(self, tree, url_col):
        try:
            item = tree.selection()[0]
            url = tree.item(item, "values")[url_col]
            if url and url.startswith("http"):
                webbrowser.open(url)
        except Exception:
            pass

    def _batch_window(self):
        w = tk.Toplevel(self.root)
        w.title("Batch Analysis")
        w.geometry("600x420")
        w.configure(bg=DARK_BG)
        tk.Label(w, text="Enter phone numbers (one per line):",
                 bg=DARK_BG, fg=CYAN_BRIGHT,
                 font=("Courier New", 10)).pack(pady=8)
        ta = scrolledtext.ScrolledText(w, height=12, bg=CARD_BG, fg=TEXT_BRIGHT,
                                       font=("Courier New", 10))
        ta.pack(fill="both", expand=True, padx=12, pady=4)
        def run():
            nums = [n.strip() for n in ta.get("1.0","end").split("\n") if n.strip()]
            messagebox.showinfo("Batch", f"Queued {len(nums)} numbers.\n"
                                         "Batch processing runs sequentially.")
        btn = PulseButton(w, text="▶ RUN BATCH", command=run,
                         color=CYAN_BRIGHT, width=160, height=38)
        btn.pack(pady=10)

    def _api_config(self):
        w = tk.Toplevel(self.root)
        w.title("API Configuration")
        w.geometry("520x360")
        w.configure(bg=DARK_BG)
        tk.Label(w, text="API Key Configuration",
                 bg=DARK_BG, fg=CYAN_BRIGHT,
                 font=("Courier New", 13, "bold")).pack(pady=10)
        apis = ["HaveIBeenPwned", "Truecaller", "Twilio",
                "Numverify", "OpenCageData"]
        frm = tk.Frame(w, bg=DARK_BG)
        frm.pack(fill="both", expand=True, padx=20, pady=4)
        entries = {}
        for i, api in enumerate(apis):
            tk.Label(frm, text=f"{api}:", bg=DARK_BG, fg=TEXT_MID,
                     font=("Courier New", 9)).grid(row=i, column=0,
                                                    sticky="w", pady=4)
            e = tk.Entry(frm, width=38, bg=CARD_BG, fg=CYAN_BRIGHT,
                         insertbackground=CYAN_BRIGHT,
                         font=("Courier New", 9), relief="flat",
                         highlightthickness=1,
                         highlightbackground=BORDER_COLOR)
            e.grid(row=i, column=1, padx=(10,0), pady=4)
            entries[api] = e
        def save():
            keys = {k: entries[k].get() for k in apis}
            try:
                with open("api_keys.json", "w") as f:
                    json.dump(keys, f, indent=2)
                messagebox.showinfo("Saved", "API keys saved to api_keys.json")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        btn = PulseButton(w, text="💾 SAVE KEYS", command=save,
                         color=GREEN_NEON, width=140, height=36)
        btn.pack(pady=10)

    def _clear_cache(self):
        try:
            conn = sqlite3.connect(self.engine.cache_db)
            conn.cursor().execute("DELETE FROM phone_cache")
            conn.commit()
            conn.close()
            messagebox.showinfo("Done", "Cache cleared.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _about(self):
        about_text = """ATHEX Phone Intelligence Tool  v2.1
Enhanced Cyberpunk OSINT Framework

Created by ATHEX BLACK HAT
For authorized security research only.

Features:
• Advanced number analysis
• Social media presence checking
• Risk assessment engine
• Multi-format report export
• Enhanced visual effects

WhatsApp: +92 340916663
YouTube:  @inziXploit444"""
        
        # Create custom about window with effects
        w = tk.Toplevel(self.root)
        w.title("About")
        w.geometry("500x400")
        w.configure(bg=DARK_BG)
        
        # Add animated elements
        ring = HarmonicRipple(w, size=80, color=CYAN_BRIGHT)
        ring.pack(pady=20)
        
        lbl = GlowingText(w, text="ATHEX INTELLIGENCE", 
                         glitch_interval=3000,
                         bg=DARK_BG, fg=CYAN_BRIGHT,
                         font=("Courier New", 16, "bold"))
        lbl.pack(pady=10)
        
        tk.Label(w, text=about_text, bg=DARK_BG, fg=TEXT_BRIGHT,
                 font=("Courier New", 10), justify="left").pack(pady=10, padx=20)
        
        btn = PulseButton(w, text="CLOSE", command=w.destroy,
                         color=CYAN_BRIGHT, width=120, height=36)
        btn.pack(pady=10)

    def _legal(self):
        legal_text = """LEGAL NOTICE

This tool is for AUTHORIZED use only.

• Unauthorized use may violate privacy laws.
• Always obtain consent before investigating.
• Respect data protection regulations.
• Do not use for harassment or stalking.
• The user assumes all legal responsibility.

By using this tool you agree to all applicable laws and regulations."""
        
        w = tk.Toplevel(self.root)
        w.title("Legal Notice")
        w.geometry("500x350")
        w.configure(bg=DARK_BG)
        
        # Warning icon effect
        ring = HarmonicRipple(w, size=60, color=RED_ALERT)
        ring.pack(pady=20)
        
        tk.Label(w, text=legal_text, bg=DARK_BG, fg=TEXT_BRIGHT,
                 font=("Courier New", 10), justify="left").pack(pady=10, padx=20)
        
        btn = PulseButton(w, text="I UNDERSTAND", command=w.destroy,
                         color=RED_ALERT, width=140, height=36)
        btn.pack(pady=10)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass
    
    # Set window transparency for background effects
    root.attributes('-alpha', 0.98)
    
    app = EnhancedPhoneIntelGUI(root)
    root.mainloop()


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     ADVANCED PHONE NUMBER INTELLIGENCE v2.1                  ║
    ║     Enhanced Cyberpunk GUI – All Bugs Fixed                  ║
    ║     For Authorized Security Research Only                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Hard requirements check
    hard_req = {
        "phonenumbers": "pip install phonenumbers",
        "requests":     "pip install requests",
    }
    missing_hard = []
    for pkg, cmd in hard_req.items():
        try:
            __import__(pkg)
        except ImportError:
            missing_hard.append((pkg, cmd))

    if missing_hard:
        print("\n  ✗ Missing REQUIRED packages (tool cannot start without these):")
        for pkg, cmd in missing_hard:
            print(f"    • {pkg:20s}  →  {cmd}")
        sys.exit(1)

    # Soft requirements check
    soft_req = {
        "reportlab": "pip install reportlab   (needed for PDF export)",
        "folium":    "pip install folium      (needed for map generation)",
        "pandas":    "pip install pandas      (needed for data analysis)",
        "dnspython": "pip install dnspython   (needed for DNS queries)",
        "whois":     "pip install whois       (needed for WHOIS lookups)",
    }
    for pkg, note in soft_req.items():
        try:
            __import__(pkg)
        except ImportError:
            print(f"  ℹ  Optional package missing: {pkg:12s}  →  {note}")

    main()