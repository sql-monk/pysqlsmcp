"""Tests for AdHocMCPProvider and adhocmcp server.

Unit tests (no SQL Server required):
  - Provider returns exactly one tool named 'executeQuery'
  - Tool schema matches expected parameters
  - Tool delegates to SQLSProvider.execute_query with correct arguments
  - FastMCP server exposes the tool via the provider

Integration tests (require SQL Server — use PYSQLSMCP_TEST_SERVER env var):
  - Provider tool executes a real query and returns JSON results
"""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure mssql_python is importable in environments without the real driver.
# Integration tests detect the mock and skip automatically.
_MSSQL_MOCKED = "mssql_python" not in sys.modules
if _MSSQL_MOCKED:
    sys.modules["mssql_python"] = MagicMock()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adhocmcpprovider import AdHocMCPProvider

# Skip integration tests when running without a real SQL Server driver.
_requires_sql_server = pytest.mark.skipif(
    _MSSQL_MOCKED,
    reason="mssql_python driver not installed — SQL Server required for integration tests",
)


# ═══════════════════════════════════════════════════════════════
#   Unit tests — no database connection required
# ═══════════════════════════════════════════════════════════════

def _run(coro):
    """Run an async coroutine in a fresh event loop."""
    return asyncio.run(coro)


class TestAdHocMCPProviderUnit:
    """Unit tests for AdHocMCPProvider using mocks."""

    def test_provider_lists_one_tool(self):
        """Provider must expose exactly one tool."""
        provider = AdHocMCPProvider()
        tools = _run(provider.list_tools())
        assert len(tools) == 1

    def test_tool_name_is_executeQuery(self):
        """The single tool must be named 'executeQuery'."""
        provider = AdHocMCPProvider()
        tools = _run(provider.list_tools())
        assert tools[0].name == "executeQuery"

    def test_tool_has_required_params(self):
        """Tool schema must require server, database, query, impersonate."""
        provider = AdHocMCPProvider()
        tools = _run(provider.list_tools())
        schema = tools[0].parameters
        required = set(schema.get("required", []))
        assert "server" in required
        assert "database" in required
        assert "query" in required
        assert "impersonate" in required

    def test_tool_has_optional_params(self):
        """Tool schema must have optional 'params' field."""
        provider = AdHocMCPProvider()
        tools = _run(provider.list_tools())
        schema = tools[0].parameters
        assert "params" in schema.get("properties", {})
        assert "params" not in schema.get("required", [])

    def test_tool_delegates_to_sqlsprovider(self):
        """executeQuery tool must delegate to SQLSProvider.execute_query."""
        fake_result = json.dumps({"query": "SELECT 1", "rowCount": 1, "columns": ["x"], "rows": [[1]]})

        with patch("adhocmcpprovider.SQLSProvider") as MockProvider:
            mock_instance = MagicMock()
            mock_instance.execute_query.return_value = fake_result
            MockProvider.return_value = mock_instance

            provider = AdHocMCPProvider()
            tools = _run(provider._list_tools())
            tool = tools[0]

            result = _run(
                tool.run({"server": "srv", "database": "db", "query": "SELECT 1", "impersonate": "mcp-server"})
            )

            MockProvider.assert_called_once_with("srv", "db", "mcp-server")
            mock_instance.execute_query.assert_called_once_with("SELECT 1", None)
            assert fake_result in str(result)

    def test_tool_passes_params_as_tuple(self):
        """Params list must be converted to tuple before passing to execute_query."""
        fake_result = json.dumps({"query": "SELECT ?", "rowCount": 1, "columns": ["x"], "rows": [["a"]]})

        with patch("adhocmcpprovider.SQLSProvider") as MockProvider:
            mock_instance = MagicMock()
            mock_instance.execute_query.return_value = fake_result
            MockProvider.return_value = mock_instance

            provider = AdHocMCPProvider()
            tools = _run(provider._list_tools())
            tool = tools[0]

            _run(tool.run({"server": "srv", "database": "db", "query": "SELECT ?",
                           "impersonate": "mcp-server", "params": ["a"]}))

            mock_instance.execute_query.assert_called_once_with("SELECT ?", ("a",))

    def test_tool_none_params_passes_none(self):
        """When params is None (omitted), execute_query receives None."""
        fake_result = json.dumps({"query": "SELECT 42", "rowCount": 1, "columns": ["v"], "rows": [[42]]})

        with patch("adhocmcpprovider.SQLSProvider") as MockProvider:
            mock_instance = MagicMock()
            mock_instance.execute_query.return_value = fake_result
            MockProvider.return_value = mock_instance

            provider = AdHocMCPProvider()
            tools = _run(provider._list_tools())
            tool = tools[0]

            _run(tool.run({"server": "srv", "database": "db", "query": "SELECT 42",
                           "impersonate": "mcp-server"}))

            mock_instance.execute_query.assert_called_once_with("SELECT 42", None)


class TestAdHocMCPServerUnit:
    """Unit tests for the adhocmcp FastMCP server."""

    def test_server_exposes_executeQuery_tool(self):
        """The adhocmcp FastMCP server must expose the executeQuery tool."""
        from fastmcp import FastMCP
        from adhocmcpprovider import AdHocMCPProvider

        mcp = FastMCP("pysqlsmcp-adhoc-test")
        mcp.add_provider(AdHocMCPProvider())

        tools = _run(mcp.list_tools())
        tool_names = [t.name for t in tools]
        assert "executeQuery" in tool_names

    def test_server_tool_call_delegates_to_provider(self):
        """Calling executeQuery on the server must route through the provider."""
        fake_result = json.dumps({"query": "SELECT 1", "rowCount": 0})

        with patch("adhocmcpprovider.SQLSProvider") as MockProvider:
            mock_instance = MagicMock()
            mock_instance.execute_query.return_value = fake_result
            MockProvider.return_value = mock_instance

            from fastmcp import FastMCP
            from adhocmcpprovider import AdHocMCPProvider

            mcp = FastMCP("pysqlsmcp-adhoc-test2")
            mcp.add_provider(AdHocMCPProvider())

            result = _run(mcp.call_tool("executeQuery", {
                "server": "localhost",
                "database": "mydb",
                "query": "SELECT 1",
                "impersonate": "mcp-server",
            }))

            MockProvider.assert_called_once_with("localhost", "mydb", "mcp-server")
            mock_instance.execute_query.assert_called_once_with("SELECT 1", None)
            assert fake_result in str(result)


# ═══════════════════════════════════════════════════════════════
#   Integration tests — require SQL Server
# ═══════════════════════════════════════════════════════════════

def _tool_text(result) -> str:
    """Extract the text content from a ToolResult."""
    return result.content[0].text


@_requires_sql_server
class TestAdHocMCPProviderIntegration:
    """Integration tests for AdHocMCPProvider against a live SQL Server."""

    def test_execute_query_select_one(self, server, main_db, impersonate):
        """Provider tool executes SELECT 1 and returns a valid result."""
        provider = AdHocMCPProvider()
        tools = _run(provider._list_tools())
        tool = tools[0]

        raw = _run(tool.run({"server": server, "database": main_db,
                             "query": "SELECT 1 AS val", "impersonate": impersonate}))

        result = json.loads(_tool_text(raw))
        assert "error" not in result
        assert result["rows"][0][0] == 1

    def test_execute_query_with_params(self, server, main_db, impersonate):
        """Provider tool forwards params correctly to SQLSProvider."""
        provider = AdHocMCPProvider()
        tools = _run(provider._list_tools())
        tool = tools[0]

        raw = _run(tool.run({
            "server": server,
            "database": main_db,
            "query": "SELECT name FROM sys.tables WHERE name = ?",
            "impersonate": impersonate,
            "params": ["Customers"],
        }))

        result = json.loads(_tool_text(raw))
        assert "error" not in result
        assert result["rowCount"] == 1
        assert result["rows"][0][0] == "Customers"

    def test_execute_query_sys_tables(self, server, main_db, impersonate):
        """Provider tool can query sys.tables metadata."""
        provider = AdHocMCPProvider()
        tools = _run(provider._list_tools())
        tool = tools[0]

        raw = _run(tool.run({
            "server": server,
            "database": main_db,
            "query": "SELECT name FROM sys.tables ORDER BY name",
            "impersonate": impersonate,
        }))

        result = json.loads(_tool_text(raw))
        assert "error" not in result
        table_names = [row[0] for row in result["rows"]]
        assert "Customers" in table_names
