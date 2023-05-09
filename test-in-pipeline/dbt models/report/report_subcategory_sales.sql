-- This would potentially go into a reporting and visualization tool.

with subcategory_sales as (
    select
        fpc.category_key,
        fpc.subcategory_key,
        sum(fis.order_quantity) as subcategory_sales_count,
        sum(fis.sales_amount) as subcategory_sales_total
    from {{ source('adventureworks', 'fact_internet_sales') }} fis
        left join {{ ref('fact_product_category') }} fpc on fis.product_key = fpc.product_key
    group by fpc.subcategory_key, fpc.category_key
    order by fpc.subcategory_key
) select
    subcategory_sales.category_key as category_key,
    subcategory_sales.subcategory_key as subcategory_key,
    dps.english_product_subcategory_name as subcategory_name,
    subcategory_sales.subcategory_sales_count as sales_count,
    subcategory_sales.subcategory_sales_total as sales_total
from subcategory_sales
    left join dim_product_subcategory dps on subcategory_sales.subcategory_key = dps.product_subcategory_key
