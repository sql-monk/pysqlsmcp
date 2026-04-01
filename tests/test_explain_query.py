"""
Tests for tool: explainQuery
Returns XML execution plan without running the query.

Group: explain_query
"""
import json
import pytest
from mcp.server.fastmcp import FastMCP
from tools.explain_query import register


def _tool(server, database, impersonate):
    mcp = FastMCP("test")
    register(mcp)
    fn = mcp._tool_manager._tools["explainQuery"].fn
    return fn, server, database, impersonate


class TestExplainQueryBasic:
    """XQ-001 … XQ-004: Core explain functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_returns_plan(self):
        """XQ-001: Simple SELECT returns an XML plan."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT 1 AS v", impersonate=self.imp))
        assert "error" not in r
        assert r["plan"] is not None
        assert "ShowPlanXML" in r["plan"]

    def test_plan_contains_query_reference(self):
        """XQ-002: Plan XML references the query statement."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT CustomerID FROM dbo.Customers",
                               impersonate=self.imp))
        assert "error" not in r
        assert "Customers" in r["plan"]

    def test_bad_sql_returns_error(self):
        """XQ-003: Invalid SQL returns error key."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="BAD SQL XYZ", impersonate=self.imp))
        assert "error" in r

    def test_plan_for_join(self):
        """XQ-004: JOIN query produces a valid plan."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT c.FullName, o.TotalAmount FROM dbo.Customers c JOIN sales.Orders o ON o.CustomerID = c.CustomerID",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ShowPlanXML" in r["plan"]


class TestExplainQueryTestDb:
    """XQ-101 … XQ-105: Explain plans for test database objects."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.fn, self.server, self.db, self.imp = _tool(server, database, impersonate)

    def test_explain_view(self):
        """XQ-101: Explain plan for view query."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT * FROM dbo.vw_CustomerOrders",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ShowPlanXML" in r["plan"]

    def test_explain_cross_schema(self):
        """XQ-102: Explain plan for cross-schema join."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT oi.*, p.ProductName FROM sales.OrderItems oi JOIN inventory.Products p ON p.ProductID = oi.ProductID",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ShowPlanXML" in r["plan"]

    def test_explain_function_call(self):
        """XQ-103: Explain plan for query calling scalar function."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT dbo.fn_OrderTotal(1) AS total",
                               impersonate=self.imp))
        assert "error" not in r
        assert r["plan"] is not None

    def test_explain_procedure_via_select(self):
        """XQ-104: Explain plan for a SELECT that references multiple schemas."""
        r = json.loads(self.fn(server=self.server, database=self.db,
                               query="SELECT p.ProductName, p.Price, p.StockQty FROM inventory.Products p WHERE p.StockQty < 20",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ShowPlanXML" in r["plan"]

    def test_explain_aux_db(self):
        """XQ-105: Explain plan against aux database."""
        r = json.loads(self.fn(server=self.server, database="mcp_test_aux",
                               query="SELECT * FROM dbo.vw_StockSummary",
                               impersonate=self.imp))
        assert "error" not in r
        assert "ShowPlanXML" in r["plan"]
