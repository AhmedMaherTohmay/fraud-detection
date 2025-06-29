# For Monitoring services
A real-time system that detects suspicious credit card transactions using machine learning.

## 🔧 Setup

1. SETUP MONITORING : run setup.py with the appropriate function Whether install (to install requirements)/ start (to start monitoring services) /stop (to stop monitoring services)
2. RUN TESTING : from tests run generate_test_data.py to make random test json files followed up bu running run_tests.py to post to the api and test things out
3. API : Run metrics_app.py (monitoring configured app.py/testing phases so it wasn't pushed into the main app.py)

## Quick Start Commands (if you're lazy~) ##

## installing and starting monitoring services 
1. python src/monitoring/setup.py install
2. python src/monitoring/setup.py start
3. python src/monitoring/setup.py stop

## Running the API
1. python metrics_app.py

## Running Test
1. python tests/monitoring_tests/generate_test_data.py
2. python tests/monitoring_tests/run_tests.py

## yey~