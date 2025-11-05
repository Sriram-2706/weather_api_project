import sqlite3
import pandas as pd
from .config import CLEANED_DATA_PATH, DB_PATH

def init_db():
    df = pd.read_csv(CLEANED_DATA_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('weather', conn, if_exists='replace', index=False)
    conn.close()
    return len(df)

def query_weather(month=None, date=None):
    conn = sqlite3.connect(DB_PATH)
    q = "SELECT Date, _conds, _tempm, _hum, _pressurem, _heatindexm FROM weather"
    if date:
        q += f" WHERE Date='{date}'"
    elif month:
        q += f" WHERE Month={int(month)}"
    df = pd.read_sql_query(q, conn)
    conn.close()
    return df.to_dict(orient='records')

def query_temp_stats(year):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM weather WHERE Year={int(year)}", conn)
    conn.close()
    stats = df.groupby('Month')['_tempm'].agg(['max','median','min']).reset_index()
    return stats.to_dict(orient='records')
