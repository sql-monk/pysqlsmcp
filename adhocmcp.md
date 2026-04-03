# adhocmcp — Ad-Hoc SQL MCP Server

## Overview

`adhocmcp.py` is a [FastMCP](https://gofastmcp.com/) server that exposes a single tool — **`executeQuery`** — allowing any MCP client to run ad-hoc SQL queries against any SQL Server database instance.

Unlike the main `sqlsmcp.py` server (which provides multiple specialised tools and requires server/database configuration at startup), `adhocmcp` accepts full connection parameters **at call time**, making it suitable for:

- Multi-tenant or multi-database environments
- Dynamic exploration without server-level pre-configuration
- Lightweight deployments where only raw query execution is needed

---

## Architecture

```
adhocmcp.py
 └── FastMCP("pysqlsmcp-adhoc")
      └── AdHocMCPProvider          (adhocmcpprovider.py)
           └── executeQuery tool
                └── isqls.execute_query()   (isqls.py)
```

### `AdHocMCPProvider` (`adhocmcpprovider.py`)

Implements `Provider` from `fastmcp.server.providers`.

Overrides `_list_tools()` to return a single dynamically-built `executeQuery` tool.  
Each invocation of the tool creates a fresh `isqls` instance with the supplied connection parameters.

### `adhocmcp.py`

FastMCP server entry point:

```python
from fastmcp import FastMCP
from adhocmcpprovider import AdHocMCPProvider

mcp = FastMCP("pysqlsmcp-adhoc")
mcp.add_provider(AdHocMCPProvider())

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Tool: `executeQuery`

Executes a SQL query against a specified SQL Server database using impersonated credentials.

### Parameters

| Parameter    | Type            | Required | Description |
|--------------|-----------------|----------|-------------|
| `server`     | `string`        | ✅       | SQL Server instance name or host address (e.g. `localhost`, `.\SQLEXPRESS`) |
| `database`   | `string`        | ✅       | Target database name |
| `query`      | `string`        | ✅       | SQL query to execute |
| `impersonate`| `string`        | ✅       | SQL Server login to impersonate via `EXECUTE AS LOGIN` |
| `params`     | `list` \| `null`| ❌       | Positional query parameters for `?` placeholders (DB-API style) |

### Return value

JSON string with one of the following shapes:

**SELECT query (rows returned):**
```json
{
  "query": "SELECT name FROM sys.tables",
  "rowCount": 3,
  "columns": ["name"],
  "rows": [["Customers"], ["Orders"], ["Products"]]
}
```

**DML query (no rows):**
```json
{
  "query": "INSERT INTO ...",
  "rowCount": 1
}
```

**Error:**
```json
{
  "error": "...",
  "query": "SELECT ...",
  "sqlErrorNumber": 208,
  "sqlState": "42S02"
}
```

---

## Usage

### stdio transport (default)

```bash
python adhocmcp.py
```

Configure your MCP client (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "pysqlsmcp-adhoc": {
      "command": "python",
      "args": ["C:/path/to/adhocmcp.py"]
    }
  }
}
```

### Calling the tool

Example tool invocation (JSON):

```json
{
  "name": "executeQuery",
  "arguments": {
    "server": "localhost",
    "database": "mcp_test_main",
    "query": "SELECT name FROM sys.tables WHERE name = ?",
    "impersonate": "mcp-server",
    "params": ["Customers"]
  }
}
```

---

## Security

The same security model as `sqlsmcp.py` applies:

- **Impersonation** — every query runs under `EXECUTE AS LOGIN = '<impersonate>'`. Grant only the minimum required permissions to the impersonated login.
- **`REVERT` neutralisation** — the `REVERT` keyword in queries is replaced with `/*revert*/` by `isqls` to prevent escaping the impersonated context.
- **Read-Uncommitted isolation** — queries run with `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED` and `SET LOCK_TIMEOUT 1000` to minimise blocking.

---

## Requirements

```
fastmcp>=3.2.0
mssql-python
```

Install:

```bash
pip install fastmcp mssql-python
```

---

## Tests

Unit tests (no SQL Server required) are in `tests/test_adhocmcp.py`.  
They are automatically included when running the integration test suite via `tests/run_tests.py`.

Run unit tests only:

```bash
cd /path/to/pysqlsmcp
python -m pytest tests/test_adhocmcp.py -v -k "Unit"
```

Run full test suite (requires SQL Server):

```bash
python tests/run_tests.py --server localhost
```

### Test coverage

| Test class | Scope | Description |
|---|---|---|
| `TestAdHocMCPProviderUnit` | Unit | Provider API, tool schema, delegation to isqls |
| `TestAdHocMCPServerUnit` | Unit | FastMCP server integration, tool routing |
| `TestAdHocMCPProviderIntegration` | Integration | Live SQL Server queries via provider tool |

---

## Differences from `sqlsmcp.py`

| Feature | `sqlsmcp.py` | `adhocmcp.py` |
|---|---|---|
| Framework | `mcp` (official SDK) | `fastmcp` (standalone) |
| Provider pattern | Tool functions registered directly | `AdHocMCPProvider` implementing `Provider` |
| Connection scope | Per-tool call | Per-tool call |
| Tools | `executeQuery`, `explainQuery`, `getDatabasePermission`, `getAllDatabasePermission`, `requiredAdditionalPermission` | `executeQuery` only |
| Use case | Full-featured metadata server | Lightweight ad-hoc query endpoint |
