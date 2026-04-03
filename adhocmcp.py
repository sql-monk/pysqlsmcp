from fastmcp import FastMCP

from adhocmcpprovider import AdHocMCPProvider

mcp = FastMCP("pysqlsmcp-adhoc")
mcp.add_provider(AdHocMCPProvider())

if __name__ == "__main__":
    mcp.run(transport="stdio")
