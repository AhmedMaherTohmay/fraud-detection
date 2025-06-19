from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# Step 1: Define the function for categorizing part of the day
def categorize_part_of_day(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    elif 21 <= hour or hour < 5:
        return 'Night'

# Step 2: Create a transformer for part of the day logic and one-hot encoding
class PartOfDayTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.expected_columns = ['D_Evening', 'D_Morning', 'D_Night']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['hour'] = pd.to_datetime(X['trans_date_trans_time']).dt.hour
        X['part_of_day'] = X['hour'].apply(categorize_part_of_day)

        # One-hot encode
        one_hot_encoded = pd.get_dummies(X['part_of_day'], prefix='D')
        one_hot_encoded = one_hot_encoded.reindex(columns=self.expected_columns, fill_value=0)

        # Merge and drop unnecessary columns
        X = pd.concat([X, one_hot_encoded], axis=1)
        X.drop(columns=['part_of_day', 'hour'], inplace=True)

        return X


if __name__ == "__main__":
    # Step 3: Define the pipeline
    pipeline = Pipeline([
        ('part_of_day_categorization', PartOfDayTransformer())
    ])
    
    # Step 4: Apply the pipeline to your dataset
    # transformed_df = pipeline.fit_transform(train_df)
    
    # # Inspect the transformed data
    # transformed_df.head()