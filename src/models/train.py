# src/models/train.py
import pandas as pd
import joblib
import pickle
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from src.config import DATA_PATH_TRAIN

def train_model():
    
    # Load and preprocess data
    df = pd.read_csv(DATA_PATH_TRAIN)
    pipeline = joblib.load("artifacts\preprocessing_pipeline.pkl")
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
    
    # Save model locally
    model_path = f"artificats/{model}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved at {model_path}")
    
    # Return everything needed for evaluation
    return model, X_train, y_train, X_val, y_val

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Training completed.")