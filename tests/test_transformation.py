import pandas as pd
from src.transformation import preprocess, enrich

def test_preprocess():
    df = pd.DataFrame({
        'sensor_id': ['s1']*3,
        'timestamp': ['2023-06-01T00:00:00Z']*3,
        'reading_type': ['temperature']*3,
        'value': [25, 26, 27],
        'battery_level': [3.2, 3.3, 3.1]
    })
    df = preprocess(df)
    assert not df.empty

def test_enrich():
    df = pd.DataFrame({
        'sensor_id': ['s1']*3,
        'timestamp': pd.date_range('2023-06-01', periods=3, freq='H'),
        'reading_type': ['temperature']*3,
        'value': [25, 26, 27],
        'battery_level': [3.2, 3.3, 3.1]
    })
    df = enrich(df)
    assert 'daily_avg' in df.columns
