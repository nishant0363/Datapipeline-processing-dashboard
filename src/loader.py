import os
import pyarrow as pa
import pyarrow.parquet as pq

def save_to_parquet(df, output_dir="data/processed/"):
    df['date'] = df['timestamp'].dt.date
    for date, group in df.groupby('date'):
        date_str = date.strftime('%Y-%m-%d')
        path = os.path.join(output_dir, f"{date_str}.parquet")
        table = pa.Table.from_pandas(group)
        pq.write_table(table, path, compression='snappy')
