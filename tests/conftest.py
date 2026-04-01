"""
Shared fixtures and helpers for integration tests.
Connection parameters are injected via pytest fixtures resolved from
the CLI options registered here.
"""
import json
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def pytest_addoption(parser):
    parser.addoption("--server",       required=True,  help="SQL Server host/instance")
    parser.addoption("--database",     required=True,  help="Main database (mcp_test_main)")
    parser.addoption("--database-aux", required=True,  help="Aux database (mcp_test_aux)")
    parser.addoption("--impersonate",  required=True,  help="Login to impersonate")


@pytest.fixture(scope="session")
def server(request):
    return request.config.getoption("--server")


@pytest.fixture(scope="session")
def database(request):
    return request.config.getoption("--database")


@pytest.fixture(scope="session")
def database_aux(request):
    return request.config.getoption("--database-aux")


@pytest.fixture(scope="session")
def impersonate(request):
    return request.config.getoption("--impersonate")


@pytest.fixture(scope="session")
def db(server, database, impersonate):
    """DbProvider connected to the main test database."""
    from db_provider import DbProvider
    return DbProvider(server, database, impersonate)


@pytest.fixture(scope="session")
def db_aux(server, database_aux, impersonate):
    """DbProvider connected to the aux test database."""
    from db_provider import DbProvider
    return DbProvider(server, database_aux, impersonate)


@pytest.fixture(scope="session")
def master_db(server, impersonate):
    """DbProvider connected to master."""
    from db_provider import DbProvider
    return DbProvider(server, "master", impersonate)


def parse_result(json_str: str) -> dict:
    """Parse JSON result string."""
    return json.loads(json_str)
