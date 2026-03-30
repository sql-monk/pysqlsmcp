-- ============================================================
-- mcp-server  |  SERVER LEVEL  |
-- ============================================================
USE [master];
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-server')
	CREATE LOGIN [mcp-server] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;
ALTER LOGIN [mcp-server] DISABLE;

ALTER SERVER ROLE [##MS_ServerStateReader##]            ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_ServerPerformanceStateReader##] ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DefinitionReader##]             ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_SecurityDefinitionReader##]     ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DatabaseConnector##]            ADD MEMBER [mcp-server];
GO


-- ============================================================
-- mcp-YourDatabase  |  DATABASE LEVEL  |
-- ============================================================
USE [YourDatabase];
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-YourDatabase')
	CREATE LOGIN [mcp-YourDatabase] WITH PASSWORD = '[strong pwd]', CHECK_POLICY = ON;
ALTER LOGIN [mcp-YourDatabase] DISABLE;

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-YourDatabase')
	CREATE USER [mcp-YourDatabase] FROM LOGIN [mcp-YourDatabase];

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'db_mcp_YourDatabase' AND type = 'R')
	CREATE ROLE [db_mcp_YourDatabase];

ALTER ROLE [db_mcp_YourDatabase] ADD MEMBER [mcp-YourDatabase];

GRANT VIEW DATABASE STATE             TO [db_mcp_YourDatabase];
GRANT VIEW DEFINITION             		TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE PERFORMANCE STATE TO [db_mcp_YourDatabase];
GRANT VIEW DATABASE SECURITY STATE    TO [db_mcp_YourDatabase];

ALTER ROLE [db_denydatareader] ADD MEMBER [mcp-YourDatabase];
ALTER ROLE [db_denydatawriter] ADD MEMBER [mcp-YourDatabase];
GO