from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# Step 1: Transformer for category one-hot encoding
class CategoryOneHotTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.expected_columns = [
            'category_food_dining', 'category_gas_transport', 'category_grocery_net',
            'category_grocery_pos', 'category_health_fitness', 'category_home',
            'category_kids_pets', 'category_misc_net', 'category_misc_pos',
            'category_personal_care', 'category_shopping_net', 'category_shopping_pos',
            'category_travel'
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # Drop unnecessary columns
        columns_to_drop = ['cc_num', 'trans_date_trans_time', 'amt']
        X.drop(columns=columns_to_drop, inplace=True)

        # One-hot encode and reindex to ensure consistent columns
        category_onehot = pd.get_dummies(X['category'], prefix='category')
        category_onehot = category_onehot.reindex(columns=self.expected_columns, fill_value=0)

        # Merge and drop original category
        X = pd.concat([X, category_onehot.astype(int)], axis=1)
        X.drop(columns=['category'], inplace=True)

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
    # Step 2: Define the final pipeline
    pipeline = Pipeline([
        ('category_onehot_encoding', CategoryOneHotTransformer())
    ])
    
    # Step 3: Apply the pipeline to your dataset
    transformed_df = pipeline.fit_transform(transformed_df)
    
    # Inspect the transformed data
    transformed_df.head()