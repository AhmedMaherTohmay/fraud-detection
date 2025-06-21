<<<<<<< HEAD
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, Integer, Float, Date, DateTime, ForeignKey, text
import insert_db
import sql_test


DB_PARAMS = dict(
    dbname='fraud',
    user='postgres',
    password='',      # your password if any
    host='localhost',
    port=5432
)

def main():
    try:
        # Connect to the fraud database
        conn = psycopg2.connect(**DB_PARAMS)
        print("Connected to the database successfully.")
        cur = conn.cursor()
        
#______________________________________________________________________________________________________________________#
            #CREATE THE DERNORMALISED HISRORY LAKE#
#______________________________________________________________________________________________________________________#

        # Drop existing table (if needed)
        cur.execute("DROP TABLE IF EXISTS transactions;")

        # Create a flat table
        cur.execute("""
            CREATE TABLE transactions (
                cc_num BIGINT NOT NULL,
                trans_date_trans_time TIMESTAMP NOT NULL,
                category VARCHAR(50),
                amt NUMERIC(12,2),
                lat DOUBLE PRECISION,
                long DOUBLE PRECISION,
                merch_lat DOUBLE PRECISION,
                merch_long DOUBLE PRECISION
            );
        """)

        # Index for fast lookup by cc_num
        cur.execute("CREATE INDEX idx_ccnum ON transactions(cc_num);")

        conn.commit()
        cur.close()
        conn.close()
        print("Flat transactions table created with idx_ccnum for efficient querying by cc_num.")
    
    except Exception as ex:
        print("Error during database setup:")
        print(ex)
        
        
        
#______________________________________________________________________________________________________________________#
                    #CREATE THE NORMALISED FEATURE STORE#
#______________________________________________________________________________________________________________________#


def create_feature_store():
    try:
        conn=psycopg2.connect(**DB_PARAMS)
        cur=conn.cursor()
        print("Connected To Database")
        
        cur.execute()
        
    
    except:
        print("Connection To Database Failed (feature_store)")
        

#______________________________________________________________________________________________________________________#
                    #CREATE THE FEATURE LAKE#
#______________________________________________________________________________________________________________________#

def create_feature_lake():
    DB_URL = 'postgresql+psycopg2://postgres:@localhost:5432/fraud'
    engine = create_engine(DB_URL)
    metadata = MetaData()

    # Table for unique dates
    dates = Table(
        'dates', metadata,
        Column('date_index', Date, primary_key=True)
    )

    # Feature table referencing dates
    feature_lake = Table(
        'feature_lake', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),  # surrogate PK (fine to keep; helps future-proofing)
        Column('date_index', Date, ForeignKey('dates.date_index', ondelete='CASCADE'), index=True),
        Column('time_stamp', DateTime),
        Column('last_hour_count', Float),
        Column('last_hour_avg', Float),
        Column('last_24h_count', Float),
        Column('last_24h_avg', Float),
        Column('dist', Float),
        Column('dist_diff', Float),
        Column('D_Evening', Boolean),
        Column('D_Morning', Boolean),
        Column('D_Night', Boolean),
        Column('category_food_dining', Integer),
        Column('category_gas_transport', Integer),
        Column('category_grocery_net', Integer),
        Column('category_grocery_pos', Integer),
        Column('category_health_fitness', Integer),
        Column('category_home', Integer),
        Column('category_kids_pets', Integer),
        Column('category_misc_net', Integer),
        Column('category_misc_pos', Integer),
        Column('category_personal_care', Integer),
        Column('category_shopping_net', Integer),
        Column('category_shopping_pos', Integer),
        Column('category_travel', Integer)
    )

    # Drop and recreate (order is important: drop child before parent!)
    with engine.begin() as conn:
        feature_lake.drop(conn, checkfirst=True)
        dates.drop(conn, checkfirst=True)
        metadata.create_all(conn)
        print("Tables in database after creation:",
          conn.execute(
              text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
          ).fetchall())
    


if __name__ == '__main__':
    main()
    insert_db.preprocess_and_copy(500_000)
    sql_test.check_sql()
    create_feature_lake()
    
=======

import pandas as pd
import psycopg2

# Load data with updated paths
metadata_df = pd.read_csv('data/Transaction Data/transaction_metadata.csv')
records_df = pd.read_csv('data/Transaction Data/transaction_records.csv')
activity_df = pd.read_csv('data/Customer Profiles/account_activity.csv')
customer_df = pd.read_csv('data/Customer Profiles/customer_data.csv')
merchant_df = pd.read_csv('data/Merchant Information/merchant_data.csv')
category_df = pd.read_csv('data/Merchant Information/transaction_category_labels.csv')
amount_df = pd.read_csv('data/Transaction Amounts/amount_data.csv')
anomaly_df = pd.read_csv('data/Transaction Amounts/anomaly_scores.csv')

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

# Create tables
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
    Location TEXT
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
        INSERT INTO merchant_info VALUES (%s, %s, %s)
    """, tuple(row))

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
print("Database populated successfully.")


#$env:Path += ";C:\Program Files\PostgreSQL\17\bin"
>>>>>>> fraud_detection/main
