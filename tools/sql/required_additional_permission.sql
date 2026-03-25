SELECT
    CONCAT(
        CASE WHEN d.referenced_database_name IS NOT NULL
             THEN QUOTENAME(d.referenced_database_name) + '.' ELSE '' END,
        QUOTENAME(d.referenced_schema_name), '.',
        QUOTENAME(d.referenced_entity_name)
    )                                           AS ObjectName,
    ISNULL(d.referenced_database_name, DB_NAME()) AS DatabaseName,
    d.referenced_schema_name                    AS SchemaName,
    d.referenced_entity_name                    AS EntityName
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
