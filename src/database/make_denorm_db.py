
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Load all required CSVs
metadata_df = pd.read_csv('../../data/Transaction Data/transaction_metadata.csv')
records_df = pd.read_csv('../../data/Transaction Data/transaction_records.csv')
activity_df = pd.read_csv('../../data/Customer Profiles/account_activity.csv')
customer_df = pd.read_csv('../../data/Customer Profiles/customer_data.csv')
merchant_df = pd.read_csv('../../data/Merchant Information/merchant_data.csv')
category_df = pd.read_csv('../../data/Merchant Information/transaction_category_labels.csv')
amount_df = pd.read_csv('../../data/Transaction Amounts/amount_data.csv')
anomaly_df = pd.read_csv('../../data/Transaction Amounts/anomaly_scores.csv')
coords_df = pd.read_csv('../../data/Sample_Data.csv')[['merch_lat', 'merch_long']].drop_duplicates().reset_index(drop=True)


merchant_df.drop(columns='Location', axis=1, inplace=True)
merchant_df['MerchantLat'] = coords_df['merch_lat'][:len(merchant_df)].values
merchant_df['MerchantLon'] = coords_df['merch_long'][:len(merchant_df)].values

# Merge into a single denormalized DataFrame
transactions = metadata_df.merge(records_df, on='TransactionID')
transactions = transactions.merge(category_df, on='TransactionID')
transactions = transactions.merge(amount_df, on='TransactionID')
transactions = transactions.merge(customer_df, on='CustomerID')
transactions = transactions.merge(activity_df, on='CustomerID')
transactions = transactions.merge(merchant_df, on='MerchantID')
transactions = transactions.merge(anomaly_df, on='TransactionID')


# Connect to PostgreSQL and create table
engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/denorm_trans')
transactions.to_sql('denorm_trans', con=engine, if_exists='replace', index=False)

print("Denormalized table 'denorm_trans' has been written to the PostgreSQL 'denorm_trans' database.")

# Save as a flat CSV file
transactions.to_csv('../../data/denormalized_transactions.csv', index=False)
print("Denormalized table saved to data/denormalized_transactions.csv")
