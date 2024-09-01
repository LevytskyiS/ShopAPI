from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from conf import URI_MONGO
from fetch import fetch_data
from queries import QUERY_2
from models import NomenclatureMongo


async def emoji_str(emoji: str, stock: str, item_number) -> str:
    return f"👕 Item: {item_number}\n{emoji} Stock: {stock}"


async def get_stock(item_number):
    emoji_found = "✅"
    emoji_not_found = "⭕️"

    if len(item_number) == 5:
        query_extension = (
            f"WHERE pv.product_variant_code = '{item_number}' ORDER BY pn.code;"
        )
    if len(item_number) == 7:
        query_extension = f"WHERE pn.code = '{item_number}' ORDER BY pn.code;"

    query = f"{QUERY_2} {query_extension}"
    result = await fetch_data(query)

    if not result:
        return

    if len(result) == 1:
        obj = result[0]
        stock = obj["quantity"]
        nomenclature = obj["code"]

        if stock > 0:
            return await emoji_str(emoji_found, stock, nomenclature)
        return await emoji_str(emoji_not_found, stock, nomenclature)

    if len(result) > 1:
        stock_info = ""

        for record in result:
            stock = record["quantity"]
            nomenclature = record["code"]

            if stock > 0:
                info = await emoji_str(emoji_found, stock, nomenclature)
                stock_info += f"{info}\n\n"
                continue

            info = await emoji_str(emoji_not_found, stock, nomenclature)
            stock_info += f"{info}\n\n"

        return stock_info


async def fetch_mongo_data(db_name: str, collection_name: str, param=None):
    client = AsyncIOMotorClient(URI_MONGO, server_api=ServerApi("1"))

    db = client[db_name]

    collection = db[collection_name]

    if collection_name == "nomenclature_mongo":
        filter_query = {"code": param}
        cursor = collection.find(filter_query)
        items = await cursor.to_list(length=None)
    else:
        return None

    return items


async def get_restock(db: str, item):
    data = await fetch_mongo_data(
        db_name="stock", collection_name="nomenclature_mongo", param=item
    )

    if not data:
        return

    if len(data) == 1:
        obj = data[0]
        return f"👕 {obj['code']}:\n\
🧩 {obj['quantity']}\n\n\
⭕️ No restock dates"

    sorted_data = sorted(data, key=lambda x: x["stock"])

    stock_info = ""
    for item in sorted_data:
        code = item["code"]
        quantity = item["quantity"]
        date = item["stock"].strftime("%d.%m.%Y")
        info = f"👕 {code}\n\
🧩 {quantity}\n\
📅 {date}\n\n"
        stock_info += info
    return stock_info
