-- ============================================================
-- deploy-1-server.sql
-- Creates test databases and server-level logins.
-- Execute in the context of: master
-- ============================================================

-- ── databases ───────────────────────────────────────────────
IF DB_ID('mcp_test_main') IS NULL CREATE DATABASE [mcp_test_main];
GO
IF DB_ID('mcp_test_aux') IS NULL CREATE DATABASE [mcp_test_aux];
GO

-- ── logins ──────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-test-reader')
    CREATE LOGIN [mcp-test-reader] WITH PASSWORD = '{{PASSWORD_READER}}', CHECK_POLICY = ON;
ALTER LOGIN [mcp-test-reader] DISABLE;
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-test-writer')
    CREATE LOGIN [mcp-test-writer] WITH PASSWORD = '{{PASSWORD_WRITER}}', CHECK_POLICY = ON;
ALTER LOGIN [mcp-test-writer] DISABLE;
GO

IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'mcp-test-admin')
    CREATE LOGIN [mcp-test-admin] WITH PASSWORD = '{{PASSWORD_ADMIN}}', CHECK_POLICY = ON;
ALTER LOGIN [mcp-test-admin] DISABLE;
GO
