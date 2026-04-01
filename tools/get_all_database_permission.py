import json
from typing import Optional
from db_provider import DbProvider
from tools.get_database_permission import _run as run_permission


def register(mcp):
    @mcp.tool()
    def getAllDatabasePermission(server: str, impersonate: str, user_filter: Optional[str] = None, object_filter: Optional[str] = None) -> str:
        master = DbProvider(server, "master", impersonate)
        databases = master.list_databases()
        all_rows: list = []
        all_columns: list = []
        errors: list = []
        for db in databases:
            result_json = run_permission(DbProvider(server, db, impersonate), user_filter, object_filter)
            result = json.loads(result_json)
            if "error" in result:
                errors.append({"database": db, **result})
            else:
                all_columns = result.get("columns", all_columns)
                all_rows.extend(result.get("rows", []))
        return json.dumps({
            "databasesScanned": databases,
            "rowCount": len(all_rows),
            "columns": all_columns,
            "rows": all_rows,
            "errors": errors,
        })
