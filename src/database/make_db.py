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
    