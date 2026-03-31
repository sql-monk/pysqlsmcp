"""
pysqlsmcp installer
  - generates TLS certificates (if missing)
  - creates SQL Server logins / users via scripts/mcp-server.sql or scripts/mcp-database.sql
  - registers the MCP server in agent config files (VS Code, Claude Desktop, etc.)
"""

import json
import os
import re
import secrets
import string
import sys
from pathlib import Path

import mssql_python

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
CERT_FILE = ROOT / "cert.pem"
KEY_FILE = ROOT / "key.pem"

# ── helpers ──────────────────────────────────────────────────

def _heading(text: str) -> None:
    print(f"\n{'=' * 60}\n  {text}\n{'=' * 60}")


def _ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{hint}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def _generate_password(length: int = 40) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "!@#$%^&*()-_=+" for c in pwd)
        if has_upper and has_lower and has_digit and has_special:
            return pwd


# ── 1. certificates ─────────────────────────────────────────

def ensure_certificates() -> None:
    _heading("TLS Certificates")
    if CERT_FILE.exists() and KEY_FILE.exists():
        print(f"  cert.pem and key.pem already exist — skipping.")
        return

    print("  Generating self-signed certificate …")
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    import datetime
    import ipaddress

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    KEY_FILE.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )

    subject = issuer = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=365)
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    CERT_FILE.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    print("  ✓ cert.pem and key.pem created.")


# ── 2. SQL Server users ─────────────────────────────────────

def _run_sql_script(server: str, script_path: Path, replacements: dict[str, str],
                    database: str = "master") -> None:
    """Read a .sql template, apply replacements, execute via mssql_python."""
    sql = script_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        sql = sql.replace(placeholder, value)

    # Split on GO batch separators
    batches = re.split(r'^\s*GO\s*$', sql, flags=re.MULTILINE | re.IGNORECASE)
    # Strip USE statements — we connect to the target database directly
    cleaned: list[str] = []
    for b in batches:
        b = re.sub(r'(?im)^\s*USE\s+\[.*?\]\s*;?\s*$', '', b).strip()
        if b:
            cleaned.append(b)

    conn_str = (
        f"SERVER={server};DATABASE={database};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    conn = mssql_python.connect(conn_str)
    try:
        cursor = conn.cursor()
        for batch in cleaned:
            cursor.execute(batch)
    finally:
        conn.close()


def setup_sql_users() -> None:
    _heading("SQL Server Users")
    if not _ask_yes_no("Create MCP users on a SQL Server instance?"):
        return

    server = input("  SQL Server instance (e.g. localhost): ").strip()
    if not server:
        print("  Skipped — no server provided.")
        return

    # Server-level login
    if _ask_yes_no("  Create server-level login (mcp-server)?"):
        password = _generate_password()
        _run_sql_script(server, SCRIPTS / "mcp-server.sql",
                        {"{{PASSWORD}}": password}, database="master")
        print("  ✓ Server-level login 'mcp-server' created (password auto-generated, not stored).")

    # Database-level logins
    while _ask_yes_no("  Create database-level user for a specific database?"):
        db_name = input("    Database name: ").strip()
        if not db_name:
            print("    Skipped — no name provided.")
            continue
        password = _generate_password()
        _run_sql_script(server, SCRIPTS / "mcp-database.sql", {
            "{{DATABASE}}": db_name,
            "{{PASSWORD}}": password,
        }, database=db_name)
        print(f"  ✓ Database-level user 'mcp-{db_name}' created (password auto-generated, not stored).")


# ── 3. agent integration ────────────────────────────────────

KNOWN_CONFIGS = {
    "VS Code (user)": {
        "relative": Path("Code", "User", "mcp.json"),
        "env": "APPDATA",
    },
    "Claude Desktop": {
        "relative": Path("Claude", "claude_desktop_config.json"),
        "env": "APPDATA",
    },
}


def _server_entry_vscode(host: str, port: int) -> dict:
    return {
        "type": "http",
        "url": f"https://{host}:{port}/mcp/",
    }


def _server_entry_claude(host: str, port: int) -> dict:
    python = sys.executable
    return {
        "command": python,
        "args": [
            str(ROOT / "server.py"),
            "--certfile", str(CERT_FILE),
            "--keyfile", str(KEY_FILE),
            "--host", host,
            "--port", str(port),
        ],
    }


def _find_config_files(search_root: Path) -> list[Path]:
    """Recursively search for known MCP config files."""
    found: list[Path] = []
    for label, info in KNOWN_CONFIGS.items():
        env_val = os.environ.get(info["env"], "")
        if env_val:
            candidate = Path(env_val) / info["relative"]
            if candidate.exists():
                found.append(candidate)
    # Also scan for mcp.json / claude_desktop_config.json under search_root
    if search_root.exists():
        for pattern in ("**/mcp.json", "**/claude_desktop_config.json"):
            for p in search_root.glob(pattern):
                if p not in found:
                    found.append(p)
    return found


def _patch_vscode_mcp(config_path: Path, host: str, port: int) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("servers", {})
    servers["pysqlsmcp"] = _server_entry_vscode(host, port)
    if "inputs" not in data:
        data["inputs"] = []
    config_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")


def _patch_claude_config(config_path: Path, host: str, port: int) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("mcpServers", {})
    servers["pysqlsmcp"] = _server_entry_claude(host, port)
    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def setup_agent_integration() -> None:
    _heading("Agent Integration")
    if not _ask_yes_no("Register pysqlsmcp in an agent config?"):
        return

    host = input("  Server host [localhost]: ").strip() or "localhost"
    port_str = input("  Server port [4433]: ").strip() or "4433"
    port = int(port_str)

    home = Path.home()
    search_root_str = input(f"  Search for config files in [{home}]: ").strip()
    search_root = Path(search_root_str) if search_root_str else home

    configs = _find_config_files(search_root)
    if not configs:
        print("  No agent config files found.")
        return

    print("  Found config files:")
    for i, p in enumerate(configs, 1):
        print(f"    {i}. {p}")

    selection = input("  Which to patch? (comma-separated numbers, or 'all'): ").strip().lower()
    if selection == "all":
        selected = configs
    else:
        indices = [int(x.strip()) - 1 for x in selection.split(",") if x.strip().isdigit()]
        selected = [configs[i] for i in indices if 0 <= i < len(configs)]

    for config_path in selected:
        try:
            if config_path.name == "mcp.json":
                _patch_vscode_mcp(config_path, host, port)
            elif config_path.name == "claude_desktop_config.json":
                _patch_claude_config(config_path, host, port)
            else:
                print(f"  ⚠ Unknown config format: {config_path.name} — skipped.")
                continue
            print(f"  ✓ Patched {config_path}")
        except Exception as e:
            print(f"  ✗ Failed to patch {config_path}: {e}")


# ── main ─────────────────────────────────────────────────────

def main() -> None:
    _heading("pysqlsmcp installer")
    ensure_certificates()
    setup_sql_users()
    setup_agent_integration()
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
