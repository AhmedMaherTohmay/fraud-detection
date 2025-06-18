# src/monitoring/drift_evidently.py
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import os
from datetime import datetime

# Your drift-relevant features
DRIFT_FEATURES = [
    'amt',
    'category',
]

def run_drift_report(train_df: pd.DataFrame, recent_df: pd.DataFrame, output_html: str = None):
    """
    Generates a drift report comparing recent data to training data.
    Returns:
        - drift_detected (bool)
        - report_json (dict)
    """
    # Only use relevant features
    train = train_df[DRIFT_FEATURES].copy()
    recent = recent_df[DRIFT_FEATURES].copy()

    # Build the report
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=train, current_data=recent)

    # Save report to HTML if path is given
    if output_html:
        os.makedirs(os.path.dirname(output_html), exist_ok=True)
        report.save_html(output_html)

    # Check if drift was detected
    drift_result = report.as_dict()
    drift_detected = drift_result['metrics'][0]['result']['dataset_drift']

    return drift_detected, drift_result


if __name__ == "__main__":
    # Example usage
    train_df = pd.read_csv('data/cleaned_train.csv')
    recent_df = pd.read_csv('data/cleaned_test.csv')
    drift_detected, report_json = run_drift_report(train_df, recent_df)
    print(f"Drift detected: {drift_detected}")