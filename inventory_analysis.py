import pandas as pd
from datetime import datetime

# Load data
df = pd.read_csv("inventory_data.csv")

# Convert dates
df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"])

# Today's date
today = datetime.today()

# Days left
df["Days_Left"] = (df["Expiry_Date"] - today).dt.days

# Expiry status
def classify(days):
    if days <= 0:
        return "Expired"
    elif days <= 7:
        return "About to Expire, Add Offer ⚡"
    elif days <= 20:
        return "Priority Sale 🔔"
    else:
        return "Safe"

df["Expiry_Status"] = df["Days_Left"].apply(classify)

def action(status):
    if status == "Expired":
        return "Remove from inventory"
    elif status == "Add Offer ⚡":
        return "Apply discount (10-30%)"
    elif status == "Priority Sale 🔔":
        return "Promote product / increase visibility"
    else:
        return "No action needed"

df["Recommended_Action"] = df["Expiry_Status"].apply(action)

# Restock alert
df["Restock_Status"] = df["Stock_Quantity"].apply(
    lambda x: "Restock Needed" if x < 20 else "Sufficient"
)

# Show expiry alerts
print("\n🚨 Smart Expiry Alerts:\n")
print(df[df["Expiry_Status"] != "Safe"][[
    "Product_Name", "Days_Left", "Expiry_Status", "Recommended_Action"
]])

# Show restock alerts
print("\n📦 Restock Alerts:\n")
print(df[df["Restock_Status"] == "Restock Needed"][["Product_Name", "Stock_Quantity"]])