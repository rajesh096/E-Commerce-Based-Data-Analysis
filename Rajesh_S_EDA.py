# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from tabulate import tabulate

# Set Seaborn style for modern, polished plots
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# Load datasets
customers = pd.read_csv("Customers.csv")
products = pd.read_csv("Products.csv")
transactions = pd.read_csv("Transactions.csv")

# ---- INSIGHT 1: Regional Analysis ---- #
# Merge customers with transactions to include region
merged_data = pd.merge(transactions, customers, on="CustomerID", how="inner")

# Group by region and calculate transactions and sales
region_summary = (
    merged_data.groupby("Region")
    .agg(TotalTransactions=("TransactionID", "count"), TotalSales=("TotalValue", "sum"))
    .reset_index()
)

# Print structured regional summary
print("\n" + "="*50)
print(f"{'REGIONAL TRANSACTION SUMMARY':^50}")
print("="*50)
print(tabulate(region_summary, headers='keys', tablefmt='pretty', showindex=False))

# Visualization
plt.figure(figsize=(14, 8))
sns.barplot(data=region_summary, x="Region", y="TotalSales", palette="coolwarm", hue=None, edgecolor="black")
plt.title("Regional Sales Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Region", fontsize=14)
plt.ylabel("Total Sales (in USD)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ---- INSIGHT 2: Monthly Sales Trends ---- #
# Convert TransactionDate to datetime
transactions["TransactionDate"] = pd.to_datetime(transactions["TransactionDate"])

# Extract month from TransactionDate
transactions["Month"] = transactions["TransactionDate"].dt.month

# Group by ProductID and Month to get monthly sales trends
product_month_summary = (
    transactions.groupby(["ProductID", "Month"])
    .agg(TotalSales=("TotalValue", "sum"), TotalQuantity=("Quantity", "sum"))
    .reset_index()
)

# Print structured monthly sales summary
print("\n" + "="*50)
print(f"{'PRODUCT SALES BY MONTH':^50}")
print("="*50)
print(tabulate(product_month_summary, headers='keys', tablefmt='pretty', showindex=False))

# Visualization for a specific product
plt.figure(figsize=(14, 8))
product_example = product_month_summary[product_month_summary["ProductID"] == "P001"]
sns.lineplot(data=product_example, x="Month", y="TotalSales", marker="o", color="darkblue", linewidth=2.5)
plt.title("Monthly Sales Trend for Product P001", fontsize=18, fontweight="bold")
plt.xlabel("Month", fontsize=14)
plt.ylabel("Total Sales (in USD)", fontsize=14)
plt.xticks(range(1, 13), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ---- INSIGHT 3: Peak Transaction Hours ---- #
# Extract hour from TransactionDate
transactions["Hour"] = transactions["TransactionDate"].dt.hour

# Group by hour to find peak transaction hours
hourly_summary = (
    transactions.groupby("Hour")
    .agg(TotalTransactions=("TransactionID", "count"))
    .reset_index()
)

# Print structured peak transaction hours summary
print("\n" + "="*50)
print(f"{'PEAK TRANSACTION HOURS':^50}")
print("="*50)
print(tabulate(hourly_summary, headers='keys', tablefmt='pretty', showindex=False))

# Visualization
plt.figure(figsize=(14, 8))
sns.barplot(data=hourly_summary, x="Hour", y="TotalTransactions", palette="coolwarm", hue=None, edgecolor="black")
plt.title("Peak Transaction Hours", fontsize=18, fontweight="bold")
plt.xlabel("Hour of the Day", fontsize=14)
plt.ylabel("Number of Transactions", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ---- INSIGHT 4: Product Sales During Peak Hours ---- #
# Find the peak hour
peak_hour = hourly_summary.loc[hourly_summary["TotalTransactions"].idxmax(), "Hour"]

# Filter transactions during the peak hour
peak_hour_transactions = transactions[transactions["Hour"] == peak_hour]

# Summarize product sales during the peak hour
peak_hour_product_sales = (
    peak_hour_transactions.groupby("ProductID")
    .agg(TotalSales=("TotalValue", "sum"), TotalQuantity=("Quantity", "sum"))
    .reset_index()
)

# Print structured product sales during peak hour summary
print("\n" + "="*50)
print(f"{'PRODUCT SALES DURING PEAK HOUR':^50}")
print("="*50)
print(tabulate(peak_hour_product_sales, headers='keys', tablefmt='pretty', showindex=False))

# Visualization for top products during the peak hour
plt.figure(figsize=(14, 8))
top_peak_products = peak_hour_product_sales.sort_values(by="TotalSales", ascending=False).head(10)
sns.barplot(data=top_peak_products, x="ProductID", y="TotalSales", palette="viridis", hue=None, edgecolor="black")
plt.title("Top Product Sales During Peak Hour", fontsize=18, fontweight="bold")
plt.xlabel("Product ID", fontsize=14)
plt.ylabel("Total Sales (in USD)", fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ---- INSIGHT 5: Stock Recommendations ---- #
# Combine product and sales data
product_sales_summary = (
    transactions.groupby("ProductID")
    .agg(TotalSales=("TotalValue", "sum"), TotalQuantity=("Quantity", "sum"))
    .reset_index()
)

# Merge with product prices
product_recommendations = pd.merge(product_sales_summary, products, on="ProductID", how="inner")

# Sort by TotalSales and Price to prioritize restocking
product_recommendations = product_recommendations.sort_values(by=["TotalSales", "Price"], ascending=False)

# Print structured stock recommendations summary
print("\n" + "="*50)
print(f"{'STOCK RECOMMENDATIONS':^50}")
print("="*50)
print(tabulate(product_recommendations[["ProductID", "ProductName", "Category", "TotalSales", "Price"]],
               headers='keys', tablefmt='pretty', showindex=False))

# Visualization for Stock Recommendations (Total Sales by Product and Category)
plt.figure(figsize=(14, 8))

# Sort the data by total sales for better visualization
top_recommendations = product_recommendations.head(20)  # Taking top 20 products for better readability

sns.barplot(data=top_recommendations, x="ProductName", y="TotalSales", hue="Category", palette="Set2", edgecolor="black")

# Set the title and labels
plt.title("Top 20 Stock Recommendations Based on Total Sales", fontsize=18, fontweight="bold")
plt.xlabel("Product Name", fontsize=14)
plt.ylabel("Total Sales (in USD)", fontsize=14)
plt.xticks(rotation=45, fontsize=12, ha="right")
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ---- INSIGHT 6: New Product Launches ---- #
# Define new products as those with sales data starting late in the timeline
launch_date_threshold = transactions["TransactionDate"].max() - pd.Timedelta(days=90)

# Identify new products
new_products = products[~products["ProductID"].isin(transactions["ProductID"].unique())]

# Print structured new product launches summary
print("\n" + "="*50)
print(f"{'NEW PRODUCT LAUNCHES':^50}")
print("="*50)
print(tabulate(new_products, headers='keys', tablefmt='pretty', showindex=False))

# Visualization for new product launches
if not new_products.empty:
    plt.figure(figsize=(14, 8))
    sns.barplot(data=new_products, x="ProductName", y="Price", palette="pastel", hue=None, edgecolor="black")
    plt.title("New Product Launches and Their Prices", fontsize=18, fontweight="bold")
    plt.xlabel("Product Name", fontsize=14)
    plt.ylabel("Price (in USD)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12, ha="right")
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
else:
    print("\nNo new products were launched within the timeframe.")