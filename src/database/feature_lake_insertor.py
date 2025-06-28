# feature_lake_insertor.py
import pandas as pd
import joblib
from sqlalchemy import create_engine, text
from src.config import DB_URL, DATA_PATH_TRAIN

FEATURE_LAKE_COLUMNS = [
    "date_index", "time_stamp", "last_hour_count", "last_hour_avg",
    "last_24h_count", "last_24h_avg", "dist", "dist_diff",
    "D_Evening", "D_Morning", "D_Night",
    "category_food_dining", "category_gas_transport", "category_grocery_net",
    "category_grocery_pos", "category_health_fitness", "category_home",
    "category_kids_pets", "category_misc_net", "category_misc_pos",
    "category_personal_care", "category_shopping_net", "category_shopping_pos",
    "category_travel", "fraud_score"
]

def ensure_date_exists(engine, date_val):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO dates (date_index) VALUES (:d) ON CONFLICT DO NOTHING"),
                {"d": date_val}
            )
    except Exception as e:
        print(f"Failed to ensure date {date_val} in dates table: {e}")
        raise

def insert_into_feature_lake(transformed_df):
    try:
        engine = create_engine(DB_URL)
        df = transformed_df[FEATURE_LAKE_COLUMNS].copy()
        df["date_index"] = pd.to_datetime(df["date_index"]).dt.date

        BOOL_COLS = ["D_Evening", "D_Morning", "D_Night"]
        def force_bool(val):
            if pd.isnull(val): return None
            if isinstance(val, bool): return val
            if isinstance(val, (float, int)): return bool(int(val))
            if isinstance(val, str): return val.strip().lower() in ("1", "true", "yes", "y", "t")
            return bool(val)

        for col in BOOL_COLS:
            if col in df.columns:
                df[col] = df[col].apply(force_bool)

        date_val = df["date_index"].iloc[0]
        ensure_date_exists(engine, date_val)

        df.to_sql('feature_lake', engine, if_exists='append', index=False)
        print("Inserted one row into feature_lake.")
    except Exception as e:
        print("Unexpected failure during insertion pipeline:", e)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH_TRAIN)
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    pipeline = joblib.load("artifacts/preprocessing_pipeline.pkl")
    transformed_df = pipeline.transform(df)
    transformed_df.drop(columns=['is_fraud'], inplace=True, errors='ignore')

    transaction = transformed_df.iloc[:1].copy()
    time_stamp = df["trans_date_trans_time"].iloc[0]
    transaction["time_stamp"] = time_stamp
    transaction["date_index"] = time_stamp.date()
    insert_into_feature_lake(transaction)