-- ============================================================
-- deploy-3-mcp-test-aux.sql
-- Creates all objects in mcp_test_aux.
-- Execute in the context of: mcp_test_aux
-- ============================================================

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
CREATE OR ALTER VIEW dbo.vw_StockSummary AS
SELECT w.WarehouseName, w.Region, ws.ProductID, ws.Quantity
FROM   dbo.WarehouseStock ws
JOIN   dbo.Warehouses     w ON w.WarehouseID = ws.WarehouseID;
GO

-- cross-database view: reads product names from mcp_test_main
CREATE OR ALTER VIEW dbo.vw_StockWithProductNames AS
SELECT w.WarehouseName, p.ProductName, ws.Quantity
FROM   dbo.WarehouseStock                ws
JOIN   dbo.Warehouses                    w ON w.WarehouseID = ws.WarehouseID
JOIN   [mcp_test_main].inventory.Products p ON p.ProductID   = ws.ProductID;
GO

-- ── functions ───────────────────────────────────────────────
CREATE OR ALTER FUNCTION dbo.fn_WarehouseTotalQty(@WarehouseID INT)
RETURNS INT
AS
BEGIN
    DECLARE @total INT;
    SELECT @total = SUM(Quantity) FROM dbo.WarehouseStock WHERE WarehouseID = @WarehouseID;
    RETURN ISNULL(@total, 0);
END
GO

-- ── procedures ──────────────────────────────────────────────
CREATE OR ALTER PROCEDURE dbo.usp_GetWarehouseInfo @WarehouseID INT
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
CREATE OR ALTER PROCEDURE dbo.usp_StockReport @WarehouseID INT
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
