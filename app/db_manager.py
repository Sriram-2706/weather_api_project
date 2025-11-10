import sqlite3, pandas as pd
from datetime import datetime
from .config import CLEANED_DATA_PATH, DB_PATH

def init_db():
    df = pd.read_excel(CLEANED_DATA_PATH)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('weather', conn, if_exists='replace', index=False)
    conn.close()
    return len(df)

def query_weather_date(date):
    conn = sqlite3.connect(DB_PATH)
    q = f"SELECT datetime_utc, Date, Time, _conds, _tempm, _hum, _pressurem, _heatindexm FROM weather WHERE strftime('%Y-%m-%d', Date)='{date}'"
    df = pd.read_sql_query(q, conn)
    conn.close()
    return df.to_dict(orient='records')

def weather_first_occurrence(month):
    conn = sqlite3.connect(DB_PATH)
    q = f"SELECT * FROM weather WHERE Month={int(month)} ORDER BY datetime_utc LIMIT 1"
    df = pd.read_sql_query(q, conn)
    conn.close()
    return df.to_dict(orient='records')

def weather_month_year(month, year):
    conn = sqlite3.connect(DB_PATH)
    q = f"SELECT * FROM weather WHERE Month={int(month)} AND Year={int(year)} ORDER BY datetime_utc"
    df = pd.read_sql_query(q, conn)
    conn.close()
    return df.to_dict(orient='records')

def weather_month_analysis(month):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT _conds, _tempm, Year FROM weather WHERE Month={int(month)}", conn)
    conn.close()
    if df.empty:
        return []
    summary = {
        "condition_counts": df['_conds'].value_counts().to_dict(),
        "temp_min": float(df['_tempm'].min()),
        "temp_max": float(df['_tempm'].max()),
        "temp_median": float(df['_tempm'].median())
    }
    return summary
def query_temp_stats(year):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM weather WHERE Year={int(year)}", conn)
    conn.close()
    if df.empty:
        return [{"message": "No data"}]
    stats = df.groupby('Month')['_tempm'].agg(['max', 'median', 'min']).reset_index()
    return stats.to_dict(orient='records')

