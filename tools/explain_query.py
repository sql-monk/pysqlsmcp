from typing import Optional
from db_provider import DbProvider


def register(mcp):
    @mcp.tool()
    def explainQuery(
        server: str,
        database: str,
        query: str,
        impersonate: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        db_provider = DbProvider(server, database, impersonate)
        return db_provider.explain_query(query)
