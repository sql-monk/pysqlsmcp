"""
Tests for tool: getDatabasePermission
Lists role memberships and permissions for a database.

Group: get_database_permission
"""
import json
import pytest
from mcp.server.fastmcp import FastMCP
from tools.get_database_permission import register


def _tool(server, database, impersonate):
    mcp = FastMCP("test")
    register(mcp)
    fn = mcp._tool_manager._tools["getDatabasePermission"].fn
    return fn, server, database, impersonate


class TestGetDatabasePermission:
    """DP-001 … DP-008: Permission listing for mcp_test_main."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_no_filter(self):
        """DP-001: Returns permissions without filters."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1
        assert "columns" in r

    def test_user_filter_reader(self):
        """DP-002: Filter by user mcp-test-reader returns its permissions."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="mcp-test-reader"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_user_filter_writer(self):
        """DP-003: Filter by user mcp-test-writer."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="mcp-test-writer"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_user_filter_admin(self):
        """DP-004: Filter by user mcp-test-admin."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="mcp-test-admin"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_object_filter_customers(self):
        """DP-005: Filter by object 'Customers'."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               object_filter="Customers"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_object_filter_products(self):
        """DP-006: Filter by object 'Products'."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               object_filter="Products"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_both_filters(self):
        """DP-007: Filter by user and object simultaneously."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="mcp-test-admin",
                               object_filter="Customers"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_nonexistent_user_returns_empty(self):
        """DP-008: Non-existent user filter returns zero rows (no error)."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="nonexistent_user_xyz"))
        assert "error" not in r
        assert r["rowCount"] == 0


class TestGetDatabasePermissionAux:
    """DP-101 … DP-103: Permission listing for mcp_test_aux."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database_aux, impersonate):
        self.fn, self.server, _, self.imp = _tool(server, database_aux, impersonate)
        self.db = database_aux

    def test_aux_no_filter(self):
        """DP-101: Returns permissions for aux db without filters."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_aux_user_filter(self):
        """DP-102: Filter by mcp-test-reader in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               user_filter="mcp-test-reader"))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_aux_object_filter(self):
        """DP-103: Filter by object 'Warehouses' in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               impersonate=self.imp,
                               object_filter="Warehouses"))
        assert "error" not in r
        assert r["rowCount"] >= 1
