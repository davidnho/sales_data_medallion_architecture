SELECT

    sale_id,
    customer_id,
    product_id,
    quantity,
    CAST(sale_date AS DATE) sale_date

FROM {{ source('retail','bronze_sales') }}
