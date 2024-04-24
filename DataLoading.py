import os.path
import sys
import time

import pandas as pd
import sqlite3
import chardet


def process_csv(file_name, table_name, db_filename, chunk_size=10000, conn=None):
    start_time = time.time()
    if not os.path.isfile(file_name):
        print("File not found")
        return
    if conn is None:
        conn = sqlite3.connect(db_filename)
    print("Process Request Received")
    with open(file_name, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    for chunk in pd.read_csv(file_name, chunksize=chunk_size, encoding=encoding):
        chunk.to_sql(table_name, conn, if_exists='replace', index=False)
        print("Data Chunk Processed")
    print("Data Written")
    conn.commit()
    print("Commit Successful")
    conn.close()
    print("Connection Closed")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time is " + str(elapsed_time) + " seconds")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        table_name = file_name.rstrip(".csv")
        db_filename = table_name + '.db'
        process_csv(file_name, table_name, db_filename)
        print("Data Conversion Successful")
    else:
        print("Please provide a CSV File")