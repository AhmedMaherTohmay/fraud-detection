# File paths
DATA_PATH = "data/cleaned_train.csv"

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
    'unix_time'
]