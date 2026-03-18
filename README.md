# pysqlsmcp

Python HTTP/SSE MCP server built with [FastMCP](https://github.com/jlowin/fastmcp) and `mssql-python`. Implements the same tools as the C# `sqlsmcp` project.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Generate TLS certificate

```bash
python gen_cert.py
```

Generates `cert.pem` and `key.pem` in the current directory (self-signed, valid for localhost / 127.0.0.1).

## Start the server

```bash
python server.py --certfile cert.pem --keyfile key.pem
```

Optional flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `0.0.0.0` | Bind address |
| `--port` | `8444` | Bind port |
| `--certfile` | *(required)* | Path to TLS certificate |
| `--keyfile` | *(required)* | Path to TLS private key |

## Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `selectQuery` | `server`, `database`, `from_`, `username?`, `password?`, `with_?`, `select?`, `where?`, `group_by?`, `having?`, `order_by?` | Executes a SELECT query built from parts |
| `getDatabasePermission` | `server`, `database`, `user_filter?`, `object_filter?`, `username?`, `password?` | Returns database role/permission assignments for one database |
| `getAllDatabasePermission` | `server`, `user_filter?`, `object_filter?`, `username?`, `password?` | Runs `getDatabasePermission` across all accessible databases and aggregates results |
| `requiredAdditionalPermission` | `server`, `database`, `object`, `username?`, `password?` | Returns cross-schema / cross-database dependencies for a stored procedure or view |

Parameters marked `?` are optional. When `username` and `password` are omitted, Windows Authentication (`Trusted_Connection=yes`) is used.

## VS Code MCP configuration

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "pysqlsmcp": {
      "type": "http",
      "url": "https://localhost:8444/mcp"
    }
  }
}
```

## Authentication

- **SQL Server auth:** pass `username` and `password` in each tool call.
- **Windows auth:** omit `username` and `password`; the server process identity is used.

## Running tests

```bash
pytest tests/
```

Test files:

| File | Covers |
|------|--------|
| `tests/test_db_provider.py` | `DbProvider` — execute_query, list_databases, connection strings |
| `tests/test_select_query.py` | `_run` SQL construction, no-params contract |
| `tests/test_get_database_permission.py` | `_run` parameter tuple layout |
| `tests/test_get_all_database_permission.py` | wrapper: aggregation, error collection |
| `tests/test_required_additional_permission.py` | 8× object param tuple |
| `tests/test_server.py` | FastMCP instance, tool registration |

## Logs

Query activity is appended to `sqlsmcp.log` in the project root.
