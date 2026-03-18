import json
import pytest
from unittest.mock import MagicMock, patch, call


def _make_db_provider(databases=None, rows=None, error=False):
    provider = MagicMock()
    if error:
        provider.execute_query.return_value = json.dumps(
            {"error": "Connection failed", "query": "", "sqlErrorNumber": 18456, "sqlState": "28000"}
        )
    else:
        provider.execute_query.return_value = json.dumps(
            {"query": "", "rowCount": len(rows or []), "columns": ["roleName", "userName"], "rows": rows or []}
        )
    provider.list_databases.return_value = databases or []
    return provider


class TestGetAllDatabasePermission:
    def test_aggregates_rows_from_all_databases(self, mocker):
        rows_db1 = [["role1", "userA"], ["role2", "userB"]]
        rows_db2 = [["role3", "userC"]]

        def make_provider(server, db, username, password):
            provider = MagicMock()
            if db == "master":
                provider.list_databases.return_value = ["db1", "db2"]
            elif db == "db1":
                provider.execute_query.return_value = json.dumps(
                    {"query": "", "rowCount": 2, "columns": ["roleName", "userName"], "rows": rows_db1}
                )
            else:
                provider.execute_query.return_value = json.dumps(
                    {"query": "", "rowCount": 1, "columns": ["roleName", "userName"], "rows": rows_db2}
                )
            return provider

        mocker.patch("tools.get_all_database_permission.DbProvider", side_effect=make_provider)

        from tools.get_all_database_permission import register
        mcp = MagicMock()
        captured = {}

        def tool_decorator():
            def inner(fn):
                captured["fn"] = fn
                return fn
            return inner

        mcp.tool = tool_decorator
        register(mcp)

        result = json.loads(captured["fn"]("myserver"))
        assert result["rowCount"] == 3
        assert result["databasesScanned"] == ["db1", "db2"]
        assert len(result["rows"]) == 3
        assert result["errors"] == []

    def test_collects_errors_without_stopping(self, mocker):
        def make_provider(server, db, username, password):
            provider = MagicMock()
            if db == "master":
                provider.list_databases.return_value = ["good_db", "bad_db", "also_good"]
            elif db == "bad_db":
                provider.execute_query.return_value = json.dumps(
                    {"error": "Access denied", "query": "", "sqlErrorNumber": 229, "sqlState": "42000"}
                )
            else:
                provider.execute_query.return_value = json.dumps(
                    {"query": "", "rowCount": 1, "columns": ["roleName"], "rows": [["r1"]]}
                )
            return provider

        mocker.patch("tools.get_all_database_permission.DbProvider", side_effect=make_provider)

        from tools.get_all_database_permission import register
        mcp = MagicMock()
        captured = {}
        mcp.tool = lambda: lambda fn: captured.update({"fn": fn}) or fn
        register(mcp)

        result = json.loads(captured["fn"]("myserver"))
        assert result["rowCount"] == 2
        assert len(result["errors"]) == 1
        assert result["errors"][0]["database"] == "bad_db"

    def test_calls_run_permission_once_per_database(self, mocker):
        def make_provider(server, db, username, password):
            provider = MagicMock()
            if db == "master":
                provider.list_databases.return_value = ["a", "b", "c"]
            else:
                provider.execute_query.return_value = json.dumps(
                    {"query": "", "rowCount": 0, "columns": [], "rows": []}
                )
            return provider

        mocker.patch("tools.get_all_database_permission.DbProvider", side_effect=make_provider)
        run_mock = mocker.patch("tools.get_all_database_permission.run_permission",
                                return_value=json.dumps({"query": "", "rowCount": 0, "columns": [], "rows": []}))

        from tools.get_all_database_permission import register
        mcp = MagicMock()
        captured = {}
        mcp.tool = lambda: lambda fn: captured.update({"fn": fn}) or fn
        register(mcp)

        captured["fn"]("myserver")
        assert run_mock.call_count == 3
