import pytest
from unittest.mock import patch, MagicMock


class TestServerModule:
    def test_mcp_is_fastmcp_instance(self):
        from mcp.server.fastmcp import FastMCP
        import server
        assert isinstance(server.mcp, FastMCP)

    def test_mcp_name(self):
        import server
        assert server.mcp.name == "pysqlsmcp"

    def test_four_tools_registered(self):
        import server
        tools = server.mcp._tool_manager.list_tools()
        tool_names = {t.name for t in tools}
        assert "selectQuery" in tool_names
        assert "getDatabasePermission" in tool_names
        assert "getAllDatabasePermission" in tool_names
        assert "requiredAdditionalPermission" in tool_names
