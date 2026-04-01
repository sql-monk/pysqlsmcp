"""Tests for explainQuery tool under mcp-server impersonation.

mcp-server has VIEW DATABASE STATE → can use SET SHOWPLAN_XML ON
to generate execution plans without actually accessing user data.
"""

import json
import pytest
from db_provider import DbProvider


class TestExplainQueryMain:
    """Execution plans on mcp_test_main via mcp-server."""

    def test_simple_select_plan(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query("SELECT * FROM dbo.Customers"))
        assert "error" not in result, f"Unexpected error: {result.get('error')}"
        assert result.get("plan") is not None
        assert "ShowPlanXML" in result["plan"]

    def test_join_plan(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query(
            "SELECT c.FullName, o.TotalAmount "
            "FROM dbo.Customers c JOIN sales.Orders o ON o.CustomerID = c.CustomerID"
        ))
        assert "error" not in result
        assert "ShowPlanXML" in result["plan"]

    def test_cross_schema_join_plan(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query(
            "SELECT oi.ItemID, p.ProductName "
            "FROM sales.OrderItems oi "
            "JOIN inventory.Products p ON p.ProductID = oi.ProductID"
        ))
        assert "error" not in result
        assert "ShowPlanXML" in result["plan"]

    def test_cross_db_view_plan(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query("SELECT * FROM dbo.vw_AuxWarehouse"))
        assert "error" not in result
        assert result.get("plan") is not None

    def test_subquery_plan(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query(
            "SELECT c.FullName, (SELECT COUNT(*) FROM sales.Orders o WHERE o.CustomerID = c.CustomerID) AS cnt "
            "FROM dbo.Customers c"
        ))
        assert "error" not in result
        assert "ShowPlanXML" in result["plan"]

    def test_invalid_table_returns_error(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query("SELECT * FROM dbo.NonExistentTable"))
        assert "error" in result

    def test_invalid_syntax_returns_error(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(db.explain_query("SELEC * FORM dbo.Customers"))
        assert "error" in result


class TestExplainQueryAux:
    """Execution plans on mcp_test_aux via mcp-server."""

    def test_warehouse_plan(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(db.explain_query("SELECT * FROM dbo.Warehouses"))
        assert "error" not in result
        assert "ShowPlanXML" in result["plan"]

    def test_join_plan(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(db.explain_query(
            "SELECT w.WarehouseName, ws.ProductID, ws.Quantity "
            "FROM dbo.WarehouseStock ws "
            "JOIN dbo.Warehouses w ON w.WarehouseID = ws.WarehouseID"
        ))
        assert "error" not in result
        assert "ShowPlanXML" in result["plan"]

    def test_function_in_query_plan(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(db.explain_query("SELECT dbo.fn_WarehouseTotalQty(1) AS Total"))
        assert "error" not in result
        assert result.get("plan") is not None

    def test_cross_db_view_plan(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(db.explain_query("SELECT * FROM dbo.vw_StockWithProductNames"))
        assert "error" not in result
        assert result.get("plan") is not None
