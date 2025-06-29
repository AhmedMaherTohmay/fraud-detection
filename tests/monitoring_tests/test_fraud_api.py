# tests/monitoring_tests/test_fraud_api.py
import requests
import json
import time
from datetime import datetime
from pathlib import Path
import sys

class FraudAPITester:
    def __init__(self, api_url="http://localhost:5000/predict"):
        self.api_url = api_url
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "generated_data"
        
        # Test statistics
        self.stats = {
            'successful_requests': 0,
            'failed_requests': 0,
            'total_fraud_score': 0,
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'response_times': [],
            'errors': []
        }
    
    def check_api_status(self):
        """Check if the API is running"""
        try:
            response = requests.get(self.api_url.replace('/predict', '/'))
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def send_transaction(self, transaction_file, transaction_num):
        """Send a single transaction to the fraud API"""
        
        try:
            # Read transaction data
            with open(transaction_file, 'r') as f:
                transaction_data = json.load(f)
            
            print(f"📊 Transaction {transaction_num}/20")
            print(f"   🕐 Time: {transaction_data['trans_date_trans_time']}")
            print(f"   🏷️  Category: {transaction_data['category']}")
            print(f"   💰 Amount: ${transaction_data['amt']}")
            print(f"   💳 Card: ***{str(transaction_data['cc_num'])[-4:]}")
            
            # Send request
            start_time = time.time()
            response = requests.post(self.api_url, json=transaction_data, timeout=30)
            response_time = time.time() - start_time
            self.stats['response_times'].append(response_time)
            
            if response.status_code == 200:
                result = response.json()
                fraud_prob = result.get('fraud_probability', 0)
                status = result.get('status', 'unknown')
                user_type = result.get('user_type', 'unknown')
                
                # Determine risk level
                if fraud_prob >= 65:
                    risk_level = "🔴 HIGH RISK"
                    self.stats['high_risk_count'] += 1
                elif fraud_prob >= 35:
                    risk_level = "🟡 MEDIUM RISK"
                    self.stats['medium_risk_count'] += 1
                else:
                    risk_level = "🟢 LOW RISK"
                    self.stats['low_risk_count'] += 1
                
                print(f"   ✅ Status: {status}")
                print(f"   🎯 Fraud Score: {fraud_prob:.3f}")
                print(f"   📈 Risk Level: {risk_level}")
                print(f"   👤 User Type: {user_type}")
                print(f"   ⏱️  Response Time: {response_time:.3f}s")
                
                self.stats['successful_requests'] += 1
                self.stats['total_fraud_score'] += fraud_prob
                
                return True, fraud_prob
                
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"   ❌ Error: {error_msg}")
                self.stats['failed_requests'] += 1
                self.stats['errors'].append(error_msg)
                return False, 0
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network Error: {e}"
            print(f"   ❌ {error_msg}")
            self.stats['failed_requests'] += 1
            self.stats['errors'].append(error_msg)
            return False, 0
        except Exception as e:
            error_msg = f"Unexpected Error: {e}"
            print(f"   ❌ {error_msg}")
            self.stats['failed_requests'] += 1
            self.stats['errors'].append(error_msg)
            return False, 0
    
    def run_test_suite(self, transaction_count=20, delay=1):
        """Run the complete test suite"""
        
        print("🚀 Starting Fraud Detection API Test Suite")
        print("=" * 60)
        
        # Check if API is running
        if not self.check_api_status():
            print("❌ API is not running! Please start your Flask app first.")
            print("   Run: python app.py")
            return False
        
        print("✅ API is running")
        
        # Check if test data exists
        if not self.data_dir.exists() or not any(self.data_dir.glob("transaction_*.json")):
            print("❌ Test data not found! Generating test data...")
            from .generate_test_data import FraudTestDataGenerator
            generator = FraudTestDataGenerator()
            generator.generate_transactions(transaction_count)
        
        # Run tests
        for i in range(1, transaction_count + 1):
            transaction_file = self.data_dir / f"transaction_{i:02d}.json"
            
            if not transaction_file.exists():
                print(f"❌ Transaction file {transaction_file} not found!")
                continue
                
            self.send_transaction(transaction_file, i)
            print("-" * 60)
            
            # Wait before next request (except for the last one)
            if i < transaction_count:
                time.sleep(delay)
        
        # Print summary
        self.print_summary()
        return True
    
    def print_summary(self):
        """Print test summary statistics"""
        total_requests = self.stats['successful_requests'] + self.stats['failed_requests']
        avg_response_time = sum(self.stats['response_times']) / len(self.stats['response_times']) if self.stats['response_times'] else 0
        avg_fraud_score = self.stats['total_fraud_score'] / self.stats['successful_requests'] if self.stats['successful_requests'] > 0 else 0
        
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"📈 Total Requests: {total_requests}")
        print(f"✅ Successful: {self.stats['successful_requests']}")
        print(f"❌ Failed: {self.stats['failed_requests']}")
        print(f"📊 Success Rate: {(self.stats['successful_requests']/total_requests)*100:.1f}%" if total_requests > 0 else "N/A")
        print(f"⏱️  Average Response Time: {avg_response_time:.3f}s")
        print(f"🎯 Average Fraud Score: {avg_fraud_score:.3f}")
        print()
        print("🚨 Risk Distribution:")
        print(f"   🔴 High Risk (≥0.7): {self.stats['high_risk_count']}")
        print(f"   🟡 Medium Risk (0.3-0.7): {self.stats['medium_risk_count']}")
        print(f"   🟢 Low Risk (<0.3): {self.stats['low_risk_count']}")
        
        if self.stats['errors']:
            print()
            print("❌ Errors encountered:")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        
        print("=" * 60)
        print("🎯 Monitor your dashboards:")
        print("   📊 Grafana: http://localhost:3000")
        print("   🔍 Prometheus: http://localhost:9090")
        print("   📈 App Metrics: http://localhost:5000/metrics")

if __name__ == "__main__":
    tester = FraudAPITester()
    tester.run_test_suite()