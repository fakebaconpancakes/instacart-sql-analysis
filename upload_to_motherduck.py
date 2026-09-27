import duckdb
import tomllib

print("Loading MotherDuck token from secrets...")
with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

token = secrets["MOTHERDUCK_TOKEN"]


print("Connecting to MotherDuck cloud...")
md_con = duckdb.connect(f"md:instacart_db?motherduck_token={token}")

sqlite_filename = "data\instacart.db" #database location

print(f"Attaching local database '{sqlite_filename}'...")
md_con.execute(f"ATTACH '{sqlite_filename}' AS local_sqlite (TYPE SQLITE);")

sqlite_tables = md_con.execute("SHOW TABLES FROM local_sqlite;").fetchall() #fetch all data

print(f"Found {len(sqlite_tables)} tables to upload.\n")

#Upload each table to MotherDuck
for (table_name,) in sqlite_tables:
    print(f"Uploading '{table_name}' to MotherDuck...")
    md_con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM local_sqlite.{table_name};")
    print(f"'{table_name}' uploaded successfully!")

print("\n All tables uploaded to MotherDuck successfully!")