import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine, text

#  $env:Path += ";C:\Program Files\PostgreSQL\17\bin"

#SQL ALCHEMY
DB_URL = "postgresql+psycopg2://postgres:@localhost:5432/fraud"
engine = create_engine(DB_URL)


# You can adjust these as needed
DB_PARAMS = dict(
    dbname='fraud',
    user='postgres',
    password='',      # your password if any
    host='localhost',
    port=5432
)

def check_sql():
    conn=psycopg2.connect(**DB_PARAMS)
    cur=conn.cursor()
    
    cur.execute(
        '''
        SELECT COUNT(*)
        From Transactions
        '''
    )
    
    output = cur.fetchall()
    
    for row in output:
        print("Table row count = ")
        print(row)

def sql_command():
    conn=psycopg2.connect(**DB_PARAMS)
    cur=conn.cursor()
    
    cur.execute(
        '''
        SELECT cc_num, trans_date_trans_time AS timestamp_col
        FROM transactions
        WHERE cc_num = 3576431665303017 AND trans_date_trans_time >= NOW() - INTERVAL '24 hours'
        ORDER BY timestamp_col DESC;
        '''
    )
    
    output = cur.fetchall()
    
    for row in output:
        print(row)

def get_recent_transactions(cc_num):
    conn=psycopg2.connect(**DB_PARAMS)
    cur=conn.cursor()
    external_ts = "2019-06-22 00:00:00"
    with conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM transactions
            WHERE cc_num = %s
            AND trans_date_trans_time BETWEEN (%s::timestamp - INTERVAL '24 hours') AND %s::timestamp
            ORDER BY trans_date_trans_time DESC
        """, (cc_num, external_ts, external_ts))  # external_ts must be a datetime or string
        output = cur.fetchall()

        
        for row in output:
            print(row)
            

def Check_Frames(cc_num):
    # connect to Database
    with engine.connect() as conn:
        frame = pd.read_sql_query(text("""
            SELECT *
            FROM transactions
            WHERE cc_num = :ccnum
            AND trans_date_trans_time >= (
                SELECT MAX(trans_date_trans_time)
                FROM transactions
                WHERE cc_num = :ccnum
            ) - INTERVAL '24 hours'
            AND trans_date_trans_time <= (
                SELECT MAX(trans_date_trans_time)
                FROM transactions
                WHERE cc_num = :ccnum
            )
            ORDER BY trans_date_trans_time DESC
        """), conn, params={"ccnum": cc_num})
    return frame  # Return the DataFrame

def show_feature_lake():
    # connect to Database
    with engine.connect() as conn:
        frame = pd.read_sql_query(text("""
            SELECT *
            FROM feature_lake
            
        """), conn)
    return print(frame)  # Return the DataFrame


if __name__ == '__main__':
    #frame = Check_Frames(4992346398065154184)#3576431665303017)
    #print(frame.head(), frame.info(), '\n',not frame.empty)
    
    get_recent_transactions(3576431665303017)
    show_feature_lake()