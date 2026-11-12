import random 
import csv
from datetime import date, timedelta  

filename = "raw_sales.csv"

cities = ['Минск', 'Могилев', 'Брест', 'Гродно', 'Гомель', 'Витебск']

products = [
    ["P001", "Ноутбук", "Электроника", 3500.00],
    ["P002", "Телефон", "Электроника", 2500.00],
    ["P003", "Планшет", "Электроника", 1500.00],
    ["P004", "Наушники", "Электроника", 700.00],
    ["P005", "Мышь", "Электроника", 150.00],
    ["P006", "Гордость и предубеждение", "Книги", 30.00],
    ["P007", "Преступление и наказание", "Книги", 20.00],
    ["P008", "Горе от ума", "Книги", 15.00],
    ["P009", "Братья Карамазовы", "Книги", 70.00],
    ["P010", "Белые ночи", "Книги", 40.00],
    ["P011", "Шкаф", "Мебель", 2000.00],
    ["P012", "Стол", "Мебель", 1100.00],
    ["P013", "Кровать", "Мебель", 2100.00],
    ["P014", "Стул", "Мебель", 500.00],
    ["P015", "Кресло", "Мебель", 350.00],
    ["P016", "Мармелад", "Еда", 5.00],
    ["P017", "Мороженое", "Еда", 20.00],
    ["P018", "Бекон", "Еда", 9.00],
    ["P019", "Сыр", "Еда", 4.50],
    ["P020", "Яблоко", "Еда", 3.40],
]

start_day = date(2025, 1, 1)
end_day = date(2026, 12, 31)
days_available = end_day - start_day

all_data = []

for i in range(1, 1001):
    data = dict()
    # Генерация order_id
    data["order_id"] = i

    # Генерация order_date
    random_day_amount = random.randint(0, days_available.days)
    data["order_date"] = start_day + timedelta(days=random_day_amount)

    # Генерация product_id
    random_product = random.randint(0, len(products) - 1)
    data["product_id"] = products[random_product][0]

    # Генерация product_name
    data["product_name"] = products[random_product][1]

    # Генерация category
    data["category"] = products[random_product][2]

    # Генерация customer_id
    data["customer_id"] = random.randint(1, 200)

    # Генерация city 
    if not random.random() <= 0.1:
        data["city"] = random.choice(cities)

    # Генерация quantity
    if not random.random() <= 0.05:
        data["quantity"] = random.randint(1, 5)

    # Генерация price
    if random.random() <= 0.05:
        data["price"] = products[random_product][3] * -1
    else:
        data["price"] = products[random_product][3]

    all_data.append(data)

for _ in range(50):
    all_data.append(random.choice(all_data))

# Запись в файл
with open(filename, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["order_id", "order_date", "product_id", "product_name", "category", "customer_id", "city", "quantity", "price"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

