"""
SQL Script Provider for FastMCP

Parses .sql files from a directory and creates Tool objects that can be registered with MCP.
Each .sql file should have the format:
/*
Tool description (can be multi-line)

@param_name - parameter description
@another    - another parameter description
*/

DECLARE
    @param_name INT,
    @another    NVARCHAR(128);

SELECT ... WHERE col = @param_name AND another = @another
"""

import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
from sqlsprovider import SQLSProvider


@dataclass
class SqlParam:
    """SQL parameter definition"""
    name: str  # without @
    sql_type: str
    description: str = ""


@dataclass
class SqlTool:
    """Parsed SQL tool"""
    name: str
    description: str
    params: list[SqlParam]
    query: str
    param_definitions: str  # for sp_executesql, e.g. "@id INT, @name NVARCHAR(128)"


class SQLScriptProvider:
    """Provider that loads SQL scripts as MCP tools"""

    def __init__(self, sql_tools_dir: str | Path):
        self.sql_tools_dir = Path(sql_tools_dir)
        if not self.sql_tools_dir.exists():
            raise ValueError(f"Directory not found: {self.sql_tools_dir}")

    def _parse_header_comment(self, content: str) -> tuple[str, dict[str, str], str]:
        """
        Parse the header comment from SQL file.
        Returns: (description, param_descriptions, remaining_content)
        """
        # Match /* ... */
        match = re.match(r'/\*\s*(.*?)\s*\*/', content, re.DOTALL)
        if not match:
            return "", {}, content

        comment_body = match.group(1)
        remaining = content[match.end():].strip()

        # Split into description and param docs
        lines = comment_body.strip().split('\n')
        description_lines = []
        param_descriptions = {}

        for line in lines:
            line = line.strip()
            # Check if it's a parameter description line
            param_match = re.match(r'@(\w+)\s*-\s*(.+)', line)
            if param_match:
                param_name = param_match.group(1)
                param_desc = param_match.group(2).strip()
                param_descriptions[param_name] = param_desc
            else:
                description_lines.append(line)

        description = '\n'.join(description_lines).strip()
        return description, param_descriptions, remaining

    def _parse_declare_block(self, content: str) -> tuple[list[SqlParam], str]:
        """
        Parse DECLARE block from SQL.
        Returns: (params, remaining_content)
        """
        # Match DECLARE ... ; (everything up to the semicolon after variable declarations)
        match = re.match(r'DECLARE\s+(.*?);', content, re.DOTALL | re.IGNORECASE)
        if not match:
            return [], content

        declare_body = match.group(1)
        remaining = content[match.end():].strip()

        params = []
        # Split by comma and parse each parameter
        param_decls = re.split(r',\s*(?=@)', declare_body)

        for decl in param_decls:
            decl = decl.strip()
            if not decl:
                continue

            # Match @param_name TYPE
            param_match = re.match(r'@(\w+)\s+(\w+(?:\s*\(\s*\d+\s*\))?)', decl, re.IGNORECASE)
            if param_match:
                param_name = param_match.group(1)
                sql_type = param_match.group(2).strip()
                params.append(SqlParam(name=param_name, sql_type=sql_type))

        return params, remaining

    def _parse_sql_file(self, file_path: Path) -> SqlTool:
        """Parse a single SQL file into a SqlTool"""
        content = file_path.read_text(encoding="utf-8")

        # Parse header comment
        description, param_descriptions, content = self._parse_header_comment(content)

        # Parse DECLARE block
        params, query = self._parse_declare_block(content)

        # Update param descriptions
        for param in params:
            if param.name in param_descriptions:
                param.description = param_descriptions[param.name]

        # Build param_definitions string for sp_executesql
        param_definitions = ", ".join([f"@{p.name} {p.sql_type}" for p in params])

        # Tool name from filename (without .sql extension)
        tool_name = file_path.stem

        return SqlTool(
            name=tool_name,
            description=description or f"Execute {tool_name}",
            params=params,
            query=query.strip(),
            param_definitions=param_definitions,
        )

    def _build_param_mapping(self, params: list[SqlParam]) -> str:
        """
        Build parameter mapping for sp_executesql.
        Maps external params @_p_name to internal params @name.
        Returns: string like "@id = @_p_id, @name = @_p_name"
        """
        if not params:
            return ""
        return ", ".join([f"@{p.name} = @_p_{p.name}" for p in params])

    def _wrap_query_with_sp_executesql(self, query: str, param_definitions: str, param_mapping: str) -> str:
        """
        Wrap the query with sp_executesql for parameterized execution.
        """
        if not param_definitions:
            # No parameters, return query as-is
            return query

        # Escape single quotes in query
        query_escaped = query.replace("'", "''")

        sql = f"EXEC sp_executesql N'{query_escaped}'"
        if param_definitions:
            sql += f", N'{param_definitions}'"
        if param_mapping:
            sql += f", {param_mapping}"
        sql += ";"

        return sql

    def load_tools(self) -> list[SqlTool]:
        """Load all SQL tools from the directory"""
        tools = []
        for sql_file in self.sql_tools_dir.glob("*.sql"):
            try:
                tool = self._parse_sql_file(sql_file)
                tools.append(tool)
            except Exception as e:
                print(f"Warning: Failed to parse {sql_file.name}: {e}")
        return tools

    def register_tools(self, mcp: FastMCP, server: str, impersonate: str = "mcp-server"):
        """
        Register all SQL tools with the MCP server.

        Args:
            mcp: FastMCP instance
            server: SQL Server instance name
            impersonate: SQL user to impersonate (default: "mcp-server")
        """
        tools = self.load_tools()

        for tool in tools:
            # Create the tool function
            def create_tool_func(sql_tool: SqlTool):
                """Closure to capture sql_tool"""

                def tool_func(database: str, **kwargs) -> str:
                    """
                    Execute SQL tool.

                    Args:
                        database: Target database name
                        **kwargs: Tool parameters
                    """
                    # Build parameter tuple with _p_ prefix
                    param_values = []
                    for param in sql_tool.params:
                        value = kwargs.get(param.name)
                        param_values.append(value)

                    # Wrap query with sp_executesql
                    param_mapping = self._build_param_mapping(sql_tool.params)
                    wrapped_query = self._wrap_query_with_sp_executesql(
                        sql_tool.query,
                        sql_tool.param_definitions,
                        param_mapping
                    )

                    # Execute via SQLSProvider
                    provider = SQLSProvider(server, database, impersonate)
                    return provider.execute_query(wrapped_query, tuple(param_values) if param_values else None)

                # Set function metadata
                tool_func.__name__ = sql_tool.name
                tool_func.__doc__ = sql_tool.description

                # Add parameter annotations
                annotations = {"database": str, "return": str}
                for param in sql_tool.params:
                    # Map SQL types to Python types
                    python_type = self._sql_type_to_python(param.sql_type)
                    annotations[param.name] = Optional[python_type]
                tool_func.__annotations__ = annotations

                return tool_func

            # Register the tool
            tool_func = create_tool_func(tool)
            mcp.tool()(tool_func)

    def _sql_type_to_python(self, sql_type: str) -> type:
        """Map SQL type to Python type"""
        sql_type_upper = sql_type.upper()

        if any(t in sql_type_upper for t in ['INT', 'BIGINT', 'SMALLINT', 'TINYINT']):
            return int
        elif any(t in sql_type_upper for t in ['DECIMAL', 'NUMERIC', 'FLOAT', 'REAL', 'MONEY']):
            return float
        elif any(t in sql_type_upper for t in ['BIT']):
            return bool
        else:
            return str
