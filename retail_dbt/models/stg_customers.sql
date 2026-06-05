SELECT

    customer_id,
    customer_name,
    city,
    country

FROM {{ source('retail','bronze_customers') }}
