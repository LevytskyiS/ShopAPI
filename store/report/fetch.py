import asyncio

import asyncpg
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values

from queries import QUERY_1

env_vars = dotenv_values(".env")
DB_HOST = env_vars.get("HOST")
DB_PORT = env_vars.get("PORT")
DB_NAME = env_vars.get("NAME")
DB_USER = env_vars.get("USER")
DB_PASSWORD = env_vars.get("PASSWORD")


async def fetch_data(query: str):
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
