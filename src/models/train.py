# src/models/train.py
import pandas as pd
import joblib
import pickle
<<<<<<< HEAD
=======
import json
>>>>>>> fraud_detection/main
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from src.config import DATA_PATH_TRAIN

def train_model():
    
    # Load and preprocess data
    df = pd.read_csv(DATA_PATH_TRAIN)
<<<<<<< HEAD
    pipeline = joblib.load("artifacts\preprocessing_pipeline.pkl")
=======
    pipeline = joblib.load("artifacts/preprocessing_pipeline.pkl")
>>>>>>> fraud_detection/main
    features = pipeline.transform(df)
    
    # Split data
    X = features.drop(columns=['is_fraud'])
    y = features['is_fraud']
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Model parameters
    params = {
        'n_estimators': 100,
        'max_samples': 'auto',
        'contamination': 'auto',
        'random_state': 42,
        'verbose': 0
    }
    
    # Train model
    model = IsolationForest(**params)
    model.fit(X_train)
<<<<<<< HEAD
    
    # Save model locally
    model_path = f"artificats/{model}.pkl"
=======
    scores = model.decision_function(X_train)
    
    max_score = scores.max()
    min_score = scores.min()
    with open("artifacts/scores.json", "w") as f:
        json.dump({"max_score": max_score, "min_score": min_score}, f, indent=2)
    
    # Save model locally
    model_path = f"artifacts/iso_forest_model.pkl"
>>>>>>> fraud_detection/main
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved at {model_path}")
    
    # Return everything needed for evaluation
    return model, X_train, y_train, X_val, y_val

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Training completed.")