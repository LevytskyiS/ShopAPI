async def validate_nomenclature_stock(item: str):
    """Validate the nomenclature of an item."""
    if len(item) != 5 and len(item) != 7:
        return False, "❌ Nomenclature must be 5 or 7 signs long."

    else:
        return True, ""


async def validate_nomenclature_restock(item: str):
    """Validate the nomenclature of an item."""
    if len(item) != 7:
        return False, "❌ Nomenclature must be 7 signs long."

    else:
        return True, ""
