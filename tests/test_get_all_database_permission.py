"""
Tests for tool: getAllDatabasePermission
Scans all accessible databases and aggregates permissions.

Group: get_all_database_permission
"""
import json
import pytest
from mcp.server.fastmcp import FastMCP
from tools.get_all_database_permission import register


def _tool(server, impersonate):
    mcp = FastMCP("test")
    register(mcp)
    fn = mcp._tool_manager._tools["getAllDatabasePermission"].fn
    return fn, server, impersonate


class TestGetAllDatabasePermission:
    """AP-001 … AP-006: Aggregated permission listing across databases."""

    @pytest.fixture(autouse=True)
    def setup(self, server, impersonate):
        self.fn, self.server, self.imp = _tool(server, impersonate)

    def test_no_filter(self):
        """AP-001: Returns aggregated permissions without filters."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp))
        assert "databasesScanned" in r
        assert r["rowCount"] >= 1
        assert "columns" in r

    def test_scans_test_databases(self):
        """AP-002: Scanned databases include mcp_test_main and mcp_test_aux."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp))
        scanned = r["databasesScanned"]
        assert "mcp_test_main" in scanned
        assert "mcp_test_aux" in scanned

    def test_user_filter_reader(self):
        """AP-003: Filter by mcp-test-reader across all databases."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp,
                               user_filter="mcp-test-reader"))
        assert r["rowCount"] >= 1

    def test_user_filter_admin(self):
        """AP-004: Filter by mcp-test-admin across all databases."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp,
                               user_filter="mcp-test-admin"))
        assert r["rowCount"] >= 1

    def test_object_filter(self):
        """AP-005: Filter by object 'Customers' across all databases."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp,
                               object_filter="Customers"))
        assert r["rowCount"] >= 1

    def test_nonexistent_user_returns_zero_rows(self):
        """AP-006: Non-existent user filter returns zero aggregated rows."""
        r = json.loads(self.fn(server=self.server, impersonate=self.imp,
                               user_filter="nonexistent_user_xyz"))
        assert r["rowCount"] == 0
