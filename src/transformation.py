import pandas as pd
import numpy as np

def preprocess(df):
    df = df.drop_duplicates()
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

    # Fill missing
    df = df.dropna(subset=['value'])

    # Detect outliers
    df['z_score'] = (df['value'] - df['value'].mean()) / df['value'].std()
    df = df[df['z_score'].abs() <= 3]

    return df

def enrich(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date

    # Daily average
    daily_avg = df.groupby(['sensor_id', 'reading_type', 'date'])['value'].mean().reset_index(name='daily_avg')
    df = df.merge(daily_avg, on=['sensor_id', 'reading_type', 'date'], how='left')

    # Sort for rolling
    df = df.sort_values(['sensor_id', 'reading_type', 'timestamp'])

    # 7-day rolling average per sensor_id and reading_type
    df['rolling_avg'] = (
        df
        .set_index('timestamp')
        .groupby(['sensor_id', 'reading_type'])['value']
        .rolling('7D')
        .mean()
        .reset_index(level=[0,1], drop=True)
        .values
    )

    # Calibration (example)
    calibration_params = {'temperature': (1.02, -0.5), 'humidity': (0.98, 1.0)}
    for r_type, (m, c) in calibration_params.items():
        df.loc[df['reading_type'] == r_type, 'value'] = df['value'] * m + c

    # Anomaly detection
    expected_ranges = {
        'temperature': (0, 60),
        'humidity': (0, 100),
        'soil_moisture': (0, 100),
        'light_intensity': (0, 2000)
    }

    def is_anomalous(row):
        rtype = row['reading_type']
        if rtype in expected_ranges:
            lo, hi = expected_ranges[rtype]
            return not (lo <= row['value'] <= hi)
        return False

    df['anomalous_reading'] = df.apply(is_anomalous, axis=1)

    return df
