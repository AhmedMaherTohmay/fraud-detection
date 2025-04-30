from flask import Flask, request, jsonify
import pandas as pd
from src.models.predict import FraudPredictor
from src.config import PREDICTION_COLS

app = Flask(__name__)
predictor = FraudPredictor()

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
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        data = pd.DataFrame(data)
        data = data[PREDICTION_COLS]  # Only keep required columns
        
        # Get prediction (probability score)
        score = predictor.predict(data)
        
        return jsonify({
            "fraud_probability": float(score[0]),  # Convert numpy float to Python float
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