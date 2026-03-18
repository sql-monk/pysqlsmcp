import json
import pytest
from unittest.mock import MagicMock, patch, call


@pytest.fixture
def mock_connect(mocker):
    return mocker.patch("mssql_python.connect")


def _make_cursor(rows=None, columns=None, error=None):
    cursor = MagicMock()
    if error:
        cursor.execute.side_effect = error
    else:
        cursor.description = [(col,) for col in (columns or [])]
        cursor.fetchall.return_value = rows or []
    return cursor


def _make_conn(cursor):
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn


class TestExecuteQuery:
    def test_success_returns_json(self, mock_connect):
        cursor = _make_cursor(rows=[("alice", 1), ("bob", 2)], columns=["name", "id"])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        result = json.loads(DbProvider("srv", "db").execute_query("SELECT 1"))

        assert result["rowCount"] == 2
        assert result["columns"] == ["name", "id"]
        assert result["rows"] == [["alice", 1], ["bob", 2]]
        assert "query" in result

    def test_error_returns_error_json(self, mock_connect):
        error = Exception("Login failed")
        error.args = (18456, "28000")
        cursor = _make_cursor(error=error)
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        result = json.loads(DbProvider("srv", "db").execute_query("SELECT 1"))

        assert "error" in result
        assert result["sqlErrorNumber"] == 18456
        assert result["sqlState"] == "28000"

    def test_params_passed_to_execute(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=["x"])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        DbProvider("srv", "db").execute_query("SELECT ? AS x", ("hello",))

        cursor.execute.assert_called_once_with("SELECT ? AS x", ("hello",))

    def test_no_params_passes_empty_tuple(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=[])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        DbProvider("srv", "db").execute_query("SELECT 1")

        cursor.execute.assert_called_once_with("SELECT 1", ())

    def test_connection_closed_on_success(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=[])
        conn = _make_conn(cursor)
        mock_connect.return_value = conn

        from db_provider import DbProvider
        DbProvider("srv", "db").execute_query("SELECT 1")

        conn.close.assert_called_once()


class TestListDatabases:
    def test_returns_list_of_names(self, mock_connect):
        cursor = _make_cursor(rows=[("db1",), ("db2",), ("db3",)])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        result = DbProvider("srv", "master").list_databases()

        assert result == ["db1", "db2", "db3"]

    def test_empty_returns_empty_list(self, mock_connect):
        cursor = _make_cursor(rows=[])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        result = DbProvider("srv", "master").list_databases()

        assert result == []


class TestConnectionString:
    def test_sql_auth_uses_uid_pwd(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=[])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        DbProvider("myserver", "mydb", "user1", "pass1").execute_query("SELECT 1")

        conn_str = mock_connect.call_args[0][0]
        assert "UID=user1" in conn_str
        assert "PWD=pass1" in conn_str
        assert "Trusted_Connection" not in conn_str

    def test_windows_auth_uses_trusted_connection(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=[])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        DbProvider("myserver", "mydb").execute_query("SELECT 1")

        conn_str = mock_connect.call_args[0][0]
        assert "Trusted_Connection=yes" in conn_str
        assert "UID" not in conn_str

    def test_server_and_database_in_conn_string(self, mock_connect):
        cursor = _make_cursor(rows=[], columns=[])
        mock_connect.return_value = _make_conn(cursor)

        from db_provider import DbProvider
        DbProvider("SQL01", "AdventureWorks").execute_query("SELECT 1")

        conn_str = mock_connect.call_args[0][0]
        assert "SERVER=SQL01" in conn_str
        assert "DATABASE=AdventureWorks" in conn_str
