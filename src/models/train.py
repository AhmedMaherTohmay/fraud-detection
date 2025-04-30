# src/models/train.py
import mlflow
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from src.pipelines import final_pipeline
from src.config import MODEL_NAME, DATA_PATH

def train_model():
    """Train and log model without evaluation metrics"""
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("fraud_detection")
    
    # Load and preprocess data
    df = pd.read_csv(DATA_PATH)
    features = final_pipeline(df)
    
    # Split data
    X = features.drop(columns=['is_fraud'])
    y = features['is_fraud']
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    with mlflow.start_run():
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
        
        # Log only basic info
        mlflow.log_params(params)
        mlflow.log_metric("train_samples", len(X_train))
        
        # Log model
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=MODEL_NAME
        )
        
        # Return everything needed for evaluation
        return model, X_train, y_train, X_val, y_val

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Training completed. Run evaluation separately.")