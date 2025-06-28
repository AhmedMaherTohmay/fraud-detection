# src/config.py
import os
from dotenv import load_dotenv
import certifi

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

MODEL_PARAMS = {
    'n_estimators': 100,
    'max_samples': 'auto',
    'contamination': 'auto',
    'random_state': 42,
    'verbose': 0
}

# Database config
DB_PARAMS = {
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USERNAME'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': 3306,
    'ssl_ca': certifi.where(),  # Add SSL configuration
    'ssl_verify_cert': True
}

# SQLAlchemy connection string
DB_URL = (
    f"mysql+pymysql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"
    f"?ssl_ca={DB_PARAMS['ssl_ca']}"
)


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