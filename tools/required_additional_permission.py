from pathlib import Path
from typing import Optional
from db_provider import DbProvider

_SQL_DIR = Path(__file__).parent / "sql"
REQUIRED_PERM_QUERY = (_SQL_DIR / "required_additional_permission.sql").read_text(encoding="utf-8")


def _run(db_provider: DbProvider, object: str) -> str:
    params = (object,) * 8
    return db_provider.execute_query(REQUIRED_PERM_QUERY, params)


def register(mcp):
    @mcp.tool()
    def requiredAdditionalPermission(
        server: str,
        database: str,
        object: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        mcplevel: int = 0,
    ) -> str:
        db_provider = DbProvider(server, database, username, password, mcplevel)
        return _run(db_provider, object)
