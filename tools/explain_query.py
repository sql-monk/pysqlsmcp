from db_provider import DbProvider


def register(mcp):
    @mcp.tool()
    def explainQuery(
        server: str,
        database: str,
        query: str,
        impersonate: str,
        params: Optional[list] = None,
    ) -> str:
        db_provider = DbProvider(server, database, impersonate)
        return db_provider.execute_query(query, params=params, explain=True)
