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

QUERY_2 = """
    SELECT 
        pv.product_variant_code, pn.code, pn.price, pn.quantity
    FROM 
        products_nomenclature pn
    INNER JOIN 
        products_productvariant pv 
        ON pn.product_variant_id = pv.id
"""

QUERY_3 = """
    SELECT 
        pn.name AS product_name,                
        pn.code AS product_code,                
        ps.specification AS product_specification, 
        pc_category.name AS category_name,      
        pg_gender.name AS gender_name,          
        pt.type AS product_type,                
        pst.subtitle AS product_subtitle,       
        ptr.trademark AS trademark_name         
    FROM 
        products_product pp
    JOIN 
        products_codenamemixin pn 
        ON pp.codenamemixin_ptr_id = pn.id
    JOIN 
        products_specification ps 
        ON pp.specification_id = ps.id
    JOIN 
        products_category pc 
        ON pp.product_category_id = pc.codenamemixin_ptr_id
    JOIN 
        products_codenamemixin pc_category 
        ON pc.codenamemixin_ptr_id = pc_category.id
    JOIN 
        products_gender pg 
        ON pp.product_gender_id = pg.codenamemixin_ptr_id
    JOIN 
        products_codenamemixin pg_gender 
        ON pg.codenamemixin_ptr_id = pg_gender.id
    JOIN 
        products_producttype pt 
        ON pp.type_id = pt.id
    JOIN 
        products_subtitle pst 
        ON pp.subtitle_id = pst.id
    JOIN 
        products_trademark ptr 
        ON pp.trademark_id = ptr.id
"""
