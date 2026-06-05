SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(sales_amount) AS revenue
FROM {{ ref('fact_sales') }}
GROUP BY 1
ORDER BY 1