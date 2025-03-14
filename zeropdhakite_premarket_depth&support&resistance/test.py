import json
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

list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip()
        if symbol != "":
            list_of_stocks.append(symbol)


import time
start_time = time.time()  # Record the start time
print(f"Start time: {time.ctime(start_time)}")

import asyncio
import concurrent.futures

li =[]

def fetch_data(symbol):
    try:
        token = kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"]
        data = kite.historical_data(
            instrument_token=token,
            from_date='2024-12-24',
            to_date='2024-12-24',
            interval='3minute')
        li.append({'symol':symbol, 'high':data[-1]['high'] , 'low': data[-1]['low'] })
        return symbol, data
    except Exception as e:
        print(e)
        return symbol, None

async def fetch_all_stocks(symbols):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_data, symbol) for symbol in symbols]
        return await asyncio.gather(*tasks)

start_time = time.time()
loop = asyncio.get_event_loop()
results = loop.run_until_complete(fetch_all_stocks(list_of_stocks))

end_time = time.time()
print(f"Total execution time: {end_time - start_time:.2f} seconds")

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time
print(f"End time: {time.ctime(end_time)}")
print(f"Total execution time: {elapsed_time:.2f} seconds")

