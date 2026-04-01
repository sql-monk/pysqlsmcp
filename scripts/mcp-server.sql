-- ============================================================
-- mcp-server  |  SERVER LEVEL  |
-- ============================================================
USE [master];
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-server')
	CREATE LOGIN [mcp-server] WITH PASSWORD = '{{PASSWORD}}', CHECK_POLICY = ON;
ALTER LOGIN [mcp-server] DISABLE;

ALTER SERVER ROLE [##MS_ServerStateReader##]            ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_ServerPerformanceStateReader##] ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DefinitionReader##]             ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_SecurityDefinitionReader##]     ADD MEMBER [mcp-server];
ALTER SERVER ROLE [##MS_DatabaseConnector##]            ADD MEMBER [mcp-server];
GO

DECLARE @sql NVARCHAR(max) = '';
SELECT @sql +=	REPLACE('
	USE [@@db];
	IF USER_ID(''mcp-server'') IS NULL CREATE USER [mcp-server] FROM LOGIN [mcp-server];
	IF USER_ID(''db_mcpserver'') IS NULL CREATE ROLE db_mcpserver;
	ALTER ROLE db_mcpserver ADD MEMBER [mcp-server];
	GRANT VIEW DEFINITION, SHOWPLAN TO db_mcpserver;
		GRANT SELECT ON SCHEMA::sys TO db_mcpserver;', '@@db', name)
FROM sys.databases
WHERE state_desc = 'ONLINE';

EXEC(@sql);