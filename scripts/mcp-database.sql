-- ============================================================
-- mcp-{{DATABASE}}  |  DATABASE LEVEL  |
-- ============================================================
USE [{{DATABASE}}];
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-{{DATABASE}}')
	CREATE LOGIN [mcp-{{DATABASE}}] WITH PASSWORD = '{{PASSWORD}}', CHECK_POLICY = ON;
ALTER LOGIN [mcp-{{DATABASE}}] DISABLE;

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-{{DATABASE}}')
	CREATE USER [mcp-{{DATABASE}}] FROM LOGIN [mcp-{{DATABASE}}];

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'db_mcp_{{DATABASE}}' AND type = 'R')
	CREATE ROLE [db_mcp_{{DATABASE}}];

ALTER ROLE [db_mcp_{{DATABASE}}] ADD MEMBER [mcp-{{DATABASE}}];

GRANT VIEW DATABASE STATE             TO [db_mcp_{{DATABASE}}];
GRANT VIEW DEFINITION             		TO [db_mcp_{{DATABASE}}];
GRANT VIEW DATABASE PERFORMANCE STATE TO [db_mcp_{{DATABASE}}];
GRANT VIEW DATABASE SECURITY STATE    TO [db_mcp_{{DATABASE}}];

ALTER ROLE [db_denydatareader] ADD MEMBER [mcp-{{DATABASE}}];
ALTER ROLE [db_denydatawriter] ADD MEMBER [mcp-{{DATABASE}}];
GO
