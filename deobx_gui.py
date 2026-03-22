#!/usr/bin/env python3
"""
Advanced Deobfuscator Tool - GUI Interface
Supports Bash and Python obfuscated scripts
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
from pathlib import Path
from datetime import datetime

# GUI imports
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext, font
    from tkinter import Menu, Toplevel
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("GUI libraries not available. Running in CLI mode.")

class AdvancedDeobfuscator:
    def __init__(self):
        self.supported_patterns = {
            'bash': [
                r'bash -c "\$\(base64 -d <<<',
                r'eval\s*"echo\s+[a-zA-Z0-9+/]+={0,2}\s*"',
                r'exec\s+\$\(echo\s+[a-zA-Z0-9+/]+={0,2}',
                r'\\n[a-zA-Z0-9+/]+={0,2}"\)"',
                r'\\n[a-zA-Z0-9+/]+={0,2}',
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
                r'import\s+base64',
                r'import\s+marshal',
                r'import\s+zlib',
                r'import\s+types',
                r'__import__\(',
                r'getattr\([^)]+\)',
                r'chr\([^)]+\)',
                r'ord\([^)]+\)',
            ]
        }
        
        self.obfuscation_techniques = {
            'base64': 'Base64 Encoding',
            'base64_multiple': 'Multiple Base64 Layers',
            'gzip': 'Gzip Compression',
            'zlib': 'Zlib Compression',
            'hex': 'Hexadecimal Encoding',
            'octal': 'Octal Encoding',
            'unicode': 'Unicode Escapes',
            'xor': 'XOR Encryption',
            'rot': 'ROT13/ROT-N',
            'marshal': 'Python Marshal',
            'compile': 'Python Compile',
            'eval_exec': 'eval/exec Obfuscation',
            'string_manipulation': 'String Manipulation',
            'reverse': 'String Reversal',
        }
        
        self.deobfuscation_history = []
        
    def detect_language(self, content):
        """Detect if content is Bash or Python"""
        lines = content.split('\n')[:20]
        
        bash_indicators = [
            '#!/bin/bash', '#!/bin/sh', '#!/usr/bin/env bash',
            'bash -c', 'eval "$', 'exec "$', '$(', '`',
            'export ', 'declare ', 'local ', 'readonly ',
            'if [', 'then', 'fi', 'do', 'done', 'while',
            'case ', 'esac', 'function ', 'fi',
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
        else:
            # Check file extension if available
            return 'unknown'
    
    def analyze_obfuscation(self, content, language):
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
        
        # Check for multiple base64 layers
        if language == 'bash' and 'base64 -d' in content and 'base64' in content:
            base64_count = content.count('base64')
            if base64_count > 1:
                findings.append({
                    'technique': 'base64_multiple',
                    'confidence': 80,
                    'details': f'Multiple Base64 operations detected ({base64_count})'
                })
        
        # Check for compression
        if 'gzip' in content or 'zcat' in content:
            findings.append({
                'technique': 'gzip',
                'confidence': 85,
                'details': 'Gzip compression detected'
            })
        
        if 'zlib' in content or 'compress' in content:
            findings.append({
                'technique': 'zlib',
                'confidence': 85,
                'details': 'Zlib compression detected'
            })
        
        # Check for hex encoding
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        hex_matches = re.findall(hex_pattern, content)
        if hex_matches:
            findings.append({
                'technique': 'hex',
                'confidence': 95,
                'details': f'Hexadecimal encoding detected ({len(hex_matches)} instances)'
            })
        
        # Check for unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})+'
        unicode_matches = re.findall(unicode_pattern, content)
        if unicode_matches:
            findings.append({
                'technique': 'unicode',
                'confidence': 90,
                'details': f'Unicode escapes detected ({len(unicode_matches)} instances)'
            })
        
        # Check for eval/exec
        if 'eval' in content or 'exec' in content:
            findings.append({
                'technique': 'eval_exec',
                'confidence': 75,
                'details': 'eval/exec usage detected (common in obfuscation)'
            })
        
        # Check for string manipulation
        if 'sed ' in content or 'tr ' in content or 'awk ' in content:
            findings.append({
                'technique': 'string_manipulation',
                'confidence': 70,
                'details': 'String manipulation commands detected'
            })
        
        # Check for marshal (Python specific)
        if language == 'python' and 'marshal' in content:
            findings.append({
                'technique': 'marshal',
                'confidence': 95,
                'details': 'Python marshal module usage detected'
            })
        
        # Check for compile (Python specific)
        if language == 'python' and 'compile(' in content:
            findings.append({
                'technique': 'compile',
                'confidence': 90,
                'details': 'Python compile() function detected'
            })
        
        # Check for XOR patterns
        xor_patterns = [r'\^', r'xor', r'XOR']
        if any(pattern in content.lower() for pattern in xor_patterns):
            findings.append({
                'technique': 'xor',
                'confidence': 60,
                'details': 'Possible XOR encryption detected'
            })
        
        # Check for ROT patterns
        rot_patterns = [r'tr [A-Za-z] [N-ZA-Mn-za-m]', r'rot13', r'ROT']
        if any(pattern in content.lower() for pattern in rot_patterns):
            findings.append({
                'technique': 'rot',
                'confidence': 85,
                'details': 'Possible ROT13/ROT-N encryption detected'
            })
        
        # Check for reversed strings
        if 'rev' in content or '[::-1]' in content:
            findings.append({
                'technique': 'reverse',
                'confidence': 70,
                'details': 'String reversal detected'
            })
        
        return findings
    
    def extract_base64_strings(self, content):
        """Extract all potential Base64 strings"""
        # More precise Base64 pattern
        pattern = r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{20,}={0,2}(?![A-Za-z0-9+/])'
        return re.findall(pattern, content)
    
    def decode_base64(self, encoded_string, multiple=False):
        """Decode Base64 string, optionally multiple times"""
        decoded = encoded_string
        layers = []
        
        while True:
            try:
                # Try to decode
                decoded_bytes = base64.b64decode(decoded)
                
                # Try to decode as UTF-8 string
                try:
                    decoded = decoded_bytes.decode('utf-8')
                    layers.append(decoded)
                    if not multiple:
                        break
                except UnicodeDecodeError:
                    # Might be binary data or another layer
                    # Try to see if it's another Base64 string
                    try:
                        decoded = decoded_bytes.decode('ascii')
                        # Check if it looks like another Base64
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
                        
            except Exception as e:
                # Not Base64 anymore
                break
        
        return layers if multiple else decoded
    
    def decode_hex(self, hex_string):
        """Decode hexadecimal string"""
        try:
            # Remove \x prefixes
            if hex_string.startswith('\\x'):
                hex_string = hex_string.replace('\\x', '')
            # Decode hex
            return bytes.fromhex(hex_string).decode('utf-8', errors='ignore')
        except:
            return hex_string
    
    def decode_unicode_escapes(self, text):
        """Decode Unicode escape sequences"""
        try:
            return bytes(text, 'utf-8').decode('unicode_escape')
        except:
            return text
    
    def decode_rot(self, text, rot=13):
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
    
    def extract_python_marshal(self, content):
        """Extract and decode Python marshal data"""
        marshal_patterns = [
            r'marshal\.loads\(base64\.b64decode\(["\']([^"\']+)["\']\)\)',
            r'base64\.b64decode\(["\']([^"\']+)["\']\)',
        ]
        
        for pattern in marshal_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                try:
                    # Decode base64
                    decoded = base64.b64decode(match)
                    # Try to unmarshal
                    code_obj = marshal.loads(decoded)
                    # Try to decompile
                    try:
                        import dis
                        import io
                        output = io.StringIO()
                        dis.dis(code_obj, file=output)
                        return output.getvalue()
                    except:
                        return f"[Marshaled Code Object: {code_obj}]"
                except Exception as e:
                    continue
        return None
    
    def deobfuscate_bash(self, content, aggressive=False):
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
        # Pattern: eval "$(echo ... | base64 -d)"
        eval_pattern = r'eval\s*"\$\(([^)]+)\)"'
        eval_matches = re.findall(eval_pattern, content)
        for match in eval_matches:
            steps.append(f"Found eval pattern: {match[:50]}...")
        
        # Step 3: Handle nested commands
        # Replace $(...) with their potential output
        cmd_pattern = r'\$\(([^)]+)\)'
        
        def replace_command(match):
            cmd = match.group(1)
            if 'base64 -d' in cmd:
                # Try to extract and decode base64
                b64_pattern = r'echo\s+([A-Za-z0-9+/]+={0,2})'
                b64_match = re.search(b64_pattern, cmd)
                if b64_match:
                    try:
                        decoded = base64.b64decode(b64_match.group(1)).decode('utf-8')
                        steps.append(f"Decoded command: {decoded[:100]}...")
                        return decoded
                    except:
                        pass
            return f"# COMMAND: {cmd}"
        
        if aggressive:
            content = re.sub(cmd_pattern, replace_command, content)
        
        # Step 4: Decode hex escapes
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        
        def decode_hex_match(match):
            hex_str = match.group(0)
            decoded = self.decode_hex(hex_str)
            if decoded != hex_str:
                steps.append(f"Decoded hex: {decoded[:100]}...")
            return decoded
        
        content = re.sub(hex_pattern, decode_hex_match, content)
        
        # Step 5: Decode unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})'
        
        def decode_unicode_match(match):
            uni_str = match.group(0)
            decoded = self.decode_unicode_escapes(uni_str)
            if decoded != uni_str:
                steps.append(f"Decoded unicode: {decoded[:100]}...")
            return decoded
        
        content = re.sub(unicode_pattern, decode_unicode_match, content)
        
        # Step 6: Try to identify and decode ROT13
        if 'tr [A-Za-z] [N-ZA-Mn-za-m]' in content:
            # This is ROT13
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'echo' in line and 'tr [A-Za-z] [N-ZA-Mn-za-m]' in line:
                    # Extract the string being echoed
                    echo_pattern = r'echo\s+([^|]+)'
                    echo_match = re.search(echo_pattern, line)
                    if echo_match:
                        encoded = echo_match.group(1).strip().strip('"\'')
                        decoded = self.decode_rot(encoded, 13)
                        lines[i] = f"# DECODED ROT13: {decoded}"
                        steps.append(f"Decoded ROT13: {decoded[:100]}...")
            content = '\n'.join(lines)
        
        # Step 7: Try to reconstruct the script
        # Find all echo statements that might contain code
        echo_pattern = r'echo\s+["\']?([^"\']+)["\']?\s*(\|.*)?$'
        
        # Store deobfuscation info
        deobfuscation_info = {
            'original_length': len(original),
            'deobfuscated_length': len(content),
            'steps': steps,
            'techniques_found': self.analyze_obfuscation(original, 'bash'),
            'base64_strings_found': len(base64_strings),
            'hex_strings_found': len(re.findall(hex_pattern, original)),
        }
        
        return content, deobfuscation_info
    
    def deobfuscate_python(self, content, aggressive=False):
        """Deobfuscate Python script"""
        original = content
        steps = []
        
        # Step 1: Try to extract and execute marshal-based obfuscation
        marshal_result = self.extract_python_marshal(content)
        if marshal_result:
            steps.append("Extracted Python marshal data")
            content = f"# Extracted from marshal:\n{marshal_result}\n\n# Original:\n{content}"
        
        # Step 2: Decode Base64 strings
        base64_strings = self.extract_base64_strings(content)
        for b64 in base64_strings:
            try:
                decoded = self.decode_base64(b64)
                if decoded != b64 and len(decoded) > 10:
                    steps.append(f"Decoded Base64: {decoded[:100]}...")
                    # Replace in content with comment
                    content = content.replace(b64, f"# DECODED_BASE64: {decoded[:50]}...")
            except:
                pass
        
        # Step 3: Handle exec/eval patterns
        exec_patterns = [
            r'exec\(([^)]+)\)',
            r'eval\(([^)]+)\)',
        ]
        
        for pattern in exec_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                steps.append(f"Found exec/eval: {match[:50]}...")
                if aggressive and 'base64' in match:
                    # Try to decode what's inside
                    b64_match = re.search(r'["\']([A-Za-z0-9+/]+={0,2})["\']', match)
                    if b64_match:
                        try:
                            decoded = base64.b64decode(b64_match.group(1)).decode('utf-8')
                            steps.append(f"Decoded exec content: {decoded[:100]}...")
                        except:
                            pass
        
        # Step 4: Decode hex escapes
        hex_pattern = r'(\\x[0-9a-fA-F]{2})+'
        
        def decode_hex_match(match):
            hex_str = match.group(0)
            decoded = self.decode_hex(hex_str)
            if decoded != hex_str:
                steps.append(f"Decoded hex: {decoded[:100]}...")
            return decoded
        
        content = re.sub(hex_pattern, decode_hex_match, content)
        
        # Step 5: Decode unicode escapes
        unicode_pattern = r'(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})'
        
        def decode_unicode_match(match):
            uni_str = match.group(0)
            decoded = self.decode_unicode_escapes(uni_str)
            if decoded != uni_str:
                steps.append(f"Decoded unicode: {decoded[:100]}...")
            return decoded
        
        content = re.sub(unicode_pattern, decode_unicode_match, content)
        
        # Step 6: Handle chr() constructions
        # Pattern: chr(65)+chr(66)+...
        chr_pattern = r'chr\((\d+)\)'
        
        def decode_chr_match(match):
            try:
                char_code = int(match.group(1))
                return chr(char_code)
            except:
                return match.group(0)
        
        if aggressive:
            # Simple chr() decoding
            content = re.sub(chr_pattern, decode_chr_match, content)
        
        # Step 7: Try to decompile bytecode if present
        if b'\x03\xf3' in content.encode() or b'__pycache__' in content:
            steps.append("Possible bytecode detected")
        
        # Step 8: Try to format/beautify Python code
        try:
            import autopep8
            content = autopep8.fix_code(content)
            steps.append("Formatted Python code with autopep8")
        except ImportError:
            pass
        
        # Store deobfuscation info
        deobfuscation_info = {
            'original_length': len(original),
            'deobfuscated_length': len(content),
            'steps': steps,
            'techniques_found': self.analyze_obfuscation(original, 'python'),
            'base64_strings_found': len(base64_strings),
            'exec_eval_found': len(re.findall(r'exec\(|eval\(', original)),
        }
        
        return content, deobfuscation_info
    
    def deobfuscate_file(self, filepath, aggressive=False):
        """Deobfuscate a file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Detect language
            language = self.detect_language(content)
            
            # Analyze obfuscation
            analysis = self.analyze_obfuscation(content, language)
            
            # Deobfuscate based on language
            if language == 'bash':
                deobfuscated, info = self.deobfuscate_bash(content, aggressive)
            elif language == 'python':
                deobfuscated, info = self.deobfuscate_python(content, aggressive)
            else:
                deobfuscated = content
                info = {
                    'error': f'Unknown language: {language}',
                    'analysis': analysis
                }
            
            # Add file info
            info['filename'] = os.path.basename(filepath)
            info['filepath'] = filepath
            info['language'] = language
            info['timestamp'] = datetime.now().isoformat()
            info['analysis'] = analysis
            
            # Calculate hash
            info['md5'] = hashlib.md5(content.encode()).hexdigest()
            info['sha256'] = hashlib.sha256(content.encode()).hexdigest()
            
            # Add to history
            self.deobfuscation_history.append(info)
            
            return deobfuscated, info
            
        except Exception as e:
            return f"Error deobfuscating file: {str(e)}", {'error': str(e)}


class DeobfuscatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Deobfuscator Tool")
        self.root.geometry("1200x800")
        
        # Initialize deobfuscator engine
        self.deobfuscator = AdvancedDeobfuscator()
        
        # Current file info
        self.current_file = None
        self.current_content = ""
        self.deobfuscated_content = ""
        self.analysis_info = {}
        
        # Set icon (if available)
        try:
            self.root.iconbitmap('deobfuscator.ico')
        except:
            pass
        
        # Setup styles
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        
        # Configure colors
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.accent_color = '#4a9eff'
        self.warning_color = '#ff6b6b'
        self.success_color = '#51cf66'
        
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12))
        style.configure('Status.TLabel', font=('Segoe UI', 10))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
        
        # Configure notebook style
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', font=('Segoe UI', 10))
        
        # Set window background
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create menu bar
        self.create_menu_bar()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for controls
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        ttk.Label(top_frame, text="File:", style='Subtitle.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.file_label = ttk.Label(top_frame, text="No file selected", style='Status.TLabel')
        self.file_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Browse button
        ttk.Button(top_frame, text="Browse...", command=self.browse_file,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # Language display
        self.lang_label = ttk.Label(top_frame, text="Language: Unknown", style='Status.TLabel')
        self.lang_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Aggressive mode checkbox
        self.aggressive_var = tk.BooleanVar()
        self.aggressive_check = ttk.Checkbutton(top_frame, text="Aggressive Mode",
                                               variable=self.aggressive_var)
        self.aggressive_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Deobfuscate button
        ttk.Button(top_frame, text="Deobfuscate", command=self.deobfuscate,
                  style='Accent.TButton').pack(side=tk.LEFT)
        
        # Save button
        ttk.Button(top_frame, text="Save Result", command=self.save_result,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Original Content
        self.original_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.original_tab, text="Original")
        
        self.original_text = scrolledtext.ScrolledText(
            self.original_tab, wrap=tk.WORD, font=('Consolas', 10),
            bg='#1e1e1e', fg='#d4d4d4', insertbackground='white'
        )
        self.original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2: Deobfuscated Content
        self.deobfuscated_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.deobfuscated_tab, text="Deobfuscated")
        
        self.deobfuscated_text = scrolledtext.ScrolledText(
            self.deobfuscated_tab, wrap=tk.WORD, font=('Consolas', 10),
            bg='#1e1e1e', fg='#d4d4d4', insertbackground='white'
        )
        self.deobfuscated_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 3: Analysis
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Analysis")
        
        # Analysis text widget
        self.analysis_text = scrolledtext.ScrolledText(
            self.analysis_tab, wrap=tk.WORD, font=('Consolas', 10),
            bg='#1e1e1e', fg='#d4d4d4', height=20
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 4: Statistics
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        
        # Statistics display
        self.stats_text = scrolledtext.ScrolledText(
            self.stats_tab, wrap=tk.WORD, font=('Consolas', 10),
            bg='#1e1e1e', fg='#d4d4d4'
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = ttk.Frame(self.root, height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_bar, variable=self.progress_var,
                                          mode='indeterminate', length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=10)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.browse_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Result...", command=self.save_result, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Batch Deobfuscate...", command=self.batch_deobfuscate)
        tools_menu.add_command(label="Compare Files...", command=self.compare_files)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings...", command=self.show_settings)
        
        # View menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Hex View", command=self.show_hex_view)
        view_menu.add_command(label="Strings View", command=self.show_strings_view)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_guide)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.browse_file())
        self.root.bind('<Control-s>', lambda e: self.save_result())
    
    def browse_file(self):
        """Browse for file to deobfuscate"""
        filetypes = [
            ("All files", "*.*"),
            ("Python files", "*.py"),
            ("Bash files", "*.sh"),
            ("Text files", "*.txt"),
        ]
        
        filename = filedialog.askopenfilename(
            title="Select file to deobfuscate",
            filetypes=filetypes
        )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, filename):
        """Load file into GUI"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.current_file = filename
            self.current_content = content
            
            # Update GUI
            self.file_label.config(text=os.path.basename(filename))
            
            # Detect language
            language = self.deobfuscator.detect_language(content)
            self.lang_label.config(text=f"Language: {language.capitalize()}")
            
            # Display content
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, content)
            
            # Clear other tabs
            self.deobfuscated_text.delete(1.0, tk.END)
            self.analysis_text.delete(1.0, tk.END)
            self.stats_text.delete(1.0, tk.END)
            
            # Analyze file
            self.analyze_file()
            
            self.update_status(f"Loaded: {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def analyze_file(self):
        """Analyze the loaded file"""
        if not self.current_content:
            return
        
        language = self.deobfuscator.detect_language(self.current_content)
        analysis = self.deobfuscator.analyze_obfuscation(self.current_content, language)
        
        # Display analysis
        self.analysis_text.delete(1.0, tk.END)
        
        self.analysis_text.insert(tk.END, "=== OBFUSCATION ANALYSIS ===\n\n")
        self.analysis_text.insert(tk.END, f"File: {os.path.basename(self.current_file)}\n")
        self.analysis_text.insert(tk.END, f"Language: {language}\n")
        self.analysis_text.insert(tk.END, f"Size: {len(self.current_content):,} bytes\n\n")
        
        if analysis:
            self.analysis_text.insert(tk.END, "Detected Techniques:\n")
            self.analysis_text.insert(tk.END, "-" * 40 + "\n")
            for item in analysis:
                confidence_color = self.success_color if item['confidence'] > 80 else self.warning_color
                self.analysis_text.insert(tk.END, f"• {item['technique']}: {item['details']}\n")
                self.analysis_text.insert(tk.END, f"  Confidence: {item['confidence']}%\n\n")
        else:
            self.analysis_text.insert(tk.END, "No obvious obfuscation techniques detected.\n")
        
        # Show statistics
        self.show_statistics()
    
    def show_statistics(self):
        """Show file statistics"""
        if not self.current_content:
            return
        
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=== FILE STATISTICS ===\n\n")
        
        # Basic stats
        self.stats_text.insert(tk.END, f"File Name: {os.path.basename(self.current_file)}\n")
        self.stats_text.insert(tk.END, f"File Size: {len(self.current_content):,} bytes\n")
        self.stats_text.insert(tk.END, f"Lines: {self.current_content.count(chr(10)) + 1}\n")
        
        # Hash values
        import hashlib
        md5 = hashlib.md5(self.current_content.encode()).hexdigest()
        sha256 = hashlib.sha256(self.current_content.encode()).hexdigest()
        
        self.stats_text.insert(tk.END, f"\nMD5: {md5}\n")
        self.stats_text.insert(tk.END, f"SHA256: {sha256}\n")
        
        # Character statistics
        self.stats_text.insert(tk.END, "\n=== CHARACTER ANALYSIS ===\n\n")
        
        total_chars = len(self.current_content)
        printable = sum(1 for c in self.current_content if c.isprintable() or c in '\n\r\t')
        non_printable = total_chars - printable
        
        self.stats_text.insert(tk.END, f"Total Characters: {total_chars:,}\n")
        self.stats_text.insert(tk.END, f"Printable: {printable:,} ({printable/total_chars*100:.1f}%)\n")
        self.stats_text.insert(tk.END, f"Non-printable: {non_printable:,} ({non_printable/total_chars*100:.1f}%)\n")
        
        # Check for suspicious patterns
        self.stats_text.insert(tk.END, "\n=== SUSPICIOUS PATTERNS ===\n\n")
        
        patterns = [
            ("Base64 strings", r'[A-Za-z0-9+/]{20,}={0,2}'),
            ("Hex escapes", r'\\x[0-9a-fA-F]{2}'),
            ("Unicode escapes", r'\\u[0-9a-fA-F]{4}'),
            ("eval calls", r'eval\('),
            ("exec calls", r'exec\('),
            ("base64 -d", r'base64.*-d'),
        ]
        
        for name, pattern in patterns:
            count = len(re.findall(pattern, self.current_content))
            if count > 0:
                self.stats_text.insert(tk.END, f"{name}: {count}\n")
    
    def deobfuscate(self):
        """Deobfuscate the current file"""
        if not self.current_content:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        
        try:
            self.update_status("Deobfuscating...")
            self.progress_bar.start()
            self.root.update()
            
            # Get aggressive mode setting
            aggressive = self.aggressive_var.get()
            
            # Deobfuscate
            deobfuscated, info = self.deobfuscator.deobfuscate_file(
                self.current_file, aggressive
            )
            
            # Store results
            self.deobfuscated_content = deobfuscated
            self.analysis_info = info
            
            # Display deobfuscated content
            self.deobfuscated_text.delete(1.0, tk.END)
            self.deobfuscated_text.insert(1.0, deobfuscated)
            
            # Update analysis tab
            self.update_analysis_tab(info)
            
            # Switch to deobfuscated tab
            self.notebook.select(1)  # Index 1 is deobfuscated tab
            
            self.update_status(f"Deobfuscation complete. Reduced by {self.get_reduction_percentage():.1f}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Deobfuscation failed: {str(e)}")
            self.update_status("Deobfuscation failed")
        finally:
            self.progress_bar.stop()
    
    def update_analysis_tab(self, info):
        """Update analysis tab with deobfuscation info"""
        self.analysis_text.delete(1.0, tk.END)
        
        self.analysis_text.insert(tk.END, "=== DEOBFUSCATION REPORT ===\n\n")
        
        self.analysis_text.insert(tk.END, f"File: {info.get('filename', 'Unknown')}\n")
        self.analysis_text.insert(tk.END, f"Language: {info.get('language', 'Unknown')}\n")
        self.analysis_text.insert(tk.END, f"Timestamp: {info.get('timestamp', 'Unknown')}\n\n")
        
        self.analysis_text.insert(tk.END, "=== SIZE COMPARISON ===\n\n")
        orig_len = info.get('original_length', 0)
        deob_len = info.get('deobfuscated_length', 0)
        reduction = ((orig_len - deob_len) / orig_len * 100) if orig_len > 0 else 0
        
        self.analysis_text.insert(tk.END, f"Original: {orig_len:,} bytes\n")
        self.analysis_text.insert(tk.END, f"Deobfuscated: {deob_len:,} bytes\n")
        self.analysis_text.insert(tk.END, f"Reduction: {reduction:.1f}%\n\n")
        
        self.analysis_text.insert(tk.END, "=== TECHNIQUES FOUND ===\n\n")
        techniques = info.get('analysis', [])
        if techniques:
            for tech in techniques:
                color = self.success_color if tech['confidence'] > 80 else self.warning_color
                self.analysis_text.insert(tk.END, f"• {tech['technique']}\n")
                self.analysis_text.insert(tk.END, f"  Confidence: {tech['confidence']}%\n")
                self.analysis_text.insert(tk.END, f"  Details: {tech['details']}\n\n")
        else:
            self.analysis_text.insert(tk.END, "No obfuscation techniques detected.\n\n")
        
        self.analysis_text.insert(tk.END, "=== DEOBFUSCATION STEPS ===\n\n")
        steps = info.get('steps', [])
        if steps:
            for i, step in enumerate(steps, 1):
                self.analysis_text.insert(tk.END, f"{i}. {step}\n")
        else:
            self.analysis_text.insert(tk.END, "No deobfuscation steps recorded.\n")
    
    def get_reduction_percentage(self):
        """Calculate size reduction percentage"""
        if not self.current_content or not self.deobfuscated_content:
            return 0
        
        orig_len = len(self.current_content)
        deob_len = len(self.deobfuscated_content)
        
        if orig_len == 0:
            return 0
        
        return ((orig_len - deob_len) / orig_len) * 100
    
    def save_result(self):
        """Save deobfuscated result to file"""
        if not self.deobfuscated_content:
            messagebox.showwarning("Warning", "No deobfuscated content to save!")
            return
        
        # Suggest filename
        if self.current_file:
            base_name = os.path.basename(self.current_file)
            name, ext = os.path.splitext(base_name)
            suggested_name = f"{name}_deobfuscated{ext}"
        else:
            suggested_name = "deobfuscated_result.txt"
        
        filename = filedialog.asksaveasfilename(
            title="Save Deobfuscated Result",
            initialfile=suggested_name,
            defaultextension=".txt",
            filetypes=[
                ("All files", "*.*"),
                ("Python files", "*.py"),
                ("Bash files", "*.sh"),
                ("Text files", "*.txt"),
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.deobfuscated_content)
                
                # Also save analysis report
                report_filename = f"{os.path.splitext(filename)[0]}_report.txt"
                with open(report_filename, 'w', encoding='utf-8') as f:
                    f.write(self.analysis_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"Saved deobfuscated file to:\n{filename}\n\nAnalysis report saved to:\n{report_filename}")
                self.update_status(f"Saved to {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def batch_deobfuscate(self):
        """Batch deobfuscate multiple files"""
        messagebox.showinfo("Info", "Batch deobfuscation feature coming soon!")
    
    def compare_files(self):
        """Compare original and deobfuscated files"""
        if not self.current_content or not self.deobfuscated_content:
            messagebox.showwarning("Warning", "Load and deobfuscate a file first!")
            return
        
        # Create comparison window
        compare_win = Toplevel(self.root)
        compare_win.title("File Comparison")
        compare_win.geometry("1000x700")
        
        # Create split view
        paned = ttk.PanedWindow(compare_win, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Original side
        orig_frame = ttk.Frame(paned)
        ttk.Label(orig_frame, text="ORIGINAL", font=('Segoe UI', 11, 'bold')).pack(pady=5)
        orig_text = scrolledtext.ScrolledText(
            orig_frame, wrap=tk.WORD, font=('Consolas', 9),
            bg='#1e1e1e', fg='#d4d4d4', height=30
        )
        orig_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        orig_text.insert(1.0, self.current_content)
        orig_text.configure(state='disabled')
        
        # Deobfuscated side
        deob_frame = ttk.Frame(paned)
        ttk.Label(deob_frame, text="DEOBFUSCATED", font=('Segoe UI', 11, 'bold')).pack(pady=5)
        deob_text = scrolledtext.ScrolledText(
            deob_frame, wrap=tk.WORD, font=('Consolas', 9),
            bg='#1e1e1e', fg='#d4d4d4', height=30
        )
        deob_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        deob_text.insert(1.0, self.deobfuscated_content)
        deob_text.configure(state='disabled')
        
        paned.add(orig_frame)
        paned.add(deob_frame)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_win = Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("500x400")
        
        # Create settings notebook
        settings_notebook = ttk.Notebook(settings_win)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="General")
        
        ttk.Label(general_frame, text="Deobfuscation Settings", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        # Auto-detect language
        auto_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Auto-detect script language",
                       variable=auto_detect_var).pack(anchor=tk.W, pady=5)
        
        # Save report automatically
        save_report_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Save analysis report automatically",
                       variable=save_report_var).pack(anchor=tk.W, pady=5)
        
        # Advanced settings
        advanced_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(advanced_frame, text="Advanced")
        
        ttk.Label(advanced_frame, text="Advanced Options", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        # Max recursion depth
        ttk.Label(advanced_frame, text="Max recursion depth:").pack(anchor=tk.W, pady=5)
        depth_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=10, width=10)
        depth_spinbox.pack(anchor=tk.W, pady=5)
        depth_spinbox.set(5)
        
        # Timeout settings
        ttk.Label(advanced_frame, text="Timeout (seconds):").pack(anchor=tk.W, pady=5)
        timeout_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=60, width=10)
        timeout_spinbox.pack(anchor=tk.W, pady=5)
        timeout_spinbox.set(30)
        
        # Save/Cancel buttons
        button_frame = ttk.Frame(settings_win)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=settings_win.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_win.destroy).pack(side=tk.RIGHT, padx=5)
    
    def show_hex_view(self):
        """Show hex view of current file"""
        if not self.current_content:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        
        hex_win = Toplevel(self.root)
        hex_win.title("Hex View")
        hex_win.geometry("800x600")
        
        # Create hex view text widget
        hex_text = scrolledtext.ScrolledText(
            hex_win, wrap=tk.WORD, font=('Consolas', 9),
            bg='#000000', fg='#00ff00'
        )
        hex_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Convert to hex
        hex_content = self.current_content.encode()
        hex_dump = ""
        
        for i in range(0, len(hex_content), 16):
            # Offset
            hex_dump += f"{i:08x}: "
            
            # Hex values
            for j in range(16):
                if i + j < len(hex_content):
                    hex_dump += f"{hex_content[i + j]:02x} "
                else:
                    hex_dump += "   "
            
            hex_dump += " "
            
            # ASCII representation
            for j in range(16):
                if i + j < len(hex_content):
                    char = hex_content[i + j]
                    if 32 <= char <= 126:
                        hex_dump += chr(char)
                    else:
                        hex_dump += "."
                else:
                    hex_dump += " "
            
            hex_dump += "\n"
        
        hex_text.insert(1.0, hex_dump)
        hex_text.configure(state='disabled')
    
    def show_strings_view(self):
        """Show printable strings from file"""
        if not self.current_content:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        
        strings_win = Toplevel(self.root)
        strings_win.title("Strings View")
        strings_win.geometry("800x600")
        
        # Create strings view text widget
        strings_text = scrolledtext.ScrolledText(
            strings_win, wrap=tk.WORD, font=('Consolas', 9),
            bg='#1e1e1e', fg='#d4d4d4'
        )
        strings_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Extract printable strings (minimum 4 characters)
        content_bytes = self.current_content.encode()
        strings = []
        current_string = []
        
        for byte in content_bytes:
            if 32 <= byte <= 126:
                current_string.append(chr(byte))
            else:
                if len(current_string) >= 4:
                    strings.append(''.join(current_string))
                current_string = []
        
        # Add last string if any
        if len(current_string) >= 4:
            strings.append(''.join(current_string))
        
        # Display strings
        strings_text.insert(1.0, f"Found {len(strings)} printable strings (min 4 chars):\n\n")
        for i, s in enumerate(strings, 1):
            strings_text.insert(tk.END, f"{i:4d}. {s}\n")
    
    def show_guide(self):
        """Show user guide"""
        guide_text = """
        ADVANCED DEOBFUSCATOR TOOL - USER GUIDE
        
        1. LOADING FILES
           - Click 'Browse' or use File -> Open (Ctrl+O)
           - Supports Python (.py), Bash (.sh), and text files
        
        2. DEOBFUSCATION
           - Click 'Deobfuscate' to analyze and deobfuscate
           - Enable 'Aggressive Mode' for more thorough deobfuscation
           - View results in the 'Deobfuscated' tab
        
        3. ANALYSIS
           - The 'Analysis' tab shows detected obfuscation techniques
           - The 'Statistics' tab shows file metrics and patterns
        
        4. SAVING RESULTS
           - Use 'Save Result' or File -> Save (Ctrl+S)
           - Saves both deobfuscated code and analysis report
        
        5. ADDITIONAL TOOLS
           - Hex View: View file in hexadecimal format
           - Strings View: Extract printable strings
           - Compare: Side-by-side comparison of original/deobfuscated
        
        SUPPORTED OBFUSCATION TECHNIQUES:
        - Base64 encoding (single and multiple layers)
        - Hexadecimal encoding (\x00 style)
        - Unicode escapes (\u0000)
        - ROT13/ROT-N encryption
        - Python marshal serialization
        - eval()/exec() obfuscation
        - String manipulation
        - And more...
        """
        
        guide_win = Toplevel(self.root)
        guide_win.title("User Guide")
        guide_win.geometry("700x500")
        
        guide_text_widget = scrolledtext.ScrolledText(
            guide_win, wrap=tk.WORD, font=('Segoe UI', 10)
        )
        guide_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        guide_text_widget.insert(1.0, guide_text)
        guide_text_widget.configure(state='disabled')
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        ADVANCED REVERSE ENGINEERING TOOL
        
        Version: 2.0
        Author: ATHEX BLACK HAT
        
        Description:
        A comprehensive tool for deobfuscating Bash and Python scripts.
        Supports multiple obfuscation techniques and provides detailed analysis.
        
        Features:
        - Support for Bash and Python scripts
        - Detection of multiple obfuscation techniques
        - GUI interface with side-by-side comparison
        - Statistical analysis and reporting
        - Hex view and strings extraction
        
  License:
         
DONT TRY TO MODIFY OR SELL THIS TOOL. IF YOU TRY ILL FUCK YOUR SYSTEM SILENTLY BECAUSE THIS SCRIPT HAVE HIDDEN PAYLOAD. IF YOU TRY TO MODIFY ONE LINE OF CODE THE PAYLAOD AUTOMATICALLY INJECT IN HARDWARE AND GIVE FULL ACCESS OF YOUR SYSTEM TO ATHEX BLACK HAT. THEN YOU KNOW WHAT ATHEX CAN DO THEY HAVE POWER TO DESTROY THE WHOLE WORLD IN JUST SOME CLICKS SO WHO ARE YOU THEN MFS.
        """
        
        messagebox.showinfo("About", about_text)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update()


def main():
    """Main entry point"""
    if GUI_AVAILABLE:
        # Run with GUI
        root = tk.Tk()
        app = DeobfuscatorGUI(root)
        root.mainloop()
    else:
        # Run in CLI mode
        print("GUI not available. Running in command-line mode.")
        print("Usage: python deobfuscator.py -f <file> [-a]")
        print("Options:")
        print("  -f, --file      File to deobfuscate")
        print("  -a, --aggressive Use aggressive deobfuscation")
        print("  -o, --output    Output file (optional)")
        
        # Simple CLI functionality
        import argparse
        parser = argparse.ArgumentParser(description="Deobfuscate Bash/Python scripts")
        parser.add_argument("-f", "--file", required=True, help="Input file")
        parser.add_argument("-a", "--aggressive", action="store_true", help="Aggressive mode")
        parser.add_argument("-o", "--output", help="Output file")
        
        args = parser.parse_args()
        
        deobfuscator = AdvancedDeobfuscator()
        result, info = deobfuscator.deobfuscate_file(args.file, args.aggressive)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Deobfuscated content saved to: {args.output}")
        else:
            print("\n=== DEOBFUSCATED CONTENT ===\n")
            print(result[:2000])  # Print first 2000 chars
            if len(result) > 2000:
                print(f"\n[...] Output truncated. Total: {len(result):,} chars")
            
            # Print analysis summary
            print(f"\n=== ANALYSIS SUMMARY ===")
            print(f"File: {info.get('filename')}")
            print(f"Language: {info.get('language')}")
            print(f"Original size: {info.get('original_length'):,} bytes")
            print(f"Deobfuscated size: {info.get('deobfuscated_length'):,} bytes")
            
            techniques = info.get('analysis', [])
            if techniques:
                print(f"\nDetected techniques:")
                for tech in techniques:
                    print(f"  - {tech['technique']} ({tech['confidence']}%)")


if __name__ == "__main__":
    main()