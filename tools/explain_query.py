from isqls import isqls


def register(mcp):
    @mcp.tool()
    def explainQuery(
        server: str,
        database: str,
        query: str,
        impersonate: str,
        params: list = None,
    ) -> str:
        db_provider = isqls(server, database, impersonate)
        return db_provider.execute_query(query, params=tuple(params) if params else None, explain=True)
