from flask import Flask, jsonify
import sqlite3

# Initialize the Flask application.
app = Flask(__name__)

DB_FILE = "rates.db"
# Fetches the data from DB
def get_rates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f'SELECT date, currency, rate FROM rates ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()

    # Transform for better readibility for the API
    return [
        {"date": row[0], "currency": row[1], "rate": row[2]}
        for row in rows
    ]

# GET API
@app.route('/api/rates/USD', methods=['GET'])
def get_items():
    data = get_rates()
    return jsonify(data)
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)