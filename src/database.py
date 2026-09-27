import os
import streamlit as st
import duckdb


@st.cache_resource
def get_db_connection():
    token = st.secrets["MOTHERDUCK_TOKEN"]
    return duckdb.connect(f"md:instacart_db?motherduck_token={token}")


def execute_query(sql_query: str):
    con = get_db_connection()
    return con.execute(sql_query).df()


def read_sql_file(file_name: str) -> str:
    file_path = os.path.join("queries", file_name)
    with open(file_path, "r") as f:
        return f.read()