# src/config.py

# Data paths
DATA_PATH = "data/cleaned_train.csv"

# Model config
MODEL_CONFIG = {
    'NAME': "fraud_isoforest",
    'THRESHOLD': 42.5
}

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'port': '5432'
}

# Prediction columns
PREDICTION_COLS = [
    'cc_num', 
    'trans_date_trans_time',
    'category',
    'amt',
    'lat',
    'long',
    'merch_lat',
    'merch_long'
]

# Explicit exports
__all__ = ['DATA_PATH', 'MODEL_CONFIG', 'DB_CONFIG', 'PREDICTION_COLS']