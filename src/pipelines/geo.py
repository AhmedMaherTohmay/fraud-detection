from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

# Haversine function
def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)
    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2 - lat1) / 2.0) ** 2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2.0) ** 2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))

# Custom transformer for haversine and processing
class HaversineAndProcessDataTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lat_col, long_col, merch_lat_col, merch_long_col, group_col):
        self.lat_col = lat_col
        self.long_col = long_col
        self.merch_lat_col = merch_lat_col
        self.merch_long_col = merch_long_col
        self.group_col = group_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # Calculate distance between transaction and merchant
        X['dist'] = haversine(
            X[self.lat_col],
            X[self.long_col],
            X[self.merch_lat_col],
            X[self.merch_long_col]
        )
        # Calculate distance from the previous transaction
        X['prev_dist'] = X.groupby(self.group_col)['dist'].shift(1)
        # Fill NaN values for the first transaction with the current distance
        X['prev_dist'].fillna(X['dist'], inplace=True)
        # Calculate the difference between current and previous distances
        X['dist_diff'] = abs(X['dist'] - X['prev_dist'])
        # Drop unnecessary columns
        X.drop(columns=[self.lat_col, self.long_col, self.merch_lat_col, self.merch_long_col, 'prev_dist'], inplace=True)
        return X

if __name__ == "__main__":
    transformed_df = pd.DataFrame({
        "trans_date_trans_time": ["2025-04-16 12:34:56", "2025-04-16 13:22:11"],
        "cc_num": [1234567890123456, 2345678901234567],
        "merchant": ["Amazon", "Walmart"],
        "category": ["electronics", "grocery_pos"],
        "amt": [250.75, 45.00],
        "lat": [40.7128, 34.0522],
        "long": [-74.0060, -118.2437],
        "merch_lat": [40.7306, 34.0525],
        "merch_long": [-73.9352, -118.2430],
        "unix_time": [1650102896, 1650105731]
    })
    # Define the pipeline
    pipeline = Pipeline([
        ('haversine_and_processing', HaversineAndProcessDataTransformer(
            lat_col='lat', long_col='long', 
            merch_lat_col='merch_lat', merch_long_col='merch_long', 
            group_col='cc_num'
        ))
    ])
    
    # Apply the pipeline to your dataset
    transformed_df = pipeline.fit_transform(transformed_df)
    
    # Inspect the transformed data
    transformed_df.head()