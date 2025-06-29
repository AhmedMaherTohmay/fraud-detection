# tests/monitoring_tests/generate_test_data.py
import json
import datetime
import random
import os
from pathlib import Path

class FraudTestDataGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "generated_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Base transaction data
        self.base_transaction = {
            "trans_date_trans_time": "2020-06-23 16:02:35",
            "cc_num": 4992346398065154184,
            "category": "electronics",
            "amt": 251.75,
            "lat": 40.7128,
            "long": -74.0060,
            "merch_lat": 40.7306,
            "merch_long": -73.9352
        }
        
        # Categories to vary
        self.categories = [
            "electronics" ,"grocery_pos", "gas_transport", "entertainment", 
            "personal_care", "health_fitness", "food_dining", "shopping_net",
            "travel", "kids_pets", "home", "automotive", "miscellaneous",
            "shopping_pos", "online", "pharmacy", "clothing", "restaurant",
            "hotel", "transport"
        ]
        
        # Amounts to vary (realistic transaction amounts)
        self.amounts = [
            251.75
        ]
    
    def generate_transactions(self, count=20):
        """Generate test transactions with incrementing timestamps"""
        transactions = []
        base_time = datetime.datetime.strptime("2020-06-23 16:02:35", "%Y-%m-%d %H:%M:%S")
        
        print(f"🔄 Generating {count} test transactions...")
        
        for i in range(count):
            # Increment time by 1 second
            current_time = base_time + datetime.timedelta(seconds=i)
            
            transaction = {
                "trans_date_trans_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "cc_num": self.base_transaction["cc_num"],
                "category": self.categories[i % len(self.categories)],
                "amt": self.amounts[i % len(self.amounts)],
                "lat": round(self.base_transaction["lat"] + random.uniform(-0.1, 0.1), 4),  # Slight location variation
                "long": round(self.base_transaction["long"],  + random.uniform(-0.1, 0.1), 4),
                "merch_lat": round(self.base_transaction["merch_lat"], + random.uniform(-0.1, 0.1), 4),
                "merch_long": round(self.base_transaction["merch_long"] + random.uniform(-0.1, 0.1), 4)
            }
            
            transactions.append(transaction)
            
            # Save individual transaction files
            transaction_file = self.data_dir / f'transaction_{i+1:02d}.json'
            with open(transaction_file, 'w') as f:
                json.dump(transaction, f, indent=4)
        
        # Save all transactions in one file
        all_transactions_file = self.data_dir / 'all_transactions.json'
        with open(all_transactions_file, 'w') as f:
            json.dump(transactions, f, indent=4)
        
        print(f"✅ Generated {count} transaction files in {self.data_dir}")
        print(f"📁 Individual files: transaction_01.json to transaction_{count:02d}.json")
        print(f"📁 Combined file: all_transactions.json")
        
        return transactions
    
    def clean_generated_data(self):
        """Clean up generated test data"""
        if self.data_dir.exists():
            for file in self.data_dir.glob("*.json"):
                file.unlink()
            print("🧹 Cleaned up generated test data")

if __name__ == "__main__":
    generator = FraudTestDataGenerator()
    generator.generate_transactions(20)