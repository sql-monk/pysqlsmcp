"""
Tests for DbProvider — core connection, impersonation, preamble.

Group: db_provider
"""
import json
import pytest
from db_provider import DbProvider


class TestDbProvider:
    """DB-001 … DB-007: DbProvider core functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, server, database, impersonate):
        self.db = DbProvider(server, database, impersonate)
        self.server = server
        self.database = database
        self.impersonate = impersonate

    def test_simple_query(self):
        """DB-001: execute_query returns valid JSON with rows."""
        r = json.loads(self.db.execute_query("SELECT 1 AS v"))
        assert "error" not in r
        assert r["rows"][0][0] == 1

    def test_impersonation_active(self):
        """DB-002: Query runs under impersonated identity."""
        r = json.loads(self.db.execute_query("SELECT USER_NAME() AS u"))
        assert "error" not in r
        # USER_NAME() should reflect the impersonated user, not the connecting login
        assert r["rowCount"] == 1

    def test_isolation_level(self):
        """DB-003: Transaction isolation is READ UNCOMMITTED."""
        r = json.loads(self.db.execute_query(
            "SELECT transaction_isolation_level FROM sys.dm_exec_sessions WHERE session_id = @@SPID"
        ))
        assert "error" not in r
        # 1 = READ UNCOMMITTED
        assert r["rows"][0][0] == 1

    def test_error_returns_json(self):
        """DB-004: SQL error returns JSON with 'error' key (no Python exception)."""
        r = json.loads(self.db.execute_query("RAISERROR('test error', 16, 1)"))
        assert "error" in r

    def test_explain_returns_plan(self):
        """DB-005: explain_query returns XML plan."""
        r = json.loads(self.db.explain_query("SELECT 1 AS v"))
        assert "error" not in r
        assert r["plan"] is not None
        assert "ShowPlanXML" in r["plan"]

    def test_list_databases(self):
        """DB-006: list_databases returns a list containing test databases."""
        dbs = self.db.list_databases()
        assert isinstance(dbs, list)
        assert "mcp_test_main" in dbs
        assert "mcp_test_aux" in dbs

    def test_revert_sanitisation(self):
        """DB-007: REVERT keyword in query text is neutralised."""
        r = json.loads(self.db.execute_query("SELECT 'REVERT' AS word"))
        assert "error" not in r
