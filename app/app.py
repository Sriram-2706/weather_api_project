from flask import Flask, jsonify, request, render_template
from .data_cleaner import clean_data
from .db_manager import (
    init_db, query_weather_date, weather_first_occurrence,
    weather_month_year, weather_month_analysis, query_temp_stats
)
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/init')
def initialize():
    df = clean_data()
    rows = init_db()
    return jsonify({"message": "Database initialized successfully", "rows": rows})

@app.route('/weather-date')
def weather_by_date():
    date = request.args.get('date')
    data = query_weather_date(date)
    return jsonify(data)

@app.route('/weather-first-occurrence')
def first_occurrence():
    month = request.args.get('month')
    data = weather_first_occurrence(month)
    return jsonify(data)

@app.route('/weather-month-analysis')
def month_analysis():
    month = request.args.get('month')
    data = weather_month_analysis(month)
    return jsonify(data)

@app.route('/weather-month-year')
def month_year_data():
    month = request.args.get('month')
    year = request.args.get('year')
    data = weather_month_year(month, year)
    return jsonify(data)

@app.route('/temperature-stats')
def temp_stats():
    year = request.args.get('year')
    data = query_temp_stats(year)
    return jsonify(data)

def startup_db_init():
    db_path = "../data/weather.db"
    if not os.path.exists(db_path):
        print("⚙️ Initializing database before server start...")
        try:
            with app.app_context():
                initialize()
            print("✅ Database initialized successfully.")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
    else:
        print("✅ Database already exists, skipping init.")

if __name__ == '__main__':
    with app.app_context():
        startup_db_init()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
