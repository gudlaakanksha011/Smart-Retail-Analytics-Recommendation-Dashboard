import pandas as pd

# Load sales data
df = pd.read_csv("sales_data.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Extract month
df["Month"] = df["Date"].dt.to_period("M")

# 📊 Monthly revenue
monthly_sales = df.groupby("Month")["Revenue"].sum()

print("\n📊 Monthly Revenue:\n")
print(monthly_sales)

# 🏆 Top-selling product each month
top_products = df.groupby(["Month", "Product_Name"])["Quantity_Sold"].sum().reset_index()

top_products = top_products.sort_values(
    ["Month", "Quantity_Sold"], ascending=[True, False]
)

top_per_month = top_products.groupby("Month").first()

print("\n🏆 Top Product Each Month:\n")
print(top_per_month)