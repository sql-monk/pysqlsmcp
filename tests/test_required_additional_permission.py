"""
Tests for tool: requiredAdditionalPermission
Lists cross-schema and cross-database dependencies.

Group: required_additional_permission
"""
import json
import pytest
from mcp.server.fastmcp import FastMCP
from tools.required_additional_permission import register


def _tool(server, impersonate):
    mcp = FastMCP("test")
    register(mcp)
    fn = mcp._tool_manager._tools["requiredAdditionalPermission"].fn
    return fn, server, impersonate


class TestRequiredAdditionalPermission:
    """RA-001 … RA-008: Dependency analysis for procedures, views, functions."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.imp = _tool(server, impersonate)
        self.db = database

    def test_proc_cross_schema(self):
        """RA-001: usp_SearchProducts depends on inventory.Products (cross-schema)."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="dbo.usp_SearchProducts",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1

    def test_proc_with_function_dep(self):
        """RA-002: usp_GetCustomerOrders depends on dbo.fn_OrderTotal."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="sales.usp_GetCustomerOrders",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1

    def test_proc_cross_database(self):
        """RA-003: usp_ProductWarehouseStock depends on mcp_test_aux objects."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="dbo.usp_ProductWarehouseStock",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1
        # Check that at least one dependency references mcp_test_aux
        has_aux = any("mcp_test_aux" in str(row) for row in r["rows"])
        assert has_aux, "Expected cross-db dependency on mcp_test_aux"

    def test_view_cross_schema_deps(self):
        """RA-004: vw_OrderDetails depends on sales.OrderItems + inventory.Products."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="sales.vw_OrderDetails",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1

    def test_view_cross_database(self):
        """RA-005: vw_AuxWarehouse depends on mcp_test_aux.dbo.Warehouses."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="dbo.vw_AuxWarehouse",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1

    def test_nonexistent_object_returns_zero(self):
        """RA-006: Non-existent object returns zero rows."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               object="dbo.nonexistent_proc_xyz",
                               impersonate=self.imp))
        assert r["rowCount"] == 0

    def test_aux_proc_cross_db(self):
        """RA-007: usp_StockReport in aux db depends on mcp_test_main."""
        r = json.loads(self.fn(server=self.server, database="mcp_test_aux",
                               object="dbo.usp_StockReport",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1

    def test_aux_view_cross_db(self):
        """RA-008: vw_StockWithProductNames in aux depends on mcp_test_main."""
        r = json.loads(self.fn(server=self.server, database="mcp_test_aux",
                               object="dbo.vw_StockWithProductNames",
                               impersonate=self.imp))
        assert r["rowCount"] >= 1
