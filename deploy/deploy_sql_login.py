"""
pysqlsmcp — SQL Server login setup
  - creates SQL Server users for impersonation via scripts/mcp-database.sql
"""

import re
import secrets
import string
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


# ── SQL Server users ─────────────────────────────────────────

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


# ── main ─────────────────────────────────────────────────────

def main() -> None:
    _heading("pysqlsmcp — SQL login setup")
    setup_sql_users()
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
