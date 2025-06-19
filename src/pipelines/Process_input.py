import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from src.models.predictions_testing import predict_fraud

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
    
    # Get History DataFrame
    with engine.connect() as conn:
        history_frame = pd.read_sql_query(text("""
            SELECT *
            FROM transactions
            WHERE cc_num = :ccnum
            AND trans_date_trans_time BETWEEN (:external_ts - INTERVAL '24 hours') AND :external_ts
            ORDER BY trans_date_trans_time DESC;
        """), conn, params={"ccnum": cc_num, "external_ts": timestamp })
        
    # Ensure datetime format
    history_frame['trans_date_trans_time'] = pd.to_datetime(history_frame['trans_date_trans_time'])
    
    
    current_time = input_data.loc[0, 'trans_date_trans_time']
    
    #print(history_frame)

    # Check for existing records
    if not history_frame.empty:
        result = pd.concat([history_frame, input_data], ignore_index=True)
        result = result.sort_values(by=['trans_date_trans_time'], ascending=False).reset_index(drop=True)
    else:
        print(f"No records found for cc_num: {cc_num}")
        result = pd.DataFrame()
        
    # ADD the new transaction to the database
    try:
        input_data.to_sql('transactions', engine, if_exists='append', index=False)
        print("Succesful insertion to Database")
    except:
        print("Failed To Append to Database")
        
    return result

if __name__ == "__main__":
    # Load train_df
    #train_df = pd.read_csv('data/cleaned_train.csv')
    
    # Example JSON data
    json_data =  {
        "trans_date_trans_time": "2019-08-06 12:14:33",
        "cc_num": 3576431665303017,
        "category": "personal_care",
        "amt": 29.84,
        "lat": 40.3207,
        "long": -110.4360,
        "merch_lat": 39.450498,
        "merch_long": -109.960431
    }

    
    # Apply the function
    result = process_json_and_search(json_data)
    print(result.head(20))
    result_frame = predict_fraud(result)
    #print(result_frame)
    # Display the result
    #print(result.tail(1))