from src.pipelines.category import CategoryOneHotTransformer as category_pipline
from src.pipelines.geo import HaversineAndProcessDataTransformer as distance
from src.pipelines.time import PartOfDayTransformer
from src.pipelines.rolling import AddAverageColumns 
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib

test_df = pd.DataFrame({
    "trans_date_trans_time": ["2025-04-16 12:34:56", "2025-04-16 13:22:11"],
    "cc_num": [1234567890123456, 2345678901234567],
    "category": ["electronics", "grocery_pos"],
    "amt": [250.75, 45.00],
    "lat": [40.7128, 34.0522],
    "long": [-74.0060, -118.2437],
    "merch_lat": [40.7306, 34.0525],
    "merch_long": [-73.9352, -118.2430]
})

# cols_to_keep = ['cc_num', 'trans_date_trans_time', 'category', 'amt', 'lat', 'long', 'merch_lat', 'merch_long', 'unix_time']
def final_pipeline():
    return Pipeline([
        ('add_average_columns', AddAverageColumns()),
        ('distance_difference', distance(lat_col='lat', long_col='long', 
                merch_lat_col='merch_lat', merch_long_col='merch_long', 
                group_col='cc_num')),
        ('part_of_day_categorization', PartOfDayTransformer()),
        ('category_onehot_encoding', category_pipline())
    ])


if __name__ == "__main__":
    # Inspect the transformed data
    train_df = pd.read_csv('data/cleaned_train.csv')
    pipeline = final_pipeline()
    transformed_train = pipeline.fit_transform(train_df)
    # print(transformed_train)
    joblib.dump(pipeline, 'artifacts/preprocessing_pipeline.pkl')
    pipeline = joblib.load('artifacts/preprocessing_pipeline.pkl')
    transformed_test = pipeline.transform(test_df)
    print(transformed_test)
    print("############\n"*3)
    print(transformed_test.info())