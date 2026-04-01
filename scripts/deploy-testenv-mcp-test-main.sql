-- ============================================================
-- deploy-2-mcp-test-main.sql
-- Creates all objects in mcp_test_main.
-- Execute in the context of: mcp_test_main
-- ============================================================

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
CREATE OR ALTER VIEW dbo.vw_CustomerOrders AS
SELECT c.CustomerID, c.FullName, o.OrderID, o.OrderDate, o.TotalAmount
FROM   dbo.Customers c
JOIN   sales.Orders  o ON o.CustomerID = c.CustomerID;
GO

CREATE OR ALTER VIEW sales.vw_OrderDetails AS
SELECT oi.ItemID, oi.OrderID, p.ProductName, oi.Quantity, oi.UnitPrice,
       oi.Quantity * oi.UnitPrice AS LineTotal
FROM   sales.OrderItems    oi
JOIN   inventory.Products  p  ON p.ProductID = oi.ProductID;
GO

CREATE OR ALTER VIEW inventory.vw_LowStock AS
SELECT ProductID, ProductName, Category, StockQty
FROM   inventory.Products
WHERE  StockQty < 20;
GO

-- cross-database view: reads from mcp_test_aux
CREATE OR ALTER VIEW dbo.vw_AuxWarehouse AS
SELECT WarehouseID, WarehouseName, Region
FROM   [mcp_test_aux].dbo.Warehouses;
GO

-- ── functions ───────────────────────────────────────────────
CREATE OR ALTER FUNCTION dbo.fn_OrderTotal(@OrderID INT)
RETURNS DECIMAL(18,2)
AS
BEGIN
    DECLARE @total DECIMAL(18,2);
    SELECT @total = SUM(Quantity * UnitPrice) FROM sales.OrderItems WHERE OrderID = @OrderID;
    RETURN ISNULL(@total, 0);
END
GO

CREATE OR ALTER FUNCTION inventory.fn_StockValue(@ProductID INT)
RETURNS DECIMAL(18,2)
AS
BEGIN
    DECLARE @val DECIMAL(18,2);
    SELECT @val = Price * StockQty FROM inventory.Products WHERE ProductID = @ProductID;
    RETURN ISNULL(@val, 0);
END
GO

-- ── procedures ──────────────────────────────────────────────
CREATE OR ALTER PROCEDURE sales.usp_GetCustomerOrders @CustomerID INT
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

CREATE OR ALTER PROCEDURE dbo.usp_SearchProducts @SearchTerm NVARCHAR(100)
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
CREATE OR ALTER PROCEDURE dbo.usp_ProductWarehouseStock @ProductID INT
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
