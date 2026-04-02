/*
Get index usage statistics for a specific table or all tables.
Shows how often indexes are used for seeks, scans, lookups, and updates.

@table_name - Table name filter (use % for wildcard, NULL for all tables)
*/

DECLARE
    @table_name NVARCHAR(128);

SELECT
    OBJECT_NAME(s.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc AS index_type,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates,
    s.last_user_seek,
    s.last_user_scan,
    s.last_user_lookup
FROM sys.dm_db_index_usage_stats s
    INNER JOIN sys.indexes i
        ON s.object_id = i.object_id
        AND s.index_id = i.index_id
WHERE s.database_id = DB_ID()
    AND (@table_name IS NULL OR OBJECT_NAME(s.object_id) LIKE @table_name)
ORDER BY s.user_seeks + s.user_scans + s.user_lookups DESC
