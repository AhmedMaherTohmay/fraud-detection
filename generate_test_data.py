import json
import datetime
import random

# Base transaction data
base_transaction = {
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
categories = [
    "electronics", "grocery_pos", "gas_transport", "entertainment", 
    "personal_care", "health_fitness", "food_dining", "shopping_net",
    "travel", "kids_pets", "home", "automotive", "miscellaneous",
    "shopping_pos", "online", "pharmacy", "clothing", "restaurant",
    "hotel", "transport"
]

# Amounts to vary (realistic transaction amounts)
amounts = [
    15.99, 45.50, 89.99, 125.00, 200.75, 67.25, 33.99, 78.50,
    159.99, 95.25, 42.75, 185.00, 220.99, 55.50, 103.25,
    175.99, 88.75, 245.00, 66.99, 134.50
]

# Generate 20 transactions
transactions = []
base_time = datetime.datetime.strptime("2020-06-23 16:02:35", "%Y-%m-%d %H:%M:%S")

for i in range(20):
    # Increment time by 1 second
    current_time = base_time + datetime.timedelta(seconds=i)
    
    transaction = {
        "trans_date_trans_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "cc_num": base_transaction["cc_num"] + i,  # Increment card number
        "category": categories[i],
        "amt": amounts[i],
        "lat": round(base_transaction["lat"] + random.uniform(-0.1, 0.1), 4),  # Slight location variation
        "long": round(base_transaction["long"] + random.uniform(-0.1, 0.1), 4),
        "merch_lat": round(base_transaction["merch_lat"] + random.uniform(-0.1, 0.1), 4),
        "merch_long": round(base_transaction["merch_long"] + random.uniform(-0.1, 0.1), 4)
    }
    
    transactions.append(transaction)
    
    # Save individual transaction files
    with open(f'transaction_{i+1:02d}.json', 'w') as f:
        json.dump(transaction, f, indent=4)

# Save all transactions in one file
with open('all_transactions.json', 'w') as f:
    json.dump(transactions, f, indent=4)

print("Generated 20 transaction files (transaction_01.json to transaction_20.json)")
print("Also created all_transactions.json with all transactions")