import json
import datetime
from pathlib import Path

import mssql_python
import re

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
    def __init__(self, server: str, database: str, impersonate: str = "", timeout: int = 90):
        self._server = server
        self._database = database
        self._impersonate = impersonate
        self._timeout = timeout

    def _connection_string(self) -> str:
        return (
            f"SERVER={self._server};DATABASE={self._database};"
            "Trusted_Connection=yes;TrustServerCertificate=yes;"
        )

    def _impersonate_sql(self) -> str:
        name = self._impersonate.replace("'", "''")
        return (
            f"EXECUTE AS LOGIN = N'{name}';\n"
            f"DECLARE @__mcp_check NVARCHAR(128) = USER_NAME();\n"
            f"IF @__mcp_check <> N'{name}'\n"
            f"BEGIN\n"
            f"    REVERT;\n"
            f"    RAISERROR('MCP impersonation failed: USER_NAME()=[%s]', 16, 1, @__mcp_check);\n"
            f"END\n"
        )

    def execute_query(self, query: str, params: tuple | None = None) -> str:
        query = re.sub(r'(?i)\brevert\b', '/*revert*/', query)
        try:
            conn = mssql_python.connect(self._connection_string())
            conn.timeout = self._timeout
            try:
                cursor = conn.cursor()
                cursor.execute(_SET_PREAMBLE)
                cursor.execute(self._impersonate_sql())
                try:
                    cursor.execute(query, params or ())
                    if cursor.description:
                        rows = cursor.fetchall()
                        columns = [desc[0] for desc in cursor.description]
                        result = {
                            "query": query,
                            "rowCount": len(rows),
                            "columns": columns,
                            "rows": [list(row) for row in rows],
                        }
                    else:
                        result = {
                            "query": query,
                            "rowCount": cursor.rowcount if cursor.rowcount >= 0 else 0,
                        }
                finally:
                    try:
                        cursor.execute("REVERT;")
                    except Exception:
                        pass
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

    def explain_query(self, query: str) -> str:
        try:
            conn = mssql_python.connect(self._connection_string())
            conn.timeout = self._timeout
            try:
                cursor = conn.cursor()
                cursor.execute(_SET_PREAMBLE)
                cursor.execute("SET SHOWPLAN_XML ON;")
                cursor.execute(query)
                row = cursor.fetchone()
                plan_xml = row[0] if row else None
                cursor.execute("SET SHOWPLAN_XML OFF;")
                result = {"query": query, "plan": plan_xml}
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
        result = json.loads(self.execute_query(_LIST_DATABASES_SQL))
        if "error" in result:
            raise RuntimeError(result["error"])
        return [row[0] for row in result["rows"]]

    def _log(self, tool_name: str, **fields) -> None:
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        parts = " ".join(f"{k}={v!r}" for k, v in fields.items())
        line = f"{timestamp} [{tool_name}] {parts}\n"
        try:
            with open(_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line)
        except OSError:
            pass
