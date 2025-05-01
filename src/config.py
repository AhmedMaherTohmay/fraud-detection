# File paths
TRAIN_DATA_PATH = "data/cleaned_train.csv"
TEST_DATA_PATH = "data/cleaned_test.csv"

# Model configuration
MODEL_NAME = "fraud_isoforest"
THRESHOLD = 42.5  # Decision threshold for transformed scores

# Prediction columns
PREDICTION_COLS = [
    'cc_num', 
    'trans_date_trans_time',
    'category',
    'amt',
    'lat',
    'long',
    'merch_lat',
    'merch_long',
]

# Database
DB_CONFIG = {
    'host': 'localhost',
    'dbname':'postgres',
    'user': 'postgres',
    'password': 'root',
    'port' : '5432'
}