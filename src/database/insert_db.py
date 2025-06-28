# insert_db.py
import pymysql
import os
from src.config import DATA_PATH_TRAIN, DB_PARAMS

TEMP_FILE = "temp_batch.csv"

def preprocess_and_copy(limit=100):
    with open(DATA_PATH_TRAIN, 'r') as infile, open(TEMP_FILE, 'w') as outfile:
        header = infile.readline()
        written = 0
        for line_num, line in enumerate(infile, start=2):
            if line.strip() == "":
                continue
            fields = line.strip().split(',')
            if len(fields) != 9:
                print(f"Skipping malformed line {line_num}: {line.strip()}")
                continue
            cc_num = str(int(float(fields[0])))
            out_fields = [cc_num] + fields[1:8]
            outfile.write(','.join(out_fields) + '\n')
            written += 1
            if 0 < limit <= written:
                print(f"Stopped at {written} records (limit reached).")
                break

    conn = pymysql.connect(**DB_PARAMS, local_infile=1)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            cc_num BIGINT NOT NULL,
            trans_date_trans_time TIMESTAMP NOT NULL,
            category VARCHAR(50),
            amt DECIMAL(12,2),
            lat DECIMAL(12,6),
            `long` DECIMAL(12,6),
            merch_lat DECIMAL(12,6),
            merch_long DECIMAL(12,6)
        )
    """)

    cur.execute(f"""
        LOAD DATA LOCAL INFILE '{TEMP_FILE}'
        INTO TABLE transactions
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\n'
        (cc_num, trans_date_trans_time, category, amt, lat, `long`, merch_lat, merch_long)
    """)

    conn.commit()
    cur.close()
    conn.close()
    os.remove(TEMP_FILE)
    print(f"Loaded {written} records into transactions table.")

if __name__ == '__main__':
    preprocess_and_copy()