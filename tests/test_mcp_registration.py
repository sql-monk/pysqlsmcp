"""
Tests for MCP tool registration — verifies all tools are properly
registered on the FastMCP instance.

Group: mcp_registration
"""
import pytest
from mcp.server.fastmcp import FastMCP
from tools.execute_query import register as reg1
from tools.explain_query import register as reg2
from tools.get_database_permission import register as reg3
from tools.get_all_database_permission import register as reg4
from tools.required_additional_permission import register as reg5


EXPECTED_TOOLS = [
    "executeQuery",
    "explainQuery",
    "getDatabasePermission",
    "getAllDatabasePermission",
    "requiredAdditionalPermission",
]


class TestMcpRegistration:
    """MR-001 … MR-003: Tool registration checks."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mcp = FastMCP("test")
        reg1(self.mcp)
        reg2(self.mcp)
        reg3(self.mcp)
        reg4(self.mcp)
        reg5(self.mcp)

    def test_all_tools_registered(self):
        """MR-001: All five tools are registered on the MCP instance."""
        registered = list(self.mcp._tool_manager._tools.keys())
        for name in EXPECTED_TOOLS:
            assert name in registered, f"Tool '{name}' not registered"

    def test_tool_count(self):
        """MR-002: Exactly 5 tools are registered."""
        assert len(self.mcp._tool_manager._tools) == 5

    def test_tools_are_callable(self):
        """MR-003: Each registered tool has a callable function."""
        for name in EXPECTED_TOOLS:
            tool = self.mcp._tool_manager._tools[name]
            assert callable(tool.fn), f"Tool '{name}' fn is not callable"
