"""Tests for requiredAdditionalPermission tool under mcp-server.

This tool reads sys.sql_expression_dependencies and sys.synonyms —
both accessible via VIEW DEFINITION. No user data access required.
"""

import json
import pytest
from isqls import isqls
from tools.required_additional_permission import _run as run_single, _run_recursive


# ═══════════════════════════════════════════════════════════════
#   Cross-database dependencies — mcp_test_main
# ═══════════════════════════════════════════════════════════════

class TestCrossDepsMain:
    """Cross-db dependency detection on mcp_test_main."""

    def test_view_aux_warehouse_refs_aux(self, server, main_db, impersonate):
        """vw_AuxWarehouse references mcp_test_aux.dbo.Warehouses."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "dbo.vw_AuxWarehouse"))
        assert "error" not in result, f"Unexpected error: {result.get('error')}"
        assert result["rowCount"] >= 1
        found_aux = any("mcp_test_aux" in str(row) for row in result["rows"])
        assert found_aux, "Should detect cross-db dependency on mcp_test_aux"

    def test_proc_product_warehouse_stock_refs_aux(self, server, main_db, impersonate):
        """usp_ProductWarehouseStock references mcp_test_aux tables."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "dbo.usp_ProductWarehouseStock"))
        assert "error" not in result
        assert result["rowCount"] >= 1
        found_aux = any("mcp_test_aux" in str(row) for row in result["rows"])
        assert found_aux

    def test_synonym_warehouses(self, server, main_db, impersonate):
        """syn_Warehouses -> mcp_test_aux.dbo.Warehouses."""
        result = json.loads(_run_recursive(server, main_db, "dbo.syn_Warehouses", impersonate))
        assert "error" not in result

    def test_local_view_no_cross_deps(self, server, main_db, impersonate):
        """vw_CustomerOrders is local-only — 0 cross-db deps."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "dbo.vw_CustomerOrders"))
        assert "error" not in result
        assert result["rowCount"] == 0

    def test_local_proc_search_products_no_deps(self, server, main_db, impersonate):
        """usp_SearchProducts uses only local tables."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "dbo.usp_SearchProducts"))
        assert "error" not in result
        assert result["rowCount"] == 0

    def test_cross_schema_proc(self, server, main_db, impersonate):
        """sales.usp_GetCustomerOrders crosses schema boundary (sales -> dbo)."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "sales.usp_GetCustomerOrders"))
        # May or may not detect cross-schema depending on schema ownership
        assert "error" not in result

    def test_nonexistent_object(self, server, main_db, impersonate):
        """Non-existent object — should return 0 rows, not error."""
        db = isqls(server, main_db, impersonate)
        result = json.loads(run_single(db, "dbo.zzz_no_such_object"))
        assert "error" not in result
        assert result["rowCount"] == 0


# ═══════════════════════════════════════════════════════════════
#   Cross-database dependencies — mcp_test_aux
# ═══════════════════════════════════════════════════════════════

class TestCrossDepsAux:
    """Cross-db dependency detection on mcp_test_aux."""

    def test_view_stock_with_products_refs_main(self, server, aux_db, impersonate):
        """vw_StockWithProductNames references mcp_test_main.inventory.Products."""
        db = isqls(server, aux_db, impersonate)
        result = json.loads(run_single(db, "dbo.vw_StockWithProductNames"))
        assert "error" not in result
        assert result["rowCount"] >= 1
        found_main = any("mcp_test_main" in str(row) for row in result["rows"])
        assert found_main, "Should detect cross-db dependency on mcp_test_main"

    def test_proc_stock_report_refs_main(self, server, aux_db, impersonate):
        """usp_StockReport references mcp_test_main.inventory.Products."""
        db = isqls(server, aux_db, impersonate)
        result = json.loads(run_single(db, "dbo.usp_StockReport"))
        assert "error" not in result
        assert result["rowCount"] >= 1

    def test_synonym_products(self, server, aux_db, impersonate):
        """syn_Products -> mcp_test_main.inventory.Products."""
        result = json.loads(_run_recursive(server, aux_db, "dbo.syn_Products", impersonate))
        assert "error" not in result

    def test_local_proc_get_warehouse_info_no_deps(self, server, aux_db, impersonate):
        """usp_GetWarehouseInfo is local-only."""
        db = isqls(server, aux_db, impersonate)
        result = json.loads(run_single(db, "dbo.usp_GetWarehouseInfo"))
        assert "error" not in result
        assert result["rowCount"] == 0

    def test_local_view_stock_summary_no_deps(self, server, aux_db, impersonate):
        """vw_StockSummary is local-only."""
        db = isqls(server, aux_db, impersonate)
        result = json.loads(run_single(db, "dbo.vw_StockSummary"))
        assert "error" not in result
        assert result["rowCount"] == 0


# ═══════════════════════════════════════════════════════════════
#   Recursive dependency resolution
# ═══════════════════════════════════════════════════════════════

class TestRecursiveDependencies:
    """Recursive cross-db dependency traversal."""

    def test_recursive_from_product_warehouse_stock(self, server, main_db, impersonate):
        """usp_ProductWarehouseStock -> mcp_test_aux tables (recursive)."""
        result = json.loads(_run_recursive(server, main_db, "dbo.usp_ProductWarehouseStock", impersonate))
        assert "error" not in result
        assert result["rowCount"] >= 1

    def test_recursive_from_stock_report(self, server, aux_db, impersonate):
        """usp_StockReport -> mcp_test_main.inventory.Products (recursive)."""
        result = json.loads(_run_recursive(server, aux_db, "dbo.usp_StockReport", impersonate))
        assert "error" not in result
        assert result["rowCount"] >= 1

    def test_recursive_local_proc_zero_deps(self, server, main_db, impersonate):
        """Local-only proc — recursive should return 0."""
        result = json.loads(_run_recursive(server, main_db, "dbo.usp_SearchProducts", impersonate))
        assert "error" not in result
        assert result["rowCount"] == 0

    def test_recursive_nonexistent_object(self, server, main_db, impersonate):
        """Non-existent object — recursive returns 0."""
        result = json.loads(_run_recursive(server, main_db, "dbo.zzz_no_such_object", impersonate))
        assert "error" not in result
        assert result["rowCount"] == 0
