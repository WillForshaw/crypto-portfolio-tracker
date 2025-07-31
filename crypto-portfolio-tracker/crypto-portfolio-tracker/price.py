#Get crypto prices using CoinGecko API
import requests 
import os 
from dotenv import load_dotenv

load_dotenv()
api_key  = os.getenv("CG_API_KEY")

# simple function to get price of a sigle coin using api in order to test api and get familiar
def coin_price(coinID, currency):

    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {
        "x-cg-demo-api-key": api_key
    }

    params = {
        'ids': coinID,          
        'vs_currencies': currency   
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()

x = coin_price('bitcoin', 'usd')
print(x)