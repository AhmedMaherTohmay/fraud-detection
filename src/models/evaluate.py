import sys
from pathlib import Path
import mlflow
import pandas as pd
import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, classification_report
)
from sklearn.model_selection import train_test_split

# Fix 1: Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Fix 2: Correct imports
from src.config import MODEL_NAME, DATA_PATH
from src.pipelines import final_pipeline

def log_metrics(run_id, X, y, prefix=""):
    """Evaluation metrics calculation"""
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
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
    
    with mlflow.start_run(run_id=run_id):
        for name, value in metrics.items():
            mlflow.log_metric(f"{prefix}{name}", value)
        
        report = classification_report(y, y_pred_binary)
        mlflow.log_text(report, f"{prefix}classification_report.txt")
    
    return metrics

def evaluate_model():
    """Main evaluation function"""
    mlflow.set_tracking_uri("file:./mlruns")
    
    # Get the latest training run
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(
        experiment_ids=["780391087486925493"],
        order_by=["attributes.start_time DESC"],
        max_results=1
    )
    
    if not runs:
        raise ValueError("No training runs found")
    
    run_id = runs[0].info.run_id
    
    # Load and process data
    df = pd.read_csv(DATA_PATH)
    features = final_pipeline(df)
    X = features.drop(columns=['is_fraud'])
    y = features['is_fraud']
    _, X_val, _, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Evaluating model...")
    val_metrics = log_metrics(run_id, X_val, y_val, "val_")
    
    print("\nValidation Metrics:")
    for name, value in val_metrics.items():
        print(f"{name}: {value:.4f}" if isinstance(value, float) else f"{name}: {value}")

if __name__ == "__main__":
    evaluate_model()