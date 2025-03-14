import logging
import os
import json
from kiteconnect import KiteConnect
from datetime import datetime, timedelta
import pandas as pd
api_key = ''
secret = ''

# Set up logging
# logging.basicConfig(level=logging.DEBUG)

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
  

def print_account_balance():
    try:
        margins = kite.margins()
        available_balance = margins['equity']['available']['cash']
        print(f"Your available balance is: {available_balance}")
    except Exception as e:
        logging.error(f"Error fetching account balance: {e}")

# Authenticate and print the account balance
authenticate()

stock_symbols = ["NSE:TCS"]

timeframe = "day"  # 1-day timeframe candles

# Function to fetch historical data and add EMA9 and EMA20
def fetch_historical_data_with_ema(kite, symbol, interval, days):
    try:

        end_date = datetime.now()  
        start_date = end_date - timedelta(days=days) 

        # Get instrument token for the symbol
        instruments = kite.instruments("NSE")
        instrument_token = None
        for instrument in instruments:
            if instrument['tradingsymbol'] == symbol.split(":")[1]:  # Extract 'TCS' from 'NSE:TCS'
                instrument_token = instrument['instrument_token']
                break
        
        if not instrument_token:
            print(f"Instrument token for {symbol} not found.")
            return
    
        data = kite.historical_data(instrument_token, start_date, end_date, interval)

        df = pd.DataFrame(data)
   
        df['EMA9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
        
        return df.tail(200)
    
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")

# Loop through stock symbols and fetch historical data with EMA
for symbol in stock_symbols:
    print(f"\nFetching data for {symbol}...\n")
    df = fetch_historical_data_with_ema(kite, symbol, timeframe, days=1000)
    
    list_of_data = df.apply(lambda row: {
    'date': row['date'].strftime('%Y-%m-%d'),  # Format the date
    'open': row['open'],
    'high': row['high'],
    'low': row['low'],
    'close': row['close'],
    'volume': row['volume'],
    'EMA9': row['EMA9'],
    'EMA20': row['EMA20']
}, axis=1).tolist()

    for  i in range(len(list_of_data)-1):
        if list_of_data[i + 1]['EMA9'] < list_of_data[i + 1]['EMA20'] and  list_of_data[i]['EMA9'] > list_of_data[i]['EMA20']:
            print(list_of_data[i + 1]['date'])
