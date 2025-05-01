import numpy as np
import pandas as pd
import joblib
from src.config import DATA_PATH_TEST
# Transform scores to make fraud cases have higher values
def transform_scores(scores):
    """
    Convert Isolation Forest scores to fraud scores where:
    - Higher values indicate higher probability of fraud
    - Scores range from 0 (normal) to 100 (definite fraud)
    """
    # Shift scores so anomalies are positive
    shifted = -scores  # Invert the scores
    
    # Normalize to 0-100 range
    min_score, max_score = np.min(shifted), np.max(shifted)
    normalized = 100 * (shifted - min_score) / (max_score - min_score)
    
    return normalized

def predict_fraud(df):
    # Load and preprocess data
    pipeline = joblib.load('artifacts/preprocessing_pipeline.pkl')
    transformed_df = pipeline.transform(df)
    transformed_df.drop(columns=['is_fraud'], inplace=True)
    
    # Load the saved model
    iso_forest_loaded = joblib.load("artifacts/iso_forest_model.pkl")
    
    # Make predictions
    val_scores = iso_forest_loaded.decision_function(transformed_df)
    val_proba = transform_scores(val_scores)
    return val_proba

if __name__ == "__main__":
    # Inspect the transformed data
    df = pd.read_csv(DATA_PATH_TEST)
    val_proba = predict_fraud(df)
    print(val_proba[-1])