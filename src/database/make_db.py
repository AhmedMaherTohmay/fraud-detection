
import pandas as pd
import psycopg2

# Load data
metadata_df = pd.read_csv('../../data/Transaction Data/transaction_metadata.csv')
records_df = pd.read_csv('../../data/Transaction Data/transaction_records.csv')
activity_df = pd.read_csv('../../data/Customer Profiles/account_activity.csv')
customer_df = pd.read_csv('../../data/Customer Profiles/customer_data.csv')
merchant_df = pd.read_csv('../../data/Merchant Information/merchant_data.csv')
category_df = pd.read_csv('../../data/Merchant Information/transaction_category_labels.csv')
amount_df = pd.read_csv('../../data/Transaction Amounts/amount_data.csv')
anomaly_df = pd.read_csv('../../data/Transaction Amounts/anomaly_scores.csv')
coords_df = pd.read_csv('../../data/Sample_Data.csv')[['merch_lat', 'merch_long']].drop_duplicates().reset_index(drop=True)

# Assign a unique lat/lon to each merchant
merchant_df = merchant_df.copy()
merchant_df['MerchantLat'] = coords_df['merch_lat'][:len(merchant_df)].values
merchant_df['MerchantLon'] = coords_df['merch_long'][:len(merchant_df)].values

# Merge customer and account activity
customer_info_df = pd.merge(customer_df, activity_df, on='CustomerID')

# Merge transaction info
transaction_info_df = metadata_df.merge(records_df, on='TransactionID')
transaction_info_df = transaction_info_df.merge(category_df, on='TransactionID')
transaction_info_df = transaction_info_df.merge(amount_df, on='TransactionID')
transaction_info_df = transaction_info_df.merge(anomaly_df, on='TransactionID')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="transactions",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create tables with merchant lat/lon
cur.execute("""
DROP TABLE IF EXISTS transaction_info, transactions, customer_info, merchant_info CASCADE;

CREATE TABLE customer_info (
    CustomerID INT PRIMARY KEY NOT NULL, 
    Name TEXT,
    Age INT,
    Address TEXT,
    AccountBalance FLOAT,
    LastLogin DATE
);

CREATE TABLE merchant_info (
    MerchantID INT PRIMARY KEY NOT NULL,
    MerchantName TEXT,
    MerchantLat FLOAT,
    MerchantLon FLOAT
);

CREATE TABLE transactions (
    TransactionID INT PRIMARY KEY NOT NULL,
    Timestamp TIMESTAMP,
    CustomerID INT REFERENCES customer_info(CustomerID),
    MerchantID INT REFERENCES merchant_info(MerchantID),
    Amount FLOAT
);

CREATE TABLE transaction_info (
    TransactionID INT PRIMARY KEY REFERENCES transactions(TransactionID),
    Category TEXT,
    TransactionAmount FLOAT,
    AnomalyScore FLOAT
);
""")

# Insert data
for _, row in customer_info_df.iterrows():
    cur.execute("""
        INSERT INTO customer_info VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

for _, row in merchant_df.iterrows():
    cur.execute("""
        INSERT INTO merchant_info VALUES (%s, %s, %s, %s)
    """, (
        row['MerchantID'], row['MerchantName'],
        row['MerchantLat'], row['MerchantLon']
    ))

for _, row in transaction_info_df.iterrows():
    cur.execute("""
        INSERT INTO transactions VALUES (%s, %s, %s, %s, %s)
    """, (
        row['TransactionID'], row['Timestamp'], row['CustomerID'],
        row['MerchantID'], row['Amount']
    ))

    cur.execute("""
        INSERT INTO transaction_info VALUES (%s, %s, %s, %s)
    """, (
        row['TransactionID'], row['Category'],
        row['TransactionAmount'], row['AnomalyScore']
    ))

conn.commit()
cur.close()
conn.close()
print("Database populated successfully with merchant coordinates.")
