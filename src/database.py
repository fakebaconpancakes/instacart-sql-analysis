import sqlite3
import pandas as pd
import os

def get_db_connection():
    return sqlite3.connect('data/instacart.db')

def execute_query(query: str) -> pd.DataFrame:
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def read_sql_file(file_name: str) -> str:
    file_path = os.path.join('queries',file_name)
    with open(file_path, 'r') as f:
        return f.read()