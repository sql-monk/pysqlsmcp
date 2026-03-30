# pysqlsmcp

Python MCP (Model Context Protocol) server for safe, read-oriented access to Microsoft SQL Server. Built with [FastMCP](https://github.com/jlowin/fastmcp), [`mssql-python`](https://pypi.org/project/mssql-python/) and served over HTTPS via Uvicorn.

## Key design principles

1. **Impersonation-first security** — every query runs under `EXECUTE AS`, never under the connecting login's own permissions.
2. **Defensive SET preamble** — session settings are forced before every statement to prevent blocking and priority escalation.
3. **TLS only** — the server requires a certificate; plain HTTP is not supported.

---

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

python gen_cert.py             # creates cert.pem + key.pem (self-signed, localhost/127.0.0.1)
python server.py --certfile cert.pem --keyfile key.pem
```

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `0.0.0.0` | Bind address |
| `--port` | `8444` | Bind port |
| `--certfile` | *(required)* | Path to TLS certificate |
| `--keyfile` | *(required)* | Path to TLS private key |

---

## Installation & configuration

### SQL Server setup

The file [`tools/sql/login_and_user_creation.sql`](tools/sql/login_and_user_creation.sql) contains the reference DDL.

#### Server level — `mcp-server` login

```sql
CREATE LOGIN [mcp-server] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;

-- Read-only server roles (SQL Server 2022+)
ALTER SERVER ROLE [##MS_ServerStateReader##]            ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_ServerPerformanceStateReader##] ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DefinitionReader##]             ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_SecurityDefinitionReader##]     ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DatabaseConnector##]            ADD MEMBER [mcp-server];
```

#### Database level — `mcp-{database}` user

For each database where `mcplevel=1` is used:

```sql
CREATE LOGIN  [mcp-YourDatabase] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;
CREATE USER   [mcp-YourDatabase] FROM LOGIN [mcp-YourDatabase];
CREATE ROLE   [db_mcp_YourDatabase];

ALTER ROLE [db_mcp_YourDatabase] ADD MEMBER [mcp-YourDatabase];

GRANT VIEW DATABASE STATE             TO [db_mcp_YourDatabase];
GRANT VIEW ANY DEFINITION             TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE PERFORMANCE STATE TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE SECURITY STATE    TO [db_mcp_YourDatabase];

-- Deny data access — metadata only
ALTER ROLE [db_denydatareader] ADD MEMBER [mcp-YourDatabase];
ALTER ROLE [db_denydatawriter] ADD MEMBER [mcp-YourDatabase];
```

The connecting login must also be granted:

```sql
-- For mcplevel=0:
GRANT IMPERSONATE ON LOGIN::[mcp-server] TO [connecting_login];

-- For mcplevel=1 (per database):
GRANT IMPERSONATE ON USER::[mcp-YourDatabase] TO [connecting_user];
```

### VS Code MCP configuration

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

---

## Safe query execution

### SET preamble

Every query session begins with a forced preamble (`_SET_PREAMBLE` in `db_provider.py`):

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET LOCK_TIMEOUT 1000;
SET DEADLOCK_PRIORITY LOW;
```

| Statement | Purpose |
|-----------|---------|
| `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED` | Dirty reads — the MCP server never needs transactional consistency and must not place shared locks that block production writes. |
| `SET LOCK_TIMEOUT 1000` | If a lock is still required (DDL metadata, etc.), the query fails after 1 second instead of waiting indefinitely. |
| `SET DEADLOCK_PRIORITY LOW` | If a deadlock occurs, SQL Server kills the MCP session first, protecting production workloads. |

These settings guarantee that MCP activity cannot degrade production performance — no locks held, fast timeout, lowest deadlock priority.

Additionally, `explain_query` wraps the user query with:

```sql
SET SHOWPLAN_XML ON;
-- user query (not actually executed)
SET SHOWPLAN_XML OFF;
```

This returns the XML execution plan without running the query.

### Impersonation (`EXECUTE AS`)

Impersonation is the core security mechanism. The connecting login (e.g. Windows auth or SQL auth) is **never** the identity that runs user queries. Instead, `DbProvider` immediately switches context after the SET preamble.

#### Two impersonation levels (`mcplevel`)

Every tool accepts an `mcplevel` parameter (default `0`):

| `mcplevel` | `EXECUTE AS` statement | Effective identity | Use case |
|------------|------------------------|-------------------|----------|
| `0` | `EXECUTE AS LOGIN = N'mcp-server'` | Server-level login `mcp-server` | Broad read-only access across all databases via server roles |
| `1` | `EXECUTE AS USER = N'mcp-{database}'` | Database-level user `mcp-{database}` | Fine-grained per-database permissions via database roles |

#### How it works step-by-step

1. Connection is established with the caller's credentials (SQL auth or Windows auth).
2. `_SET_PREAMBLE` is executed (isolation, lock timeout, deadlock priority).
3. `EXECUTE AS LOGIN` or `EXECUTE AS USER` switches the security context.
4. A verification check confirms the switch actually happened:
   - Level 0: `SYSTEM_USER` must equal `mcp-server`
   - Level 1: `USER_NAME()` must equal `mcp-{database}`
5. If verification fails — `REVERT` + `RAISERROR` — the query never runs.
6. The user query executes under the impersonated identity.
7. `REVERT` restores the original context (always runs, even on error via `finally`).

#### Why this matters

- The connecting login needs only `IMPERSONATE` permission, not direct data access.
- Permissions are centrally managed on the `mcp-server` login / `mcp-{database}` users.
- Even if an AI agent crafts a malicious query, it runs under the restricted impersonated identity.
- The verification step prevents silent failures where `EXECUTE AS` succeeds syntactically but the context is not what was expected.

---

## Tools

All tools accept `server`, `username?`, `password?`, and `mcplevel?` (default `0`).
When `username`/`password` are omitted, Windows Authentication (`Trusted_Connection=yes`) is used.

| Tool | Extra parameters | Description |
|------|-----------------|-------------|
| `executeQuery` | `database`, `query` | Executes an arbitrary query under impersonation and returns rows + columns as JSON |
| `explainQuery` | `database`, `query` | Returns the XML execution plan (`SHOWPLAN_XML`) without executing the query |
| `getDatabasePermission` | `database`, `user_filter?`, `object_filter?` | Lists role memberships and permissions for one database (queries `sys.database_role_members` + `sys.database_permissions`) |
| `getAllDatabasePermission` | `user_filter?`, `object_filter?` | Runs `getDatabasePermission` across every accessible database and aggregates the results |
| `requiredAdditionalPermission` | `database`, `object` | Lists cross-schema and cross-database dependencies for a stored procedure or view (via `sys.sql_expression_dependencies`) |

---

## Project structure

```
server.py                  — Uvicorn HTTPS entry point, registers all tools
db_provider.py             — Connection, SET preamble, EXECUTE AS, query execution
gen_cert.py                — Generates self-signed TLS cert (cert.pem + key.pem)
tools/
  execute_query.py         — executeQuery tool
  explain_query.py         — explainQuery tool
  get_database_permission.py       — getDatabasePermission tool
  get_all_database_permission.py   — getAllDatabasePermission tool
  required_additional_permission.py — requiredAdditionalPermission tool
  sql/
    get_database_permission.sql      — Permission query
    required_additional_permission.sql — Dependency query
    login_and_user_creation.sql      — Reference DDL for mcp-server setup
```

## Logs

Query activity is appended to `sqlsmcp.log` in the project root.
