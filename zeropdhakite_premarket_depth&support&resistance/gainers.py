stock_list = []

with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip()
        if symbol != "":
            stock_list.append(symbol)



import logging
import os
import json
from kiteconnect import KiteConnect, KiteTicker
from datetime import datetime, timedelta
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
import json


api_key = ''
secret = ''

kite = KiteConnect(api_key=api_key)

TOKEN_FILE = "access_token.json"

def save_access_token(token):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({"access_token": token}, f)

def load_access_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get("access_token")
    return None


def authenticate():
    access_token = load_access_token()
    if access_token:
        kite.set_access_token(access_token)
        try:
            kite.margins() 
        except Exception as e:
            logging.warning("Access token may be invalid, re-authenticating...")
            return get_access_token() 
    else:
        return get_access_token()

def get_access_token():
    print("Go to the following URL to authorize:")
    print(kite.login_url())
    request_token = input("Enter the request token: ")
    data = kite.generate_session(request_token, api_secret=secret)
    kite.set_access_token(data["access_token"])
    save_access_token(data["access_token"])
  

authenticate()


# Loop through the stock list and fetch data



result = []
for symbol in stock_list[0:1]:
    try:
        # Fetch historical data
        data = kite.historical_data(
            instrument_token=kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"],
            from_date='2024-12-30',
            to_date='2024-12-30',
            interval='2minute',
        )
        # print(data[0])
        change = data[0]['close'] - data[0]['open']
        change_percentage = (change / data[0]['open']) * 100 
        result.append({'symbol':symbol , 'change_percentage': round(change_percentage,2)})
        
        
        # print(result)
        # print(change)
        # print(symbol)
        # df = pd.DataFrame(data)
        # df['symbol'] =symbol
        # change = df['close']- df['open']
        # df['percentage_change'] =round((change/df['open']) *100,2)


    except Exception as e:
        print(e)


# After the loop, sort the list by 'change_percentage' in descending order
result_sorted = sorted(result, key=lambda x: x['change_percentage'], reverse=True)

# Print the sorted result
for item in result_sorted:
    print(f"Symbol: {item['symbol']}, Change Percentage: {item['change_percentage']}%")