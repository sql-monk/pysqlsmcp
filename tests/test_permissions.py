"""Tests for getDatabasePermission and getAllDatabasePermission tools.

mcp-server has VIEW DEFINITION + VIEW DATABASE SECURITY STATE →
can query sys.database_permissions, sys.database_role_members, etc.
These tools read permission metadata, not user data.
"""

import json
import pytest
from db_provider import DbProvider
from tools.get_database_permission import _run as run_permission


# ═══════════════════════════════════════════════════════════════
#   getDatabasePermission — mcp_test_main
# ═══════════════════════════════════════════════════════════════

class TestPermissionsMain:
    """Permission metadata queries on mcp_test_main."""

    def test_all_permissions_no_filter(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db))
        assert "error" not in result, f"Unexpected error: {result.get('error')}"
        assert result["rowCount"] > 0
        assert "roleName" in result["columns"]

    def test_filter_by_user_reader(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-reader"))
        assert "error" not in result
        assert result["rowCount"] > 0
        user_col = result["columns"].index("userName")
        users = {row[user_col] for row in result["rows"]}
        assert "mcp-test-reader" in users

    def test_filter_by_user_writer(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-writer"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_user_admin(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-admin"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_object_customers(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, object_filter="Customers"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_object_products(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, object_filter="Products"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_object_nonexistent(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, object_filter="ZZZ_NoSuchObject"))
        assert "error" not in result
        assert result["rowCount"] == 0

    def test_combined_filter_admin_customers(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-admin", object_filter="Customers"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_combined_filter_reader_orders(self, server, main_db, impersonate):
        db = DbProvider(server, main_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-reader", object_filter="Orders"))
        assert "error" not in result
        assert result["rowCount"] > 0


# ═══════════════════════════════════════════════════════════════
#   getDatabasePermission — mcp_test_aux
# ═══════════════════════════════════════════════════════════════

class TestPermissionsAux:
    """Permission metadata queries on mcp_test_aux."""

    def test_all_permissions(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(run_permission(db))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_user_admin(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(run_permission(db, user_filter="mcp-test-admin"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_object_warehouses(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(run_permission(db, object_filter="Warehouses"))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_filter_by_object_shipments(self, server, aux_db, impersonate):
        db = DbProvider(server, aux_db, impersonate)
        result = json.loads(run_permission(db, object_filter="Shipments"))
        assert "error" not in result
        assert result["rowCount"] > 0
 