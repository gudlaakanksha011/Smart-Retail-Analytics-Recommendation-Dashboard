import pandas as pd

# Load datasets
inventory = pd.read_csv("inventory_data.csv")
sales = pd.read_csv("sales_data.csv")

# Total quantity sold per product
sales_summary = sales.groupby("Product_Name")["Quantity_Sold"].sum().reset_index()

# Merge with inventory
df = pd.merge(inventory, sales_summary, on="Product_Name", how="left")

# Fill missing sales with 0
df["Quantity_Sold"] = df["Quantity_Sold"].fillna(0)

# Recommendation logic
def recommend(row):
    if row["Quantity_Sold"] > 200 and row["Stock_Quantity"] < 30:
        return "🔥 High Demand → Increase Stock"
    elif row["Quantity_Sold"] < 50 and row["Stock_Quantity"] > 50:
        return "⚠️ Low Demand → Reduce Stock"
    elif row["Stock_Quantity"] < 20:
        return "📦 Restock Needed"
    else:
        return "✅ Balanced"

df["Recommendation"] = df.apply(recommend, axis=1)

# Show recommendations
print("\n🎯 Product Recommendations:\n")
print(df[[
    "Product_Name",
    "Stock_Quantity",
    "Quantity_Sold",
    "Recommendation"
]])