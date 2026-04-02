"""
Tests for SQLScriptProvider

Tests the SQL file parser and tool registration.
"""

import pytest
from pathlib import Path
from sqlscriptprovider import SQLScriptProvider, SqlTool, SqlParam


def test_parse_header_comment():
    """Test parsing header comment with description and parameters"""
    provider = SQLScriptProvider(Path("sql_tools"))

    content = """/*
Get table information

@table_name - Name of the table
@schema_name - Name of the schema
*/

DECLARE @table_name NVARCHAR(128);

SELECT * FROM sys.tables WHERE name = @table_name
"""

    description, param_descriptions, remaining = provider._parse_header_comment(content)

    assert "Get table information" in description
    assert "table_name" in param_descriptions
    assert param_descriptions["table_name"] == "Name of the table"
    assert "schema_name" in param_descriptions
    assert param_descriptions["schema_name"] == "Name of the schema"
    assert "DECLARE" in remaining


def test_parse_declare_block():
    """Test parsing DECLARE block with parameters"""
    provider = SQLScriptProvider(Path("sql_tools"))

    content = """DECLARE
    @id INT,
    @name NVARCHAR(128),
    @price DECIMAL(10, 2);

SELECT * FROM products"""

    params, remaining = provider._parse_declare_block(content)

    assert len(params) == 3
    assert params[0].name == "id"
    assert params[0].sql_type == "INT"
    assert params[1].name == "name"
    assert params[1].sql_type == "NVARCHAR(128)"
    assert params[2].name == "price"
    assert "SELECT * FROM products" in remaining


def test_parse_sql_file():
    """Test parsing a complete SQL file"""
    # Create a temporary SQL file for testing
    test_dir = Path("/tmp/test_sql_tools")
    test_dir.mkdir(exist_ok=True)

    test_file = test_dir / "test_tool.sql"
    test_file.write_text("""/*
Get product by ID

@product_id - Product identifier
*/

DECLARE
    @product_id INT;

SELECT * FROM products WHERE id = @product_id
""")

    provider = SQLScriptProvider(test_dir)
    tool = provider._parse_sql_file(test_file)

    assert tool.name == "test_tool"
    assert "Get product by ID" in tool.description
    assert len(tool.params) == 1
    assert tool.params[0].name == "product_id"
    assert tool.params[0].description == "Product identifier"
    assert "SELECT * FROM products" in tool.query
    assert "@product_id INT" in tool.param_definitions

    # Cleanup
    test_file.unlink()
    test_dir.rmdir()


def test_build_param_mapping():
    """Test building parameter mapping for sp_executesql"""
    provider = SQLScriptProvider(Path("sql_tools"))

    params = [
        SqlParam("id", "INT"),
        SqlParam("name", "NVARCHAR(128)"),
    ]

    mapping = provider._build_param_mapping(params)

    assert "@id = @_p_id" in mapping
    assert "@name = @_p_name" in mapping


def test_wrap_query_with_sp_executesql():
    """Test wrapping query with sp_executesql"""
    provider = SQLScriptProvider(Path("sql_tools"))

    query = "SELECT * FROM products WHERE id = @id"
    param_definitions = "@id INT"
    param_mapping = "@id = @_p_id"

    wrapped = provider._wrap_query_with_sp_executesql(query, param_definitions, param_mapping)

    assert "EXEC sp_executesql" in wrapped
    assert "SELECT * FROM products WHERE id = @id" in wrapped
    assert "@id INT" in wrapped
    assert "@id = @_p_id" in wrapped


def test_sql_type_to_python():
    """Test SQL type to Python type mapping"""
    provider = SQLScriptProvider(Path("sql_tools"))

    assert provider._sql_type_to_python("INT") == int
    assert provider._sql_type_to_python("BIGINT") == int
    assert provider._sql_type_to_python("DECIMAL(10,2)") == float
    assert provider._sql_type_to_python("NVARCHAR(128)") == str
    assert provider._sql_type_to_python("BIT") == bool


def test_load_tools_from_directory():
    """Test loading all SQL tools from directory"""
    sql_tools_dir = Path(__file__).parent.parent / "sql_tools"

    if not sql_tools_dir.exists():
        pytest.skip("sql_tools directory not found")

    provider = SQLScriptProvider(sql_tools_dir)
    tools = provider.load_tools()

    assert len(tools) > 0

    # Check that we have the expected tools
    tool_names = [tool.name for tool in tools]
    assert "getIndexUsage" in tool_names or "getDatabasePermission" in tool_names


def test_parse_no_params():
    """Test parsing a SQL file with no parameters"""
    test_dir = Path("/tmp/test_sql_tools_no_params")
    test_dir.mkdir(exist_ok=True)

    test_file = test_dir / "no_params.sql"
    test_file.write_text("""/*
Get all wait stats
*/

DECLARE
    @dummy INT;

SELECT * FROM sys.dm_os_wait_stats
""")

    provider = SQLScriptProvider(test_dir)
    tool = provider._parse_sql_file(test_file)

    assert tool.name == "no_params"
    assert len(tool.params) == 1  # @dummy
    assert "SELECT * FROM sys.dm_os_wait_stats" in tool.query

    # Cleanup
    test_file.unlink()
    test_dir.rmdir()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
