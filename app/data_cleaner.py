import pandas as pd
import numpy as np
from .config import RAW_DATA_PATH, CLEANED_DATA_PATH

def clean_data():
    df = pd.read_excel(RAW_DATA_PATH)
    df.replace(['Unknown', 'unknown', 'N/A', 'n/a', 'NULL', 'null', ' ', ''], np.nan, inplace=True)

    num_cols = ['_tempm', '_hum', '_pressurem', '_heatindexm', '_dewptm']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    df.loc[(df['_pressurem'] < 950) | (df['_pressurem'] > 1050), '_pressurem'] = np.nan
    df.loc[(df['_hum'] < 0) | (df['_hum'] > 100), '_hum'] = np.nan
    df.loc[(df['_tempm'] < -10) | (df['_tempm'] > 50), '_tempm'] = np.nan
    df.loc[(df['_heatindexm'] < -10) | (df['_heatindexm'] > 60), '_heatindexm'] = np.nan

    df['_conds'] = df['_conds'].astype(str).str.strip().str.title().replace({'Unknown': 'Unspecified'})
    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], format='%Y%m%d-%H:%M', errors='coerce')

    df['Year'] = df['datetime_utc'].dt.year
    df['Month'] = df['datetime_utc'].dt.month
    df['Date'] = df['datetime_utc'].dt.date
    df['Time'] = df['datetime_utc'].dt.strftime('%H:%M')

    df.to_excel(CLEANED_DATA_PATH, index=False)
    print(f"✅ Cleaned data saved to {CLEANED_DATA_PATH} (NaNs preserved)")
    return df
