# app.py
import pandas as pd
import time
from flask import Flask, request, jsonify
from src.pipelines.Process_input import process_json_and_search
from src.models.predictions import predict_fraud
from src.monitoring.metrics import init_metrics

app = Flask(__name__)

# Initialize monitoring metrics
app_metrics = init_metrics(app)

@app.route('/')
def home():
    return '<h1>Fraud Detection API</h1><p>Send POST request to /predict with transaction data</p>'

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for fraud prediction with comprehensive metrics."""
    
    prediction_start_time = time.time()
    
    try:
        data = request.get_json()
        print(data)
        
        if not data:
            app_metrics['api_errors'].labels(error_type='no_data').inc()
            return jsonify({"error": "No data provided"}), 400
        
        # Track transaction amount if available
        if 'amt' in data:
            app_metrics['transaction_amount_histogram'].observe(float(data['amt']))
        
        # Track transaction category if available
        if 'category' in data:
            app_metrics['transaction_categories'].labels(category=data['category']).inc()
        
        # Process data with timing
        process_start_time = time.time()
        processed_data, exists = process_json_and_search(data)
        app_metrics['data_processing_time'].observe(time.time() - process_start_time)
        
        print(processed_data)
        
        # Get prediction if this isn't a first time transaction
        if not processed_data.empty:
            app_metrics['existing_users'].inc()
            
            # Model prediction with timing
            model_start_time = time.time()
            score = predict_fraud(processed_data, exists)
            app_metrics['model_prediction_time'].observe(time.time() - model_start_time)
            
            fraud_score = float(score[-1])
            
            # Update metrics based on prediction
            app_metrics['fraud_score_distribution'].observe(fraud_score)
            app_metrics['current_fraud_score'].set(fraud_score/100)
            
            # Categorize risk levels
            if fraud_score > 65:
                app_metrics['high_risk_transactions'].inc()
                app_metrics['fraud_predictions_total'].labels(prediction_result='high_risk', status='existing_user').inc()
            elif fraud_score > 35:
                app_metrics['medium_risk_transactions'].inc()
                app_metrics['fraud_predictions_total'].labels(prediction_result='medium_risk', status='existing_user').inc()
            else:
                app_metrics['low_risk_transactions'].inc()
                app_metrics['fraud_predictions_total'].labels(prediction_result='low_risk', status='existing_user').inc()
            
            return jsonify({
                "fraud_probability": fraud_score,
                "status": "success",
                "processing_time": time.time() - prediction_start_time
            })
        
        # First time user
        app_metrics['first_time_users'].inc()
        app_metrics['fraud_predictions_total'].labels(prediction_result='first_time_user', status='new_user').inc()
        app_metrics['current_fraud_score'].set(1.0)
        
        return jsonify({
            "fraud_probability": 1.0,
            "status": "success",
            "processing_time": time.time() - prediction_start_time
        })
        
    except Exception as e:
        app_metrics['api_errors'].labels(error_type='prediction_error').inc()
        return jsonify({
            "error": str(e),
            "status": "failed",
            "processing_time": time.time() - prediction_start_time
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)