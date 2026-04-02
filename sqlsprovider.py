import json
import datetime
from pathlib import Path

import mssql_python
import os
import re

_LOG_PATH = Path(__file__).parent / "debug.log.md"

_SET_PREAMBLE = """
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET LOCK_TIMEOUT 1000;
SET DEADLOCK_PRIORITY LOW;
"""


class SQLSProvider:
    def __init__(self, server: str, database: str, impersonate: str = "mcp-server", timeout: int = 90, dbgmode: bool | None = None):
        self._server = server
        self._database = database
        self._impersonate = impersonate
        self._timeout = timeout
        self._dbgmode = dbgmode if dbgmode is not None else os.environ.get("PYSQLSMCP_DBG", "").lower() in ("1", "true")

    def _connection_string(self) -> str:
        return (
            f"SERVER={self._server};DATABASE={self._database};Trusted_Connection=yes;TrustServerCertificate=yes;"
        )

    def _impersonate_sql(self) -> str:
        name = self._impersonate.replace("'", "''")
        return (
            f"EXECUTE AS LOGIN = N'{name}';\nSELECT SYSTEM_USER AS impersonat_check;"
        )

    def _log(self, query: str, message: str = "", params: tuple | None = None, type: str = "COMPLETE") -> None:
        if self._dbgmode:
            _ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3]
            _type = f"{(type=='ERROR') and '<span style=\"color:darkorange;\">ERROR</span>' or type}"
            _summary = f"{_ts} {_type} <span style=\"font-weight:bold;\">[{self._server}] [{self._database}]</span>"
            _param = (params) and f"\n`{str(params)}`\n" or ""
            _query = f"\n```sql\n{query}\n```\n"
            _details = (message) and f"\n{message}\n{_param}{_query}" or f"{_param}{_query}"

            with open(_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(f"<details>\n<summary>\n{_summary}\n</summary>\n{_details}\n</details>\n\n")

    def execute_query(self, query: str, params: tuple | None = None, explain: bool = False) -> str:
        query = re.sub(r'(?i)\brevert\b', '/*revert*/', query)
        try:
            conn = mssql_python.connect(self._connection_string())
            conn.timeout = self._timeout
            try:
                cursor = conn.cursor()
                cursor.execute(_SET_PREAMBLE)
                if explain:
                    cursor.execute("SET SHOWPLAN_XML ON;")
                    cursor.execute(query)
                    row = cursor.fetchone()
                    plan_xml = row[0] if row else None
                    cursor.execute("SET SHOWPLAN_XML OFF;")
                    result = {"query": query, "plan": plan_xml}
                else:
                    cursor.execute(self._impersonate_sql())
                    rowImp = cursor.fetchone()
                    if rowImp and rowImp[0].lower() == self._impersonate.lower():
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
                conn.close()
                self._log(query, params=params)
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
            self._log(query, message=e, params=params, type="ERROR")
        return json.dumps(result, default=str)
