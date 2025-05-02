import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:root@localhost/transactions")
df = pd.read_csv('..\..\data\Sample_Data.csv')
df.to_sql('transactions', engine, index=False, if_exists='replace')  # "replace" creates table