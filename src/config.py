# src/config.py
import os
from dotenv import load_dotenv

# Get the absolute path to the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# Data paths
DATA_PATH_TRAIN = "data/cleaned_train.csv"
DATA_PATH_TEST = "data/cleaned_test.csv"

# Model config
MODEL_CONFIG = {
    'NAME': "fraud_isoforest",
    'THRESHOLD': 42.5
}

# Database config
# config.py

DB_PARAMS = {
    'dbname': 'fraud',
    'user': 'postgres',
    'password': os.environ.get('DB_PASSWORD'),  # Add your real password here if needed
    'host': 'localhost',
    'port': 5432
}
print(DB_PARAMS)


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

DRIFT_FEATURES = [
    'amt',
]   

# Explicit exports
__all__ = ['DATA_PATH', 'MODEL_CONFIG', 'DB_CONFIG', 'PREDICTION_COLS', 'DRIFT_FEATURES']