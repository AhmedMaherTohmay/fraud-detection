import pymysql
import pandas as pd
from src.config import DB_CONFIG

class DBConnector:
    def __init__(self):
        self.connection = pymysql.connect(**DB_CONFIG)
    
    def fetch_transactions(self, cc_num, hours=24):
        """Fetch transactions for a card in last X hours"""
        query = f"""
        SELECT * FROM transactions 
        WHERE cc_num = %s 
        AND trans_date_trans_time >= NOW() - INTERVAL {hours} HOUR
        ORDER BY trans_date_trans_time DESC
        """
        return pd.read_sql(query, self.connection, params=(cc_num,))
    
    def close(self):
        self.connection.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    with DBConnector() as db:
        # Get last 24h for specific card
        transactions = db.fetch_transactions(cc_num='1234567890123456')
    
    print(transactions)