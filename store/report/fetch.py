import asyncpg

from conf import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


async def fetch_data(query: str) -> list:
    """Retieve data from the database using the provided query."""

    connection_params = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
        "host": DB_HOST,
        "port": DB_PORT,
    }
    conn = await asyncpg.connect(**connection_params)
    result = await conn.fetch(query)
    await conn.close()
    return result
