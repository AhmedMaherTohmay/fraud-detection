#!/usr/bin/env python3
# tests/monitoring_tests/test_fraud_api.sh (Python script)

import requests
import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

def run_bash_style_test():
    """Run fraud detection API test in bash-style output"""
    
    script_dir = Path(__file__).parent
    data_dir = script_dir / "generated_data"
    api_url = "http://localhost:5000/predict"
    
    print("🚀 Starting Fraud Detection API Test Suite")
    print(f"📁 Test directory: {script_dir}")
    print(f"📁 Data directory: {data_dir}")
    print("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding correctly!")
            return False
    except requests.exceptions.RequestException:
        print("❌ API is not running! Please start your Flask app first.")
        print("   Run: python app.py")
        return False
    
    print("✅ API is running and accessible")
    
    # Check if test data exists, generate if not
    if not data_dir.exists() or not any(data_dir.glob("transaction_*.json")):
        print("📝 Test data not found! Generating...")
        from generate_test_data import FraudTestDataGenerator
        generator = FraudTestDataGenerator()
        generator.generate_transactions(20)
    else:
        print("✅ Test data found")
    
    counter = 1
    successful = 0
    failed = 0
    
    print(f"📤 Sending 20 transactions with 1-second intervals...")
    print("=" * 60)
    
    # Loop through all transaction files
    for i in range(1, 21):
        transaction_file = data_dir / f"transaction_{i:02d}.json"
        
        if not transaction_file.exists():
            print(f"❌ Transaction file {transaction_file.name} not found!")
            failed += 1
            continue
        
        print(f"📤 Sending transaction {counter}/20...")
        
        try:
            # Read and send transaction
            with open(transaction_file, 'r') as f:
                transaction_data = json.load(f)
            
            start_time = time.time()
            response = requests.post(api_url, json=transaction_data, timeout=30)
            response_time = time.time() - start_time
            
            print(f"Transaction {counter}:")
            print(f"  📊 Data: {transaction_data['category']} - ${transaction_data['amt']}")
            
            if response.status_code == 200:
                result = response.json()
                fraud_prob = result.get('fraud_probability', 0)
                status = result.get('status', 'unknown')
                
                print(f"  ✅ Status: {response.status_code}")
                print(f"  🎯 Fraud Score: {fraud_prob:.3f}")
                print(f"  ⏱️  Time: {response_time:.3f}s")
                print(f"  📝 Response: {result}")
                successful += 1
            else:
                print(f"  ❌ Status: {response.status_code}")
                print(f"  📝 Response: {response.text}")
                failed += 1
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
        
        print("-" * 40)
        counter += 1
        
        # Wait 1 second before next request (except for the last one)
        if counter <= 20:
            time.sleep(1)
    
    # Final summary
    print("=" * 60)
    print("📊 TEST COMPLETE!")
    print(f"✅ Successful: {successful}/20")
    print(f"❌ Failed: {failed}/20")
    print(f"📈 Success Rate: {(successful/20)*100:.1f}%")
    print("=" * 60)
    print("🎯 Check your monitoring dashboard:")
    print("   📊 Grafana: http://localhost:3000")
    print("   🔍 Prometheus: http://localhost:9090")
    print("   📈 App Metrics: http://localhost:5000/metrics")
    
    return successful == 20

if __name__ == "__main__":
    success = run_bash_style_test()
    sys.exit(0 if success else 1)