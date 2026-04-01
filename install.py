"""
pysqlsmcp installer
  - creates SQL Server users for impersonation via scripts/mcp-database.sql
  - deploys test databases (mcp_test_main, mcp_test_aux) for integration testing
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


# ── 1. SQL Server users ──────────────────────────────────────

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
        print("  - Skipped — no server provided.")
        return

    while _ask_yes_no("  Create MCP user for a database?"):
        db_name = input("    Database name: ").strip()
        if not db_name:
            print("    - Skipped — no name provided.")
            continue
        password = _generate_password()
        _run_sql_script(server, SCRIPTS / "mcp-database.sql", {
            "{{DATABASE}}": db_name,
            "{{PASSWORD}}": password,
        }, database=db_name)
        print(f"+ User 'mcp-{db_name}' created (password auto-generated, not stored).")


# ── 2. deploy test databases ─────────────────────────────────

def _run_sql_script_raw(server: str, script_path: Path, replacements: dict[str, str]) -> None:
    """Execute a multi-database .sql script via master, keeping USE/GO semantics."""
    sql = script_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        sql = sql.replace(placeholder, value)

    batches = re.split(r'^\s*GO\s*$', sql, flags=re.MULTILINE | re.IGNORECASE)

    conn_str = (
        f"SERVER={server};DATABASE=master;"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    conn = mssql_python.connect(conn_str)
    try:
        cursor = conn.cursor()
        for batch in batches:
            batch = batch.strip()
            if batch:
                cursor.execute(batch)
    finally:
        conn.close()


def setup_test_databases() -> None:
    _heading("Test Databases")
    if not _ask_yes_no("Deploy test databases (mcp_test_main, mcp_test_aux)?", default=False):
        return

    server = input("  SQL Server instance (e.g. localhost): ").strip()
    if not server:
        print("  - Skipped — no server provided.")
        return

    replacements = {
        "{{PASSWORD_READER}}": _generate_password(),
        "{{PASSWORD_WRITER}}": _generate_password(),
        "{{PASSWORD_ADMIN}}":  _generate_password(),
    }

    try:
        _run_sql_script_raw(server, SCRIPTS / "deploy-test-databases.sql", replacements)
        print("+ Databases mcp_test_main and mcp_test_aux deployed successfully.")
        print("  Test users: mcp-test-reader, mcp-test-writer, mcp-test-admin")
        print("  NOTE: Grant IMPERSONATE on these users to your connecting login.")
    except Exception as e:
        print(f"- Failed to deploy test databases: {e}")


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


def _server_entry() -> dict:
    python = sys.executable
    return {
        "command": python,
        "args": [str(ROOT / "sqlsmcp.py")],
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


def _patch_vscode_mcp(config_path: Path) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("servers", {})
    servers["pysqlsmcp"] = _server_entry()
    if "inputs" not in data:
        data["inputs"] = []
    config_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")


def _patch_claude_config(config_path: Path) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("mcpServers", {})
    servers["pysqlsmcp"] = _server_entry()
    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def setup_agent_integration() -> None:
    _heading("Agent Integration")
    if not _ask_yes_no("Register pysqlsmcp in an agent config?"):
        return

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
                _patch_vscode_mcp(config_path)
            elif config_path.name == "claude_desktop_config.json":
                _patch_claude_config(config_path)
            else:
                print(f"! Unknown config format: {config_path.name} — skipped.")
                continue
            print(f"+ Patched {config_path}")
        except Exception as e:
            print(f"- Failed to patch {config_path}: {e}")


# ── main ─────────────────────────────────────────────────────

def main() -> None:
    _heading("pysqlsmcp installer")
    setup_sql_users()
    setup_test_databases()
    setup_agent_integration()
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
