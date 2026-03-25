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
