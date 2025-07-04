from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# Step 1: Define a transformer for adding average columns
class AddAverageColumns(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Ensure data is sorted by credit card and transaction time
        df = X.copy()
        
        # Convert to datetime if not already and sort by cc_num and trans_date_trans_time
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        df = df.sort_values(by=['cc_num', 'trans_date_trans_time']).reset_index(drop=True)
        
        # Temporarily set datetime as index for rolling calculations
        original_index = df.index
        df.set_index('trans_date_trans_time', inplace=True)
        
        # Calculate rolling features for each credit card
        grouped = df.groupby('cc_num')
        
        # Last hour rolling features
        df['last_hour_sum'] = grouped['amt'].rolling('1h').sum().reset_index(level=0, drop=True)
        df['last_hour_count'] = grouped['amt'].rolling('1h').count().reset_index(level=0, drop=True)
        df['last_hour_avg'] = (df['last_hour_sum'] / df['last_hour_count']).round(2)
        
        # Last 24 hours rolling features
        df['last_24h_sum'] = grouped['amt'].rolling('24h').sum().reset_index(level=0, drop=True)
        df['last_24h_count'] = grouped['amt'].rolling('24h').count().reset_index(level=0, drop=True)
        df['last_24h_avg'] = (df['last_24h_sum'] / df['last_24h_count']).round(2)
        
        rolling_100_medians = (
            grouped['amt']
            .rolling(window=100, min_periods=1)
            .median()
            .reset_index(level=0, drop=True)
        )
        df['last_100_median'] = rolling_100_medians
        
        # Reset index to original
        df.reset_index(inplace=True)
        df.index = original_index
        
        # Fill NaN values (first transactions for each card)
        df['last_hour_avg'] = df['last_hour_avg'].fillna(0)
        df['last_24h_avg'] = df['last_24h_avg'].fillna(0)
        df['last_hour_sum'] = df['last_hour_sum'].fillna(0)
        df['last_24h_sum'] = df['last_24h_sum'].fillna(0)
        df['last_100_median'] = df['last_100_median'].fillna(0)
        
        return df

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
    # Step 2: Define the pipeline
    pipeline = Pipeline([
        ('add_avg_columns', AddAverageColumns())
    ])
    
    # Step 3: Use the pipeline on the dataset
    transformed_df = pipeline.fit_transform(transformed_df)
    
    # Inspect the transformed data
    print(transformed_df.head())