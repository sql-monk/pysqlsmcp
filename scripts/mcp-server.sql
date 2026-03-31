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
