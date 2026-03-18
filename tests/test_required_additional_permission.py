import json
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def db_provider():
    provider = MagicMock()
    provider.execute_query.return_value = json.dumps(
        {"query": "", "rowCount": 0, "columns": [], "rows": []}
    )
    return provider


class TestRun:
    def test_object_repeated_eight_times(self, db_provider):
        from tools.required_additional_permission import _run
        _run(db_provider, "dbo.MyProc")
        _, params = db_provider.execute_query.call_args[0]
        assert len(params) == 8
        assert all(p == "dbo.MyProc" for p in params)

    def test_object_id_integer_string(self, db_provider):
        from tools.required_additional_permission import _run
        _run(db_provider, "12345")
        _, params = db_provider.execute_query.call_args[0]
        assert params == ("12345",) * 8

    def test_returns_json_string(self, db_provider):
        from tools.required_additional_permission import _run
        result = _run(db_provider, "dbo.Proc1")
        parsed = json.loads(result)
        assert "rowCount" in parsed
