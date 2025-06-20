import pandas as pd

# Function to process JSON data and combine it with train_df data
def process_json_and_search(json_data, data):
    # Convert JSON data to a DataFrame
    input_data = pd.DataFrame([json_data])

    # Ensure datetime format
    data['trans_date_trans_time'] = pd.to_datetime(data['trans_date_trans_time'])
    input_data['trans_date_trans_time'] = pd.to_datetime(input_data['trans_date_trans_time'])

    # Extract cc_num and timestamp
    cc_num = input_data.loc[0, 'cc_num']
    current_time = input_data.loc[0, 'trans_date_trans_time']


    last_24h_records = data[
        (data['cc_num'] == cc_num) &
        (data['trans_date_trans_time'] >= current_time - pd.Timedelta(hours=24)) &
        (data['trans_date_trans_time'] < current_time)
    ]
    return pd.concat([last_24h_records, input_data], ignore_index=True)



if __name__ == "__main__":
    # Load train_df
    train_df = pd.read_csv('data/cleaned_train.csv')
    
    # Example JSON data
    json_data = {
        "trans_date_trans_time": "2020-06-21 10:58:58",
        "cc_num": 4992346398065154184,
        "category": "electronics",
        "amt": 251.75,
        "lat": 40.7128,
        "long": -74.0060,
        "merch_lat": 40.7306,
        "merch_long": -73.9352,
    }
    
    # Apply the function
    result = process_json_and_search(json_data, train_df)
    
    # Display the result
    print(result.tail(1))