from pathlib import Path
from typing import Optional
from sqlsprovider import SQLSProvider


def _run(db_provider: SQLSProvider, user_filter: Optional[str] = None, object_filter: Optional[str] = None) -> str:
    params = (user_filter, user_filter, object_filter, object_filter, object_filter)
    _path = Path(__file__).parent / "sql"/ "get_database_permission.sql"
    query = _path.read_text(encoding="utf-8")
    return db_provider.execute_query(query, params)


def register(mcp):
    @mcp.tool()
    def getDatabasePermission(
        server: str,
        database: str,
        impersonate: str,
        user_filter: Optional[str] = None,
        object_filter: Optional[str] = None,
    ) -> str:
        db_provider = SQLSProvider(server, database, impersonate)
        return _run(db_provider, user_filter, object_filter)
