stock_list = []

with open("leverage_5x_stocks.txt", "r") as file:  
    for line in file:
        symbol = line.strip()
        if symbol != "":
            stock_list.append(symbol)

# print(stock_list) 
# print(len(stock_list))        




import logging
import os
import json
from kiteconnect import KiteConnect, KiteTicker
from datetime import datetime, timedelta
# import pandas as pd
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

import time
from concurrent.futures import ThreadPoolExecutor

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


# # Print the start time
# start_time = time.time()  # Record the start time
# print(f"Start time: {time.ctime(start_time)}")

# # Function to fetch market depth for a symbol
# def fetch_market_depth(symbol):
#     try:
#         quote_data = kite.quote(f"NSE:{symbol}")
#         buy_quantity = quote_data[f'NSE:{symbol}']['buy_quantity']
#         sell_quantity = quote_data[f'NSE:{symbol}']['sell_quantity']
#         # print(f"{symbol}: Buy Quantity: {buy_quantity}, Sell Quantity: {sell_quantity}")
#     except Exception as e:
#         print(f"Error fetching market depth for {symbol}: {e}")

# # Use ThreadPoolExecutor to fetch data for all symbols concurrently
# with ThreadPoolExecutor(max_workers=5) as executor:
#     executor.map(fetch_market_depth, stock_list)

# # Calculate and print the completion time
# end_time = time.time()  # Record the end time
# elapsed_time = end_time - start_time  # Calculate the elapsed time
# print(f"End time: {time.ctime(end_time)}")
# print(f"Total execution time: {elapsed_time:.2f} seconds")


# # Print the start time
# start_time = time.time()  # Record the start time
# print(f"Start time: {time.ctime(start_time)}")

stock_list= ['WIPRO']

for symbol in stock_list:
    try:
        # Fetch market depth data
        quote_data = kite.quote(f"NSE:{symbol}")
        buy_quantity=quote_data[f'NSE:{symbol}']['buy_quantity']
        sell_quantity=quote_data[f'NSE:{symbol}']['sell_quantity']

        print(buy_quantity , sell_quantity)
        print((buy_quantity / sell_quantity))

    except Exception as e:
        print(f"Error fetching market depth for {symbol}: {e}")


# # Calculate and print the completion time
# end_time = time.time()  # Record the end time
# elapsed_time = end_time - start_time  # Calculate the elapsed time
# print(f"End time: {time.ctime(end_time)}")
# print(f"Total execution time: {elapsed_time:.2f} seconds")