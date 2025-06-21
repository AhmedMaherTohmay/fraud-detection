import pandas as pd
<<<<<<< HEAD
import psycopg2
from sqlalchemy import create_engine, text
from src.models.predictions_testing import predict_fraud

#from src.models.predictions import predict_fraud



#SQL ALCHEMY
DB_URL = "postgresql+psycopg2://postgres:@localhost:5432/fraud"
engine = create_engine(DB_URL)



# Function to process JSON data and combine it with train_df data
def process_json_and_search(json_data):
    
    # Convert JSON data to a DataFrame
    input_data = pd.DataFrame([json_data])

    # Extract cc_num and timestamp
    cc_num = int(input_data.loc[0, 'cc_num'])
    input_data['trans_date_trans_time'] = pd.to_datetime(input_data['trans_date_trans_time'])
    timestamp = input_data['trans_date_trans_time'].max()
    
    # Querying the Database
    with engine.connect() as conn:
        # Check For History of CC_NUM
        history_frame = pd.read_sql_query(text("""
            SELECT *
            FROM transactions
            WHERE cc_num = :ccnum
            AND trans_date_trans_time BETWEEN (:external_ts - INTERVAL '24 hours') AND :external_ts
            ORDER BY trans_date_trans_time DESC;
        """), conn, params={"ccnum": cc_num, "external_ts": timestamp })
        
        # Check if trans_date_trans_time for this cc_num already exists in table
        exists_query = conn.execute(
            text("""
                SELECT 1 FROM transactions
                WHERE cc_num = :ccnum AND trans_date_trans_time = :trans_time
                LIMIT 1
            """), {"ccnum": cc_num, "trans_time": timestamp}
        )
        already_exists = exists_query.fetchone() is not None
        print("Exists query\n:", exists_query)
        print("\nEntry Existence in Database 1:", already_exists)
        
    # Ensure datetime format
    history_frame['trans_date_trans_time'] = pd.to_datetime(history_frame['trans_date_trans_time'])

    # Check for existing records
    if not history_frame.empty:
        if not already_exists : 
            result = pd.concat([history_frame, input_data], ignore_index=True)
            result = result.sort_values(by=['trans_date_trans_time'], ascending=False).reset_index(drop=True)
        else:
            result = history_frame.sort_values(by=['trans_date_trans_time'], ascending = False).reset_index(drop=True)
    else:
        print(f"No records found for cc_num: {cc_num}")
        result = input_data
        
    print("\nhistory Frame:\n", history_frame)
    print("\nResult Frame:\n", result)
    
        
    # ADD the new transaction to the database
    try:
        if not already_exists:
            input_data.to_sql('transactions', engine, if_exists='append', index=False)
            print("Successful insertion to Database")
        else:
            print("Duplicate transaction: Not inserting to Database")
    except Exception as e:
        print(f"Failed To Append to Database: {e}")
    print("n Entry Existence in Database 1.5:", already_exists)
    return result, already_exists

if __name__ == "__main__":
    # Load train_df
    #train_df = pd.read_csv('data/cleaned_train.csv')
    
    # Example JSON data
    json_data =  {
        "trans_date_trans_time": "2019-08-05 17:39:33",
        "cc_num": 3576431665303017,
        "category": "personal_care",
        "amt": 29.84,
        "lat": 40.3207,
        "long": -110.4360,
        "merch_lat": 39.450498,
        "merch_long": -109.960431
    }

    
    # Apply the function
    result, exists = process_json_and_search(json_data)
    print(f"\nResulting Frame after function\n:{result}",f"\nEntry in Database after running function 2: {exists}\n")
    result_frame = predict_fraud(result, exists)
    print(result_frame)
    # Display the result
    #print(result.tail(1))
=======

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
>>>>>>> fraud_detection/main
