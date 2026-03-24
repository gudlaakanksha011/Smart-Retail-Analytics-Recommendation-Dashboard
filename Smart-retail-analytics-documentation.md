# 🛍️ Smart Retail Analytics Dashboard – Project Documentation

---

## 📌 Project Overview

This project is an end-to-end retail analytics system designed to help businesses:

* Track product expiry
* Manage inventory
* Analyze sales performance
* Calculate profit
* Generate product recommendations

---

## 🛠️ Tech Stack

Python • Pandas • Streamlit • Matplotlib • Git

---

# 🚀 STEP 0: Project Setup (Git + Folder Setup)

### 📁 Create Project Folder

```bash id="1p5d7h"
mkdir Smart-Retail-Analytics-Dashboard
cd Smart-Retail-Analytics-Dashboard
```

---

### 🔧 Initialize Git

```bash id="q7d2m1"
git init
```

---

### 📄 Create initial files

```bash id="1hr3cs"
touch app.py generate_inventory.py generate_sales.py sales_analysis.py README.md
```

---

### 📌 Add files to Git

```bash id="u3n8s2"
git add .
git commit -m "Initial project setup"
```

---

## 🚀 STEP 1: Install Dependencies

```bash id="o9k2x7"
pip install pandas streamlit matplotlib
```

---

## 📊 STEP 2: Generate Inventory Dataset

### File: `generate_data.py`

```python id="invcode"
# (same as your existing code)
```

### ▶️ Run

```bash id="runinv"
python generate_data.py
```

### ✅ Output

```
✅ Inventory dataset created!
```

---

## 📊 STEP 3: Generate Sales Dataset

### File: `sales_data.py`

```python id="salescode"
# (same as your existing code)
```

### ▶️ Run

```bash id="runsales"
python sales_data.py
```

---

## 📊 STEP 4: Sales Analysis

### ▶️ Run

```bash id="runsalesanalysis"
python sales_analysis.py
```

---

## 📦 STEP 5: Expiry Logic

```python id="expirylogic"
def classify(days):
    if days <= 0:
        return "Expired"
    elif days <= 7:
        return "Add Offer"
    elif days <= 20:
        return "Priority Sale"
    else:
        return "Safe"
```

---

## 💰 STEP 6: Profit Calculation

```python id="profitlogic"
sales["Cost"] = sales["Price"] * sales["Quantity_Sold"]
sales["Selling_Price"] = sales["Price"] * 1.3
sales["Revenue"] = sales["Selling_Price"] * sales["Quantity_Sold"]

profit = sales["Revenue"].sum() - sales["Cost"].sum()
```

---

## 🎯 STEP 7: Recommendation System

```python id="recomlogic"
def recommend(row):
    if row["Quantity_Sold"] > 200 and row["Stock_Quantity"] < 30:
        return "Increase Stock"
    elif row["Quantity_Sold"] < 50 and row["Stock_Quantity"] > 50:
        return "Reduce Stock"
    else:
        return "Balanced"
```

---

## 📈 STEP 8: Run Dashboard

```bash id="rundashboard"
streamlit run app.py
```

---

# 🚀 STEP 9: Git Workflow (Version Control)

### Add new changes

```bash id="gitadd"
git add .
```

---

### Commit changes

```bash id="gitcommit"
git commit -m "Added analytics and dashboard features"
```

---

### Connect to GitHub repo

```bash id="gitremote"
git remote add origin https://github.com/your-username/your-repo-name.git
```

---

### Push code

```bash id="gitpush"
git branch -M main
git push -u origin main
```

---

### Future updates

```bash id="gitupdate"
git add .
git commit -m "Updated feature"
git push
```

---

# 📊 Expected Output

* Inventory dataset (200 records)
* Sales dataset
* Sales trends & insights
* Expiry alerts
* Profit calculations
* Streamlit dashboard

---

# 💡 Business Impact

* Reduces product expiry loss
* Improves sales strategy
* Optimizes stock levels
* Enables data-driven decisions

---

# 🚀 Conclusion

This project demonstrates:

* End-to-end analytics pipeline
* Business-focused problem solving
* Dashboard development
* Git-based version control workflow
