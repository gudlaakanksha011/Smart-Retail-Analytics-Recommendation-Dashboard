import pandas as pd
import streamlit as st
from datetime import datetime
import random

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Retail Dashboard", layout="wide")

st.markdown("## 🛍️ Smart Retail Analytics Dashboard")
st.markdown("---")

# ------------------ LOAD DATA ------------------
inventory = pd.read_csv("inventory_data.csv")
sales = pd.read_csv("sales_data.csv")

# ------------------ DATE PROCESSING ------------------
inventory["Expiry_Date"] = pd.to_datetime(inventory["Expiry_Date"])
sales["Date"] = pd.to_datetime(sales["Date"])

today = datetime.today()
inventory["Days_Left"] = (inventory["Expiry_Date"] - today).dt.days

# ------------------ EXPIRY LOGIC ------------------
def classify(days):
    if days <= 0:
        return "Expired"
    elif days <= 7:
        return "Add Offer ⚡"
    elif days <= 20:
        return "Priority Sale 🔔"
    else:
        return "Safe"

inventory["Expiry_Status"] = inventory["Days_Left"].apply(classify)

# ------------------ RESTOCK ------------------
inventory["Restock_Status"] = inventory["Stock_Quantity"].apply(
    lambda x: "Restock Needed" if x < 20 else "Sufficient"
)

# ------------------ DISCOUNT ------------------
def discount_suggestion(status):
    if status == "Add Offer ⚡":
        return "20% Discount"
    elif status == "Priority Sale 🔔":
        return "10% Discount"
    else:
        return "No Discount"

inventory["Discount"] = inventory["Expiry_Status"].apply(discount_suggestion)

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("🔍 Filters")
category = st.sidebar.selectbox("Select Category", inventory["Category"].unique())
filtered_inventory = inventory[inventory["Category"] == category]

# ------------------ KPI ------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{int(sales['Revenue'].sum())}")
col2.metric("Total Products", inventory["Product_Name"].nunique())
col3.metric("Low Stock Items", len(inventory[inventory["Stock_Quantity"] < 20]))

# ------------------ PROFIT CALCULATION ------------------
sales_with_price = pd.merge(
    sales,
    inventory[["Product_Name", "Price"]],
    on="Product_Name",
    how="left"
)

# Random margin per row
sales_with_price["Margin"] = [
    random.uniform(1.2, 1.5) for _ in range(len(sales_with_price))
]

sales_with_price["Selling_Price"] = (
    sales_with_price["Price"] * sales_with_price["Margin"]
)

sales_with_price["Revenue"] = (
    sales_with_price["Selling_Price"] * sales_with_price["Quantity_Sold"]
)

sales_with_price["Cost"] = (
    sales_with_price["Price"] * sales_with_price["Quantity_Sold"]
)

total_cost = sales_with_price["Cost"].sum()
total_revenue = sales_with_price["Revenue"].sum()
profit = total_revenue - total_cost

profit_margin = (profit / total_revenue) * 100 if total_revenue != 0 else 0

# ------------------ PROFIT DISPLAY ------------------
st.subheader("💰 Profit Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"₹{int(total_revenue)}")
col2.metric("Cost", f"₹{int(total_cost)}")
col3.metric("Profit", f"₹{int(profit)}")

st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# ------------------ TABS ------------------
tab1, tab2, tab3 = st.tabs(["📦 Inventory", "📊 Sales", "🎯 Recommendations"])

# ================== TAB 1 ==================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Expiry Alerts")
        st.dataframe(filtered_inventory[filtered_inventory["Expiry_Status"] != "Safe"])

    with col2:
        st.subheader("📦 Restock Alerts")
        st.dataframe(filtered_inventory[filtered_inventory["Restock_Status"] == "Restock Needed"])

    st.subheader("🏷️ Discount Suggestions")
    st.dataframe(filtered_inventory[["Product_Name", "Expiry_Status", "Discount"]])

    st.subheader("⚠️ High Risk Products")
    risk_products = filtered_inventory[
        (filtered_inventory["Expiry_Status"] != "Safe") &
        (filtered_inventory["Stock_Quantity"] < 30)
    ]
    st.dataframe(risk_products)

# ================== TAB 2 ==================
with tab2:
    sales["Month"] = sales["Date"].dt.to_period("M")

    monthly_sales = sales.groupby("Month")["Revenue"].sum()

    st.subheader("📊 Monthly Revenue Trend")
    st.area_chart(monthly_sales)

    top_products = (
        sales.groupby("Product_Name")["Quantity_Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("🏆 Top Selling Products")
    st.bar_chart(top_products)

    selected_product = st.selectbox("Select Product", sales["Product_Name"].unique())
    product_data = sales[sales["Product_Name"] == selected_product]
    product_sales = product_data.groupby("Month")["Quantity_Sold"].sum()

    st.subheader(f"📈 Sales Trend for {selected_product}")
    st.line_chart(product_sales)

# ================== TAB 3 ==================
with tab3:
    sales_summary = sales.groupby("Product_Name")["Quantity_Sold"].sum().reset_index()

    df = pd.merge(inventory, sales_summary, on="Product_Name", how="left")
    df["Quantity_Sold"] = df["Quantity_Sold"].fillna(0)

    def recommend(row):
        if row["Quantity_Sold"] > 200 and row["Stock_Quantity"] < 30:
            return "🔥 Increase Stock"
        elif row["Quantity_Sold"] < 50 and row["Stock_Quantity"] > 50:
            return "⚠️ Reduce Stock"
        elif row["Stock_Quantity"] < 20:
            return "📦 Restock Needed"
        else:
            return "✅ Balanced"

    df["Recommendation"] = df.apply(recommend, axis=1)

    st.subheader("🎯 Smart Recommendations")
    st.dataframe(df[["Product_Name", "Stock_Quantity", "Quantity_Sold", "Recommendation"]])

# ------------------ PROFIT BY PRODUCT ------------------
product_profit = sales_with_price.groupby("Product_Name").agg({
    "Revenue": "sum",
    "Cost": "sum"
}).reset_index()

product_profit["Profit"] = product_profit["Revenue"] - product_profit["Cost"]

st.subheader("💰 Profit by Product")
st.dataframe(product_profit)

st.bar_chart(product_profit.set_index("Product_Name")["Profit"])

# ------------------ DOWNLOAD ------------------
st.download_button(
    label="📥 Download Inventory Report",
    data=inventory.to_csv(index=False),
    file_name="inventory_report.csv",
    mime="text/csv"
)