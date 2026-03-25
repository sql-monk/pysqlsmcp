import json
import datetime
from pathlib import Path

import mssql_python

_LOG_PATH = Path(__file__).parent / "sqlsmcp.log"

_SET_PREAMBLE = """
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET LOCK_TIMEOUT 1000;
SET DEADLOCK_PRIORITY LOW;
"""

_LIST_DATABASES_SQL = """
SELECT name FROM sys.databases
WHERE state_desc = 'ONLINE'
  AND HAS_DBACCESS(name) = 1
ORDER BY name
"""


class DbProvider:
    def __init__(self, server: str, database: str, username: str | None = None, password: str | None = None):
        self._server = server
        self._database = database
        self._username = username
        self._password = password

    def _connection_string(self) -> str:
        if self._username and self._password:
            return (
                f"SERVER={self._server};DATABASE={self._database};"
                f"UID={self._username};PWD={self._password};"
                "TrustServerCertificate=yes;CommandTimeout=60;"
            )
        return (
            f"SERVER={self._server};DATABASE={self._database};"
            "Trusted_Connection=yes;TrustServerCertificate=yes;CommandTimeout=60;"
        )

    def execute_query(self, query: str, params: tuple | None = None) -> str:
        try:
            conn = mssql_python.connect(self._connection_string())
            try:
                cursor = conn.cursor()
                cursor.execute(_SET_PREAMBLE)
                cursor.execute(query, params or ())
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                result = {
                    "query": query,
                    "rowCount": len(rows),
                    "columns": columns,
                    "rows": [list(row) for row in rows],
                }
            finally:
                conn.close()
        except Exception as e:
            sql_error_number = None
            sql_state = None
            if hasattr(e, "args") and e.args:
                if len(e.args) >= 2:
                    sql_error_number = e.args[0]
                    sql_state = e.args[1]
                else:
                    sql_error_number = e.args[0]
            result = {
                "error": str(e),
                "query": query,
                "sqlErrorNumber": sql_error_number,
                "sqlState": sql_state,
            }
        return json.dumps(result, default=str)

    def list_databases(self) -> list[str]:
        conn = mssql_python.connect(self._connection_string())
        try:
            cursor = conn.cursor()
            cursor.execute(_SET_PREAMBLE)
            cursor.execute(_LIST_DATABASES_SQL)
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [row[0] for row in rows]

    def _log(self, tool_name: str, **fields) -> None:
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        parts = " ".join(f"{k}={v!r}" for k, v in fields.items())
        line = f"{timestamp} [{tool_name}] {parts}\n"
        try:
            with open(_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line)
        except OSError:
            pass
