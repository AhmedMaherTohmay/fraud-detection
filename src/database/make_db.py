# make_db.py
import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, Integer, Float, Date, DateTime, ForeignKey, text
import insert_db
from src.config import DB_PARAMS, DB_URL


def main():
    try:
        conn = pymysql.connect(**DB_PARAMS)
        print("Connected to the database successfully.")
        cur = conn.cursor()

        # Drop and recreate transactions table
        cur.execute("DROP TABLE IF EXISTS transactions;")
        cur.execute("""
            CREATE TABLE transactions (
                cc_num BIGINT NOT NULL,
                trans_date_trans_time TIMESTAMP NOT NULL,
                category VARCHAR(50),
                amt DECIMAL(12,2),
                lat DECIMAL(12,6),
                `long` DECIMAL(12,6),
                merch_lat DECIMAL(12,6),
                merch_long DECIMAL(12,6)
            );
        """)
        cur.execute("CREATE INDEX idx_ccnum ON transactions(cc_num);")

        conn.commit()
        cur.close()
        conn.close()
        print("Flat transactions table created with idx_ccnum for efficient querying by cc_num.")
    except Exception as ex:
        print("Error during database setup:")
        print(ex)


def create_feature_store():
    try:
        conn = pymysql.connect(**DB_PARAMS)
        cur = conn.cursor()
        print("Connected To Database (feature_store)")
        # TODO: Add actual SQL statements to create feature store tables
        # cur.execute("""CREATE TABLE feature_store (...)""")
        cur.close()
        conn.close()
    except Exception as e:
        print("Connection to Database Failed (feature_store):", e)


def create_feature_lake():
    engine = create_engine(DB_URL)
    metadata = MetaData()

    dates = Table(
        'dates', metadata,
        Column('date_index', Date, primary_key=True)
    )

    feature_lake = Table(
        'feature_lake', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
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
        Column('category_travel', Integer),
        Column('fraud_score', Float)
    )

    with engine.begin() as conn:
        feature_lake.drop(conn, checkfirst=True)
        dates.drop(conn, checkfirst=True)
        metadata.create_all(conn)
        print("Tables in database after creation:",
              conn.execute(
                  text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
              ).fetchall())


if __name__ == '__main__':
    main()
    insert_db.preprocess_and_copy(500_000)
    create_feature_lake()
