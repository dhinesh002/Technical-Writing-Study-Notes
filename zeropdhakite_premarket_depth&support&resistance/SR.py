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

def calculate_pivot_points(df ,symbol):
    df['symbol'] = symbol
    df['Pivot'] = (df['high'] + df['low'] + df['close']) / 3
    df['Support1'] = 2 * df['Pivot'] - df['high']
    df['Resistance1'] = 2 * df['Pivot'] - df['low']    
    df['Support2'] = df['Pivot'] - (df['Resistance1'] - df['Support1'])
    df['Resistance2'] = df['Pivot'] + (df['Resistance1'] - df['Support1'])
    
    return df


import json
import pandas as pd

# Initialize an empty dictionary to store all symbols
all_data = {}

# Loop through the stock list and fetch data
for symbol in stock_list:
    try:
        # Fetch historical data
        data = kite.historical_data(
            instrument_token=kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"],
            from_date='2024-01-23',
            to_date='2024-12-31',
            interval='day',
        )

        df = pd.DataFrame(data)

        # Calculate pivot points
        df = calculate_pivot_points(df, symbol)
        df = df[['date', 'symbol', 'Pivot', 'Support1', 'Resistance1', 'Support2', 'Resistance2']].tail(1)
        
        date_str = df.iloc[0]['date'].strftime('%Y-%m-%d %H:%M:%S')

        # Add the symbol's data to the dictionary
        all_data[symbol] = {
            'date': date_str,
            'symbol': df.iloc[0]['symbol'],
            'Pivot': round(df.iloc[0]['Pivot'], 2),
            'Support1': round(df.iloc[0]['Support1'], 2),
            'Resistance1': round(df.iloc[0]['Resistance1'], 2),
            'Support2': round(df.iloc[0]['Support2'], 2),
            'Resistance2': round(df.iloc[0]['Resistance2'], 2),
        }

        print(df)

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Write the final dictionary to the file as JSON
with open("output_file.json", "w") as file:
    json.dump(all_data, file, indent=4)
