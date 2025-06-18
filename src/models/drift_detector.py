# src/models/drift_detector.py

import pandas as pd
from scipy.stats import ks_2samp, chi2_contingency

DRIFT_FEATURES = [
    'amt',
    'category',
]

def detect_drift(train_df: pd.DataFrame, recent_df: pd.DataFrame, threshold: float = 0.3):
    drifted_features = {}

    for feature in DRIFT_FEATURES:
        if feature not in train_df.columns or feature not in recent_df.columns:
            continue

        if pd.api.types.is_numeric_dtype(train_df[feature]):
            stat, p_val = ks_2samp(train_df[feature].dropna(), recent_df[feature].dropna())
            if p_val < threshold:
                drifted_features[feature] = {
                    "test": "ks_test",
                    "p_value": p_val
                }

        else:  # Categorical
            crosstab = pd.crosstab(train_df[feature], recent_df[feature])
            try:
                stat, p_val, dof, expected = chi2_contingency(crosstab)
                if p_val < threshold:
                    drifted_features[feature] = {
                        "test": "chi2",
                        "p_value": p_val
                    }
            except ValueError:
                continue  # If categories don't overlap enough

    # Decide: is retraining needed?
    retrain_needed = len(drifted_features) >= 2

    return retrain_needed, drifted_features


if __name__ == "__main__":
    # Example usage
    train_df = pd.read_csv('data/cleaned_train.csv')
    recent_df = pd.read_csv('data/cleaned_test.csv')

    retrain_needed, drifted_features = detect_drift(train_df, recent_df)

    if retrain_needed:
        print("Retraining needed due to feature drift.")
        print("Drifted features:", drifted_features)
    else:
        print("No significant drift detected.")