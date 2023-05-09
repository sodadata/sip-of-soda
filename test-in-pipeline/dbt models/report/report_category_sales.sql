-- This would potentially go into a reporting and visualization tool.

with category_sales as (
    select
        fpc.category_key,
        sum(fis.order_quantity) as category_sales_count,
        sum(fis.sales_amount) as category_sales_total
    from {{ source('adventureworks', 'fact_internet_sales') }} fis
        left join {{ ref('fact_product_category') }} fpc on fis.product_key = fpc.product_key
    group by fpc.category_key
    order by fpc.category_key
) select
    category_sales.category_key as category_key,
    dpc.english_product_category_name as category_name,
    category_sales.category_sales_count as sales_count,
    category_sales.category_sales_total as sales_total
from category_sales
    left join dim_product_category dpc on category_sales.category_key = dpc.product_category_key
