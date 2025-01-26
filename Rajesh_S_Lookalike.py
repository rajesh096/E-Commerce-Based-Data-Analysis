import pandas as pd

# Load datasets
customers = pd.read_csv('Customers.csv')
products = pd.read_csv('Products.csv')
transactions = pd.read_csv('Transactions.csv')

# Merge transactions with customers
customer_transactions = pd.merge(transactions, customers, on='CustomerID', how='inner')

# Merge the result with products
full_data = pd.merge(customer_transactions, products, on='ProductID', how='inner')

# Total Spending per customer
total_spending = full_data.groupby('CustomerID')['TotalValue'].sum().reset_index()
total_spending.rename(columns={'TotalValue': 'TotalSpending'}, inplace=True)

# Average Transaction Value per customer
avg_transaction_value = full_data.groupby('CustomerID')['TotalValue'].mean().reset_index()
avg_transaction_value.rename(columns={'TotalValue': 'AvgTransactionValue'}, inplace=True)

# Purchase Frequency per customer
purchase_frequency = full_data.groupby('CustomerID')['TransactionID'].count().reset_index()
purchase_frequency.rename(columns={'TransactionID': 'PurchaseFrequency'}, inplace=True)

# Category Preferences per customer
category_preferences = full_data.groupby(['CustomerID', 'Category']).size().unstack(fill_value=0)

# Combine all features into a single DataFrame
customer_features = total_spending.merge(avg_transaction_value, on='CustomerID')
customer_features = customer_features.merge(purchase_frequency, on='CustomerID')
customer_features = customer_features.merge(category_preferences, on='CustomerID')

# Total Spending per customer
total_spending = full_data.groupby('CustomerID')['TotalValue'].sum().reset_index()
total_spending.rename(columns={'TotalValue': 'TotalSpending'}, inplace=True)

# Average Transaction Value per customer
avg_transaction_value = full_data.groupby('CustomerID')['TotalValue'].mean().reset_index()
avg_transaction_value.rename(columns={'TotalValue': 'AvgTransactionValue'}, inplace=True)

# Purchase Frequency per customer
purchase_frequency = full_data.groupby('CustomerID')['TransactionID'].count().reset_index()
purchase_frequency.rename(columns={'TransactionID': 'PurchaseFrequency'}, inplace=True)

# Category Preferences per customer
category_preferences = full_data.groupby(['CustomerID', 'Category']).size().unstack(fill_value=0)

# Combine all features into a single DataFrame
customer_features = total_spending.merge(avg_transaction_value, on='CustomerID')
customer_features = customer_features.merge(purchase_frequency, on='CustomerID')
customer_features = customer_features.merge(category_preferences, on='CustomerID')

# Total Spending per customer
total_spending = full_data.groupby('CustomerID')['TotalValue'].sum().reset_index()
total_spending.rename(columns={'TotalValue': 'TotalSpending'}, inplace=True)

# Average Transaction Value per customer
avg_transaction_value = full_data.groupby('CustomerID')['TotalValue'].mean().reset_index()
avg_transaction_value.rename(columns={'TotalValue': 'AvgTransactionValue'}, inplace=True)

# Purchase Frequency per customer
purchase_frequency = full_data.groupby('CustomerID')['TransactionID'].count().reset_index()
purchase_frequency.rename(columns={'TransactionID': 'PurchaseFrequency'}, inplace=True)

# Category Preferences per customer
category_preferences = full_data.groupby(['CustomerID', 'Category']).size().unstack(fill_value=0)

# Combine all features into a single DataFrame
customer_features = total_spending.merge(avg_transaction_value, on='CustomerID')
customer_features = customer_features.merge(purchase_frequency, on='CustomerID')
customer_features = customer_features.merge(category_preferences, on='CustomerID')

# Exclude self-similarity and get the top 3 most similar customers
top_similarities = {}
for customer in customer_features['CustomerID'].head(20):
    similar_customers = similarity_df.loc[customer].sort_values(ascending=False).iloc[1:4]  # Exclude the first one (self)
    top_similarities[customer] = similar_customers

# Display the results for the first 20 customers
for customer, similarities in top_similarities.items():
    print(f"Top similar customers for {customer}:")
    print(similarities)
    print("\n")
