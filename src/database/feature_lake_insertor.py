import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text, MetaData, Table

DB_CONNECTION_STRING = "postgresql+psycopg2://postgres:@localhost:5432/fraud"

FEATURE_LAKE_COLUMNS = [
    "date_index",
    "time_stamp",
    "last_hour_count", "last_hour_avg", "last_24h_count", "last_24h_avg",
    "dist", "dist_diff", "D_Evening", "D_Morning", "D_Night",
    "category_food_dining", "category_gas_transport", "category_grocery_net", "category_grocery_pos",
    "category_health_fitness", "category_home", "category_kids_pets", "category_misc_net",
    "category_misc_pos", "category_personal_care", "category_shopping_net",
    "category_shopping_pos", "category_travel"
]

def ensure_date_exists(engine, date_val):
    """Insert the date into 'dates' if it does not exist."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO dates (date_index) VALUES (:d) ON CONFLICT DO NOTHING"),
                {"d": date_val}
            )
    except Exception as e:
        print(f"Failed to ensure date {date_val} in dates table: {e}")
        raise   # Reraise so logic knows the date did not go in

def insert_into_feature_lake(transformed_df):
    """
    Inserts a single-row DataFrame into feature_lake table, 
    ensuring the date exists in dates. All wrapped in try/except.
    """
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        
        # Clean and reindex columns
        df = transformed_df[FEATURE_LAKE_COLUMNS].copy()
        # Convert date for PostgreSQL
        df["date_index"] = pd.to_datetime(df["date_index"]).dt.date

        date_val = df["date_index"].iloc[0]
        try:
            ensure_date_exists(engine, date_val)
        except Exception as e:
            print(f"Aborting feature row insertion due to date error: {e}")
            return

        try:
            df.to_sql('feature_lake', engine, if_exists='append', index=False)
            print("Inserted one row into feature_lake.")
        except Exception as e:
            print("Failed to insert row into feature_lake:", e)
    
    except Exception as e:
        print("Unexpected failure during insertion pipeline:", e)
        

if __name__ == "__main__":
    pass