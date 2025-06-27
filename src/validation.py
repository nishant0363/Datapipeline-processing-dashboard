import duckdb
import pandas as pd

def validate_and_profile(df):
    # 🛠️ Normalize timezone: remove tz info for DuckDB compatibility
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(None)

    con = duckdb.connect()
    con.register('sensor_data', df)

    report = con.execute("""
        SELECT
            reading_type,
            COUNT(*) AS total_records,
            SUM(CASE WHEN anomalous_reading THEN 1 ELSE 0 END)*100.0/COUNT(*) AS anomaly_pct,
            SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END)*100.0/COUNT(*) AS missing_pct
        FROM sensor_data
        GROUP BY reading_type
    """).fetchdf()

    # Gaps Detection using Pandas
    df['hour'] = df['timestamp'].dt.floor('h')
    gaps_list = []

    for sensor in df['sensor_id'].unique():
        df_sensor = df[df['sensor_id'] == sensor]
        all_hours = pd.date_range(df_sensor['hour'].min(), df_sensor['hour'].max(), freq='h')

        actual_hours = df_sensor['hour'].unique()
        missing = len(set(all_hours) - set(actual_hours))
        gaps_list.append({'sensor_id': sensor, 'missing_hours': missing})

    gaps = pd.DataFrame(gaps_list)
    gaps.to_csv("data/data_gaps_report.csv", index=False)

    report.to_csv("data/data_quality_report.csv", index=False)
    return report, gaps
