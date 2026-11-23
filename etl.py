import csv 
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

file_path = os.path.join(os.path.dirname(__file__), "raw_sales.csv")
with open(file_path, mode="r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)

print(data[0])
print(data[1])
print(data[2])
print(data[3])
print(data[4])
print(len(data))

def clean_data(raw_data):
    clean_rows = []
    seen = set()
    for d in data:
        if d["city"] == "" or d["quantity"] == "":
            continue 
        if float(d["price"]) < 0:
            continue
        unique_key = (d["order_id"], d["product_id"], d["order_date"])
        if unique_key in seen:
            continue
        seen.add(unique_key)
        quantity = int(d["quantity"])
        price = float(d["price"])
        clean_row = {
            "order_id": int(d["order_id"]),
            "order_date": d["order_date"],
            "product_id": d["product_id"],
            "product_name": d["product_name"],
            "category": d["category"],
            "customer_id": int(d["customer_id"]),
            "city": d["city"],
            "quantity": quantity,
            "price": price,
            "total_amount": round(quantity * price, 2)
        }

        clean_rows.append(clean_row)
    return clean_rows

clean = clean_data(data)
print(f"Было: {len(data)}, Осталось: {len(clean)}")
print(clean[0])

def locations_to_db(data):
    seen_locations = set(row["city"] for row in data)
    for location in seen_locations:
        cursor.execute("insert into dim_locations (city) values (%s);", (location, ))
    conn.commit()

def products_to_db(data):
    seen_products = set()
    for row in data:
        if row["product_id"] in seen_products:
            continue 
        seen_products.add(row["product_id"])
        cursor.execute("insert into dim_products (product_id, product_name, category, base_price) values (%s, %s, %s, %s);", (row["product_id"], row["product_name"], row["category"], row["price"]))
    conn.commit()

def customers_to_db(data):
    for row in data:
        cursor.execute("select location_id from dim_locations where city = %s;", (row["city"], ))
        location_id = cursor.fetchone()[0]
        cursor.execute("insert into dim_customers (customer_id, location_id) values (%s, %s) on conflict (customer_id) do nothing;", (row["customer_id"], location_id))
    conn.commit()

def fact_sales_to_db(data):
    for row in data:
        cursor.execute("insert into fact_sales (order_id, sale_date, product_id, customer_id, quantity, price, total_amount) values (%s, %s, %s, %s, %s, %s, %s);", (row["order_id"], row["order_date"], row["product_id"], row["customer_id"], row["quantity"], row["price"], row["total_amount"]))
    conn.commit()

locations_to_db(clean)
products_to_db(clean)
customers_to_db(clean)
fact_sales_to_db(clean)

cursor.close()
conn.close()