-- Общая выручка
select sum(total_amount) from fact_sales; 

-- Выручка по категориям товаров
select dp.category, sum(fs.total_amount) as total_revenue
from fact_sales fs
join dim_products dp using(product_id)
group by dp.category 
order by total_revenue desc;

-- Топ-5 самых продаваемых товаров по количеству
select dp.product_name, sum(fs.quantity) total_quantity
from dim_products dp 
join fact_sales fs using(product_id)
group by dp.product_name 
order by total_quantity desc
limit 5;

-- Выручка по городам
select dl.city, sum(fs.total_amount) as total_revenue 
from dim_locations dl
join dim_customers dc using(location_id)
join fact_sales fs using(customer_id)
group by dl.city 
order by total_revenue desc;

-- Лучший клиент (по сумме покупок)
select dc.customer_id, sum(fs.total_amount) as total_sum 
from dim_customers dc 
join fact_sales fs using(customer_id)
group by dc.customer_id 
order by total_sum desc 
limit 1;

