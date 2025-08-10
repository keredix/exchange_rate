import requests
import csv
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


def main():
    get_data()


# Function to get data from the API
def get_data():

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    # Check status code of the request
    if response.status_code == 200:
        data = json.loads(json.dumps(response.json()))
        exchange_rate = data.get("conversion_rates", {})
        return exchange_rate
    else:
        print(f"Request failed with status code {response.status_code}")

main()