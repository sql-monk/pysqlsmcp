import json
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def db_provider():
    provider = MagicMock()
    provider.execute_query.return_value = json.dumps(
        {"query": "", "rowCount": 0, "columns": [], "rows": []}
    )
    return provider


class TestRun:
    def test_basic_select_all(self, db_provider):
        from tools.select_query import _run
        _run(db_provider, from_="dbo.MyTable")
        sql = db_provider.execute_query.call_args[0][0]
        assert "SELECT * FROM dbo.MyTable" in sql

    def test_custom_select(self, db_provider):
        from tools.select_query import _run
        _run(db_provider, select="id, name", from_="dbo.Users")
        sql = db_provider.execute_query.call_args[0][0]
        assert "SELECT id, name FROM dbo.Users" in sql

    def test_full_query_order(self, db_provider):
        from tools.select_query import _run
        _run(
            db_provider,
            with_="cte AS (SELECT 1 AS x)",
            select="x",
            from_="cte",
            where="x = 1",
            group_by="x",
            having="COUNT(*) > 0",
            order_by="x DESC",
        )
        sql = db_provider.execute_query.call_args[0][0]
        lines = sql.strip().splitlines()
        assert lines[0].startswith("WITH cte")
        assert "SELECT x FROM cte" in sql
        assert "WHERE x = 1" in sql
        assert "GROUP BY x" in sql
        assert "HAVING COUNT(*) > 0" in sql
        assert "ORDER BY x DESC" in sql

    def test_no_where_when_not_provided(self, db_provider):
        from tools.select_query import _run
        _run(db_provider, from_="dbo.T")
        sql = db_provider.execute_query.call_args[0][0]
        assert "WHERE" not in sql

    def test_execute_called_without_params(self, db_provider):
        from tools.select_query import _run
        _run(db_provider, from_="dbo.T")
        # execute_query must be called with only the sql string (no second arg)
        args, kwargs = db_provider.execute_query.call_args
        assert len(args) == 1
        assert kwargs == {}

    def test_returns_json_string(self, db_provider):
        from tools.select_query import _run
        result = _run(db_provider, from_="dbo.T")
        parsed = json.loads(result)
        assert "rowCount" in parsed
