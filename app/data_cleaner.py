import pandas as pd
import numpy as np
from .config import RAW_DATA_PATH, CLEANED_DATA_PATH

def clean_data():
    df = pd.read_csv(RAW_DATA_PATH)
    df.replace(['Unknown','unknown','N/A','n/a','NULL','null',' ',''], np.nan, inplace=True)
    df.drop(columns=['_precipm','_wgustm','_windchillm'], inplace=True, errors='ignore')
    
    for c in ['_tempm','_hum','_pressurem','_heatindexm','_dewptm']:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    df = df[df['_pressurem'].between(950,1050)]
    df = df[df['_hum'].between(0,100)]
    df = df[df['_tempm'].between(-10,50)]

    df.fillna({
        '_tempm': df['_tempm'].median(),
        '_hum': df['_hum'].median(),
        '_pressurem': df['_pressurem'].median(),
        '_heatindexm': df['_heatindexm'].median()
    }, inplace=True)

    df['_conds'] = df['_conds'].astype(str).str.strip().str.title().replace({'Unknown':'Unspecified'})
    
    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], format='%Y%m%d-%H:%M', errors='coerce')
    df['Year'] = df['datetime_utc'].dt.year
    df['Month'] = df['datetime_utc'].dt.month
    df['Date'] = df['datetime_utc'].dt.date

    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"✅ Cleaned data saved to {CLEANED_DATA_PATH}")
    return df
