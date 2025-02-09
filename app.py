import pickle
import pandas as pd
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the model and scaler from the file
with open('xgb_model.pkl', 'rb') as file:
    XGB = pickle.load(file)

scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoders.pkl')


@app.route('/')
def home():
    return '<h1>Fraud Detection</h1>'

# Define the route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()
    
    test_df = pd.DataFrame(data)

    # Preprocess the data
    test_df['trans_date_trans_time'] = pd.to_datetime(test_df['trans_date_trans_time'], format='mixed')
    test_df['hour'] = test_df['trans_date_trans_time'].dt.hour
    test_df['month'] = test_df['trans_date_trans_time'].dt.month
    columns_to_drop = ['first', 'last', 'unix_time', 'dob', 'cc_num', 'zip', 'city','street', 'state', 'trans_num', 'trans_date_trans_time']
    test_df = test_df.drop(columns_to_drop, axis=1)
    test_df['merchant'] = test_df['merchant'].apply(lambda x : x.replace('fraud_',''))
    test_df['gender'] = test_df['gender'].map({'F': 0, 'M': 1})

    # apply encoding
    for col in ['job', 'merchant', 'category']:
        test_df[col] = encoders[col].transform(test_df[col])

    X_test = test_df.drop("is_fraud", axis=1)

    # Transform the data
    X_test = scaler.transform(X_test)

    # Make predictions
    predictions = XGB.predict(X_test)

    # Return the predictions as JSON
    return jsonify(predictions.tolist())

if __name__ == '__main__':
    # app.run(debug=True)
    print("Running")

# curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test_data.json