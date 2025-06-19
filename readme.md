# Fraud Detection API

A real-time system that detects suspicious credit card transactions using machine learning.

## 🔧 Setup

1. **Install requirements**:

   ```bash
   pip install -r requirements.txt
   ```
2. **Configure the database**:

   - Edit `src/config/database.py` with your credentials

## 🚀 Quick Start

1. **Start the API**:

   ```bash
   python src/main/app.py
   ```
2. **Test with sample data**:

   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test_data.json
   ```

## 💻 How It Works

1. Receives transaction data via API
2. Checks similar transactions from last 24h
3. Processes through ML model
4. Returns fraud probability (0-100)

## 📌 Requirements

- Python 3.8+
- PSQL
- MLflow (for model tracking)

###  Key Features of This Version:

1. **Minimalist Design** - Only essential information
2. **Visual Hierarchy** - Emojis and spacing for readability
3. **Action-Oriented** - Focuses on "how to use" rather than theory
4. **Technical Clarity** - Explains what each folder does simply
