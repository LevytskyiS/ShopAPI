from fetch import fetch_data
from queries import QUERY_2


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
