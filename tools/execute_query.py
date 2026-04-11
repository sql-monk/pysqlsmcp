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
        use_login: bool = False,
        max_rows: int = 5000,
    ) -> str:
        db_provider = isqls(server, database, impersonate, use_login=use_login, max_rows=max_rows)
        return db_provider.execute_query(query, tuple(params) if params else None)
