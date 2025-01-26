import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning, message=".Could not find the number of physical cores.")
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

customers = pd.read_csv("E:/Projects/Data_analysis/Customers.csv")
transactions = pd.read_csv("E:/Projects/Data_analysis/Transactions.csv")

print("Customers Columns:", customers.columns)

if 'SignupDate' in customers.columns:
    customers['SignupDate'] = pd.to_datetime(customers['SignupDate'], errors='coerce')
    current_date = datetime.now()
    customers['Age'] = current_date.year - customers['SignupDate'].dt.year
    customers['Age'] -= (customers['SignupDate'].dt.month > current_date.month) | ((customers['SignupDate'].dt.month == current_date.month) & (customers['SignupDate'].dt.day > current_date.day))
else:
    print("Error: 'SignupDate' column not found in the dataset.")

merged_data = pd.merge(transactions, customers[['CustomerID', 'Age']], on='CustomerID', how='left')

print("Merged Data Columns:", merged_data.columns)

merged_data['TotalSpent'] = merged_data.groupby('CustomerID')['TotalValue'].transform('sum')
merged_data = merged_data.drop_duplicates(subset='CustomerID')

features = merged_data[['Age', 'TotalSpent']]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

n_clusters = 4

kmeans = KMeans(n_clusters=n_clusters, random_state=42)
merged_data['Cluster'] = kmeans.fit_predict(scaled_features)

db_index = davies_bouldin_score(scaled_features, merged_data['Cluster'])
print(f"DB Index: {db_index:.4f}")

plt.figure(figsize=(10, 6))
plt.scatter(merged_data['Age'], merged_data['TotalSpent'], c=merged_data['Cluster'], cmap='viridis', s=50)
plt.title(f'Customer Segmentation with {n_clusters} Clusters')
plt.xlabel('Age')
plt.ylabel('Total Spent')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

print(merged_data[['CustomerID', 'Age', 'TotalSpent', 'Cluster']].head())

merged_data.to_csv('Clustered_Customers.csv', index=False)
