from typing import Optional
from isqls import isqls


def register(mcp):
    @mcp.tool()
    def executeQuery(
        server: str,
        database: str,
        query: str,
        impersonate: str,
        params: Optional[list] = None,
    ) -> str:
        db_provider = isqls(server, database, impersonate)
        return db_provider.execute_query(query, tuple(params) if params else None)
