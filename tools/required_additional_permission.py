from typing import Optional
from db_provider import DbProvider

REQUIRED_PERM_QUERY = """
SELECT
    CONCAT(
        CASE WHEN d.referenced_database_name IS NOT NULL
             THEN QUOTENAME(d.referenced_database_name) + '.' ELSE '' END,
        QUOTENAME(d.referenced_schema_name), '.',
        QUOTENAME(d.referenced_entity_name)
    )                                           AS ObjectName,
    CASE
        WHEN d.referenced_database_name <> DB_NAME()
             AND d.referenced_database_name IS NOT NULL
            THEN N'Object from another database'
        WHEN ISNULL(d.referenced_database_name, DB_NAME()) = DB_NAME()
             AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
             AND USER_NAME(source_schema.principal_id) IS NOT NULL
            THEN N'Different schema owners ('
                 + USER_NAME(source_schema.principal_id)
                 + ' vs ' + USER_NAME(rs.principal_id) + ')'
        ELSE NULL
    END                                         AS PermissionReason,
    ISNULL(d.referenced_database_name, DB_NAME()) AS DatabaseName,
    d.referenced_schema_name                    AS SchemaName,
    d.referenced_entity_name                    AS EntityName,
    USER_NAME(rs.principal_id)                  AS SchemaOwner
FROM sys.sql_expression_dependencies d
    LEFT JOIN sys.schemas rs
        ON rs.name = d.referenced_schema_name
    LEFT JOIN sys.schemas source_schema
        ON source_schema.name = CASE
            WHEN PARSENAME(?, 2) IS NOT NULL THEN PARSENAME(?, 2)
            ELSE OBJECT_SCHEMA_NAME(ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)))
        END
WHERE d.referencing_id = ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?))
  AND ISNULL(TRY_CONVERT(INT, ?), OBJECT_ID(?)) IS NOT NULL
  AND (
        (d.referenced_database_name <> DB_NAME()
         AND d.referenced_database_name IS NOT NULL)
      OR
        (ISNULL(d.referenced_database_name, DB_NAME()) = DB_NAME()
         AND USER_NAME(rs.principal_id) <> USER_NAME(source_schema.principal_id)
         AND USER_NAME(source_schema.principal_id) IS NOT NULL)
  )
"""


def _run(db_provider: DbProvider, object: str) -> str:
    params = (object,) * 8
    return db_provider.execute_query(REQUIRED_PERM_QUERY, params)


def register(mcp):
    @mcp.tool()
    def requiredAdditionalPermission(
        server: str,
        database: str,
        object: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        db_provider = DbProvider(server, database, username, password)
        return _run(db_provider, object)
