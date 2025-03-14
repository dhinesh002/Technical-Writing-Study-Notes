

from kiteconnect import KiteConnect
import pandas as pd
# import pandas_ta as ta
import concurrent.futures
import os
from datetime import datetime, timedelta
import logging
from kiteconnect import KiteConnect
from kite import Get_3min_candle_data
from stocks import Stock_symbol
from tradingview import Get_current_price
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrap import FindDepth

# Your API key and secret
api_key = ''
secret = ''
access_token_file = "access_token.txt"  # File to store access token


# Initialize the Kite Connect API
kite = KiteConnect(api_key=api_key)
kite.reqsession.timeout = (10, 30)  # (connect_timeout, read_timeout)

start_time = datetime.now()

# stock_symbol = ['360ONE', 'MOTILALOFS']

def authenticate():
    """ Authenticate and generate a new session if no valid token exists. """
    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as file:
            access_token = file.read().strip()
            kite.set_access_token(access_token)
            try:
                # Try fetching user details to check if the token is still valid
                kite.profile()
                logging.info("Access token is valid. No need to reauthenticate.")
                return kite  # Return authenticated Kite instance
            except Exception as e:
                logging.warning(f"Token might have expired: {e}")

    # If token doesn't exist or is invalid, authenticate again
    print("Go to the following URL to authorize:")
    print(kite.login_url())
    request_token = input("Enter the request token: ")
    data = kite.generate_session(request_token, api_secret=secret)
    
    # Set and store the access token
    access_token = data["access_token"]
    kite.set_access_token(access_token)
    
    # Save the access token for future use
    with open(access_token_file, "w") as file:
        file.write(access_token)
    
    # logging.info("Access token set and saved successfully.")
    return kite  # Return authenticated Kite instance



def calculate_average_volume(kite, symbol):
    """ Calculate the average volume over the last 14 trading days. """
    # Set the date range for the last 14 days
    # today = datetime.now()
    # Set 'today' to yesterday's date
    today = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Set 'from_date' to 15 days before yesterday
    from_date = (datetime.now() - timedelta(days=16)).strftime('%Y-%m-%d')

    # 'to_date' is yesterday
    to_date = today

    # Get the instrument token for the stock symbol
    instrument = f'NSE:{symbol}'
    instrument_token = kite.ltp(instrument)[instrument]['instrument_token']

    # Fetch historical daily candle data for the last 14 days
    candle_data = kite.historical_data(
        instrument_token=instrument_token,
        from_date=from_date,
        to_date=to_date,
        interval='day'  # Use daily interval to get data per day
    )

    # Calculate the average volume over the last 14 days
    total_volume = sum([candle['volume'] for candle in candle_data])
    average_volume = total_volume / len(candle_data) if candle_data else 0

    return average_volume


def main(kite, symbol):
    try:
        average_volume = calculate_average_volume(kite, symbol)
        # print(f"Average volume for {symbol} over the last 14 days: {average_volume}")
        with open('volume14.txt', 'a') as file:
        
            file.write(f'[{symbol} , {average_volume}]\n')
    except:
        pass        

authenticate()


# Loop through the stock symbols
for symbol in Stock_symbol.stock_symbol:
    main(kite, symbol)