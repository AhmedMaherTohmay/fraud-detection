import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, classification_report
)
from src.config import DATA_PATH_TEST

def log_metrics(model, X, y):
    """Evaluation metrics calculation"""
    y_pred = model.predict(X)
    y_pred_binary = np.where(y_pred == -1, 1, 0)

    metrics = {
        'precision': precision_score(y, y_pred_binary),
        'recall': recall_score(y, y_pred_binary),
        'f1': f1_score(y, y_pred_binary),
        'roc_auc': roc_auc_score(y, y_pred),
        'average_precision': average_precision_score(y, y_pred),
    }

    tn, fp, fn, tp = confusion_matrix(y, y_pred_binary).ravel()
    metrics.update({
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn,
        'true_positives': tp
    })

    print("\nClassification Report:")
    print(classification_report(y, y_pred_binary))

    return metrics

def evaluate_model(model):
    """Main evaluation function"""
    # Load model and preprocessing pipeline
    pipeline = joblib.load("artifacts/preprocessing_pipeline.pkl")
    
    # Load and process data
    df = pd.read_csv(DATA_PATH_TEST)
    features = pipeline.transform(df)
    X_val = features.drop(columns=['is_fraud'])
    y_val = features['is_fraud']
    
    print("Evaluating model...")
    val_metrics = log_metrics(model, X_val, y_val)
    
    print("\nValidation Metrics:")
    for name, value in val_metrics.items():
        print(f"{name}: {value:.4f}" if isinstance(value, float) else f"{name}: {value}")

if __name__ == "__main__":
    model = joblib.load("artifacts/iso_forest_model.pkl")
    evaluate_model(model)