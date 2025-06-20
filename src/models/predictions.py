import numpy as np
import pandas as pd
import joblib
import json
from src.config import DATA_PATH_TEST
# Transform scores to make fraud cases have higher values
def transform_scores(scores, max_score, min_score):
    """
    Convert Isolation Forest scores to fraud scores where:
    - Higher values indicate higher probability of fraud
    - Scores range from 0 (normal) to 100 (definite fraud)
    """
    # Shift scores so anomalies are positive
    shifted = -scores  # Invert the scores
    
    # Normalize to 0-100 range
    normalized = 100 * (shifted - min_score) / (max_score - min_score)
    normalized = np.clip(normalized, 0, 100)
    
    return normalized

def predict_fraud(df):
    # Load and preprocess data
    pipeline = joblib.load('artifacts/preprocessing_pipeline.pkl')
    transformed_df = pipeline.transform(df)
    # Ensure 'is_fraud' column is handled correctly if not present in the transformed data
    transformed_df.drop(columns=['is_fraud'], inplace=True, errors='ignore')
    
    # Load the saved model
    iso_forest_loaded = joblib.load("artifacts/iso_forest_model.pkl")
    
    # load scores metadata
    with open("artifacts/scores.json", "r") as f:
        scores_metadata = json.load(f)
    
    # Extract max and min scores
    max_score = scores_metadata['max_score']
    min_score = scores_metadata['min_score']
    
    # Make predictions
    val_scores = iso_forest_loaded.decision_function(transformed_df)
    val_proba = transform_scores(val_scores, max_score, min_score)
    return val_proba

if __name__ == "__main__":
    # Inspect the transformed data
    df = pd.read_csv(DATA_PATH_TEST)
    val_proba = predict_fraud(df)
    print(val_proba[-1])