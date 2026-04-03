from typing import Optional, Sequence

from fastmcp.server.providers import Provider
from fastmcp.tools.base import Tool

from sqlsprovider import SQLSProvider


class AdHocMCPProvider(Provider):
    """Dynamic MCP provider that exposes a single executeQuery tool.

    The tool accepts full connection parameters at call time, making it
    suitable for ad-hoc queries against any SQL Server database without
    requiring server-level configuration.
    """

    async def _list_tools(self) -> Sequence[Tool]:
        def executeQuery(
            server: str,
            database: str,
            query: str,
            impersonate: str,
            params: Optional[list] = None,
        ) -> str:
            """Execute a SQL query against a specified SQL Server database.

            Args:
                server: SQL Server instance name or address.
                database: Target database name.
                query: SQL query to execute.
                impersonate: SQL Server login to impersonate via EXECUTE AS LOGIN.
                params: Optional list of positional query parameters (DB-API '?' placeholders).

            Returns:
                JSON string with query results or error details.
            """
            db = SQLSProvider(server, database, impersonate)
            return db.execute_query(query, tuple(params) if params else None)

        return [
            Tool.from_function(
                executeQuery,
                name="executeQuery",
                description=(
                    "Execute an ad-hoc SQL query against a specified SQL Server database "
                    "using impersonated credentials. Returns results as JSON."
                ),
            )
        ]
