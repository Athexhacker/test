#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║       ATHEX VORTEX — ADMIN LICENSE GENERATOR v1.0.0     ║
║                   generator.py  [PRIVATE]                ║
╚══════════════════════════════════════════════════════════╝
⚠  KEEP THIS FILE AND THE admin/ FOLDER PRIVATE.
   Do NOT distribute to clients.

Run:  python generator.py
Auto-installs: cryptography rich
"""

# ── 1. Auto-install ───────────────────────────────────────
import subprocess, sys, importlib.util as _ilu

_DEPS = {"cryptography": "cryptography", "rich": "rich"}

def _pip(pkg):
    for extra in ([], ["--break-system-packages"]):
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg] + extra,
            capture_output=True)
        if r.returncode == 0: return True
    return False

_miss = [pkg for mod, pkg in _DEPS.items() if _ilu.find_spec(mod) is None]
if _miss:
    print(f"[SETUP] Installing: {', '.join(_miss)}")
    for p in _miss: _pip(p)
    import os as _os
    _os.execv(sys.executable, [sys.executable] + sys.argv)

# ── 2. Imports ────────────────────────────────────────────
import os, json, struct, base64, sqlite3, secrets, hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm

console = Console()

# ── 3. Paths ──────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
ADMIN_DIR    = BASE_DIR / "admin"
PRIV_KEY     = ADMIN_DIR / "private.pem"
PUB_KEY_DEST = BASE_DIR / "config" / "public.pem"
DB_FILE      = ADMIN_DIR / "licenses.db"
EXPORT_DIR   = ADMIN_DIR / "exported_keys"

for _d in [ADMIN_DIR, EXPORT_DIR, BASE_DIR / "config"]:
    _d.mkdir(parents=True, exist_ok=True)

ASCII_LOGO = r"""
  ▄████  ███▄    █  ██▀███   █████╗ ████████╗ ██████╗ ██████╗
 ██▒ ▀█▒ ██ ▀█   █ ▓██ ▒ ██▒██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
▒██░▄▄▄░▓██  ▀█ ██▒▓██ ░▄█ ▒███████║   ██║   ██║   ██║██████╔╝
░▓█  ██▓▓██▒  ▐▌██▒▒██▀▀█▄  ██╔══██║   ██║   ██║   ██║██╔══██╗
░▒▓███▀▒▒██░   ▓██░░██▓ ▒██▒██║  ██║   ██║   ╚██████╔╝██║  ██║
 ░▒   ▒ ░ ▒░   ▒ ▒ ░ ▒▓ ░▒▓╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
   V O R T E X  ──  A D M I N  L I C E N S E  G E N E R A T O R
"""

# ── 4. RSA key management ─────────────────────────────────
_priv_key = None
_pub_key  = None

def load_or_generate_keys():
    global _priv_key, _pub_key
    if PRIV_KEY.exists():
        _priv_key = serialization.load_pem_private_key(
            PRIV_KEY.read_bytes(), password=None, backend=default_backend())
        _pub_key  = _priv_key.public_key()
        console.print("[green]✓ RSA-2048 keypair loaded[/green]")
    else:
        console.print("[yellow]⚙  Generating new RSA-2048 keypair…[/yellow]")
        _priv_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend())
        _pub_key = _priv_key.public_key()
        PRIV_KEY.write_bytes(_priv_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()))
        try: PRIV_KEY.chmod(0o600)
        except Exception: pass
        console.print(f"[green]✓ Private key → {PRIV_KEY}[/green]")
        _export_pub()

def _export_pub():
    pub_pem = _pub_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo)
    PUB_KEY_DEST.write_bytes(pub_pem)
    console.print(f"[cyan]✓ Public key → {PUB_KEY_DEST}[/cyan]")
    console.print("[bold yellow]ACTION: distribute config/public.pem alongside run.py[/bold yellow]")

def sign(data: bytes) -> bytes:
    return _priv_key.sign(data, padding.PKCS1v15(), hashes.SHA256())

# ── 5. Database ───────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""CREATE TABLE IF NOT EXISTS licenses(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        key_id      TEXT UNIQUE NOT NULL,
        hwid        TEXT NOT NULL,
        holder      TEXT NOT NULL,
        issued      TEXT NOT NULL,
        expires     TEXT,
        lifetime    INTEGER DEFAULT 0,
        max_tunnels INTEGER DEFAULT 1,
        key_blob    TEXT NOT NULL,
        revoked     INTEGER DEFAULT 0,
        notes       TEXT)""")
    conn.commit(); conn.close()

def db_insert(key_id, hwid, holder, issued, expires,
              lifetime, max_tunnels, blob, notes=""):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""INSERT INTO licenses
        (key_id,hwid,holder,issued,expires,lifetime,max_tunnels,key_blob,notes)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        (key_id, hwid, holder, issued, expires, lifetime, max_tunnels, blob, notes))
    conn.commit(); conn.close()

def db_all():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("""SELECT key_id,hwid,holder,issued,expires,
        lifetime,max_tunnels,revoked,notes FROM licenses ORDER BY id DESC""").fetchall()
    conn.close(); return rows

def db_search(term):
    t = f"%{term}%"
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("""SELECT key_id,hwid,holder,issued,expires,
        lifetime,max_tunnels,revoked,notes FROM licenses
        WHERE key_id LIKE ? OR hwid LIKE ? OR holder LIKE ?""",
        (t,t,t)).fetchall()
    conn.close(); return rows

def db_revoke(key_id) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE licenses SET revoked=1 WHERE key_id=?", (key_id,))
    n = c.rowcount; conn.commit(); conn.close(); return n > 0

def db_blob(key_id) -> Optional[tuple]:
    conn = sqlite3.connect(DB_FILE)
    r = conn.execute("SELECT key_blob,holder,hwid FROM licenses WHERE key_id=?",
                     (key_id,)).fetchone()
    conn.close(); return r

# ── 6. Key generation ─────────────────────────────────────
def generate_key(hwid: str, holder: str, duration_hours: Optional[int],
                 max_tunnels: int, lifetime: bool, notes: str) -> tuple:
    issued_dt = datetime.now(timezone.utc)
    expires_str = None
    if not lifetime:
        expires_str = (issued_dt + timedelta(hours=duration_hours)).isoformat()

    key_id = "VTX-" + secrets.token_hex(8).upper()
    payload = dict(key_id=key_id, hwid=hwid, holder=holder,
                   issued=issued_dt.isoformat(), expires=expires_str,
                   lifetime=lifetime, max_tunnels=max_tunnels, version="1.0")
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode()
    sig    = sign(payload_bytes)
    sig_len= struct.pack(">I", len(sig))
    blob   = base64.urlsafe_b64encode(sig_len + sig + payload_bytes).decode()

    db_insert(key_id, hwid, holder, issued_dt.isoformat(), expires_str,
              1 if lifetime else 0, max_tunnels, blob, notes)
    (EXPORT_DIR / f"{key_id}.key").write_text(blob)
    return key_id, blob

# ── 7. UI helpers ─────────────────────────────────────────
def print_table(rows):
    if not rows:
        console.print("[dim]No records found.[/dim]"); return
    now = datetime.now(timezone.utc)
    t = Table("Key ID","Holder","HWID (short)","Issued","Expires",
              "Max T","Status", show_header=True,
              header_style="bold blue", border_style="dim blue")
    for row in rows:
        kid,hwid,holder,issued,expires,lifetime,max_t,revoked,notes = row
        if revoked:
            status = "[red]REVOKED[/red]"
        elif lifetime:
            status = "[cyan]LIFETIME[/cyan]"
        elif expires:
            exp = datetime.fromisoformat(expires)
            if exp.tzinfo is None: exp = exp.replace(tzinfo=timezone.utc)
            if now > exp: status = "[yellow]EXPIRED[/yellow]"
            else:
                h = int((exp-now).total_seconds()//3600)
                status = f"[green]{h}h left[/green]"
        else: status = "[dim]—[/dim]"
        t.add_row(kid, holder, hwid[:14]+"…", issued[:10],
                  expires[:10] if expires else "∞", str(max_t), status)
    console.print(t)

# ── 8. Menu actions ───────────────────────────────────────
def menu_generate():
    console.rule("[bold green]GENERATE LICENSE KEY[/bold green]")
    hwid    = Prompt.ask("[cyan]Client HWID[/cyan]").strip().upper()
    if len(hwid) < 8: console.print("[red]HWID too short.[/red]"); return
    holder  = Prompt.ask("[cyan]Holder name[/cyan]").strip()
    notes   = Prompt.ask("[cyan]Notes (optional)[/cyan]", default="").strip()

    console.print("\n[bold]Duration:[/bold]")
    console.print("  [green]1[/green]  Hours")
    console.print("  [green]2[/green]  Days")
    console.print("  [green]3[/green]  Lifetime (never expires)")
    ch = Prompt.ask("Choose", choices=["1","2","3"], default="2")

    lifetime = False; duration_hours = None
    if ch == "1":
        hours = int(Prompt.ask("How many hours?", default="24"))
        duration_hours = hours
    elif ch == "2":
        days = int(Prompt.ask("How many days?", default="30"))
        duration_hours = days * 24
    else:
        lifetime = True

    max_t = int(Prompt.ask("[cyan]Max simultaneous tunnels[/cyan]", default="3"))

    console.print(Panel(
        f"HWID:        [magenta]{hwid}[/magenta]\n"
        f"Holder:      [white]{holder}[/white]\n"
        f"Duration:    [yellow]{'LIFETIME' if lifetime else str(duration_hours)+'h'}[/yellow]\n"
        f"Max Tunnels: [white]{max_t}[/white]\n"
        f"Notes:       [dim]{notes or 'none'}[/dim]",
        title="CONFIRM", border_style="green"))

    if not Confirm.ask("Generate?", default=True):
        console.print("[yellow]Cancelled.[/yellow]"); return

    key_id, blob = generate_key(hwid, holder, duration_hours, max_t, lifetime, notes)

    console.print(f"\n[bold green]✓ Key generated: {key_id}[/bold green]")
    console.print(Panel(
        f"[bold yellow]Send this key blob to the client:[/bold yellow]\n\n"
        f"[white]{blob}[/white]",
        title=f"[bold]{key_id}[/bold]", border_style="green"))
    console.print(f"[dim]Saved to: {EXPORT_DIR / (key_id+'.key')}[/dim]")

def menu_list():
    console.rule("[bold blue]ALL LICENSES[/bold blue]")
    print_table(db_all())

def menu_search():
    console.rule("[bold blue]SEARCH[/bold blue]")
    term = Prompt.ask("Search term (HWID / Holder / Key ID)").strip()
    print_table(db_search(term))

def menu_revoke():
    console.rule("[bold red]REVOKE LICENSE[/bold red]")
    kid = Prompt.ask("Key ID to revoke").strip()
    if Confirm.ask(f"Revoke [red]{kid}[/red]?", default=False):
        if db_revoke(kid): console.print(f"[green]✓ Revoked: {kid}[/green]")
        else: console.print(f"[red]Not found: {kid}[/red]")
    else: console.print("[yellow]Cancelled.[/yellow]")

def menu_view():
    console.rule("[bold cyan]VIEW KEY BLOB[/bold cyan]")
    kid = Prompt.ask("Key ID").strip()
    row = db_blob(kid)
    if not row: console.print("[red]Not found.[/red]"); return
    blob, holder, hwid = row
    console.print(Panel(
        f"Key ID:  [cyan]{kid}[/cyan]\n"
        f"Holder:  {holder}\n"
        f"HWID:    {hwid}\n\n"
        f"[bold yellow]KEY BLOB:[/bold yellow]\n[white]{blob}[/white]",
        border_style="cyan"))

def menu_export_pub():
    console.rule("[bold cyan]EXPORT PUBLIC KEY[/bold cyan]")
    _export_pub()
    console.print(Panel(PUB_KEY_DEST.read_text(),
        title="Public Key (place in config/public.pem)", border_style="cyan"))

def menu_stats():
    console.rule("[bold cyan]STATS[/bold cyan]")
    rows = db_all(); now = datetime.now(timezone.utc)
    total = len(rows)
    rev = sum(1 for r in rows if r[7])
    life= sum(1 for r in rows if r[5] and not r[7])
    exp = sum(1 for r in rows if not r[5] and not r[7] and r[4] and
              datetime.fromisoformat(r[4]).replace(tzinfo=timezone.utc) < now)
    active = total - rev - exp
    t = Table(show_header=False, border_style="dim blue")
    t.add_column("", style="dim"); t.add_column("", style="bold")
    t.add_row("Total issued", str(total))
    t.add_row("Active",    f"[green]{active}[/green]")
    t.add_row("Lifetime",  f"[cyan]{life}[/cyan]")
    t.add_row("Expired",   f"[yellow]{exp}[/yellow]")
    t.add_row("Revoked",   f"[red]{rev}[/red]")
    console.print(t)

# ── 9. Main menu ──────────────────────────────────────────
MENU = [
    ("1", "Generate License Key",  menu_generate),
    ("2", "List All Licenses",     menu_list),
    ("3", "Search Licenses",       menu_search),
    ("4", "View Key Blob",         menu_view),
    ("5", "Revoke License",        menu_revoke),
    ("6", "Export Public Key",     menu_export_pub),
    ("7", "Statistics",            menu_stats),
    ("0", "Exit",                  None),
]

def main():
    console.print(Text(ASCII_LOGO, style="bold blue"))
    console.print(Panel(
        "[bold red]⚠  PRIVATE ADMINISTRATIVE TOOL — DO NOT DISTRIBUTE  ⚠[/bold red]",
        border_style="red"))
    load_or_generate_keys()
    init_db()

    while True:
        console.print()
        console.print(Panel(
            "\n".join(f"  [bold cyan]{k}[/bold cyan]  {label}"
                      for k, label, _ in MENU),
            title="[bold blue]⬡ ATHEX VORTEX ADMIN[/bold blue]",
            border_style="blue"))
        choice = Prompt.ask("Select", choices=[k for k,_,_ in MENU], default="0")
        if choice == "0":
            console.print("[dim]Bye.[/dim]"); break
        fn = next(fn for k,_,fn in MENU if k == choice)
        try:
            fn()
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()