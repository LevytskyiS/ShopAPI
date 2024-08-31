from fetch import fetch_data
from queries import QUERY_3


async def get_product_info(code: str) -> str:
    """Fetch product information from the database."""
    parameter = f"WHERE pn.code = '{code}';"
    query = f"{QUERY_3} {parameter}"
    result = await fetch_data(query)
    if not result:
        return
    product = result[0]
    return f"👇 Product infomation:\n\n\
🖊 Name: {product['product_name']}\n\
✅ Trademark: {product['trademark_name']}\n\
🔢 Code: {product['product_code']}\n\n\
📌 Subtitle: {product['product_subtitle']}\n\
👤 Gender: {product['gender_name']}\n\
🗄 Category: {product['category_name']}\n\
📗 Type: {product['product_type']}\n\
\n📝 Specification: {product['product_specification']}\
"
