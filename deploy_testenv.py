"""
Deploy test databases (mcp_test_main, mcp_test_aux) for integration testing.
"""

import re
import secrets
import string
from pathlib import Path

import mssql_python

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"


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


def _run_sql_script(server: str, database: str, script_path: Path, replacements: dict[str, str]) -> None:
    """Execute a single-database .sql script against the given database.

    Splits on GO, runs two passes so that cross-database references succeed
    regardless of object ordering within the script.
    """
    sql = script_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        sql = sql.replace(placeholder, value)

    batches = [
        b.strip()
        for b in re.split(r'^\s*GO\s*$', sql, flags=re.MULTILINE | re.IGNORECASE)
        if b.strip()
    ]

    conn_str = (
        f"SERVER={server};DATABASE={database};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    conn = mssql_python.connect(conn_str, autocommit=True)
    try:
        # First pass — collect failures caused by cross-database ordering.
        deferred: list[str] = []
        for batch in batches:
            try:
                conn.cursor().execute(batch)
            except Exception:
                deferred.append(batch)

        # Second pass — retry; all base objects should now exist.
        for batch in deferred:
            conn.cursor().execute(batch)
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
        _run_sql_script(server, "master",        SCRIPTS / "deploy-testenv-server.sql",        replacements)
        _run_sql_script(server, "mcp_test_main", SCRIPTS / "deploy-testenv-mcp-test-main.sql", replacements)
        _run_sql_script(server, "mcp_test_aux",  SCRIPTS / "deploy-testenv-mcp-test-aux.sql",  replacements)
        print("+ Databases mcp_test_main and mcp_test_aux deployed successfully.")
        print("  Test users: mcp-test-reader, mcp-test-writer, mcp-test-admin")
        print("  NOTE: Grant IMPERSONATE on these users to your connecting login.")
    except Exception as e:
        print(f"- Failed to deploy test databases: {e}")


if __name__ == "__main__":
    setup_test_databases()
