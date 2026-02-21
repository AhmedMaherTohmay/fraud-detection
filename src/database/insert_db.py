import psycopg2
import os
from config.config import DATA_PATH_TRAIN, DB_PARAMS


TEMP_FILE = "temp_batch.csv"  # File we create for COPY

def preprocess_and_copy(limit=100):
    # Write only the desired number of data rows (skip header, drop is_fraud)
    with open(DATA_PATH_TRAIN, 'r') as infile, open(TEMP_FILE, 'w') as outfile:
        header = infile.readline()  # Skip header
        written = 0
        for line_num, line in enumerate(infile, start=2):
            if line.strip() == "":
                continue

            fields = line.strip().split(',')
            if len(fields) != 9:
                print(f"Skipping malformed line {line_num}: {line.strip()}")
                continue

            # Keep only first 8 columns (skip is_fraud), convert sci notation in cc_num
            cc_num = str(int(float(fields[0])))
            out_fields = [cc_num] + fields[1:8]
            outfile.write(','.join(out_fields) + '\n')
            written += 1
            if 0 < limit <= written:
                print(f"Stopped at {written} records (limit reached).")
                break

    # Bulk insert using COPY
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    with open(TEMP_FILE, 'r') as f:
        cur.copy_expert("""
            COPY transactions(cc_num, trans_date_trans_time, category, amt, lat, long, merch_lat, merch_long)
            FROM STDIN
            WITH CSV
        """, f)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {written} records into transactions table (using COPY).")
    os.remove(TEMP_FILE)  # Clean up temp file
    

if __name__ == '__main__':
    preprocess_and_copy()
    
'''
SELECT *
FROM transactions
WHERE cc_num = 3590000000000000
ORDER BY trans_date_trans_time;
'''    

    