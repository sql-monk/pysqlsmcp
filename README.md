# pysqlsmcp

Python MCP (Model Context Protocol) server for safe, read-oriented access to Microsoft SQL Server. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [`mssql-python`](https://pypi.org/project/mssql-python/), communicates via stdio transport.

## Key design principles

1. **Impersonation-first security** — every query runs under `EXECUTE AS`, never under the connecting login's own permissions.
2. **Defensive SET preamble** — session settings are forced before every statement to prevent blocking and priority escalation.

---

## Quick start

```bash
pip install -r requirements.txt

# interactive installer (SQL users, agent config)
python deploy/install.py
```

The server is started automatically by the MCP client (VS Code, Claude Desktop, etc.) via stdio — no manual launch needed.

---

## Installation (`deploy/install.py`)

The interactive installer handles all setup steps. Run it once after cloning:

```bash
pip install -r requirements.txt

# interactive installer (SQL users, agent config)
python deploy/install.py
```

The installer walks through two stages:

### 1. SQL Server users

The installer asks for a SQL Server instance name and then offers to create:

| Option | Script | What it creates |
|--------|--------|-----------------|
| **Per database** | [`deploy/scripts/mcp-database.sql`](deploy/scripts/mcp-database.sql) | Login `mcp-{database}`, user, role with metadata-only grants; data read/write denied |

You can create users for multiple databases in one session.

> **Security:** passwords are generated at runtime using `secrets` (40 chars, mixed case + digits + specials). They are passed to `mssql_python` in memory and **never stored or displayed**.

The connection to SQL Server uses Windows Authentication (`Trusted_Connection=yes`), so run the installer under an account that has `sysadmin` or `securityadmin` rights on the target instance.

After creating the users you still need to grant `IMPERSONATE` to the connecting login:

```sql
GRANT IMPERSONATE ON USER::[mcp-YourDatabase] TO [connecting_user];
```

### 2. Agent integration

The installer can register pysqlsmcp in agent config files so the MCP server is available immediately.

It searches for config files:

| Agent | Config file | Key |
|-------|------------|-----|
| VS Code | `mcp.json` | `servers.pysqlsmcp` |
| Claude Desktop | `claude_desktop_config.json` | `mcpServers.pysqlsmcp` |

Search starts from `%APPDATA%` (known locations) and a user-specified directory (default: home folder). You can select which found configs to patch.

Example resulting VS Code entry (`.vscode/mcp.json`):

```json
{
  "servers": {
    "pysqlsmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["path/to/pysqlsmcp/sqlsmcp.py"]
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

Every tool requires an `impersonate` parameter — the name of the database user to impersonate:

```
EXECUTE AS USER = N'{impersonate}'
```

#### How it works step-by-step

1. Connection is established with the caller's credentials (SQL auth or Windows auth).
2. `_SET_PREAMBLE` is executed (isolation, lock timeout, deadlock priority).
3. `EXECUTE AS USER` switches the security context to the specified user.
4. A verification check confirms the switch actually happened: `USER_NAME()` must equal the `impersonate` value.
5. If verification fails — `REVERT` + `RAISERROR` — the query never runs.
6. The user query executes under the impersonated identity.
7. `REVERT` restores the original context (always runs, even on error via `finally`).

#### Why this matters

- The connecting login needs only `IMPERSONATE` permission, not direct data access.
- Permissions are centrally managed on the `mcp-{database}` users.
- Even if an AI agent crafts a malicious query, it runs under the restricted impersonated identity.
- The verification step prevents silent failures where `EXECUTE AS` succeeds syntactically but the context is not what was expected.

---

## Tools

All tools accept `server` and `impersonate`. Windows Authentication (`Trusted_Connection=yes`) is always used.

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
sqlsmcp.py                 — Entry point (stdio transport), registers all tools
db_provider.py             — Connection, SET preamble, EXECUTE AS, query execution
deploy/
  install.py               — Interactive installer (SQL users, agent config)
  scripts/
    mcp-database.sql       — User/role DDL template
tools/
  execute_query.py         — executeQuery tool
  explain_query.py         — explainQuery tool
  get_database_permission.py       — getDatabasePermission tool
  get_all_database_permission.py   — getAllDatabasePermission tool
  required_additional_permission.py — requiredAdditionalPermission tool
  sql/
    get_database_permission.sql      — Permission query
    required_additional_permission.sql — Dependency query
```

## Logs

Query activity is appended to `sqlsmcp.log` in the project root.
