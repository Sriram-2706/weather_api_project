from flask import Flask, jsonify, request, render_template
from .data_cleaner import clean_data
from .db_manager import init_db, query_weather, query_temp_stats
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

@app.route('/weather')
def weather_details():
    month = request.args.get('month')
    date = request.args.get('date')
    return jsonify(query_weather(month, date))

@app.route('/temperature-stats')
def temp_stats():
    year = request.args.get('year')
    if not year:
        return jsonify({"error": "year parameter required"}), 400
    return jsonify(query_temp_stats(year))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
