# src/models/train.py
import pandas as pd
import joblib
import pickle
import json
from sqlalchemy import create_engine, text
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from src.config import MODEL_PARAMS, DB_URL


#SQL ALCHEMY
engine = create_engine(DB_URL)

def train_model():
    # Querying the Database
    with engine.connect() as conn:
        # Check For History of CC_NUM
        transformed_df = pd.read_sql_query(text("""
            SELECT *
            FROM feature_lake;
        """), conn)
    transformed_df = transformed_df.drop(columns=['id', 'time_stamp', 'date_index'])
    
    # Train model
    model = IsolationForest(**MODEL_PARAMS)
    model.fit(transformed_df)
    scores = model.decision_function(transformed_df)
    
    max_score = scores.max()
    min_score = scores.min()
    with open("artifacts/scores.json", "w") as f:
        json.dump({"max_score": max_score, "min_score": min_score}, f, indent=2)
    
    # Save model locally
    model_path = f"artifacts/iso_forest_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved at {model_path}")
    
    # Return everything needed for evaluation
    return model

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Training completed.")