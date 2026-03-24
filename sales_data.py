import pandas as pd
import random
from datetime import datetime

products = ["Milk", "Bread", "Cheese", "Yogurt", "Butter", "Eggs", "Juice", "Paneer"]

price_map = {
    "Milk": 30, "Bread": 25, "Cheese": 120, "Yogurt": 40,
    "Butter": 60, "Eggs": 6, "Juice": 80, "Paneer": 90
}

data = []

for i in range(300):
    product = random.choice(products)
    quantity = random.randint(1, 10)
    price = price_map[product]

    date = datetime(2025, random.randint(1, 12), random.randint(1, 28))

    data.append([
        date.strftime("%Y-%m-%d"),
        product,
        quantity,
        quantity * price
    ])

df = pd.DataFrame(data, columns=["Date", "Product_Name", "Quantity_Sold", "Revenue"])

df.to_csv("sales_data.csv", index=False)

print("✅ Sales dataset created!")