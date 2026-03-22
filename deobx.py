#!/usr/bin/env python3
"""
DeobX - Advanced Deobfuscator Tool
CLI Version - Supports Bash and Python obfuscated scripts
"""

import os
import sys
import re
import base64
import zlib
import marshal
import ast
import json
import hashlib
import argparse
import time
import threading
import itertools
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import subprocess
import tempfile

# Platform-specific imports
if os.name == 'nt':  # Windows
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Additional colors
    PURPLE = '\033[35m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    
class Animation:
    """Cool animations for CLI"""
    
    @staticmethod
    def spinner(stop_event, message="Processing"):
        """Display a spinner animation"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while not stop_event.is_set():
            sys.stdout.write(f'\r{Colors.CYAN}{spinner_chars[i]} {message}...{Colors.ENDC}')
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(spinner_chars)
        sys.stdout.write('\r' + ' ' * 50 + '\r')
    
    @staticmethod
    def progress_bar(iterable, prefix='Progress:', suffix='Complete', length=50, fill='█'):
        """Display a progress bar"""
        def show_progress():
            total = len(iterable)
            for i, item in enumerate(iterable, 1):
                percent = i / total
                filled_length = int(length * percent)
                bar = fill * filled_length + '-' * (length - filled_length)
                sys.stdout.write(f'\r{prefix} |{Colors.GREEN}{bar}{Colors.ENDC}| {percent:.1%} {suffix}')
                sys.stdout.flush()
                yield item
            sys.stdout.write('\n')
        return show_progress()
    
    @staticmethod
    def typewriter(text, delay=0.03):
        """Typewriter effect for text"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def pulse(text, duration=2):
        """Pulsing text effect"""
        end_time = time.time() + duration
        while time.time() < end_time:
            for intensity in range(0, 100, 10):
                color_code = f'\033[38;2;{int(50 + intensity * 2)};{int(100 + intensity)};{int(200 + intensity)}m'
                sys.stdout.write(f'\r{color_code}{text}{Colors.ENDC}')
                sys.stdout.flush()
                time.sleep(0.05)
        print()

class DeobX:
    """Main DeobX - Advanced Deobfuscator Class"""
    
    ASCII_BANNER = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                                   ║
║  {Colors.BOLD}{Colors.WHITE}██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗{Colors.CYAN}                    ║
║  {Colors.BOLD}{Colors.WHITE}██╔══██╗██╔════╝██╔═══██╗██╔══██╗╚██╗██╔╝{Colors.CYAN}                    ║
║  {Colors.BOLD}{Colors.WHITE}██║  ██║█████╗  ██║   ██║██████╔╝ ╚███╔╝ {Colors.CYAN}                    ║
║  {Colors.BOLD}{Colors.WHITE}██║  ██║██╔══╝  ██║   ██║██╔══██╗ ██╔██╗ {Colors.CYAN}                    ║
║  {Colors.BOLD}{Colors.WHITE}██████╔╝███████╗╚██████╔╝██████╔╝██╔╝ ██╗{Colors.CYAN}                    ║
║  {Colors.BOLD}{Colors.WHITE}╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝{Colors.CYAN}                    ║
║                                                                   ║
║  {Colors.GREEN}Advanced Deobfuscation Tool - CLI Edition{Colors.CYAN}                     ║
║  {Colors.YELLOW}Version: 3.0 | Author: DeobX Team | License: MIT{Colors.CYAN}            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    
    def __init__(self, verbose=False, aggressive=False, output_file=None, no_anim=False):
        self.verbose = verbose
        self.aggressive = aggressive
        self.output_file = output_file
        self.no_anim = no_anim
        self.stats = {
            'files_processed': 0,
            'total_original_size': 0,
            'total_deobfuscated_size': 0,
            'techniques_detected': {},
            'start_time': None,
            'end_time': None,
            'successful': 0,
            'failed': 0
        }
        
        self.supported_patterns = {
            'bash': [
                r'bash -c "\$\(base64 -d <<<',
                r'eval\s*"echo\s+[a-zA-Z0-9+/]+={0,2}\s*"',
                r'exec\s+\$\(echo\s+[a-zA-Z0-9+/]+={0,2}',
                r'\\n[a-zA-Z0-9+/]+={0,2}"\)"',
                r'zcat\s*<<<\s*"',
                r'openssl\s+enc\s+-d\s+-a',
                r'gzip\s+-d\s*<<<',
                r'xxd\s+-r\s+-p',
                r'tr\s+-d',
                r'sed\s+.*s/.//g',
                r'\\\\x[0-9a-fA-F]{2}',
            ],
            'python': [
                r'base64\.b64decode\([^)]+\)',
                r'marshal\.loads\([^)]+\)',
                r'exec\([^)]+\)',
                r'eval\([^)]+\)',
                r'zlib\.decompress\([^)]+\)',
                r'compile\([^)]+\)',
                r'\\x[0-9a-fA-F]{2}',
                r'\\u[0-9a-fA-F]{4}',
                r'\\U[0-9a-fA-F]{8}',
                r'__import__\(',
                r'getattr\([^)]+\)',
            ]
        }
    
    def animate_text(self, text, color=Colors.GREEN, delay=0.02):
        """Animate text with typewriter effect"""
        if self.no_anim:
            print(f"{color}{text}{Colors.ENDC}")
            return
            
        for char in text:
            sys.stdout.write(f"{color}{char}{Colors.ENDC}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def print_header(self):
        """Print animated header"""
        if self.no_anim:
            print(self.ASCII_BANNER)
        else:
            lines = self.ASCII_BANNER.split('\n')
            for line in lines:
                if line.strip():
                    self.animate_text(line, Colors.CYAN, 0.001)
                else:
                    print()
            time.sleep(0.5)
    
    def print_section(self, title, char='='):
        """Print section header with animation"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{char * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.BLUE}  {title}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.BLUE}{char * 60}{Colors.ENDC}\n")
    
    def print_success(self, message):
        """Print success message with animation"""
        self.animate_text(f"[✓] {message}", Colors.GREEN, 0.01)
    
    def print_error(self, message):
        """Print error message"""
        print(f"{Colors.FAIL}[✗] {message}{Colors.ENDC}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"{Colors.WARNING}[!] {message}{Colors.ENDC}")
    
    def print_info(self, message):
        """Print info message"""
        print(f"{Colors.BLUE}[i] {message}{Colors.ENDC}")
    
    def print_verbose(self, message):
        """Print verbose message"""
        if self.verbose:
            print(f"{Colors.DIM}[DEBUG] {message}{Colors.ENDC}")
    
    def run_with_spinner(self, func, *args, message="Processing", **kwargs):
        """Run a function with spinner animation"""
        if self.no_anim:
            return func(*args, **kwargs)
        
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=Animation.spinner, args=(stop_event, message))
        spinner_thread.start()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            stop_event.set()
            spinner_thread.join()
    
    def detect_language(self, content: str) -> str:
        """Detect if content is Bash or Python"""
        lines = content.split('\n')[:20]
        
        bash_indicators = [
            '#!/bin/bash', '#!/bin/sh', '#!/usr/bin/env bash',
            'bash -c', 'eval "$', 'exec "$', '$(', '`',
            'export ', 'declare ', 'local ', 'readonly ',
            'if [', 'then', 'fi', 'do', 'done', 'while',
        ]
        
        python_indicators = [
            '#!/usr/bin/env python', 'import ', 'from ',
            'def ', 'class ', 'try:', 'except:', 'if __name__',
            'print(', 'sys.', 'os.', 're.', 'json.',
            'exec(', 'eval(', 'compile(',
        ]
        
        bash_score = sum(1 for line in lines if any(indicator in line for indicator in bash_indicators))
        python_score = sum(1 for line in lines if any(indicator in line for indicator in python_indicators))
        
        if bash_score > python_score:
            return 'bash'
        elif python_score > bash_score:
            return 'python'
        return 'unknown'
    
    def analyze_obfuscation(self, content: str, language: str) -> List[Dict]:
        """Analyze and identify obfuscation techniques"""
        findings = []
        
        # Check for base64
        base64_pattern = r'[A-Za-z0-9+/]+={0,2}'
        base64_matches = re.findall(base64_pattern, content)
        long_base64 = [m for m in base64_matches if len(m) > 20]
        if long_base64:
            findings.append({
                'technique': 'base64',
                'confidence': 90,
                'details': f'Found {len(long_base64)} potential Base64 encoded strings'
            })
            self.stats['techniques_detected']['base64'] = self.stats['techniques_detected'].get('base64', 0) + 1
        
        # Check for multiple base64 layers
        if language == 'bash' and 'base64 -d' in content and 'base64' in content:
            base64_count = content.count('base64')
            if base64_count > 1:
                findings.append({
                    'technique': 'base64_multiple',
                    'confidence': 80,
                    'details': f'Multiple Base64 operations detected ({base64_count})'
                })
                self.stats['techniques_detected']['base64_multiple'] = self.stats['techniques_detected'].get('base64_multiple', 0) + 1
        
        # Check for compression
        if 'gzip' in content or 'zcat' in content:
            findings.append({
                'technique': 'gzip',
                'confidence': 85,
                'details': 'Gzip compression detected'
            })
            self.stats['techniques_detected']['gzip'] = self.stats['techniques_detected'].get('gzip', 0) + 1
        
        if 'zlib' in content or 'compress' in content:
            findings.append({
                'technique': 'zlib',
                'confidence': 85,
                'details': 'Zlib compression detected'
            })
            self.stats['techniques_detected']['zlib'] = self.stats['techniques_detected'].get('zlib', 0) + 1
        
        # Check for hex encoding
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        hex_matches = re.findall(hex_pattern, content)
        if hex_matches:
            findings.append({
                'technique': 'hex',
                'confidence': 95,
                'details': f'Hexadecimal encoding detected ({len(hex_matches)} instances)'
            })
            self.stats['techniques_detected']['hex'] = self.stats['techniques_detected'].get('hex', 0) + 1
        
        # Check for unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})+'
        unicode_matches = re.findall(unicode_pattern, content)
        if unicode_matches:
            findings.append({
                'technique': 'unicode',
                'confidence': 90,
                'details': f'Unicode escapes detected ({len(unicode_matches)} instances)'
            })
            self.stats['techniques_detected']['unicode'] = self.stats['techniques_detected'].get('unicode', 0) + 1
        
        # Check for eval/exec
        if 'eval' in content or 'exec' in content:
            findings.append({
                'technique': 'eval_exec',
                'confidence': 75,
                'details': 'eval/exec usage detected (common in obfuscation)'
            })
            self.stats['techniques_detected']['eval_exec'] = self.stats['techniques_detected'].get('eval_exec', 0) + 1
        
        # Check for marshal (Python specific)
        if language == 'python' and 'marshal' in content:
            findings.append({
                'technique': 'marshal',
                'confidence': 95,
                'details': 'Python marshal module usage detected'
            })
            self.stats['techniques_detected']['marshal'] = self.stats['techniques_detected'].get('marshal', 0) + 1
        
        # Check for ROT patterns
        rot_patterns = [r'tr [A-Za-z] [N-ZA-Mn-za-m]', r'rot13', r'ROT']
        if any(pattern in content.lower() for pattern in rot_patterns):
            findings.append({
                'technique': 'rot',
                'confidence': 85,
                'details': 'Possible ROT13/ROT-N encryption detected'
            })
            self.stats['techniques_detected']['rot'] = self.stats['techniques_detected'].get('rot', 0) + 1
        
        return findings
    
    def extract_base64_strings(self, content: str) -> List[str]:
        """Extract all potential Base64 strings"""
        pattern = r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{20,}={0,2}(?![A-Za-z0-9+/])'
        return re.findall(pattern, content)
    
    def decode_base64(self, encoded_string: str, multiple: bool = False) -> Any:
        """Decode Base64 string, optionally multiple times"""
        decoded = encoded_string
        layers = []
        
        while True:
            try:
                decoded_bytes = base64.b64decode(decoded)
                try:
                    decoded = decoded_bytes.decode('utf-8')
                    layers.append(decoded)
                    if not multiple:
                        break
                except UnicodeDecodeError:
                    try:
                        decoded = decoded_bytes.decode('ascii')
                        if re.match(r'^[A-Za-z0-9+/]+={0,2}$', decoded):
                            layers.append(f"[Binary/Another Layer: {len(decoded_bytes)} bytes]")
                            decoded = decoded_bytes
                            continue
                        else:
                            layers.append(decoded)
                            break
                    except:
                        layers.append(f"[Binary Data: {len(decoded_bytes)} bytes]")
                        break
            except Exception:
                break
        
        return layers if multiple else decoded
    
    def decode_hex(self, hex_string: str) -> str:
        """Decode hexadecimal string"""
        try:
            if hex_string.startswith('\\x'):
                hex_string = hex_string.replace('\\x', '')
            return bytes.fromhex(hex_string).decode('utf-8', errors='ignore')
        except:
            return hex_string
    
    def decode_unicode_escapes(self, text: str) -> str:
        """Decode Unicode escape sequences"""
        try:
            return bytes(text, 'utf-8').decode('unicode_escape')
        except:
            return text
    
    def decode_rot(self, text: str, rot: int = 13) -> str:
        """Decode ROT13/ROT-N"""
        result = []
        for char in text:
            if 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') - rot) % 26 + ord('A')))
            elif 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') - rot) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    
    def deobfuscate_bash(self, content: str) -> Tuple[str, Dict]:
        """Deobfuscate Bash script"""
        original = content
        steps = []
        
        # Step 1: Extract and decode embedded Base64
        base64_strings = self.extract_base64_strings(content)
        for b64 in base64_strings:
            try:
                decoded = self.decode_base64(b64)
                if decoded != b64 and len(decoded) > 10:
                    steps.append(f"Decoded Base64: {decoded[:100]}...")
                    content = content.replace(b64, f"# DECODED: {decoded[:50]}...")
            except:
                pass
        
        # Step 2: Handle eval/exec patterns
        eval_pattern = r'eval\s*"\$\(([^)]+)\)"'
        eval_matches = re.findall(eval_pattern, content)
        for match in eval_matches:
            steps.append(f"Found eval pattern: {match[:50]}...")
        
        # Step 3: Decode hex escapes
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        
        def decode_hex_match(match):
            hex_str = match.group(0)
            decoded = self.decode_hex(hex_str)
            if decoded != hex_str:
                steps.append(f"Decoded hex: {decoded[:100]}...")
            return decoded
        
        content = re.sub(hex_pattern, decode_hex_match, content)
        
        # Step 4: Decode unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})'
        
        def decode_unicode_match(match):
            uni_str = match.group(0)
            decoded = self.decode_unicode_escapes(uni_str)
            if decoded != uni_str:
                steps.append(f"Decoded unicode: {decoded[:100]}...")
            return decoded
        
        content = re.sub(unicode_pattern, decode_unicode_match, content)
        
        # Step 5: Try to identify and decode ROT13
        if 'tr [A-Za-z] [N-ZA-Mn-za-m]' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'echo' in line and 'tr [A-Za-z] [N-ZA-Mn-za-m]' in line:
                    echo_pattern = r'echo\s+([^|]+)'
                    echo_match = re.search(echo_pattern, line)
                    if echo_match:
                        encoded = echo_match.group(1).strip().strip('"\'')
                        decoded = self.decode_rot(encoded, 13)
                        lines[i] = f"# DECODED ROT13: {decoded}"
                        steps.append(f"Decoded ROT13: {decoded[:100]}...")
            content = '\n'.join(lines)
        
        deobfuscation_info = {
            'original_length': len(original),
            'deobfuscated_length': len(content),
            'steps': steps,
            'techniques_found': self.analyze_obfuscation(original, 'bash'),
            'base64_strings_found': len(base64_strings),
        }
        
        return content, deobfuscation_info
    
    def deobfuscate_python(self, content: str) -> Tuple[str, Dict]:
        """Deobfuscate Python script"""
        original = content
        steps = []
        
        # Step 1: Decode Base64 strings
        base64_strings = self.extract_base64_strings(content)
        for b64 in base64_strings:
            try:
                decoded = self.decode_base64(b64)
                if decoded != b64 and len(decoded) > 10:
                    steps.append(f"Decoded Base64: {decoded[:100]}...")
                    content = content.replace(b64, f"# DECODED_BASE64: {decoded[:50]}...")
            except:
                pass
        
        # Step 2: Handle exec/eval patterns
        exec_patterns = [
            r'exec\(([^)]+)\)',
            r'eval\(([^)]+)\)',
        ]
        
        for pattern in exec_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                steps.append(f"Found exec/eval: {match[:50]}...")
                if self.aggressive and 'base64' in match:
                    b64_match = re.search(r'["\']([A-Za-z0-9+/]+={0,2})["\']', match)
                    if b64_match:
                        try:
                            decoded = base64.b64decode(b64_match.group(1)).decode('utf-8')
                            steps.append(f"Decoded exec content: {decoded[:100]}...")
                        except:
                            pass
        
        # Step 3: Decode hex escapes
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        
        def decode_hex_match(match):
            hex_str = match.group(0)
            decoded = self.decode_hex(hex_str)
            if decoded != hex_str:
                steps.append(f"Decoded hex: {decoded[:100]}...")
            return decoded
        
        content = re.sub(hex_pattern, decode_hex_match, content)
        
        # Step 4: Decode unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})'
        
        def decode_unicode_match(match):
            uni_str = match.group(0)
            decoded = self.decode_unicode_escapes(uni_str)
            if decoded != uni_str:
                steps.append(f"Decoded unicode: {decoded[:100]}...")
            return decoded
        
        content = re.sub(unicode_pattern, decode_unicode_match, content)
        
        # Step 5: Handle chr() constructions
        if self.aggressive:
            chr_pattern = r'chr\((\d+)\)'
            
            def decode_chr_match(match):
                try:
                    char_code = int(match.group(1))
                    return chr(char_code)
                except:
                    return match.group(0)
            
            content = re.sub(chr_pattern, decode_chr_match, content)
            steps.append("Decoded chr() constructions")
        
        # Step 6: Try to format Python code
        try:
            import autopep8
            content = autopep8.fix_code(content)
            steps.append("Formatted Python code with autopep8")
        except ImportError:
            pass
        
        deobfuscation_info = {
            'original_length': len(original),
            'deobfuscated_length': len(content),
            'steps': steps,
            'techniques_found': self.analyze_obfuscation(original, 'python'),
            'base64_strings_found': len(base64_strings),
        }
        
        return content, deobfuscation_info
    
    def deobfuscate_file(self, filepath: str) -> Tuple[str, Dict]:
        """Deobfuscate a file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            language = self.detect_language(content)
            self.print_verbose(f"Detected language: {language}")
            
            if language == 'bash':
                deobfuscated, info = self.deobfuscate_bash(content)
            elif language == 'python':
                deobfuscated, info = self.deobfuscate_python(content)
            else:
                deobfuscated = content
                info = {'error': f'Unknown language: {language}'}
            
            info['filename'] = os.path.basename(filepath)
            info['filepath'] = filepath
            info['language'] = language
            info['timestamp'] = datetime.now().isoformat()
            info['md5'] = hashlib.md5(content.encode()).hexdigest()
            info['sha256'] = hashlib.sha256(content.encode()).hexdigest()
            
            # Update stats
            self.stats['files_processed'] += 1
            if 'error' not in info:
                self.stats['successful'] += 1
                self.stats['total_original_size'] += info.get('original_length', 0)
                self.stats['total_deobfuscated_size'] += info.get('deobfuscated_length', 0)
            else:
                self.stats['failed'] += 1
            
            return deobfuscated, info
            
        except Exception as e:
            self.print_error(f"Failed to deobfuscate {filepath}: {str(e)}")
            self.stats['failed'] += 1
            return f"Error: {str(e)}", {'error': str(e)}
    
    def display_analysis(self, info: Dict):
        """Display detailed analysis of deobfuscation"""
        if 'error' in info:
            self.print_error(f"Analysis failed: {info['error']}")
            return
        
        self.print_section("DEOBFUSCATION REPORT")
        
        # File info with colors
        print(f"{Colors.BOLD}📄 File:{Colors.ENDC} {Colors.GREEN}{info.get('filename', 'Unknown')}{Colors.ENDC}")
        print(f"{Colors.BOLD}🔤 Language:{Colors.ENDC} {Colors.CYAN}{info.get('language', 'Unknown').upper()}{Colors.ENDC}")
        print(f"{Colors.BOLD}⏰ Timestamp:{Colors.ENDC} {info.get('timestamp', 'Unknown')}")
        
        # Size comparison with progress bar
        print(f"\n{Colors.BOLD}📊 Size Comparison:{Colors.ENDC}")
        orig_len = info.get('original_length', 0)
        deob_len = info.get('deobfuscated_length', 0)
        reduction = ((orig_len - deob_len) / orig_len * 100) if orig_len > 0 else 0
        
        # Visual size bar
        max_len = max(orig_len, deob_len)
        orig_bar_len = int(30 * orig_len / max_len) if max_len > 0 else 0
        deob_bar_len = int(30 * deob_len / max_len) if max_len > 0 else 0
        
        print(f"  Original:      {Colors.FAIL}{'█' * orig_bar_len}{Colors.ENDC} {orig_len:,} bytes")
        print(f"  Deobfuscated:  {Colors.GREEN}{'█' * deob_bar_len}{Colors.ENDC} {deob_len:,} bytes")
        
        reduction_color = Colors.GREEN if reduction > 0 else Colors.WARNING
        print(f"  Reduction:     {reduction_color}{reduction:.1f}%{Colors.ENDC}")
        
        # Hashes
        print(f"\n{Colors.BOLD}🔐 Hashes:{Colors.ENDC}")
        print(f"  MD5:    {Colors.DIM}{info.get('md5', 'N/A')}{Colors.ENDC}")
        print(f"  SHA256: {Colors.DIM}{info.get('sha256', 'N/A')}{Colors.ENDC}")
        
        # Techniques detected
        print(f"\n{Colors.BOLD}🔍 Detected Obfuscation Techniques:{Colors.ENDC}")
        techniques = info.get('techniques_found', [])
        if techniques:
            for tech in techniques:
                confidence_color = Colors.GREEN if tech['confidence'] > 80 else Colors.WARNING
                print(f"  {confidence_color}▶{Colors.ENDC} {tech['technique']} ({tech['confidence']}%)")
                print(f"     {Colors.DIM}{tech['details']}{Colors.ENDC}")
        else:
            print(f"  {Colors.GREEN}✓ No obfuscation techniques detected.{Colors.ENDC}")
        
        # Deobfuscation steps (verbose only)
        if self.verbose and info.get('steps'):
            print(f"\n{Colors.BOLD}📝 Deobfuscation Steps:{Colors.ENDC}")
            steps = info.get('steps', [])
            for i, step in enumerate(steps[:15], 1):
                print(f"  {i:2d}. {Colors.DIM}{step[:100]}{Colors.ENDC}")
            if len(steps) > 15:
                print(f"  ... and {len(steps) - 15} more steps")
    
    def display_statistics(self):
        """Display overall statistics with cool animation"""
        if self.stats['files_processed'] == 0:
            return
        
        self.print_section("STATISTICS SUMMARY")
        
        print(f"{Colors.BOLD}📊 Processing Statistics:{Colors.ENDC}")
        print(f"  Files Processed:  {Colors.CYAN}{self.stats['files_processed']}{Colors.ENDC}")
        print(f"  Successful:       {Colors.GREEN}{self.stats['successful']}{Colors.ENDC}")
        print(f"  Failed:           {Colors.FAIL}{self.stats['failed']}{Colors.ENDC}")
        
        if self.stats['successful'] > 0:
            print(f"\n{Colors.BOLD}💾 Size Statistics:{Colors.ENDC}")
            print(f"  Total Original:      {self.stats['total_original_size']:,} bytes")
            print(f"  Total Deobfuscated:  {self.stats['total_deobfuscated_size']:,} bytes")
            
            if self.stats['total_original_size'] > 0:
                total_reduction = ((self.stats['total_original_size'] - self.stats['total_deobfuscated_size']) / 
                                  self.stats['total_original_size'] * 100)
                print(f"  Total Reduction:     {Colors.GREEN}{total_reduction:.1f}%{Colors.ENDC}")
        
        if self.stats['techniques_detected']:
            print(f"\n{Colors.BOLD}🎯 Techniques Detected:{Colors.ENDC}")
            sorted_tech = sorted(self.stats['techniques_detected'].items(), key=lambda x: x[1], reverse=True)
            for tech, count in sorted_tech[:10]:
                bar_len = min(30, int(30 * count / max(self.stats['techniques_detected'].values())))
                print(f"  {tech:20} [{Colors.GREEN}{'█' * bar_len}{Colors.ENDC}] {count}")
        
        if self.stats['start_time'] and self.stats['end_time']:
            elapsed = self.stats['end_time'] - self.stats['start_time']
            print(f"\n{Colors.BOLD}⏱️  Processing Time:{Colors.ENDC} {elapsed:.2f} seconds")
            if self.stats['successful'] > 0:
                avg_time = elapsed / self.stats['successful']
                print(f"  Average per file: {avg_time:.2f} seconds")
    
    def save_output(self, content: str, original_filename: str) -> Optional[str]:
        """Save deobfuscated output to file"""
        if self.output_file:
            output_path = self.output_file
        else:
            base_name = os.path.splitext(original_filename)[0]
            output_path = f"{base_name}_deobx.py"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.print_success(f"Saved to: {output_path}")
            return output_path
        except Exception as e:
            self.print_error(f"Failed to save: {str(e)}")
            return None
    
    def save_report(self, info: Dict, output_path: str):
        """Save analysis report"""
        report_path = f"{os.path.splitext(output_path)[0]}_report.txt"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("╔═══════════════════════════════════════════════════════════════╗\n")
                f.write("║                    DEOBX - ANALYSIS REPORT                    ║\n")
                f.write("╚═══════════════════════════════════════════════════════════════╝\n\n")
                
                f.write(f"File: {info.get('filename')}\n")
                f.write(f"Language: {info.get('language', 'Unknown')}\n")
                f.write(f"Timestamp: {info.get('timestamp')}\n\n")
                
                f.write("═" * 60 + "\n")
                f.write("SIZE COMPARISON\n")
                f.write("═" * 60 + "\n")
                f.write(f"Original: {info.get('original_length', 0):,} bytes\n")
                f.write(f"Deobfuscated: {info.get('deobfuscated_length', 0):,} bytes\n")
                reduction = ((info.get('original_length', 0) - info.get('deobfuscated_length', 0)) / 
                            info.get('original_length', 1) * 100)
                f.write(f"Reduction: {reduction:.1f}%\n\n")
                
                f.write("═" * 60 + "\n")
                f.write("HASHES\n")
                f.write("═" * 60 + "\n")
                f.write(f"MD5: {info.get('md5')}\n")
                f.write(f"SHA256: {info.get('sha256')}\n\n")
                
                f.write("═" * 60 + "\n")
                f.write("DETECTED TECHNIQUES\n")
                f.write("═" * 60 + "\n")
                for tech in info.get('techniques_found', []):
                    f.write(f"- {tech['technique']} ({tech['confidence']}%)\n")
                    f.write(f"  {tech['details']}\n")
                
                if info.get('steps'):
                    f.write("\n" + "═" * 60 + "\n")
                    f.write("DEOBFUSCATION STEPS\n")
                    f.write("═" * 60 + "\n")
                    for i, step in enumerate(info['steps'], 1):
                        f.write(f"{i}. {step}\n")
            
            self.print_success(f"Report saved to: {report_path}")
        except Exception as e:
            self.print_error(f"Failed to save report: {str(e)}")
    
    def process_file(self, filepath: str):
        """Process a single file"""
        self.print_info(f"Processing: {filepath}")
        
        def _process():
            return self.deobfuscate_file(filepath)
        
        deobfuscated, info = self.run_with_spinner(_process, message=f"Deobfuscating {os.path.basename(filepath)}")
        
        if 'error' in info:
            self.print_error(f"Failed to process {filepath}: {info['error']}")
            return
        
        self.display_analysis(info)
        
        # Save output
        output_path = self.save_output(deobfuscated, filepath)
        
        if output_path:
            self.save_report(info, output_path)
        
        # Show preview
        if self.verbose:
            self.print_section("PREVIEW (First 30 lines)", '-')
            lines = deobfuscated.split('\n')[:30]
            for i, line in enumerate(lines, 1):
                if line.strip():
                    print(f"{Colors.DIM}{i:4d}{Colors.ENDC} {line[:100]}")
            if len(deobfuscated.split('\n')) > 30:
                print(f"{Colors.DIM}... (truncated, total {len(deobfuscated.split('\n'))} lines){Colors.ENDC}")
        
        self.print_success(f"Successfully deobfuscated {os.path.basename(filepath)}")
    
    def process_directory(self, directory: str, pattern: str = "*"):
        """Process all files in a directory"""
        path = Path(directory)
        if not path.exists():
            self.print_error(f"Directory not found: {directory}")
            return
        
        files = list(path.glob(pattern))
        if not files:
            self.print_warning(f"No files matching '{pattern}' found in {directory}")
            return
        
        self.print_info(f"Found {len(files)} files to process")
        
        for filepath in files:
            if filepath.is_file():
                self.process_file(str(filepath))
                print()  # Empty line between files
    
    def interactive_mode(self):
        """Run in interactive mode"""
        self.print_header()
        print(f"{Colors.GREEN}Welcome to DeobX Interactive Mode{Colors.ENDC}")
        print(f"{Colors.DIM}Type 'help' for commands, 'exit' to quit{Colors.ENDC}\n")
        
        while True:
            try:
                command = input(f"{Colors.CYAN}deobx>{Colors.ENDC} ").strip()
                
                if not command:
                    continue
                
                if command == 'exit' or command == 'quit':
                    print(f"{Colors.GREEN}Goodbye!{Colors.ENDC}")
                    break
                elif command == 'help':
                    self.show_help()
                elif command.startswith('file '):
                    filepath = command[5:].strip()
                    self.stats['start_time'] = time.time()
                    self.process_file(filepath)
                    self.stats['end_time'] = time.time()
                    self.display_statistics()
                elif command.startswith('dir '):
                    parts = command.split()
                    if len(parts) >= 2:
                        directory = parts[1]
                        pattern = parts[2] if len(parts) >= 3 else "*"
                        self.stats['start_time'] = time.time()
                        self.process_directory(directory, pattern)
                        self.stats['end_time'] = time.time()
                        self.display_statistics()
                elif command == 'stats':
                    self.display_statistics()
                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.print_header()
                elif command == 'verbose':
                    self.verbose = not self.verbose
                    status = f"{Colors.GREEN}ON{Colors.ENDC}" if self.verbose else f"{Colors.FAIL}OFF{Colors.ENDC}"
                    print(f"Verbose mode: {status}")
                elif command == 'aggressive':
                    self.aggressive = not self.aggressive
                    status = f"{Colors.GREEN}ON{Colors.ENDC}" if self.aggressive else f"{Colors.FAIL}OFF{Colors.ENDC}"
                    print(f"Aggressive mode: {status}")
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interrupted{Colors.ENDC}")
                break
            except Exception as e:
                self.print_error(f"Error: {str(e)}")
    
    def show_help(self):
        """Show help information with cool formatting"""
        print(f"""
{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                     DEOBX - COMMAND HELP                        ║
╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BOLD}📁 FILE COMMANDS:{Colors.ENDC}
  {Colors.GREEN}file <path>{Colors.ENDC}      - Deobfuscate a single file
  {Colors.GREEN}dir <path> [pattern]{Colors.ENDC} - Deobfuscate all files in directory

{Colors.BOLD}⚙️  SETTINGS:{Colors.ENDC}
  {Colors.GREEN}verbose{Colors.ENDC}          - Toggle verbose output
  {Colors.GREEN}aggressive{Colors.ENDC}       - Toggle aggressive deobfuscation

{Colors.BOLD}📊 INFORMATION:{Colors.ENDC}
  {Colors.GREEN}stats{Colors.ENDC}            - Show processing statistics
  {Colors.GREEN}help{Colors.ENDC}             - Show this help message

{Colors.BOLD}🎮 CONTROL:{Colors.ENDC}
  {Colors.GREEN}clear{Colors.ENDC}            - Clear the screen
  {Colors.GREEN}exit{Colors.ENDC}             - Exit interactive mode

{Colors.BOLD}💡 EXAMPLES:{Colors.ENDC}
  {Colors.DIM}deobx> file obfuscated.py{Colors.ENDC}
  {Colors.DIM}deobx> dir /path/to/scripts/ *.py{Colors.ENDC}
  {Colors.DIM}deobx> aggressive{Colors.ENDC}
  {Colors.DIM}deobx> verbose{Colors.ENDC}

{Colors.BOLD}{Colors.GREEN}✨ Pro Tip: Use aggressive mode for deeply obfuscated scripts!{Colors.ENDC}
""")

def main():
    parser = argparse.ArgumentParser(
        description="DeobX - Advanced Deobfuscator Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.GREEN}Examples:{Colors.ENDC}
  %(prog)s -f script.py                    # Deobfuscate a single file
  %(prog)s -f script.sh -o output.sh       # Save to specific file
  %(prog)s -f script.py -a -v              # Aggressive mode with verbose
  %(prog)s -d /path/to/scripts/            # Process entire directory
  %(prog)s -d /path/to/scripts/ "*.py"     # Process only Python files
  %(prog)s -i                              # Interactive mode
  %(prog)s --no-anim                       # Disable animations
        """
    )
    
    parser.add_argument('-f', '--file', help='File to deobfuscate')
    parser.add_argument('-d', '--directory', help='Directory to process')
    parser.add_argument('-o', '--output', help='Output file (for single file)')
    parser.add_argument('-a', '--aggressive', action='store_true', help='Enable aggressive deobfuscation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--pattern', default='*', help='File pattern for directory processing (default: *)')
    parser.add_argument('--no-anim', action='store_true', help='Disable animations for faster processing')
    
    args = parser.parse_args()
    
    # Create DeobX instance
    deobx = DeobX(
        verbose=args.verbose,
        aggressive=args.aggressive,
        output_file=args.output,
        no_anim=args.no_anim
    )
    
    deobx.print_header()
    
    try:
        if args.interactive:
            deobx.interactive_mode()
        elif args.file:
            deobx.stats['start_time'] = time.time()
            deobx.process_file(args.file)
            deobx.stats['end_time'] = time.time()
            deobx.display_statistics()
        elif args.directory:
            deobx.stats['start_time'] = time.time()
            deobx.process_directory(args.directory, args.pattern)
            deobx.stats['end_time'] = time.time()
            deobx.display_statistics()
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        deobx.print_error(f"Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()