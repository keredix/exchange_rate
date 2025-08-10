import requests
import csv
import json
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
api_key = os.getenv("API_KEY")


def main():
    transformed_exchange_rates = get_data()
    load_data_to_db(transformed_exchange_rates)


# Function to get data from the API
def get_data():

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    # Check status code of the request
    if response.status_code == 200:
        data = json.loads(json.dumps(response.json()))
        exchange_rates = data.get("conversion_rates", {})
        transformed_exchange_rates = [{'currency': k, 'rate': v} for k, v in exchange_rates.items()]
        return transformed_exchange_rates
    # Return error code if the request fails
    else:
        print(f"Request failed with status code {response.status_code}")


def load_data_to_db(exchange_rates):
    # Connect to database
    sqliteConnection = sqlite3.connect('rates.db')
    cursor = sqliteConnection.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS exchange_rates (id INTEGER PRIMARY KEY, currency TEXT UNIQUE, rate REAL)')

    # Load the data to DB
    for row in exchange_rates:
        cursor.execute('INSERT INTO exchange_rates (currency, rate) VALUES (?, ?) ON CONFLICT(currency) DO UPDATE SET rate = excluded.rate', (row['currency'], row['rate']))

    # Commit and close
    sqliteConnection.commit()
    sqliteConnection.close()

main()