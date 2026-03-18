from typing import Optional
from db_provider import DbProvider


def _run(
    db_provider: DbProvider,
    with_: Optional[str] = None,
    select: Optional[str] = None,
    from_: str = "",
    where: Optional[str] = None,
    group_by: Optional[str] = None,
    having: Optional[str] = None,
    order_by: Optional[str] = None,
) -> str:
    parts = []
    if with_:
        parts.append(f"WITH {with_}")
    parts.append(f"SELECT {select or '*'} FROM {from_}")
    if where:
        parts.append(f"WHERE {where}")
    if group_by:
        parts.append(f"GROUP BY {group_by}")
    if having:
        parts.append(f"HAVING {having}")
    if order_by:
        parts.append(f"ORDER BY {order_by}")
    sql = "\n".join(parts)
    return db_provider.execute_query(sql)


def register(mcp):
    @mcp.tool()
    def selectQuery(
        server: str,
        database: str,
        from_: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        with_: Optional[str] = None,
        select: Optional[str] = None,
        where: Optional[str] = None,
        group_by: Optional[str] = None,
        having: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> str:
        db_provider = DbProvider(server, database, username, password)
        return _run(db_provider, with_=with_, select=select, from_=from_,
                    where=where, group_by=group_by, having=having, order_by=order_by)
