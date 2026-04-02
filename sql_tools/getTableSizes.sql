/*
Get table sizes including row count, reserved space, data size, and index size.

@schema_name - Schema name filter (use % for wildcard, NULL for all schemas)
@table_name - Table name filter (use % for wildcard, NULL for all tables)
*/

DECLARE
    @schema_name NVARCHAR(128),
    @table_name NVARCHAR(128);

SELECT
    s.name AS schema_name,
    t.name AS table_name,
    p.rows AS row_count,
    SUM(a.total_pages) * 8 AS total_space_kb,
    SUM(a.used_pages) * 8 AS used_space_kb,
    (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS unused_space_kb,
    SUM(CASE WHEN i.index_id IN (0, 1) THEN a.used_pages ELSE 0 END) * 8 AS data_space_kb,
    SUM(CASE WHEN i.index_id NOT IN (0, 1) THEN a.used_pages ELSE 0 END) * 8 AS index_space_kb
FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    INNER JOIN sys.indexes i
        ON t.object_id = i.object_id
    INNER JOIN sys.partitions p
        ON i.object_id = p.object_id
        AND i.index_id = p.index_id
    INNER JOIN sys.allocation_units a
        ON p.partition_id = a.container_id
WHERE (@schema_name IS NULL OR s.name LIKE @schema_name)
    AND (@table_name IS NULL OR t.name LIKE @table_name)
GROUP BY s.name, t.name, p.rows
ORDER BY SUM(a.total_pages) DESC
