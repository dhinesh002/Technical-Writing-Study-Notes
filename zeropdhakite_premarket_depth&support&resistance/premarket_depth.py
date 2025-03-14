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


import json
import pandas as pd
data = []

# Collect market depth data for the first 10 symbols in stock_list
for symbol in stock_list:
    try:
        market_depth = kite.quote("NSE:" + symbol)
        print(market_depth)
        
        # Extract bid and ask data
        bids = market_depth["NSE:" + symbol]["depth"]["buy"]
        asks = market_depth["NSE:" + symbol]["depth"]["sell"]

        # Calculate total bid and total ask
        total_bid = sum(bid['quantity'] for bid in bids)
        total_ask = sum(ask['quantity'] for ask in asks)

        # Calculate imbalance: Total Ask - Total Bid
        imbalance = total_bid - total_ask

        # Extract top bid and ask prices with quantities
        top_bid_price = bids[0]['price'] if bids else None
        top_bid_quantity = bids[0]['quantity'] if bids else None
        top_ask_price = asks[0]['price'] if asks else None
        top_ask_quantity = asks[0]['quantity'] if asks else None

        # Extract number of orders
        bid_orders = sum(bid['orders'] for bid in bids)
        ask_orders = sum(ask['orders'] for ask in asks)

        # Print market depth for the current symbol
        print(f"Market Depth for {symbol}:")
        print(f"Total Bids: {total_bid}")
        print(f"Total Asks: {total_ask}")
        print(f"Imbalance: {imbalance}")
        print(f"Top Bid Price: {top_bid_price} | Quantity: {top_bid_quantity}")
        print(f"Top Ask Price: {top_ask_price} | Quantity: {top_ask_quantity}")
        print(f"Number of Bid Orders: {bid_orders}")
        print(f"Number of Ask Orders: {ask_orders}")

        # Append the data to the list
        data.append({
            'symbol': symbol,
            'total_bid': total_bid,
            'total_ask': total_ask,
            'imbalance': imbalance,
            'top_bid_price': top_bid_price,
            'top_bid_quantity': top_bid_quantity,
            'top_ask_price': top_ask_price,
            'top_ask_quantity': top_ask_quantity,
            'bid_orders': bid_orders,
            'ask_orders': ask_orders
        })

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Sort the data by imbalance (high to low)
sorted_data = sorted(data, key=lambda x: x['imbalance'], reverse=True)

# Write the sorted data into a text file
with open("market_depth_report.txt", "w") as file:
    file.write("Market Depth Report (Sorted by Imbalance from High to Low)\n")
    file.write("=" * 60 + "\n")
    for item in sorted_data:
        file.write(f"Symbol: {item['symbol']}\n")
        file.write(f"Total Bids: {item['total_bid']}\n")
        file.write(f"Total Asks: {item['total_ask']}\n")
        file.write(f"Imbalance: {item['imbalance']}\n")
        file.write(f"Top Bid Price: {item['top_bid_price']} | Quantity: {item['top_bid_quantity']}\n")
        file.write(f"Top Ask Price: {item['top_ask_price']} | Quantity: {item['top_ask_quantity']}\n")
        file.write(f"Number of Bid Orders: {item['bid_orders']}\n")
        file.write(f"Number of Ask Orders: {item['ask_orders']}\n")
        file.write("-" * 60 + "\n")

print("Market depth data has been written to 'market_depth_report.txt'.")
