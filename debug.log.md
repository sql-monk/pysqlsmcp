<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT USER_NAME() AS CurrentUser
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT s.name AS [schema], t.name AS [table] FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id ORDER BY s.name, t.name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT c.name, TYPE_NAME(c.user_type_id) AS type_name FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id WHERE t.name = 'Customers'
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT SCHEMA_NAME(schema_id) AS [schema], name FROM sys.procedures ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name FROM sys.views ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name FROM sys.schemas WHERE name IN ('dbo', 'sales', 'inventory') ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.usp_SearchProducts')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_CustomerOrders')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(parent_object_id) AS child_table, OBJECT_NAME(referenced_object_id) AS parent_table FROM sys.foreign_keys
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(object_id) AS [table], name, type_desc FROM sys.indexes WHERE name IS NOT NULL AND OBJECT_NAME(object_id) = 'Customers'
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name, base_object_name FROM sys.synonyms ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(referencing_id) AS referencing, referenced_database_name, referenced_schema_name, referenced_entity_name FROM sys.sql_expression_dependencies WHERE referenced_database_name IS NOT NULL
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name FROM sys.tables ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name FROM sys.procedures
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.fn_WarehouseTotalQty')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name, base_object_name FROM sys.synonyms ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, login_name, status FROM sys.dm_exec_sessions
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, status, command FROM sys.dm_exec_requests
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, connect_time, net_transport FROM sys.dm_exec_connections
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 OBJECT_NAME(object_id) AS [table], user_seeks, user_scans, user_lookups FROM sys.dm_db_index_usage_stats WHERE database_id = DB_ID()
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 execution_count, total_worker_time, total_logical_reads FROM sys.dm_exec_query_stats ORDER BY total_worker_time DESC
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 wait_type, waiting_tasks_count, wait_time_ms FROM sys.dm_os_wait_stats ORDER BY wait_time_ms DESC
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT dp.name, dp.type_desc, p.permission_name, p.state_desc FROM sys.database_principals dp JOIN sys.database_permissions p ON p.grantee_principal_id = dp.principal_id WHERE dp.name LIKE 'mcp-test-%'
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT USER_NAME(role_principal_id) AS role_name, USER_NAME(member_principal_id) AS member_name FROM sys.database_role_members WHERE USER_NAME(member_principal_id) LIKE 'mcp-test-%'
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name, type_desc FROM sys.database_principals WHERE name LIKE 'role_%' ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
/*revert*/; SELECT 1 AS x
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT '/*/*revert*/*/' AS word
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers',)`

```sql
SELECT name FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:04 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('NonExistentTable_xyz',)`

```sql
SELECT name FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(1,)`

```sql
SELECT column_id, name FROM sys.columns WHERE OBJECT_NAME(object_id) = 'Customers' AND column_id = ?
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('P',)`

```sql
SELECT name FROM sys.objects WHERE type = ? ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('sales', 'Orders')`

```sql
SELECT s.name AS [schema], t.name AS [table] FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id WHERE s.name = ? AND t.name = ?
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers', 'AuditLog')`

```sql
SELECT name FROM sys.tables WHERE name IN (?, ?) ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers', 0)`

```sql
SELECT column_id, name FROM sys.columns WHERE OBJECT_NAME(object_id) = ? AND column_id > ? ORDER BY column_id
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT 1 AS val
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT 42 AS val
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None,)`

```sql
SELECT CASE WHEN ? IS NULL THEN 'yes' ELSE 'no' END AS is_null
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers',)`

```sql
SELECT name, schema_id FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('hello-world',)`

```sql
SELECT ? AS echo
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(12345,)`

```sql
SELECT ? AS echo
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-reader', 'mcp-test-reader', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-writer', 'mcp-test-writer', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'Customers', 'Customers', 'Customers')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'Products', 'Products', 'Products')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'ZZZ_NoSuchObject', 'ZZZ_NoSuchObject', 'ZZZ_NoSuchObject')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', 'Customers', 'Customers', 'Customers')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-reader', 'mcp-test-reader', 'Orders', 'Orders', 'Orders')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, 'Warehouses', 'Warehouses', 'Warehouses')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, 'Shipments', 'Shipments', 'Shipments')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:05 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT USER_NAME() AS CurrentUser
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT s.name AS [schema], t.name AS [table] FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id ORDER BY s.name, t.name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT c.name, TYPE_NAME(c.user_type_id) AS type_name FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id WHERE t.name = 'Customers'
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT SCHEMA_NAME(schema_id) AS [schema], name FROM sys.procedures ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name FROM sys.views ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name FROM sys.schemas WHERE name IN ('dbo', 'sales', 'inventory') ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.usp_SearchProducts')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_CustomerOrders')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(parent_object_id) AS child_table, OBJECT_NAME(referenced_object_id) AS parent_table FROM sys.foreign_keys
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(object_id) AS [table], name, type_desc FROM sys.indexes WHERE name IS NOT NULL AND OBJECT_NAME(object_id) = 'Customers'
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name, base_object_name FROM sys.synonyms ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT OBJECT_NAME(referencing_id) AS referencing, referenced_database_name, referenced_schema_name, referenced_entity_name FROM sys.sql_expression_dependencies WHERE referenced_database_name IS NOT NULL
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name FROM sys.tables ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name FROM sys.procedures
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.fn_WarehouseTotalQty')) AS def_text
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

```sql
SELECT name, base_object_name FROM sys.synonyms ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:09 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, login_name, status FROM sys.dm_exec_sessions
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, status, command FROM sys.dm_exec_requests
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 session_id, connect_time, net_transport FROM sys.dm_exec_connections
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 OBJECT_NAME(object_id) AS [table], user_seeks, user_scans, user_lookups FROM sys.dm_db_index_usage_stats WHERE database_id = DB_ID()
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 execution_count, total_worker_time, total_logical_reads FROM sys.dm_exec_query_stats ORDER BY total_worker_time DESC
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT TOP 5 wait_type, waiting_tasks_count, wait_time_ms FROM sys.dm_os_wait_stats ORDER BY wait_time_ms DESC
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT dp.name, dp.type_desc, p.permission_name, p.state_desc FROM sys.database_principals dp JOIN sys.database_permissions p ON p.grantee_principal_id = dp.principal_id WHERE dp.name LIKE 'mcp-test-%'
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT USER_NAME(role_principal_id) AS role_name, USER_NAME(member_principal_id) AS member_name FROM sys.database_role_members WHERE USER_NAME(member_principal_id) LIKE 'mcp-test-%'
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT name, type_desc FROM sys.database_principals WHERE name LIKE 'role_%' ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
/*revert*/; SELECT 1 AS x
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT '/*/*revert*/*/' AS word
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers',)`

```sql
SELECT name FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('NonExistentTable_xyz',)`

```sql
SELECT name FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(1,)`

```sql
SELECT column_id, name FROM sys.columns WHERE OBJECT_NAME(object_id) = 'Customers' AND column_id = ?
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('P',)`

```sql
SELECT name FROM sys.objects WHERE type = ? ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('sales', 'Orders')`

```sql
SELECT s.name AS [schema], t.name AS [table] FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id WHERE s.name = ? AND t.name = ?
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers', 'AuditLog')`

```sql
SELECT name FROM sys.tables WHERE name IN (?, ?) ORDER BY name
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers', 0)`

```sql
SELECT column_id, name FROM sys.columns WHERE OBJECT_NAME(object_id) = ? AND column_id > ? ORDER BY column_id
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT 1 AS val
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

```sql
SELECT 42 AS val
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None,)`

```sql
SELECT CASE WHEN ? IS NULL THEN 'yes' ELSE 'no' END AS is_null
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('Customers',)`

```sql
SELECT name, schema_id FROM sys.tables WHERE name = ?
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('hello-world',)`

```sql
SELECT ? AS echo
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(12345,)`

```sql
SELECT ? AS echo
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-reader', 'mcp-test-reader', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-writer', 'mcp-test-writer', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'Customers', 'Customers', 'Customers')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'Products', 'Products', 'Products')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`(None, None, 'ZZZ_NoSuchObject', 'ZZZ_NoSuchObject', 'ZZZ_NoSuchObject')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', 'Customers', 'Customers', 'Customers')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('mcp-test-reader', 'mcp-test-reader', 'Orders', 'Orders', 'Orders')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('mcp-test-admin', 'mcp-test-admin', None, None, None)`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, 'Warehouses', 'Warehouses', 'Warehouses')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`(None, None, 'Shipments', 'Shipments', 'Shipments')`

```sql
SELECT
   @@SERVERNAME                                AS serverName,
   DB_NAME()                                   AS databaseName,
   USER_NAME(rm.role_principal_id)             AS roleName,
   USER_NAME(rm.member_principal_id)           AS userName,
   p.state_desc,
   p.permission_name,
   p.class_desc,
   CASE WHEN p.class_desc = 'OBJECT_OR_COLUMN'
        THEN OBJECT_NAME(p.major_id) END        AS objectName,
   CASE p.class_desc
       WHEN 'SCHEMA'           THEN SCHEMA_NAME(p.major_id)
       WHEN 'OBJECT_OR_COLUMN' THEN OBJECT_SCHEMA_NAME(p.major_id)
   END                                          AS schemaName,
   USER_NAME(p.grantee_principal_id)            AS granteeName
FROM sys.database_role_members rm
    JOIN sys.database_permissions p
        ON p.grantee_principal_id IN (rm.role_principal_id, rm.member_principal_id)
WHERE p.type <> 'CO'
  AND (? IS NULL OR USER_NAME(rm.member_principal_id) LIKE ?)
  AND (? IS NULL
       OR (p.class_desc = 'OBJECT_OR_COLUMN' AND OBJECT_NAME(p.major_id) LIKE ?)
       OR (p.class_desc = 'SCHEMA'           AND SCHEMA_NAME(p.major_id) LIKE ?))

```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse', 'dbo.vw_AuxWarehouse')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses', 'dbo.syn_Warehouses')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders', 'dbo.vw_CustomerOrders')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders', 'sales.usp_GetCustomerOrders')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames', 'dbo.vw_StockWithProductNames')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products', 'dbo.syn_Products')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo', 'dbo.usp_GetWarehouseInfo')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary', 'dbo.vw_StockSummary')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock', 'dbo.usp_ProductWarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses', 'dbo.Warehouses')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock', 'dbo.WarehouseStock')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_aux</span>
</summary>

`('dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport', 'dbo.usp_StockReport')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products', 'inventory.Products')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts', 'dbo.usp_SearchProducts')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

<details>
<summary>
2026-04-02 00:10 COMPLETE <span style="font-style:italic">sqltest mcp_test_main</span>
</summary>

`('dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object', 'dbo.zzz_no_such_object')`

```sql
SELECT
    CONCAT(
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 3),           -- БД з base_object синоніма
            d.referenced_database_name
        )) + '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 2),           -- схема з base_object синоніма
            d.referenced_schema_name
        )), '.',
        QUOTENAME(COALESCE(
            PARSENAME(syn.base_object_name, 1),           -- об'єкт з base_object синоніма
            d.referenced_entity_name
        ))
    )                                                      AS ObjectName,
    COALESCE(
        PARSENAME(syn.base_object_name, 3),
        d.referenced_database_name,
        DB_NAME()
    )                                                      AS DatabaseName,
    COALESCE(
        PARSENAME(syn.base_object_name, 2),
        d.referenced_schema_name
    )                                                      AS SchemaName,
    COALESCE(
        PARSENAME(syn.base_object_name, 1),
        d.referenced_entity_name
    )                                                      AS EntityName,
    CASE WHEN syn.object_id IS NOT NULL THEN 1 ELSE 0 END AS IsSynonym,
    syn.name                                               AS SynonymName
FROM sys.sql_expression_dependencies d (NOLOCK)
    LEFT JOIN sys.synonyms syn (NOLOCK)
        ON syn.object_id = d.referenced_id
    LEFT JOIN sys.schemas rs (NOLOCK)
        ON rs.name = COALESCE(
            PARSENAME(syn.base_object_name, 2),
            d.referenced_schema_name
        )
    LEFT JOIN sys.schemas source_schema (NOLOCK)
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        -- cross-database: пряма залежність або синонім вказує на іншу БД
        (COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) <> DB_NAME()
         AND COALESCE(PARSENAME(syn.base_object_name, 3), d.referenced_database_name) IS NOT NULL)
      OR
        -- cross-schema ownership: перевіряємо реальну схему (з синоніма або напряму)
        (COALESCE(
            PARSENAME(syn.base_object_name, 3),
            d.referenced_database_name,
            DB_NAME()
         ) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
```

</details>

