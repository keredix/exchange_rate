import requests
import json
import os
import sqlite3
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
        

# Function to get data from the API and transform them
def get_data():
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    # Check status code of the request
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    data = json.loads(json.dumps(response.json()))
    exchange_rates = data.get("conversion_rates", {})
    transformed_exchange_rates = [{'date': "2025-08-13", 'currency': k, 'rate': v} for k, v in exchange_rates.items()]
    return transformed_exchange_rates

# Init database
def init_db():
    # Connect to DB
    conn = sqlite3.connect('rates.db')
    cursor = conn.cursor()

    # Create table if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY,
            date TEXT,
            currency TEXT,
            rate REAL,
            UNIQUE(date, currency)
        )
    """)

# Func to load data to DB
def load_data_to_db(exchange_rates):
    # Connect to DB
    sqliteConnection = sqlite3.connect('rates.db')
    cursor = sqliteConnection.cursor()

    # Load the data to DB
    for row in exchange_rates:
        sql_insert = f'INSERT INTO rates (date, currency, rate) VALUES (?, ?, ?) ON CONFLICT(date, currency) DO UPDATE SET rate = excluded.rate'
        sql_data = (row['date'], row['currency'], row['rate'])
        cursor.execute(sql_insert,sql_data)

    # Commit and close
    sqliteConnection.commit()
    sqliteConnection.close()


if __name__ == "__main__":
    transformed_exchange_rates = get_data()
    init_db()
    load_data_to_db(transformed_exchange_rates)