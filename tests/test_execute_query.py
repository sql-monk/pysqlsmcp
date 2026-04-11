"""Tests for executeQuery tool under mcp-server impersonation.

mcp-server has:
  ✓ VIEW DEFINITION — sys.tables, sys.columns, sys.procedures, OBJECT_DEFINITION
  ✓ VIEW DATABASE STATE — dm_exec_*, dm_os_*, session/connection info
  ✓ VIEW DATABASE PERFORMANCE STATE — query stats, index usage
  ✓ VIEW DATABASE SECURITY STATE — permission metadata
  ✗ User data — db_denydatareader + db_denydatawriter
"""

import json
import pytest
from isqls import isqls


# ═══════════════════════════════════════════════════════════════
#   VIEW DEFINITION — schema metadata
# ═══════════════════════════════════════════════════════════════

class TestViewDefinitionMain:
    """VIEW DEFINITION access on mcp_test_main."""

    def test_impersonation_succeeds(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("SELECT USER_NAME() AS CurrentUser"))
        assert "error" not in result, f"Impersonation failed: {result.get('error')}"

    def test_sys_tables(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT s.name AS [schema], t.name AS [table] "
            "FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id "
            "ORDER BY s.name, t.name"
        ))
        assert "error" not in result
        names = [(row[0], row[1]) for row in result["rows"]]
        assert ("dbo", "Customers") in names
        assert ("sales", "Orders") in names
        assert ("inventory", "Products") in names

    def test_sys_columns(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT c.name, TYPE_NAME(c.user_type_id) AS type_name "
            "FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id "
            "WHERE t.name = 'Customers'"
        ))
        assert "error" not in result
        col_names = [row[0] for row in result["rows"]]
        assert "CustomerID" in col_names
        assert "FullName" in col_names
        assert "Email" in col_names

    def test_sys_procedures(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT SCHEMA_NAME(schema_id) AS [schema], name "
            "FROM sys.procedures ORDER BY name"
        ))
        assert "error" not in result
        proc_names = [row[1] for row in result["rows"]]
        assert "usp_SearchProducts" in proc_names
        assert "usp_GetCustomerOrders" in proc_names

    def test_sys_views(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.views ORDER BY name"
        ))
        assert "error" not in result
        view_names = [row[0] for row in result["rows"]]
        assert "vw_CustomerOrders" in view_names
        assert "vw_AuxWarehouse" in view_names

    def test_sys_schemas(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.schemas WHERE name IN ('dbo', 'sales', 'inventory') ORDER BY name"
        ))
        assert "error" not in result
        schemas = [row[0] for row in result["rows"]]
        assert "dbo" in schemas
        assert "sales" in schemas
        assert "inventory" in schemas

    def test_object_definition_procedure(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.usp_SearchProducts')) AS def_text"
        ))
        assert "error" not in result
        assert result["rows"][0][0] is not None
        assert "SearchTerm" in result["rows"][0][0]

    def test_object_definition_view(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_CustomerOrders')) AS def_text"
        ))
        assert "error" not in result
        assert result["rows"][0][0] is not None

    def test_sys_foreign_keys(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_NAME(parent_object_id) AS child_table, "
            "OBJECT_NAME(referenced_object_id) AS parent_table "
            "FROM sys.foreign_keys"
        ))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_sys_indexes(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_NAME(object_id) AS [table], name, type_desc "
            "FROM sys.indexes WHERE name IS NOT NULL AND OBJECT_NAME(object_id) = 'Customers'"
        ))
        assert "error" not in result
        assert result["rowCount"] >= 1

    def test_sys_synonyms(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name, base_object_name FROM sys.synonyms ORDER BY name"
        ))
        assert "error" not in result
        syn_names = [row[0] for row in result["rows"]]
        assert "syn_Warehouses" in syn_names

    def test_sys_sql_expression_dependencies(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_NAME(referencing_id) AS referencing, "
            "referenced_database_name, referenced_schema_name, referenced_entity_name "
            "FROM sys.sql_expression_dependencies "
            "WHERE referenced_database_name IS NOT NULL"
        ))
        assert "error" not in result
        assert result["rowCount"] > 0


class TestViewDefinitionAux:
    """VIEW DEFINITION access on mcp_test_aux."""

    def test_sys_tables(self, server, aux_db, impersonate):
        db = isqls(server, aux_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.tables ORDER BY name"
        ))
        assert "error" not in result
        names = [row[0] for row in result["rows"]]
        assert "Warehouses" in names
        assert "WarehouseStock" in names
        assert "Shipments" in names

    def test_sys_procedures(self, server, aux_db, impersonate):
        db = isqls(server, aux_db, impersonate)
        result = json.loads(db.execute_query("SELECT name FROM sys.procedures"))
        assert "error" not in result
        procs = [row[0] for row in result["rows"]]
        assert "usp_GetWarehouseInfo" in procs
        assert "usp_StockReport" in procs

    def test_object_definition_function(self, server, aux_db, impersonate):
        db = isqls(server, aux_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.fn_WarehouseTotalQty')) AS def_text"
        ))
        assert "error" not in result
        assert result["rows"][0][0] is not None

    def test_sys_synonyms(self, server, aux_db, impersonate):
        db = isqls(server, aux_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name, base_object_name FROM sys.synonyms ORDER BY name"
        ))
        assert "error" not in result
        syn_names = [row[0] for row in result["rows"]]
        assert "syn_Products" in syn_names
        assert "syn_Customers" in syn_names


# ═══════════════════════════════════════════════════════════════
#   VIEW DATABASE STATE — DMVs, sessions, diagnostics
# ═══════════════════════════════════════════════════════════════

class TestViewDatabaseState:
    """VIEW DATABASE STATE — DMVs, diagnostics."""

    def test_dm_exec_sessions(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 session_id, login_name, status FROM sys.dm_exec_sessions"
        ))
        assert "error" not in result
        assert result["rowCount"] >= 1

    def test_dm_exec_requests(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 session_id, status, command FROM sys.dm_exec_requests"
        ))
        assert "error" not in result

    def test_dm_exec_connections(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 session_id, connect_time, net_transport FROM sys.dm_exec_connections"
        ))
        assert "error" not in result

    def test_dm_db_index_usage_stats(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 OBJECT_NAME(object_id) AS [table], "
            "user_seeks, user_scans, user_lookups "
            "FROM sys.dm_db_index_usage_stats WHERE database_id = DB_ID()"
        ))
        assert "error" not in result


# ═══════════════════════════════════════════════════════════════
#   VIEW DATABASE PERFORMANCE STATE
# ═══════════════════════════════════════════════════════════════

class TestViewDatabasePerformanceState:
    """VIEW DATABASE PERFORMANCE STATE — query stats, wait stats."""

    def test_dm_exec_query_stats(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 execution_count, total_worker_time, total_logical_reads "
            "FROM sys.dm_exec_query_stats ORDER BY total_worker_time DESC"
        ))
        assert "error" not in result

    def test_dm_os_wait_stats(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT TOP 5 wait_type, waiting_tasks_count, wait_time_ms "
            "FROM sys.dm_os_wait_stats ORDER BY wait_time_ms DESC"
        ))
        assert "error" not in result
        assert result["rowCount"] >= 1


# ═══════════════════════════════════════════════════════════════
#   VIEW DATABASE SECURITY STATE — permissions, principals
# ═══════════════════════════════════════════════════════════════

class TestViewDatabaseSecurityState:
    """VIEW DATABASE SECURITY STATE — permission metadata, principals."""

    def test_database_permissions(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT dp.name, dp.type_desc, p.permission_name, p.state_desc "
            "FROM sys.database_principals dp "
            "JOIN sys.database_permissions p ON p.grantee_principal_id = dp.principal_id "
            "WHERE dp.name LIKE 'mcp-test-%'"
        ))
        assert "error" not in result
        assert result["rowCount"] > 0

    def test_database_role_members(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT USER_NAME(role_principal_id) AS role_name, "
            "USER_NAME(member_principal_id) AS member_name "
            "FROM sys.database_role_members "
            "WHERE USER_NAME(member_principal_id) LIKE 'mcp-test-%'"
        ))
        assert "error" not in result
        assert result["rowCount"] >= 3

    def test_database_principals(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name, type_desc FROM sys.database_principals "
            "WHERE name LIKE 'role_%' ORDER BY name"
        ))
        assert "error" not in result
        role_names = [row[0] for row in result["rows"]]
        assert "role_reader" in role_names
        assert "role_writer" in role_names
        assert "role_admin" in role_names



# ═══════════════════════════════════════════════════════════════
#   Security: REVERT keyword neutralisation
# ═══════════════════════════════════════════════════════════════

class TestSecurityRevert:
    """REVERT keyword is rejected to prevent escaping impersonation."""

    def test_revert_keyword_rejected(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("REVERT; SELECT 1 AS x"))
        assert "error" in result
        assert "REVERT" in result["error"]

    def test_revert_case_insensitive(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("revert; SELECT 1 AS x"))
        assert "error" in result

    def test_revert_unicode_fullwidth(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("\uff32\uff25\uff36\uff25\uff32\uff34; SELECT 1 AS x"))
        assert "error" in result

    def test_revert_char_construction(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "EXEC(''+CHAR(82)+CHAR(69)+CHAR(86)+CHAR(69)+CHAR(82)+CHAR(84))"
        ))
        assert "error" in result

    def test_revert_as_string_literal(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("SELECT 'no_revert_here' AS word"))
        assert "error" not in result


# ═══════════════════════════════════════════════════════════════
#   Security: impersonate name validation
# ═══════════════════════════════════════════════════════════════

class TestImpersonateValidation:
    """Impersonate name must match mcp-* pattern."""

    def test_valid_name_accepted(self, server, main_db):
        db = isqls(server, main_db, "mcp-server")
        assert db._impersonate == "mcp-server"

    def test_sa_rejected(self, server, main_db):
        with pytest.raises(ValueError, match="Invalid impersonate name"):
            isqls(server, main_db, "sa")

    def test_empty_rejected(self, server, main_db):
        with pytest.raises(ValueError, match="Invalid impersonate name"):
            isqls(server, main_db, "")

    def test_arbitrary_name_rejected(self, server, main_db):
        with pytest.raises(ValueError, match="Invalid impersonate name"):
            isqls(server, main_db, "admin")

    def test_mcp_prefix_required(self, server, main_db):
        with pytest.raises(ValueError, match="Invalid impersonate name"):
            isqls(server, main_db, "not-mcp-server")

    def test_mcp_hyphen_variants(self, server, main_db):
        db = isqls(server, main_db, "mcp-test-reader")
        assert db._impersonate == "mcp-test-reader"


# ═══════════════════════════════════════════════════════════════
#   Security: EXECUTE AS USER (default) vs LOGIN
# ═══════════════════════════════════════════════════════════════

class TestImpersonationMode:
    """EXECUTE AS USER is default; LOGIN is opt-in."""

    def test_default_is_user_mode(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        assert db._use_login is False
        sql = db._impersonate_sql()
        assert "EXECUTE AS USER" in sql
        assert "USER_NAME()" in sql

    def test_login_mode_opt_in(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate, use_login=True)
        assert db._use_login is True
        sql = db._impersonate_sql()
        assert "EXECUTE AS LOGIN" in sql
        assert "SYSTEM_USER" in sql

    def test_user_mode_executes(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        result = json.loads(db.execute_query("SELECT USER_NAME() AS CurrentUser"))
        assert "error" not in result, f"EXECUTE AS USER failed: {result.get('error')}"


# ═══════════════════════════════════════════════════════════════
#   Row limit (max_rows)
# ═══════════════════════════════════════════════════════════════

class TestRowLimit:
    """Results are truncated at max_rows."""

    def test_default_max_rows(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate)
        assert db._max_rows == 5000

    def test_custom_max_rows(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate, max_rows=2)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.columns"
        ))
        assert "error" not in result
        assert result["rowCount"] <= 2
        assert result.get("truncated") is True
        assert result.get("maxRows") == 2

    def test_under_limit_no_truncation(self, server, main_db, impersonate):
        db = isqls(server, main_db, impersonate, max_rows=10000)
        result = json.loads(db.execute_query(
            "SELECT TOP 3 name FROM sys.tables"
        ))
        assert "error" not in result
        assert result["rowCount"] == 3
        assert "truncated" not in result
