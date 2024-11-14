import pandas as pd
import random
from datetime import datetime, timedelta
import os

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

first_names = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fay", "George", "Hannah", "Ivan", "Jane"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Anderson"]
domains = ["gmail.com", "yahoo.com", "outlook.com"]
product_categories = ["Electronics", "Home Appliances", "Fashion", "Sports", "Beauty", "Books"]
product_names = [
    {"name": "Smartphone", "category": "Electronics"},
    {"name": "Laptop", "category": "Electronics"},
    {"name": "Blender", "category": "Home Appliances"},
    {"name": "Air Conditioner", "category": "Home Appliances"},
    {"name": "Jacket", "category": "Fashion"},
    {"name": "Running Shoes", "category": "Sports"},
    {"name": "Perfume", "category": "Beauty"},
    {"name": "Novel", "category": "Books"}
]
descriptions = ["High-quality", "Eco-friendly", "Portable", "Ergonomic", "Energy-saving", "Affordable", "Durable", "Stylish", "Innovative", "Compact"]

num_customers = 50
num_products = 20
num_landing_pages = 40
num_ab_tests = 20
num_results = 100

data_path = "./data/"

# Ensure the data directory exists
if not os.path.exists(data_path):
    os.makedirs(data_path)
    print("Created data directory")

customers = pd.DataFrame({
    "Customer_ID": range(1, num_customers + 1),
    "Name": [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_customers)]
})

customers['Email'] = [
    f"{first.lower()}.{last.lower()}@{random.choice(domains)}" 
    for first, last in zip(customers['Name'].str.split().str[0], customers['Name'].str.split().str[1])
]

products = pd.DataFrame({
    "product_ID": range(1, num_products + 1),
    "product_name": [f"{prod['name']} Model {random.randint(100,999)}" for prod in random.choices(product_names, k=num_products)],
    "category": [prod["category"] for prod in random.choices(product_names, k=num_products)],
    "description": [f"{random.choice(descriptions)} {prod['name']}" for prod in random.choices(product_names, k=num_products)],
    "logo_url": [f"http://example.com/{prod['name'].replace(' ', '_').lower()}_{i}.png" for i, prod in enumerate(random.choices(product_names, k=num_products))],
    "release_date": [random_date(datetime(2022, 1, 1), datetime(2023, 12, 31)) for _ in range(num_products)]
})

landing_pages = pd.DataFrame({
    "landing_page_id": range(1, num_landing_pages + 1),
    "variant_type": [random.choice(["A", "B"]) for _ in range(num_landing_pages)],
    "page_url": [f"http://example.com/landing_{i}" for i in range(1, num_landing_pages + 1)],
    "product_id": [random.choice(products["product_ID"]) for _ in range(num_landing_pages)]
})

ab_testing = pd.DataFrame({
    "Test_id": range(1, num_ab_tests + 1),
    "test_name": [f"Campaign_{i}" for i in range(1, num_ab_tests + 1)],
    "start_date": [random_date(datetime(2022, 1, 1), datetime(2023, 6, 30)) for _ in range(num_ab_tests)],
    "end_date": [random_date(datetime(2023, 7, 1), datetime(2023, 12, 31)) for _ in range(num_ab_tests)],
    "landing_page_id": [random.choice(landing_pages["landing_page_id"]) for _ in range(num_ab_tests)],
    "product_id": [random.choice(products["product_ID"]) for _ in range(num_ab_tests)]
})

results = pd.DataFrame({
    "results_id": range(1, num_results + 1),
    "click_through_rate": [round(random.uniform(0.01, 0.3), 2) for _ in range(num_results)],
    "conversion_rate": [round(random.uniform(0.01, 0.25), 2) for _ in range(num_results)],
    "bounce_rate": [round(random.uniform(0.2, 0.7), 2) for _ in range(num_results)],
    "test_id": [random.choice(ab_testing["Test_id"]) for _ in range(num_results)]
})

def save_csv(dataframe, filename):
    file_path = os.path.join(data_path, filename)
    print(f"Attempting to save file at: {file_path}")
    if not os.path.exists(file_path):
        dataframe.to_csv(file_path, index=False)
        print(f"Saved {filename}")
    else:
        print(f"{filename} already exists, skipping save.")


save_csv(customers, "customers.csv")
save_csv(products, "products.csv")
save_csv(landing_pages, "landing_pages.csv")
save_csv(ab_testing, "ab_testing.csv")
save_csv(results, "results.csv")



