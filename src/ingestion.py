import duckdb
import os
import pandas as pd
from glob import glob
from datetime import datetime

def list_parquet_files(path):
    return sorted(glob(os.path.join(path, "*.parquet")))

def read_parquet_with_duckdb(file_path):
    try:
        con = duckdb.connect()
        df = con.execute(f"SELECT * FROM read_parquet('{file_path}')").fetchdf()
        con.close()
        return df
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}")
        return None

def validate_schema(df, required_columns):
    return all(col in df.columns for col in required_columns)

def ingest_files(path="data/raw/"):
    files = list_parquet_files(path)
    required_columns = ['sensor_id', 'timestamp', 'reading_type', 'value', 'battery_level']
    all_data = []

    for file in files:
        df = read_parquet_with_duckdb(file)
        if df is None:
            continue
        if not validate_schema(df, required_columns):
            print(f"[WARNING] Schema mismatch in {file}")
            continue
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)
