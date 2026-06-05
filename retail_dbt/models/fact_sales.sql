SELECT

    s.sale_id,
    s.sale_date,

    c.customer_id,
    c.customer_name,

    p.product_id,
    p.product_name,

    s.quantity,

    p.price,

    s.quantity * p.price AS sales_amount

FROM {{ ref('stg_sales') }} s

JOIN {{ ref('stg_customers') }} c
ON s.customer_id = c.customer_id

JOIN {{ ref('stg_products') }} p
ON s.product_id = p.product_id
