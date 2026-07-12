import sqlite3
import pandas as pd
import os

def run_etl():
    if not os.path.exists('data/data_csv'):
        print("ERROR: csv files are missing!")
        return
    
    conn = sqlite3.connect("data/instacart.db")

    for filename in os.listdir('data/data_csv'):
        if filename.endswith('.csv'):
            table_name = filename.replace('.csv','')
            file_path = os.path.join('data/data_csv', filename)

            print(f"{filename} is loaded to {table_name}")

            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print("All of the data has successfully been loaded!")

if __name__ == "__main__":
    run_etl()