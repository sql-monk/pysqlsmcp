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