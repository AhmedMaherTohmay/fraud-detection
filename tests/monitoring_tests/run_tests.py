#!/usr/bin/env python3
# tests/monitoring_tests/run_tests.py

import argparse
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from generate_test_data import FraudTestDataGenerator
from test_fraud_api import FraudAPITester

def main():
    parser = argparse.ArgumentParser(description='Fraud Detection API Test Suite')
    parser.add_argument('--generate-only', action='store_true', 
                       help='Only generate test data, don\'t run tests')
    parser.add_argument('--test-only', action='store_true',
                       help='Only run tests, don\'t generate data')
    parser.add_argument('--count', type=int, default=20,
                       help='Number of transactions to generate/test (default: 20)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--url', type=str, default='http://localhost:5000/predict',
                       help='API URL to test (default: http://localhost:5000/predict)')
    parser.add_argument('--clean', action='store_true',
                       help='Clean up generated test data')
    parser.add_argument('--bash-style', action='store_true',
                       help='Run in bash-style output mode')
    
    args = parser.parse_args()
    
    print("🧪 Fraud Detection API Test Suite")
    print("=" * 50)
    
    generator = FraudTestDataGenerator()
    tester = FraudAPITester(args.url)
    
    # Clean up if requested
    if args.clean:
        generator.clean_generated_data()
        print("✅ Cleanup complete")
        return
    
    # Generate data
    if not args.test_only:
        print("📝 Generating test data...")
        generator.generate_transactions(args.count)
        print()
    
    # Run tests
    if not args.generate_only:
        if args.bash_style:
            # Import and run bash-style test
            from test_fraud_api_bash import run_bash_style_test
            success = run_bash_style_test()
        else:
            print("🚀 Running API tests...")
            success = tester.run_test_suite(args.count, args.delay)
        
        if not success:
            sys.exit(1)
    
    print("✅ All operations completed successfully!")

if __name__ == "__main__":
    main()