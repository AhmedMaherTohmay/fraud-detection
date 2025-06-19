import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, BigInteger, Float
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

    your_table = Table(
        'feature_lake', metadata,
        Column('last_hour_count', Float),
        Column('last_hour_avg', Float),
        Column('last_24h_count', Float),
        Column('last_24h_avg', Float),
        Column('dist', Float),
        Column('dist_diff', Float),
        Column('D_Evening', BigInteger),
        Column('D_Morning', Boolean),
        Column('D_Night', BigInteger),
        Column('category_food_dining', BigInteger),
        Column('category_gas_transport', BigInteger),
        Column('category_grocery_net', BigInteger),
        Column('category_grocery_pos', BigInteger),
        Column('category_health_fitness', BigInteger),
        Column('category_home', BigInteger),
        Column('category_kids_pets', BigInteger),
        Column('category_misc_net', BigInteger),
        Column('category_misc_pos', BigInteger),
        Column('category_personal_care', BigInteger),
        Column('category_shopping_net', BigInteger),
        Column('category_shopping_pos', BigInteger),
        Column('category_travel', BigInteger)
    )
    
    metadata.create_all(engine)
    print("Feature_lake Created!")
    


if __name__ == '__main__':
    main()
    insert_db.preprocess_and_copy(500_000)
    sql_test.check_sql()
    create_feature_lake()
    