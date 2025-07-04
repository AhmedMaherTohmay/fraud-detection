import pandas as pd
import joblib
from sqlalchemy import create_engine, text
from src.config import DB_URL, DATA_PATH_TRAIN


FEATURE_LAKE_COLUMNS = [
    "date_index",
    "time_stamp",
    "last_hour_sum", "last_hour_count", "last_hour_avg", "last_24h_sum", "last_24h_count", "last_24h_avg", "last_100_median",
    "dist", "dist_diff", "D_Evening", "D_Morning", "D_Night",
    "category_food_dining", "category_gas_transport", "category_grocery_net", "category_grocery_pos",
    "category_health_fitness", "category_home", "category_kids_pets", "category_misc_net",
    "category_misc_pos", "category_personal_care", "category_shopping_net",
    "category_shopping_pos", "category_travel", "fraud_score"
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
        engine = create_engine(DB_URL)
        
        # Clean and reindex columns
        df = transformed_df[FEATURE_LAKE_COLUMNS].copy()
        # Convert date for PostgreSQL
        df["date_index"] = pd.to_datetime(df["date_index"]).dt.date

        # Robust boolean casting for specific columns
        BOOL_COLS = ["D_Evening", "D_Morning", "D_Night"]
        def force_bool(val):
            if pd.isnull(val):
                return None
            if isinstance(val, bool):
                return val
            if isinstance(val, (float, int)):
                return bool(int(val))
            if isinstance(val, str):
                s = val.strip().lower()
                if s in ("1", "true", "yes", "y", "t"):
                    return True
                if s in ("0", "false", "no", "n", "f"):
                    return False
            # fallback: Python truthiness
            return bool(val)
        for col in BOOL_COLS:
            if col in df.columns:
                df[col] = df[col].apply(force_bool)

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
    # Example usage
    # Load a sample DataFrame (replace with actual transformed data)
    df = pd.read_csv(DATA_PATH_TRAIN)
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    pipeline = joblib.load("artifacts/preprocessing_pipeline.pkl")
    transformed_df = pipeline.transform(df)
    transformed_df.drop(columns=['is_fraud'], inplace=True, errors='ignore')
    
    # Re Add Timestamp to transformed_df
    time_stamp = df["trans_date_trans_time"][0]
    transaction = transformed_df.iloc[:500000]
    transaction["time_stamp"] = time_stamp
    transaction["date_index"] = time_stamp.date()
    print(transaction.info())
    insert_into_feature_lake(transaction)