# src/monitoring/drift_evidently.py
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import *
import pandas as pd
import os
from datetime import datetime
from IPython.display import display, HTML
from src.config import DRIFT_FEATURES

def run_drift_report(train_df: pd.DataFrame, recent_df: pd.DataFrame, output_html: str = None):
    train = train_df[DRIFT_FEATURES].copy()
    recent = recent_df[DRIFT_FEATURES].copy()

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=train, current_data=recent)

    if output_html:
        os.makedirs(os.path.dirname(output_html), exist_ok=True)
        report.save_html(output_html)
        display(HTML(filename=output_html))  # Display dashboard directly

    drift_result = report.as_dict()
    drift_detected = drift_result['metrics'][0]['result']['dataset_drift']

    return drift_detected, drift_result


if __name__ == "__main__":
    # Example usage
    train_df = pd.read_csv('data/cleaned_train.csv')
    recent_df = pd.read_csv('data/cleaned_test.csv')
    output_path = "../artifacts/data_drift_report.html"
    drift_detected, drift_result = run_drift_report(train_df, recent_df, output_html=output_path)
    print(f"Drift detected: {drift_detected}")