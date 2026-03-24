import pandas as pd
import random
from datetime import datetime, timedelta

products = ["Milk", "Bread", "Cheese", "Yogurt", "Butter", "Eggs", "Juice", "Paneer"]
categories = ["Dairy", "Bakery", "Beverages", "Poultry"]

price_map = {
    "Milk": 30, "Bread": 25, "Cheese": 120, "Yogurt": 40,
    "Butter": 60, "Eggs": 6, "Juice": 80, "Paneer": 90
}

data = []

for i in range(1, 201):
    product = random.choice(products)
    category = random.choice(categories)
    stock = random.randint(10, 100)
    price = price_map[product]

    expiry = datetime.today() + timedelta(days=random.randint(-2, 15))

    data.append([
        100 + i,
        product,
        category,
        stock,
        expiry.strftime("%Y-%m-%d"),
        price
    ])

df = pd.DataFrame(data, columns=[
    "Product_ID", "Product_Name", "Category",
    "Stock_Quantity", "Expiry_Date", "Price"
])

df.to_csv("inventory_data.csv", index=False)

print("✅ Inventory dataset created!")