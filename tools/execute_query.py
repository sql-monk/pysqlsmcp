from typing import Optional
from sqlsprovider import SQLSProvider


def register(mcp):
    @mcp.tool()
    def executeQuery(
        server: str,
        database: str,
        query: str,
        impersonate: str,
        params: Optional[list] = None,
    ) -> str:
        db_provider = SQLSProvider(server, database, impersonate)
        return db_provider.execute_query(query, tuple(params) if params else None)
