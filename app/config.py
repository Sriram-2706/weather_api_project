import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

RAW_DATA_PATH = os.path.join(DATA_DIR, 'testset.csv')
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'cleaned_weather.csv')
DB_PATH = os.path.join(DATA_DIR, 'weather.db')
