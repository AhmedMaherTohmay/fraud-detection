import requests
import json
import time

# Test data
test_transaction = {
    "trans_date_trans_time": "2020-06-24 12:14:33",
        "cc_num": "3573030041201292",
        "category": "personal_care",
        "amt": 29.84,
        "lat": 40.3207,
        "long": -110.4360,
        "merch_lat": 39.450498,
        "merch_long": -109.960431
}

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Fraud Detection API...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
    
    # Test prediction
    try:
        payload = [None, None, test_transaction]
        response = requests.post(
            f"{base_url}/predict",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Fraud Score: {result['fraud_probability']}")
            print(f"   Is Fraud: {result['is_fraud']}")
            print(f"   Risk Level: {result['risk_level']}")
    except Exception as e:
        print(f"❌ Prediction Failed: {e}")
    
    # Wait a bit for metrics to be recorded
    time.sleep(2)
    
    # Test stats
    try:
        response = requests.get(f"{base_url}/stats")
        print(f"✅ Stats: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total Predictions: {stats['total_predictions']}")
            print(f"   Fraud Rate: {stats.get('current_fraud_rate', 0)}%")
    except Exception as e:
        print(f"❌ Stats Failed: {e}")
    
    print(f"\n🌐 Visit http://localhost:5000/dashboard to see the web interface!")

if __name__ == "__main__":
    test_api()
    test_api()
    test_api()
    test_api()
    test_api()
    test_api()
    test_api()
    