import asyncio

import asyncpg
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values

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


async def get_sales_info():
    query = """
        SELECT 
            pc.code, 
            pv.product_variant_code, 
            pn2.code, 
            pn2.price, 
            pn.quantity, 
            pn.timestamp 
        FROM 
            products_nomenclaturestock pn
        INNER JOIN 
            products_nomenclature pn2 
            ON pn.nomenclature_id = pn2.id
        INNER JOIN 
            products_productvariant pv 
            ON pn2.product_variant_id = pv.id
        INNER JOIN 
            products_codenamemixin pc 
            ON pv.base_product_id = pc.id
    """

    data: pd.DataFrame = await fetch_data(query, connection_params)
    data = await process_dates(data)
    dates = data["timestamp"].unique()
    dates.sort()
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
    )
    return data, dates


async def calculate_all_time_sales(data: pd.DataFrame) -> str:
    data = data[["prod_left", "sold", "money"]]
    mp = data.groupby(["prod_left"]).sum()
    mp10m = mp.sort_values(by="money", ascending=False)
    mp10m = mp10m.loc[mp10m["sold"] > 0][["sold", "money"]]
    czk = round(mp10m["money"].sum(), 2)
    eur = round(float(czk) / 25.3, 2)
    pcs = mp10m["sold"].sum()
    return f"💴 CZK:\n{czk:,.2f}\n\n💶 EUR:\n{eur:,.2f}\n\n🧩 Sold pieces:\n{pcs:,}"


async def turnover_all_time(days=0):
    message_title = 'All time stats:\n\n'
    dataframes = []
    data, dates = await get_sales_info()


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
        message_title = "Stats for the last 7 days:\n\n"

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
        merged = merged.sort_values(by="sold", ascending=False)
        # mrt = merged

    mrt = pd.merge(
        dataframes[0], dataframes[-1], on="item", suffixes=("_left", "_right")
    )
    mrt["sold"] = mrt["quantity_left"] - mrt["quantity_right"]
    mrt["money"] = mrt["price_left"] * mrt["sold"]
    mrt = mrt.sort_values(by="sold", ascending=False)
    info: str = await calculate_all_time_sales(mrt)
    return message_title + info
