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

# ENGINE = create_engine(
#     f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

connection_params = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT,
}


async def clean_date(date):
    date = str(date).split(".")[0]
    date = date.split("+")[0]
    return date


async def process_row(date):
    return await clean_date(date)


async def process_dates(data: pd.DataFrame):
    tasks = [process_row(date) for date in data["timestamp"]]
    data["timestamp"] = await asyncio.gather(*tasks)
    return data


async def fetch_data(query: str, connection_params: dict):
    conn = await asyncpg.connect(**connection_params)
    result = await conn.fetch(query)
    await conn.close()

    df = pd.DataFrame(
        result,
        columns=["prod", "pvcode", "item", "price", "quantity", "timestamp"],
    )
    # df = pd.DataFrame(result, columns=[column.name for column in result[0].keys()])
    return df


async def get_sales_info(query: str):
    data: pd.DataFrame = await fetch_data(query, connection_params)
    return data


async def calculate_all_time_sales(pcs: int, turnover: int) -> str:
    eur_turnover = round(float(turnover) / 25.2, 2)
    return f"💴 CZK:\n{turnover:,.2f}\n\n💶 EUR:\n{eur_turnover:,.2f}\n\n🧩 Sold pieces:\n{pcs:,}"


async def turnover_all_time(days=0):
    sold_pieces = 0
    czk_turnover = 0
    emoji = "📊 "
    message_title = "All time stats:\n\n"
    dataframes = []

    data = await get_sales_info(QUERY_1)
    data = await process_dates(data)
    dates = data["timestamp"].unique()
    dates.sort()
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
    )

    for d in dates:
        dataframes_d = data.loc[data["timestamp"] == d]

        if len(dataframes) < 1:
            dataframes.append(dataframes_d)
            continue

        elif len(dataframes) >= 1:
            dataframesd = dataframes[-1]["timestamp"].unique()[0]
            td = pd.to_datetime(d) - dataframesd

            if td <= pd.Timedelta(minutes=5):
                dataframes[-1] = pd.concat(
                    [dataframes_d, dataframes[-1]],
                    axis=0,
                )
            else:
                dataframes.append(dataframes_d)

    if days == 1:
        dataframes = dataframes[-2:]
        message_title = "Today's stats:\n\n"

    if days == 7:
        dataframes = dataframes[-7:]
        message_title = "Stats for the last 7 days:\n\n"

    if days == 15:
        dataframes = dataframes[-15:]
        message_title = "Stats for the last 15 days:\n\n"

    for i in range(1, len(dataframes)):
        current_element = dataframes[i]
        prev_element = dataframes[i - 1]
        merged = pd.merge(
            prev_element,
            current_element,
            on="item",
            suffixes=("_left", "_right"),
        )
        merged["sold"] = merged["quantity_left"] - merged["quantity_right"]
        merged["czk"] = merged["sold"] * merged["price_left"]
        merged = merged.sort_values(by="sold", ascending=False)

        soldq = merged.loc[merged["sold"] > 0]

        sq = soldq["sold"].sum()
        sold_pieces += sq
        czk = soldq["czk"].sum()
        czk_turnover += czk

    info: str = await calculate_all_time_sales(sold_pieces, czk_turnover)
    return emoji + message_title + info
