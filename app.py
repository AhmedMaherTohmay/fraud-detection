import pandas as pd
from flask import Flask, request, jsonify
from src.pipelines import process_json_and_search
from src.models.predictions import predict_fraud
app = Flask(__name__)

@app.route('/')
def home():
    
    return '<h1>Fraud Detection API</h1><p>Send POST request to /predict with transaction data</p>'

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for fraud prediction.
    
    Expects JSON with transaction data including:
    - cc_num: Credit card number
    - trans_date_trans_time: Transaction timestamp
    - category: Transaction category
    - amt: Transaction amount
    - lat/long: Customer location
    - merch_lat/merch_long: Merchant location
    - unix_time: Transaction time in Unix format
    
    Returns:
        JSON with fraud probability score (0-100)
    """
    try:
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        #df = pd.read_csv('data/cleaned_train.csv')
        data = process_json_and_search(data[0])
        
        # Get prediction (probability score)
        if not data.empty:
            score = predict_fraud(data)
            
            return jsonify({
            "fraud_probability": float(score[-1]),  # Convert numpy float to Python float
            "status": "success"
        })
        
        return jsonify({
            "fraud_probability": float(1),  # RETURN NOT FRAUD IF FIRST TIME USER
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test_data.json
# curl -X POST https://fraud-detection-production-f16f.up.railway.app/predict -H "Content-Type: application/json" -d @test_data.json