"""Tests for parameterized query support in SQLSProvider.execute_query.

Verifies that SQL parameters are passed correctly via the `params` argument
and that the resulting queries return expected data without SQL-injection risk.
"""

import json
import pytest
from sqlsprovider import SQLSProvider


class TestParamsSingleValue:
    """Single-parameter queries against sys.* metadata (no user-data access needed)."""

    def test_param_string_filters_sys_tables(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.tables WHERE name = ?",
            params=("Customers",),
        ))
        assert "error" not in result, result.get("error")
        assert result["rowCount"] == 1
        assert result["rows"][0][0] == "Customers"

    def test_param_string_no_match_returns_empty(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.tables WHERE name = ?",
            params=("NonExistentTable_xyz",),
        ))
        assert "error" not in result, result.get("error")
        assert result["rowCount"] == 0
        assert result["rows"] == []

    def test_param_int_filters_sys_columns(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        # column_id = 1 should always exist for any table
        result = json.loads(db.execute_query(
            "SELECT column_id, name FROM sys.columns "
            "WHERE OBJECT_NAME(object_id) = 'Customers' AND column_id = ?",
            params=(1,),
        ))
        assert "error" not in result, result.get("error")
        assert result["rowCount"] == 1
        assert result["rows"][0][0] == 1

    def test_param_filters_sys_objects_by_type(self, server, main_db, impersonate):
        """type='P' = stored procedures."""
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.objects WHERE type = ? ORDER BY name",
            params=("P",),
        ))
        assert "error" not in result, result.get("error")
        names = [row[0] for row in result["rows"]]
        assert "usp_SearchProducts" in names
        assert "usp_GetCustomerOrders" in names


class TestParamsMultipleValues:
    """Queries with more than one parameter placeholder."""

    def test_two_string_params(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT s.name AS [schema], t.name AS [table] "
            "FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id "
            "WHERE s.name = ? AND t.name = ?",
            params=("sales", "Orders"),
        ))
        assert "error" not in result, result.get("error")
        assert result["rowCount"] == 1
        assert result["rows"][0] == ["sales", "Orders"]

    def test_in_equivalent_via_multiple_params(self, server, main_db, impersonate):
        """Simulate IN(?,?) — two table names."""
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name FROM sys.tables WHERE name IN (?, ?) ORDER BY name",
            params=("Customers", "AuditLog"),
        ))
        assert "error" not in result, result.get("error")
        names = [row[0] for row in result["rows"]]
        assert "AuditLog" in names
        assert "Customers" in names

    def test_mixed_type_params(self, server, main_db, impersonate):
        """String + integer params in the same query."""
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT column_id, name FROM sys.columns "
            "WHERE OBJECT_NAME(object_id) = ? AND column_id > ? "
            "ORDER BY column_id",
            params=("Customers", 0),
        ))
        assert "error" not in result, result.get("error")
        assert result["rowCount"] >= 1
        for row in result["rows"]:
            assert row[0] > 0


class TestParamsNullAndEdgeCases:
    """Edge cases: None params, empty params tuple, none-value inside tuple."""

    def test_none_params_behaves_as_no_params(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT 1 AS val",
            params=None,
        ))
        assert "error" not in result, result.get("error")
        assert result["rows"][0][0] == 1

    def test_empty_tuple_params(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT 42 AS val",
            params=(),
        ))
        assert "error" not in result, result.get("error")
        assert result["rows"][0][0] == 42

    def test_null_param_value(self, server, main_db, impersonate):
        """Passing None as a parameter value should bind as SQL NULL."""
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT CASE WHEN ? IS NULL THEN 'yes' ELSE 'no' END AS is_null",
            params=(None,),
        ))
        assert "error" not in result, result.get("error")
        assert result["rows"][0][0] == "yes"


class TestParamsSelectValue:
    """Verify the actual returned values are correct, not just row counts."""

    def test_returned_columns_match_query(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT name, schema_id FROM sys.tables WHERE name = ?",
            params=("Customers",),
        ))
        assert "error" not in result, result.get("error")
        assert result["columns"] == ["name", "schema_id"]
        assert result["rows"][0][0] == "Customers"

    def test_scalar_string_param_roundtrip(self, server, main_db, impersonate):
        """The parameter value makes it through unchanged."""
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT ? AS echo",
            params=("hello-world",),
        ))
        assert "error" not in result, result.get("error")
        assert result["rows"][0][0] == "hello-world"

    def test_scalar_int_param_roundtrip(self, server, main_db, impersonate):
        db = SQLSProvider(server, main_db, impersonate)
        result = json.loads(db.execute_query(
            "SELECT ? AS echo",
            params=(12345,),
        ))
        assert "error" not in result, result.get("error")
        assert result["rows"][0][0] == 12345
