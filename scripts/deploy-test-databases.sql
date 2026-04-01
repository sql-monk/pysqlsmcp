-- ============================================================
-- deploy-test-databases.sql
-- Creates two test databases (mcp_test_main, mcp_test_aux)
-- with users, roles, tables, views, procedures, functions,
-- synonyms, and cross-database references for MCP testing.
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- 1. DATABASES
-- ────────────────────────────────────────────────────────────
IF DB_ID('mcp_test_main') IS NULL CREATE DATABASE [mcp_test_main];
GO
IF DB_ID('mcp_test_aux') IS NULL CREATE DATABASE [mcp_test_aux];
GO

-- ────────────────────────────────────────────────────────────
-- 2. LOGINS (server level)
-- ────────────────────────────────────────────────────────────
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

-- ════════════════════════════════════════════════════════════
-- 3. mcp_test_main
-- ════════════════════════════════════════════════════════════
USE [mcp_test_main];
GO

-- ── schemas ─────────────────────────────────────────────────
IF SCHEMA_ID('sales') IS NULL EXEC('CREATE SCHEMA [sales]');
GO
IF SCHEMA_ID('inventory') IS NULL EXEC('CREATE SCHEMA [inventory]');
GO

-- ── tables ──────────────────────────────────────────────────
IF OBJECT_ID('dbo.Customers', 'U') IS NULL
CREATE TABLE dbo.Customers (
    CustomerID   INT IDENTITY(1,1) PRIMARY KEY,
    FullName     NVARCHAR(200)  NOT NULL,
    Email        NVARCHAR(200)  NULL,
    CreatedAt    DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

IF OBJECT_ID('sales.Orders', 'U') IS NULL
CREATE TABLE sales.Orders (
    OrderID      INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID   INT            NOT NULL REFERENCES dbo.Customers(CustomerID),
    OrderDate    DATE           NOT NULL DEFAULT CAST(SYSUTCDATETIME() AS DATE),
    TotalAmount  DECIMAL(18,2)  NOT NULL DEFAULT 0
);
GO

IF OBJECT_ID('sales.OrderItems', 'U') IS NULL
CREATE TABLE sales.OrderItems (
    ItemID       INT IDENTITY(1,1) PRIMARY KEY,
    OrderID      INT            NOT NULL REFERENCES sales.Orders(OrderID),
    ProductID    INT            NOT NULL,
    Quantity     INT            NOT NULL DEFAULT 1,
    UnitPrice    DECIMAL(18,2)  NOT NULL
);
GO

IF OBJECT_ID('inventory.Products', 'U') IS NULL
CREATE TABLE inventory.Products (
    ProductID    INT IDENTITY(1,1) PRIMARY KEY,
    ProductName  NVARCHAR(200)  NOT NULL,
    Category     NVARCHAR(100)  NULL,
    Price        DECIMAL(18,2)  NOT NULL DEFAULT 0,
    StockQty     INT            NOT NULL DEFAULT 0
);
GO

IF OBJECT_ID('dbo.AuditLog', 'U') IS NULL
CREATE TABLE dbo.AuditLog (
    LogID        INT IDENTITY(1,1) PRIMARY KEY,
    TableName    NVARCHAR(128)  NOT NULL,
    Operation    NVARCHAR(20)   NOT NULL,
    LoggedAt     DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
    Detail       NVARCHAR(MAX)  NULL
);
GO

-- ── seed data ───────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM inventory.Products)
BEGIN
    INSERT INTO inventory.Products (ProductName, Category, Price, StockQty) VALUES
        (N'Widget A', N'Widgets',   9.99, 100),
        (N'Widget B', N'Widgets',  14.50,  50),
        (N'Gadget X', N'Gadgets',  29.99,  30),
        (N'Gadget Y', N'Gadgets',  49.99,  10),
        (N'Thingamajig', N'Misc',   4.99, 200);
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Customers)
BEGIN
    INSERT INTO dbo.Customers (FullName, Email) VALUES
        (N'Alice Johnson',  N'alice@example.com'),
        (N'Bob Smith',      N'bob@example.com'),
        (N'Carol Williams', N'carol@example.com');

    INSERT INTO sales.Orders (CustomerID, TotalAmount) VALUES
        (1, 24.49), (2, 49.99), (1, 14.50);

    INSERT INTO sales.OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES
        (1, 1, 1,  9.99), (1, 2, 1, 14.50),
        (2, 4, 1, 49.99),
        (3, 2, 1, 14.50);
END
GO

-- ── views ───────────────────────────────────────────────────
IF OBJECT_ID('dbo.vw_CustomerOrders', 'V') IS NOT NULL DROP VIEW dbo.vw_CustomerOrders;
GO
CREATE VIEW dbo.vw_CustomerOrders AS
SELECT c.CustomerID, c.FullName, o.OrderID, o.OrderDate, o.TotalAmount
FROM   dbo.Customers c
JOIN   sales.Orders  o ON o.CustomerID = c.CustomerID;
GO

IF OBJECT_ID('sales.vw_OrderDetails', 'V') IS NOT NULL DROP VIEW sales.vw_OrderDetails;
GO
CREATE VIEW sales.vw_OrderDetails AS
SELECT oi.ItemID, oi.OrderID, p.ProductName, oi.Quantity, oi.UnitPrice,
       oi.Quantity * oi.UnitPrice AS LineTotal
FROM   sales.OrderItems    oi
JOIN   inventory.Products  p  ON p.ProductID = oi.ProductID;
GO

IF OBJECT_ID('inventory.vw_LowStock', 'V') IS NOT NULL DROP VIEW inventory.vw_LowStock;
GO
CREATE VIEW inventory.vw_LowStock AS
SELECT ProductID, ProductName, Category, StockQty
FROM   inventory.Products
WHERE  StockQty < 20;
GO

-- cross-database view: reads from mcp_test_aux
IF OBJECT_ID('dbo.vw_AuxWarehouse', 'V') IS NOT NULL DROP VIEW dbo.vw_AuxWarehouse;
GO
CREATE VIEW dbo.vw_AuxWarehouse AS
SELECT WarehouseID, WarehouseName, Region
FROM   [mcp_test_aux].dbo.Warehouses;
GO

-- ── functions ───────────────────────────────────────────────
IF OBJECT_ID('dbo.fn_OrderTotal', 'FN') IS NOT NULL DROP FUNCTION dbo.fn_OrderTotal;
GO
CREATE FUNCTION dbo.fn_OrderTotal(@OrderID INT)
RETURNS DECIMAL(18,2)
AS
BEGIN
    DECLARE @total DECIMAL(18,2);
    SELECT @total = SUM(Quantity * UnitPrice) FROM sales.OrderItems WHERE OrderID = @OrderID;
    RETURN ISNULL(@total, 0);
END
GO

IF OBJECT_ID('inventory.fn_StockValue', 'FN') IS NOT NULL DROP FUNCTION inventory.fn_StockValue;
GO
CREATE FUNCTION inventory.fn_StockValue(@ProductID INT)
RETURNS DECIMAL(18,2)
AS
BEGIN
    DECLARE @val DECIMAL(18,2);
    SELECT @val = Price * StockQty FROM inventory.Products WHERE ProductID = @ProductID;
    RETURN ISNULL(@val, 0);
END
GO

-- ── procedures ──────────────────────────────────────────────
IF OBJECT_ID('sales.usp_GetCustomerOrders', 'P') IS NOT NULL DROP PROCEDURE sales.usp_GetCustomerOrders;
GO
CREATE PROCEDURE sales.usp_GetCustomerOrders @CustomerID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT o.OrderID, o.OrderDate, o.TotalAmount,
           dbo.fn_OrderTotal(o.OrderID) AS CalculatedTotal
    FROM   sales.Orders o
    WHERE  o.CustomerID = @CustomerID
    ORDER BY o.OrderDate DESC;
END
GO

IF OBJECT_ID('dbo.usp_SearchProducts', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_SearchProducts;
GO
CREATE PROCEDURE dbo.usp_SearchProducts @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT ProductID, ProductName, Category, Price, StockQty
    FROM   inventory.Products
    WHERE  ProductName LIKE N'%' + @SearchTerm + N'%'
        OR Category    LIKE N'%' + @SearchTerm + N'%';
END
GO

-- cross-database procedure: reads from mcp_test_aux
IF OBJECT_ID('dbo.usp_ProductWarehouseStock', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_ProductWarehouseStock;
GO
CREATE PROCEDURE dbo.usp_ProductWarehouseStock @ProductID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT ws.WarehouseID, w.WarehouseName, ws.Quantity
    FROM   [mcp_test_aux].dbo.WarehouseStock ws
    JOIN   [mcp_test_aux].dbo.Warehouses     w  ON w.WarehouseID = ws.WarehouseID
    WHERE  ws.ProductID = @ProductID;
END
GO

-- ── synonyms ────────────────────────────────────────────────
IF OBJECT_ID('dbo.syn_Warehouses', 'SN') IS NOT NULL DROP SYNONYM dbo.syn_Warehouses;
GO
CREATE SYNONYM dbo.syn_Warehouses FOR [mcp_test_aux].dbo.Warehouses;
GO

IF OBJECT_ID('dbo.syn_WarehouseStock', 'SN') IS NOT NULL DROP SYNONYM dbo.syn_WarehouseStock;
GO
CREATE SYNONYM dbo.syn_WarehouseStock FOR [mcp_test_aux].dbo.WarehouseStock;
GO

IF OBJECT_ID('dbo.syn_AuxGetWarehouse', 'SN') IS NOT NULL DROP SYNONYM dbo.syn_AuxGetWarehouse;
GO
CREATE SYNONYM dbo.syn_AuxGetWarehouse FOR [mcp_test_aux].dbo.usp_GetWarehouseInfo;
GO

-- ── roles ───────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_reader' AND type = 'R')
    CREATE ROLE [role_reader];
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_writer' AND type = 'R')
    CREATE ROLE [role_writer];
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_admin' AND type = 'R')
    CREATE ROLE [role_admin];
GO

-- role_reader: SELECT on tables and views
GRANT SELECT ON dbo.Customers              TO [role_reader];
GRANT SELECT ON sales.Orders               TO [role_reader];
GRANT SELECT ON inventory.Products         TO [role_reader];
GRANT SELECT ON dbo.vw_CustomerOrders      TO [role_reader];
GRANT SELECT ON sales.vw_OrderDetails      TO [role_reader];
GRANT SELECT ON inventory.vw_LowStock      TO [role_reader];
GRANT EXECUTE ON dbo.fn_OrderTotal         TO [role_reader];
GO

-- role_writer: reader + INSERT/UPDATE + EXECUTE procs
GRANT SELECT ON dbo.Customers              TO [role_writer];
GRANT SELECT ON sales.Orders               TO [role_writer];
GRANT SELECT ON sales.OrderItems           TO [role_writer];
GRANT SELECT ON inventory.Products         TO [role_writer];
GRANT SELECT ON dbo.vw_CustomerOrders      TO [role_writer];
GRANT SELECT ON sales.vw_OrderDetails      TO [role_writer];
GRANT INSERT, UPDATE ON dbo.Customers      TO [role_writer];
GRANT INSERT, UPDATE ON sales.Orders       TO [role_writer];
GRANT INSERT, UPDATE ON sales.OrderItems   TO [role_writer];
GRANT EXECUTE ON sales.usp_GetCustomerOrders  TO [role_writer];
GRANT EXECUTE ON dbo.usp_SearchProducts       TO [role_writer];
GRANT EXECUTE ON dbo.fn_OrderTotal            TO [role_writer];
GRANT EXECUTE ON inventory.fn_StockValue      TO [role_writer];
GO

-- role_admin: writer + DELETE + cross-db + audit + VIEW DEFINITION
GRANT SELECT ON dbo.Customers              TO [role_admin];
GRANT SELECT ON sales.Orders               TO [role_admin];
GRANT SELECT ON sales.OrderItems           TO [role_admin];
GRANT SELECT ON inventory.Products         TO [role_admin];
GRANT SELECT ON dbo.AuditLog               TO [role_admin];
GRANT SELECT ON dbo.vw_CustomerOrders      TO [role_admin];
GRANT SELECT ON sales.vw_OrderDetails      TO [role_admin];
GRANT SELECT ON inventory.vw_LowStock      TO [role_admin];
GRANT SELECT ON dbo.vw_AuxWarehouse        TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON dbo.Customers     TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON sales.Orders      TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON sales.OrderItems  TO [role_admin];
GRANT INSERT, UPDATE ON inventory.Products        TO [role_admin];
GRANT INSERT ON dbo.AuditLog                      TO [role_admin];
GRANT EXECUTE ON sales.usp_GetCustomerOrders      TO [role_admin];
GRANT EXECUTE ON dbo.usp_SearchProducts           TO [role_admin];
GRANT EXECUTE ON dbo.usp_ProductWarehouseStock    TO [role_admin];
GRANT EXECUTE ON dbo.fn_OrderTotal                TO [role_admin];
GRANT EXECUTE ON inventory.fn_StockValue          TO [role_admin];
GRANT VIEW DEFINITION TO [role_admin];
GO

-- standard roles
ALTER ROLE [db_datareader] ADD MEMBER [role_reader];
GO

-- ── users ───────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-reader')
    CREATE USER [mcp-test-reader] FROM LOGIN [mcp-test-reader];
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-writer')
    CREATE USER [mcp-test-writer] FROM LOGIN [mcp-test-writer];
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-admin')
    CREATE USER [mcp-test-admin]  FROM LOGIN [mcp-test-admin];
GO

ALTER ROLE [role_reader] ADD MEMBER [mcp-test-reader];
ALTER ROLE [role_writer] ADD MEMBER [mcp-test-writer];
ALTER ROLE [role_admin]  ADD MEMBER [mcp-test-admin];
GO


-- ════════════════════════════════════════════════════════════
-- 4. mcp_test_aux
-- ════════════════════════════════════════════════════════════
USE [mcp_test_aux];
GO

-- ── tables ──────────────────────────────────────────────────
IF OBJECT_ID('dbo.Warehouses', 'U') IS NULL
CREATE TABLE dbo.Warehouses (
    WarehouseID   INT IDENTITY(1,1) PRIMARY KEY,
    WarehouseName NVARCHAR(200) NOT NULL,
    Region        NVARCHAR(100) NOT NULL
);
GO

IF OBJECT_ID('dbo.WarehouseStock', 'U') IS NULL
CREATE TABLE dbo.WarehouseStock (
    StockID      INT IDENTITY(1,1) PRIMARY KEY,
    WarehouseID  INT NOT NULL REFERENCES dbo.Warehouses(WarehouseID),
    ProductID    INT NOT NULL,
    Quantity     INT NOT NULL DEFAULT 0
);
GO

IF OBJECT_ID('dbo.Shipments', 'U') IS NULL
CREATE TABLE dbo.Shipments (
    ShipmentID    INT IDENTITY(1,1) PRIMARY KEY,
    WarehouseID   INT  NOT NULL REFERENCES dbo.Warehouses(WarehouseID),
    ShippedDate   DATE NOT NULL DEFAULT CAST(SYSUTCDATETIME() AS DATE),
    Destination   NVARCHAR(200) NOT NULL,
    ItemCount     INT  NOT NULL DEFAULT 0
);
GO

-- ── seed data ───────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM dbo.Warehouses)
BEGIN
    INSERT INTO dbo.Warehouses (WarehouseName, Region) VALUES
        (N'Central Hub',  N'East'),
        (N'West Depot',   N'West'),
        (N'North Store',  N'North');

    INSERT INTO dbo.WarehouseStock (WarehouseID, ProductID, Quantity) VALUES
        (1, 1, 40), (1, 2, 20), (1, 3, 10),
        (2, 1, 30), (2, 4,  5),
        (3, 5, 80), (3, 3, 15);

    INSERT INTO dbo.Shipments (WarehouseID, Destination, ItemCount) VALUES
        (1, N'Customer site A', 5),
        (2, N'Customer site B', 3),
        (1, N'Retail outlet',   12);
END
GO

-- ── views ───────────────────────────────────────────────────
IF OBJECT_ID('dbo.vw_StockSummary', 'V') IS NOT NULL DROP VIEW dbo.vw_StockSummary;
GO
CREATE VIEW dbo.vw_StockSummary AS
SELECT w.WarehouseName, w.Region, ws.ProductID, ws.Quantity
FROM   dbo.WarehouseStock ws
JOIN   dbo.Warehouses     w ON w.WarehouseID = ws.WarehouseID;
GO

-- cross-database view: reads product names from mcp_test_main
IF OBJECT_ID('dbo.vw_StockWithProductNames', 'V') IS NOT NULL DROP VIEW dbo.vw_StockWithProductNames;
GO
CREATE VIEW dbo.vw_StockWithProductNames AS
SELECT w.WarehouseName, p.ProductName, ws.Quantity
FROM   dbo.WarehouseStock                ws
JOIN   dbo.Warehouses                    w ON w.WarehouseID = ws.WarehouseID
JOIN   [mcp_test_main].inventory.Products p ON p.ProductID   = ws.ProductID;
GO

-- ── functions ───────────────────────────────────────────────
IF OBJECT_ID('dbo.fn_WarehouseTotalQty', 'FN') IS NOT NULL DROP FUNCTION dbo.fn_WarehouseTotalQty;
GO
CREATE FUNCTION dbo.fn_WarehouseTotalQty(@WarehouseID INT)
RETURNS INT
AS
BEGIN
    DECLARE @total INT;
    SELECT @total = SUM(Quantity) FROM dbo.WarehouseStock WHERE WarehouseID = @WarehouseID;
    RETURN ISNULL(@total, 0);
END
GO

-- ── procedures ──────────────────────────────────────────────
IF OBJECT_ID('dbo.usp_GetWarehouseInfo', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_GetWarehouseInfo;
GO
CREATE PROCEDURE dbo.usp_GetWarehouseInfo @WarehouseID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT w.WarehouseID, w.WarehouseName, w.Region,
           dbo.fn_WarehouseTotalQty(w.WarehouseID) AS TotalStock
    FROM   dbo.Warehouses w
    WHERE  w.WarehouseID = @WarehouseID;
END
GO

-- cross-database procedure: reads product info from mcp_test_main
IF OBJECT_ID('dbo.usp_StockReport', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_StockReport;
GO
CREATE PROCEDURE dbo.usp_StockReport @WarehouseID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT w.WarehouseName, p.ProductName, p.Category, ws.Quantity,
           p.Price * ws.Quantity AS StockValue
    FROM   dbo.WarehouseStock                ws
    JOIN   dbo.Warehouses                    w ON w.WarehouseID = ws.WarehouseID
    JOIN   [mcp_test_main].inventory.Products p ON p.ProductID   = ws.ProductID
    WHERE  ws.WarehouseID = @WarehouseID;
END
GO

-- ── synonyms ────────────────────────────────────────────────
IF OBJECT_ID('dbo.syn_Products', 'SN') IS NOT NULL DROP SYNONYM dbo.syn_Products;
GO
CREATE SYNONYM dbo.syn_Products FOR [mcp_test_main].inventory.Products;
GO

IF OBJECT_ID('dbo.syn_Customers', 'SN') IS NOT NULL DROP SYNONYM dbo.syn_Customers;
GO
CREATE SYNONYM dbo.syn_Customers FOR [mcp_test_main].dbo.Customers;
GO

-- ── roles ───────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_reader' AND type = 'R')
    CREATE ROLE [role_reader];
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_writer' AND type = 'R')
    CREATE ROLE [role_writer];
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'role_admin' AND type = 'R')
    CREATE ROLE [role_admin];
GO

-- role_reader: SELECT
GRANT SELECT ON dbo.Warehouses       TO [role_reader];
GRANT SELECT ON dbo.WarehouseStock   TO [role_reader];
GRANT SELECT ON dbo.vw_StockSummary  TO [role_reader];
GRANT EXECUTE ON dbo.fn_WarehouseTotalQty TO [role_reader];
GO

-- role_writer: reader + INSERT/UPDATE + procs
GRANT SELECT ON dbo.Warehouses       TO [role_writer];
GRANT SELECT ON dbo.WarehouseStock   TO [role_writer];
GRANT SELECT ON dbo.Shipments        TO [role_writer];
GRANT SELECT ON dbo.vw_StockSummary  TO [role_writer];
GRANT INSERT, UPDATE ON dbo.WarehouseStock TO [role_writer];
GRANT INSERT ON dbo.Shipments              TO [role_writer];
GRANT EXECUTE ON dbo.usp_GetWarehouseInfo  TO [role_writer];
GRANT EXECUTE ON dbo.fn_WarehouseTotalQty  TO [role_writer];
GO

-- role_admin: full + cross-db + VIEW DEFINITION
GRANT SELECT ON dbo.Warehouses       TO [role_admin];
GRANT SELECT ON dbo.WarehouseStock   TO [role_admin];
GRANT SELECT ON dbo.Shipments        TO [role_admin];
GRANT SELECT ON dbo.vw_StockSummary           TO [role_admin];
GRANT SELECT ON dbo.vw_StockWithProductNames  TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON dbo.Warehouses      TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON dbo.WarehouseStock   TO [role_admin];
GRANT INSERT, UPDATE, DELETE ON dbo.Shipments        TO [role_admin];
GRANT EXECUTE ON dbo.usp_GetWarehouseInfo  TO [role_admin];
GRANT EXECUTE ON dbo.usp_StockReport       TO [role_admin];
GRANT EXECUTE ON dbo.fn_WarehouseTotalQty  TO [role_admin];
GRANT VIEW DEFINITION TO [role_admin];
GO

-- standard roles
ALTER ROLE [db_datareader] ADD MEMBER [role_reader];
GO

-- ── users ───────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-reader')
    CREATE USER [mcp-test-reader] FROM LOGIN [mcp-test-reader];
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-writer')
    CREATE USER [mcp-test-writer] FROM LOGIN [mcp-test-writer];
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'mcp-test-admin')
    CREATE USER [mcp-test-admin]  FROM LOGIN [mcp-test-admin];
GO

ALTER ROLE [role_reader] ADD MEMBER [mcp-test-reader];
ALTER ROLE [role_writer] ADD MEMBER [mcp-test-writer];
ALTER ROLE [role_admin]  ADD MEMBER [mcp-test-admin];
GO

-- ════════════════════════════════════════════════════════════
-- 5. IMPERSONATE grants (run from master)
-- ════════════════════════════════════════════════════════════
-- The connecting Windows login needs IMPERSONATE on the test users.
-- Replace [YOURLOGIN] with the actual Windows login or run as sysadmin.
-- ════════════════════════════════════════════════════════════
