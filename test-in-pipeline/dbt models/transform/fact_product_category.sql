with source_data as (

    select
        dpc.product_category_key as category_key,
        dpc.english_product_category_name as category_name,
        dps.product_subcategory_key as subcategory_key,
        dps.english_product_subcategory_name as subcategory_name,
        dim_product.product_key as product_key,
        dim_product.english_product_name as product_name
    from dim_product
        left join {{ source('adventureworks', 'dim_product_subcategory') }} dps on dim_product.product_subcategory_key = dps.product_subcategory_key
        left join {{ source('adventureworks', 'dim_product_category') }} dpc on dps.product_category_key = dpc.product_category_key

)

select *
    from source_data
order by category_key, subcategory_key, product_key
