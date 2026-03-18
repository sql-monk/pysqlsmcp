import json
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def db_provider():
    provider = MagicMock()
    provider.execute_query.return_value = json.dumps(
        {"query": "", "rowCount": 1, "columns": ["roleName", "userName"], "rows": [["role1", "user1"]]}
    )
    return provider


class TestRun:
    def test_no_filters_passes_none_tuple(self, db_provider):
        from tools.get_database_permission import _run
        _run(db_provider)
        _, params = db_provider.execute_query.call_args[0]
        assert params == (None, None, None, None, None)

    def test_user_filter_repeated_twice(self, db_provider):
        from tools.get_database_permission import _run
        _run(db_provider, user_filter="%svc%")
        _, params = db_provider.execute_query.call_args[0]
        assert params[0] == "%svc%"
        assert params[1] == "%svc%"

    def test_object_filter_repeated_three_times(self, db_provider):
        from tools.get_database_permission import _run
        _run(db_provider, object_filter="vw_%")
        _, params = db_provider.execute_query.call_args[0]
        assert params[2] == "vw_%"
        assert params[3] == "vw_%"
        assert params[4] == "vw_%"

    def test_both_filters_correct_tuple(self, db_provider):
        from tools.get_database_permission import _run
        _run(db_provider, user_filter="alice", object_filter="Orders")
        _, params = db_provider.execute_query.call_args[0]
        assert params == ("alice", "alice", "Orders", "Orders", "Orders")

    def test_returns_json_string(self, db_provider):
        from tools.get_database_permission import _run
        result = _run(db_provider)
        parsed = json.loads(result)
        assert "rowCount" in parsed
