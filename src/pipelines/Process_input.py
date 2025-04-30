import pandas as pd

# Function to process JSON data and combine it with train_df data
def process_json_and_search(json_data, train_df):
    # Convert JSON data to a DataFrame
    input_data = pd.DataFrame([json_data])

    # Extract the 'cc_num' field
    cc_num = input_data.loc[0, 'cc_num']

    # Check if the 'cc_num' exists in train_df
    if cc_num in train_df['cc_num'].values:
        # Get all records related to the 'cc_num'
        related_records = train_df[train_df['cc_num'] == cc_num]

        # Add the JSON data to the related records
        combined_df = pd.concat([related_records, input_data], ignore_index=True)
        return combined_df
    else:
        return f"No records found for cc_num: {cc_num}"


if __name__ == "__main__":
    # Example train_df (replace with your actual dataset)
    train_df = pd.DataFrame({
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
    
    # Example JSON data
    json_data = {
        "trans_date_trans_time": "2025-04-16 12:35:56",
        "cc_num": 1234567890123456,
        "merchant": "Amazon",
        "category": "electronics",
        "amt": 251.75,
        "lat": 40.7128,
        "long": -74.0060,
        "merch_lat": 40.7306,
        "merch_long": -73.9352,
        "unix_time": 1650102896
    }
    
    # Apply the function
    result = process_json_and_search(json_data, train_df)
    
    # Display the result
    print(result)