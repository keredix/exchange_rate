import requests
import json
import os
import sqlite3
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def main():
    currency_shortcut = get_currency()
    transformed_exchange_rates = get_data(currency_shortcut)
    load_data_to_db(transformed_exchange_rates,currency_shortcut)

# Function to get currency from user
def get_currency():
    while True:
        try:
            currency_shortcut = str(input("Please enter currency: "))
        except ValueError:
            sys.exit("Please use supported shortcut for currency(example. USD, CZK, EUR)")
        else:
            return currency_shortcut
        

# Function to get data from the API
def get_data(currency_shortcut):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_shortcut}"
    response = requests.get(url)

    # Check status code of the request
    if response.status_code == 200:
        data = json.loads(json.dumps(response.json()))
        exchange_rates = data.get("conversion_rates", {})
        transformed_exchange_rates = [{'date': datetime.today().strftime('%Y-%m-%d'), 'currency': k, 'rate': v} for k, v in exchange_rates.items()]
        return transformed_exchange_rates
    
    elif response.status_code == 404:
        sys.exit("Your request couldn't be completed, please try to use supported shortcut for currency(example. USD, CZK, EUR)")
    
    else:
        sys.exit(f"Request failed with status code {response.status_code}")

# Func to load data to DB
def load_data_to_db(exchange_rates,currency_shortcut):
    # Connect to database
    sqliteConnection = sqlite3.connect('rates.db')
    cursor = sqliteConnection.cursor()

    # Create table
    sql_create = f'CREATE TABLE IF NOT EXISTS "{currency_shortcut}" (id INTEGER PRIMARY KEY, date TEXT, currency TEXT, rate REAL, UNIQUE(date,currency))'
    cursor.execute(sql_create)

    # Load the data to DB
    for row in exchange_rates:
        sql_insert = f'INSERT INTO "{currency_shortcut}" (date, currency, rate) VALUES (?, ?, ?) ON CONFLICT(date, currency) DO UPDATE SET rate = excluded.rate'
        sql_data = (row['date'], row['currency'], row['rate'])
        cursor.execute(sql_insert,sql_data)

    # Commit and close
    sqliteConnection.commit()
    sqliteConnection.close()


main()