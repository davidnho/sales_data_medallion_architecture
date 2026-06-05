SELECT

    product_id,
    product_name,
    category,
    price

FROM {{ source('retail','bronze_products') }}
