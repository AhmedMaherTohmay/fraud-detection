# src/monitoring/metrics.py
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

# Global metrics - defined at module level
fraud_predictions_total = Counter(
    'fraud_predictions_total', 
    'Total number of fraud predictions made',
    ['prediction_result', 'status']
)

fraud_score_distribution = Histogram(
    'fraud_score_distribution',
    'Distribution of fraud scores',
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
)

transaction_amount_histogram = Histogram(
    'transaction_amount_histogram',
    'Distribution of transaction amounts',
    buckets=(0, 10, 50, 100, 500, 1000, 5000, 10000, float('inf'))
)

model_prediction_time = Histogram(
    'model_prediction_time_seconds',
    'Time taken for model prediction'
)

data_processing_time = Histogram(
    'data_processing_time_seconds',
    'Time taken for data processing'
)

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

first_time_users = Counter(
    'first_time_users_total',
    'Total number of first-time users'
)

existing_users = Counter(
    'existing_users_total',
    'Total number of existing users'
)

high_risk_transactions = Counter(
    'high_risk_transactions_total',
    'Number of high-risk transactions (>0.7 fraud score)'
)

medium_risk_transactions = Counter(
    'medium_risk_transactions_total',
    'Number of medium-risk transactions (0.3-0.7 fraud score)'
)

low_risk_transactions = Counter(
    'low_risk_transactions_total',
    'Number of low-risk transactions (<0.3 fraud score)'
)

api_errors = Counter(
    'api_errors_total',
    'Total API errors',
    ['error_type']
)

current_fraud_score = Gauge(
    'current_fraud_score',
    'Latest fraud score processed'
)

transaction_categories = Counter(
    'transaction_categories_total',
    'Total transactions by category',
    ['category']
)

def init_metrics(app):
    """Initialize all Prometheus metrics for the Flask app."""
    
    @app.route('/metrics')
    def metrics():
        """Endpoint to expose Prometheus metrics."""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
    @app.before_request
    def before_request():
        """Record request start time."""
        from flask import request, g
        g.start_time = time.time()
    
    @app.after_request  
    def after_request(response):
        """Record request metrics."""
        from flask import request, g
        
        # Record request count
        request_count.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
        
        # Record request duration
        if hasattr(g, 'start_time'):
            request_duration.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown'
            ).observe(time.time() - g.start_time)
        
        return response
    
    # Return all metrics as a dictionary for easy access
    return {
        'fraud_predictions_total': fraud_predictions_total,
        'fraud_score_distribution': fraud_score_distribution,
        'transaction_amount_histogram': transaction_amount_histogram,
        'model_prediction_time': model_prediction_time,
        'data_processing_time': data_processing_time,
        'first_time_users': first_time_users,
        'existing_users': existing_users,
        'high_risk_transactions': high_risk_transactions,
        'medium_risk_transactions': medium_risk_transactions,
        'low_risk_transactions': low_risk_transactions,
        'api_errors': api_errors,
        'current_fraud_score': current_fraud_score,
        'transaction_categories': transaction_categories,
        'request_count': request_count,
        'request_duration': request_duration,
    }