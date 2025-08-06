# Function that collects price of any coin for any currency from CoinGecko
# %% 
# Packages for debug cells 
from dotenv import load_dotenv
import os 
import requests
load_dotenv()
api_key  = os.getenv("CG_API_KEY")

from price import coin_price

if __name__ == "__main__":

    coinID = "bitcoin" #Variable
    currency = "gbp" #Variable

    Price = coin_price(coinID, currency)
    print(f"Current {coinID.capitalize()} price in {currency.upper()} = {Price}")



# Another function using a different endpoint to find price, market cap and volume. 
from dotenv import load_dotenv
import os 
import requests
load_dotenv()
api_key  = os.getenv("CG_API_KEY")

def coin_stats(coinID, currency):

        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {"x-cg-demo-api-key": api_key}

        params = {
        'ids': coinID,          
        'vs_currency': currency   
    }

        response = requests.get(url, headers=headers, params=params)

        return response.json()

coins = ["bitcoin", "hedera-hashgraph", "solana"]

for coin in coins:                          
     print(coin_stats(coin, "gbp"))        # Applies function to multiple coins 


# %%
# Code for importing portfolio via exchange csv


import csv

CSVS = ["2021CB.csv", "2022CB.csv", "2023CB.csv", "2024CB.csv" , "2025CB.csv"]

allData = []

for CSV in CSVS:                            # Read all csv files and store all rows in allData
      with open(CSV, "r") as file:
            reader = csv.DictReader(file) 
            for row in reader:
                next(file)  # Skip row 1
                next(file)  # Skip row 2

                allData.append(row) 
