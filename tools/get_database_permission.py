from pathlib import Path
from typing import Optional
from db_provider import DbProvider

_SQL_DIR = Path(__file__).parent / "sql"
PERMISSION_QUERY = (_SQL_DIR / "get_database_permission.sql").read_text(encoding="utf-8")


def _run(db_provider: DbProvider, user_filter: Optional[str] = None, object_filter: Optional[str] = None) -> str:
    params = (user_filter, user_filter, object_filter, object_filter, object_filter)
    return db_provider.execute_query(PERMISSION_QUERY, params)


def register(mcp):
    @mcp.tool()
    def getDatabasePermission(
        server: str,
        database: str,
        impersonate: str,
        user_filter: Optional[str] = None,
        object_filter: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        db_provider = DbProvider(server, database, impersonate)
        return _run(db_provider, user_filter, object_filter)
