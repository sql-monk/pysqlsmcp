import json
import datetime
import unicodedata
from pathlib import Path

import mssql_python
import os
import re

_LOG_PATH = Path(__file__).parent / "debug.log.md"
_LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB

_IMPERSONATE_RE = re.compile(r'^mcp-[\w-]+$')

_SET_PREAMBLE = """
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET LOCK_TIMEOUT 1000;
SET DEADLOCK_PRIORITY LOW;
"""

# impersonated sqlserver
class isqls:
    def __init__(self, server: str, database: str, impersonate: str = "mcp-server",
                 timeout: int = 90, dbgmode: bool | None = None,
                 use_login: bool = False, max_rows: int = 5000):
        if not _IMPERSONATE_RE.match(impersonate):
            raise ValueError(f"Invalid impersonate name: {impersonate!r}. Must match 'mcp-<name>' pattern.")
        self._server = server
        self._database = database
        self._impersonate = impersonate
        self._timeout = timeout
        self._dbgmode = dbgmode if dbgmode is not None else os.environ.get("PYSQLSMCP_DBG", "").lower() in ("1", "true")
        self._use_login = use_login
        self._max_rows = max_rows

    def _connection_string(self) -> str:
        return (
            f"SERVER={self._server};DATABASE={self._database};Trusted_Connection=yes;TrustServerCertificate=yes;"
        )

    def _impersonate_sql(self) -> str:
        name = self._impersonate.replace("'", "''")
        if self._use_login:
            return f"EXECUTE AS LOGIN = N'{name}';\nSELECT SYSTEM_USER AS impersonat_check;"
        return f"EXECUTE AS USER = N'{name}';\nSELECT USER_NAME() AS impersonat_check;"

    def _log(self, query: str, message: str = "", params: tuple | None = None, type: str = "COMPLETE") -> None:
        if not self._dbgmode:
            return
        try:
            if _LOG_PATH.exists() and _LOG_PATH.stat().st_size > _LOG_MAX_BYTES:
                bak = _LOG_PATH.with_suffix(".bak.md")
                if bak.exists():
                    bak.unlink()
                _LOG_PATH.rename(bak)
        except OSError:
            pass
        _ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3]
        _type = f"{(type=='ERROR') and '<span style=\"color:darkorange;\">ERROR</span>' or type}"
        _summary = f"{_ts} {_type} <span style=\"font-weight:bold;\">[{self._server}] [{self._database}]</span>"
        _param = (params) and f"\n`{str(params)}`\n" or ""
        _query = f"\n```sql\n{query}\n```\n"
        _details = (message) and f"\n{message}\n{_param}{_query}" or f"{_param}{_query}"

        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"<details>\n<summary>\n{_summary}\n</summary>\n{_details}\n</details>\n\n")

    @staticmethod
    def _validate_query(query: str) -> str | None:
        normalized = unicodedata.normalize("NFKC", query)
        if re.search(r'(?i)\brevert\b', normalized):
            return "Query rejected: REVERT keyword is not allowed."
        if re.search(r'(?i)char\s*\(\s*82\s*\).*char\s*\(\s*69\s*\).*char\s*\(\s*86\s*\).*char\s*\(\s*69\s*\).*char\s*\(\s*82\s*\).*char\s*\(\s*84\s*\)', normalized):
            return "Query rejected: detected CHAR()-based REVERT construction."
        return None

    def execute_query(self, query: str, params: tuple | None = None) -> str:
        rejection = self._validate_query(query)
        if rejection:
            return json.dumps({"error": rejection, "query": query})
        try:
            conn = mssql_python.connect(self._connection_string())
            conn.timeout = self._timeout
            try:
                cursor = conn.cursor()
                cursor.execute(_SET_PREAMBLE)
                cursor.execute(self._impersonate_sql())
                rowImp = cursor.fetchone()
                if rowImp and rowImp[0].lower() == self._impersonate.lower():
                    cursor.execute(query, params or ())
                    if cursor.description:
                        rows = cursor.fetchmany(self._max_rows + 1)
                        truncated = len(rows) > self._max_rows
                        if truncated:
                            rows = rows[:self._max_rows]
                        columns = [desc[0] for desc in cursor.description]
                        result = {
                            "query": query,
                            "rowCount": len(rows),
                            "columns": columns,
                            "rows": [list(row) for row in rows],
                        }
                        if truncated:
                            result["truncated"] = True
                            result["maxRows"] = self._max_rows
                    else:
                        result = {
                            "query": query,
                            "rowCount": cursor.rowcount if cursor.rowcount >= 0 else 0,
                        }
                self._log(query, params=params)
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
            self._log(query, message=e, params=params, type="ERROR")
        return json.dumps(result, default=str)
