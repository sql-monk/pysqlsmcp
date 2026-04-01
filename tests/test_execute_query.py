"""
Tests for tool: executeQuery
Calls the registered MCP tool function directly (bypassing MCP transport).

Group: execute_query
"""
import json
import pytest
from mcp.server.fastmcp import FastMCP
from tools.execute_query import register


def _tool(server, database, impersonate):
    mcp = FastMCP("test")
    register(mcp)
    fn = mcp._tool_manager._tools["executeQuery"].fn
    return fn, server, database, impersonate


class TestExecuteQueryBasic:
    """EQ-001 … EQ-006: Core query execution."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_simple_select(self):
        """EQ-001: Simple SELECT returns JSON with rows."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT 1 AS v", impersonate=self.imp))
        assert "error" not in r
        assert r["rows"][0][0] == 1

    def test_returns_columns(self):
        """EQ-002: Result contains column metadata."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT 42 AS answer", impersonate=self.imp))
        assert "columns" in r
        assert "answer" in r["columns"]

    def test_bad_sql_returns_error(self):
        """EQ-003: Invalid SQL returns error key in JSON (no exception)."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="BAD SQL XYZ", impersonate=self.imp))
        assert "error" in r

    def test_row_count_matches(self):
        """EQ-004: rowCount matches actual number of rows."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT v FROM (VALUES(1),(2),(3)) t(v)",
                               impersonate=self.imp))
        assert r["rowCount"] == 3
        assert len(r["rows"]) == 3

    def test_revert_in_query_neutralised(self):
        """EQ-005: REVERT keyword inside user query is sanitised."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT 'REVERT rocks' AS msg",
                               impersonate=self.imp))
        assert "error" not in r

    def test_non_select_returns_row_count(self):
        """EQ-006: Non-SELECT DML returns rowCount."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="DECLARE @x INT = 1; SELECT @x AS v",
                               impersonate=self.imp))
        assert "error" not in r
        assert "rowCount" in r


class TestExecuteQueryTestDb:
    """EQ-101 … EQ-110: Queries against mcp_test_main tables/views/procs."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_select_customers(self):
        """EQ-101: SELECT from dbo.Customers returns seeded data."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT CustomerID, FullName FROM dbo.Customers ORDER BY CustomerID",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 3

    def test_select_products(self):
        """EQ-102: SELECT from inventory.Products returns seeded products."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT ProductID, ProductName FROM inventory.Products",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 5

    def test_select_orders_join(self):
        """EQ-103: JOIN across schemas (sales.Orders + dbo.Customers)."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT c.FullName, o.TotalAmount FROM dbo.Customers c JOIN sales.Orders o ON o.CustomerID = c.CustomerID",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_view_customer_orders(self):
        """EQ-104: SELECT from dbo.vw_CustomerOrders."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.vw_CustomerOrders",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_view_order_details(self):
        """EQ-105: SELECT from sales.vw_OrderDetails."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM sales.vw_OrderDetails",
                               impersonate=self.imp))
        assert "error" not in r
        assert "LineTotal" in r["columns"]

    def test_view_low_stock(self):
        """EQ-106: SELECT from inventory.vw_LowStock returns low-stock items."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM inventory.vw_LowStock",
                               impersonate=self.imp))
        assert "error" not in r

    def test_function_order_total(self):
        """EQ-107: Scalar function dbo.fn_OrderTotal returns correct value."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT dbo.fn_OrderTotal(1) AS total",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rows"][0][0] is not None

    def test_function_stock_value(self):
        """EQ-108: Scalar function inventory.fn_StockValue."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT inventory.fn_StockValue(1) AS val",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rows"][0][0] is not None

    def test_proc_search_products(self):
        """EQ-109: EXEC dbo.usp_SearchProducts returns matching products."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="EXEC dbo.usp_SearchProducts @SearchTerm = N'Widget'",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 2

    def test_proc_get_customer_orders(self):
        """EQ-110: EXEC sales.usp_GetCustomerOrders for customer 1."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="EXEC sales.usp_GetCustomerOrders @CustomerID = 1",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1


class TestExecuteQueryCrossDb:
    """EQ-201 … EQ-205: Cross-database queries from mcp_test_main."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_cross_db_view(self):
        """EQ-201: vw_AuxWarehouse reads from mcp_test_aux."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.vw_AuxWarehouse",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 3

    def test_cross_db_procedure(self):
        """EQ-202: usp_ProductWarehouseStock reads from mcp_test_aux."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="EXEC dbo.usp_ProductWarehouseStock @ProductID = 1",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_synonym_warehouses(self):
        """EQ-203: SELECT via synonym dbo.syn_Warehouses."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.syn_Warehouses",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 3

    def test_synonym_warehouse_stock(self):
        """EQ-204: SELECT via synonym dbo.syn_WarehouseStock."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.syn_WarehouseStock",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_synonym_exec_proc(self):
        """EQ-205: EXEC via synonym dbo.syn_AuxGetWarehouse."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="EXEC dbo.syn_AuxGetWarehouse @WarehouseID = 1",
                               impersonate=self.imp))
        assert "error" not in r


class TestExecuteQueryAuxDb:
    """EQ-301 … EQ-306: Queries against mcp_test_aux."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database_aux, impersonate):
        self.fn, self.server, _, self.imp = _tool(server, database_aux, impersonate)
        self.db = database_aux

    def test_select_warehouses(self):
        """EQ-301: SELECT from dbo.Warehouses in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.Warehouses",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 3

    def test_select_warehouse_stock(self):
        """EQ-302: SELECT from dbo.WarehouseStock in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.WarehouseStock",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 7

    def test_view_stock_summary(self):
        """EQ-303: SELECT from dbo.vw_StockSummary in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.vw_StockSummary",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_cross_db_view_aux(self):
        """EQ-304: vw_StockWithProductNames reads from mcp_test_main."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.vw_StockWithProductNames",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ProductName" in r["columns"]

    def test_cross_db_proc_stock_report(self):
        """EQ-305: usp_StockReport reads cross-db from mcp_test_main."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="EXEC dbo.usp_StockReport @WarehouseID = 1",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 1

    def test_synonym_products(self):
        """EQ-306: SELECT via synonym dbo.syn_Products in aux db."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.syn_Products",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["rowCount"] >= 5
