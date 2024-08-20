QUERY_1 = """
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
