"""Shared fixtures for pysqlsmcp integration tests.

Permission model
────────────────
Connection: Windows auth (trusted).
Impersonation: EXECUTE AS LOGIN = 'mcp-server' inside each session.

mcp-server:
  Server roles: ServerStateReader, PerformanceStateReader,
                DefinitionReader, SecurityDefinitionReader, DatabaseConnector.
  Per-database: VIEW DEFINITION, VIEW DATABASE STATE,
                VIEW DATABASE PERFORMANCE STATE, VIEW DATABASE SECURITY STATE.
                db_denydatareader + db_denydatawriter → NO user data access.

All MCP tools operate under mcp-server. The tests verify:
  ✓ metadata access (sys.*, OBJECT_DEFINITION, SHOWPLAN_XML, permissions)
  ✗ user data access (SELECT/INSERT/UPDATE/DELETE on user tables/views)
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(scope="session")
def server():
    return os.environ.get("PYSQLSMCP_TEST_SERVER", "localhost")


@pytest.fixture(scope="session")
def impersonate():
    """MCP login — metadata only, no user data access."""
    return os.environ.get("PYSQLSMCP_TEST_IMPERSONATE", "mcp-server")


@pytest.fixture(scope="session")
def main_db():
    return "mcp_test_main"


@pytest.fixture(scope="session")
def aux_db():
    return "mcp_test_aux"
