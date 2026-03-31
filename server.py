import argparse
import uvicorn
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8444)
    parser.add_argument("--certfile", required=True)
    parser.add_argument("--keyfile", required=True)
    args = parser.parse_args()
    uvicorn.run(
        mcp.streamable_http_app(),
        host=args.host,
        port=args.port,
        ssl_certfile=args.certfile,
        ssl_keyfile=args.keyfile,
    )
