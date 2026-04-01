from typing import Optional
from db_provider import DbProvider


def register(mcp):
    @mcp.tool()
    def explainQuery(
        server: str,
        database: str,
        query: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        impersonate: str = "",
    ) -> str:
        db_provider = DbProvider(server, database, username, password, impersonate)
        return db_provider.explain_query(query)
