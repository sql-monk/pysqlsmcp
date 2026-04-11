import json
from pathlib import Path
from isqls import isqls

_SQL_DIR = Path(__file__).parent / "sql"
REQUIRED_PERM_QUERY = (_SQL_DIR / "required_additional_permission.sql").read_text(encoding="utf-8")

_MAX_DEPTH = 10


def _run(db_provider: isqls, object: str) -> str:
    params = (object,) * 8
    return db_provider.execute_query(REQUIRED_PERM_QUERY, params)


def _run_recursive(server: str, database: str, object: str, impersonate: str) -> str:
    all_rows: list[list] = []
    visited: set[str] = set()
    columns: list[str] | None = None

    queue: list[tuple[str, str]] = [(database, object)]

    depth = 0
    while queue and depth < _MAX_DEPTH:
        depth += 1
        next_queue: list[tuple[str, str]] = []

        for db, obj in queue:
            key = f"{db}|{obj}".lower()
            if key in visited:
                continue
            visited.add(key)

            provider = isqls(server, db, impersonate, use_login=True)
            result = json.loads(_run(provider, obj))

            if "error" in result:
                continue
            if not result.get("rows"):
                continue

            if columns is None:
                columns = result["columns"]

            for row in result["rows"]:
                row_key = f"{row[1]}|{row[2]}.{row[3]}".lower()
                if row_key not in visited:
                    all_rows.append(row)
                    target_db = row[1]   # DatabaseName
                    target_obj = f"{row[2]}.{row[3]}"  # SchemaName.EntityName
                    next_queue.append((target_db, target_obj))

        queue = next_queue

    return json.dumps({
        "rowCount": len(all_rows),
        "columns": columns or [],
        "rows": all_rows,
    }, default=str)


def register(mcp):
    @mcp.tool()
    def requiredAdditionalPermission(
        server: str,
        database: str,
        object: str,
        impersonate: str,
    ) -> str:
        return _run_recursive(server, database, object,
                              impersonate)
