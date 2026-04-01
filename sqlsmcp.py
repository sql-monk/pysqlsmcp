from mcp.server.fastmcp import FastMCP
from tools.execute_query import register as reg1
from tools.explain_query import register as reg2
from tools.get_database_permission import register as reg3
from tools.get_all_database_permission import register as reg4
from tools.required_additional_permission import register as reg5

mcp = FastMCP("pysqlsmcp")
reg1(mcp)
reg2(mcp)
reg3(mcp)
reg4(mcp)
reg5(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
