"""
SQL Script MCP Server

MCP server that automatically registers all .sql files from sql_tools/ as MCP tools.
Each .sql file becomes a tool that can be called via MCP.
"""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from sqlscriptprovider import SQLScriptProvider

# Default server and impersonate values (can be overridden via environment variables)
DEFAULT_SERVER = os.environ.get("PYSQLSMCP_SERVER", "localhost")
DEFAULT_IMPERSONATE = os.environ.get("PYSQLSMCP_IMPERSONATE", "mcp-server")

# Path to sql_tools directory
SQL_TOOLS_DIR = Path(__file__).parent / "sql_tools"

# Create MCP instance
mcp = FastMCP("pysqlsmcp-scripts")

# Load and register SQL tools
provider = SQLScriptProvider(SQL_TOOLS_DIR)
provider.register_tools(mcp, DEFAULT_SERVER, DEFAULT_IMPERSONATE)

if __name__ == "__main__":
    mcp.run(transport="stdio")
