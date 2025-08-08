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
        next(file)  # Skip row 1
        next(file)  # Skip row 2
        reader = csv.DictReader(file) 
        for row in reader:
                allData.append(row) 

# %%
# Reading transaction data to reconstruct total holdings 
import numpy as np
#Empty dicts
holdings = {}
invested = {}


import re

for row in allData:
    asset = row['Asset']
    type = row["Transaction Type"]
    qty = np.round(float(row["Quantity Transacted"]),9) # Round to 9 dp to ensure accuracy
    pricenull = row["Price at Transaction"]
    clean_price = pricenull.replace("£", "").replace("Â", "").strip()  #Removes symbols for float conversion
    price = float(clean_price)
    note = row["Fees and/or Spread"]
      
    if type in ['Buy', 'Staking Income', 'Inflation Reward','Deposit', 'Sell', 'Pro Withdrawal','Pro Deposit', 'Reward Income', 'Receive', 'Withdrawal' , 'Exchange Deposit']:   #Adding all buys to dict
         if asset not in holdings:
              holdings[asset] = 0
         holdings[asset] += qty
    if type in ['Buy', 'Staking Income', 'Inflation Reward', 'Reward Income']:
         if asset not in invested:
              invested[asset] = 0
         invested[asset] += np.round(price*qty,2)
         
    if type == 'Convert' and "Converted" in note:     #Computing notes column in order to extract information
                            
         
         matches = re.findall(r'([\d.]+)\s+([A-Z]+)', note)
         if len(matches) == 2:
              
            (from_amount_s, from_asset), (to_amount_s, to_asset) = matches
            from_amount = float(from_amount_s)
            to_amount = float(to_amount_s)
           
            if from_asset not in holdings:
                holdings[from_asset] = 0
            holdings[from_asset] -= from_amount
            
            if to_asset not in holdings:
                holdings[to_asset] = 0
            holdings[to_asset] += to_amount


for asset, qty in holdings.items():
    print(f'Quantity of {asset}, {np.round(qty, 8)}')
for asset, qty in invested.items():
     print(f'Total Invested (All Time) {asset}, £{np.round(qty, 2)} ')
# %%