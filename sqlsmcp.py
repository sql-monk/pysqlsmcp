"""
pysqlsmcp - Main MCP server

Entry point for the core pysqlsmcp MCP server.
Provides only the executeQuery tool for ad-hoc SQL queries.
"""

from mcp.server.fastmcp import FastMCP
from tools.execute_query import register as register_execute_query

mcp = FastMCP("pysqlsmcp")
register_execute_query(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
