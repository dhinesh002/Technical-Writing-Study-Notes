import concurrent.futures
import os
from datetime import datetime, timedelta
import logging
from kiteconnect import KiteConnect
from stocks import Stock_symbol
from concurrent.futures import ThreadPoolExecutor, as_completed

# Your API key and secret
api_key = ''
secret = ''
access_token_file = "access_token.txt"  # File to store access token

# Initialize the Kite Connect API
kite = KiteConnect(api_key=api_key)
kite.reqsession.timeout = (10, 30)  # (connect_timeout, read_timeout)

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
    
    logging.info("Access token set and saved successfully.")
    return kite  # Return authenticated Kite instance

# Authenticate at the beginning of the script
kite = authenticate()

gapup = []
gapdown = []

def gap(stock_symbol):
    try:
        # Today's date
        today = datetime.now().strftime('%Y-%m-%d')

        # Yesterday's date
        # today = (datetime.now() - timedelta(4)).strftime('%Y-%m-%d')

        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        print(today , yesterday)

        # Define the date and time range for today and yesterday
        from_date_today = f"{today} 09:15:00"   # Market open time today
        to_date_today = f"{today} 15:30:00"     # Market close time today

        from_date_yesterday = f"{yesterday} 09:15:00"  # Market open time yesterday
        to_date_yesterday = f"{yesterday} 15:30:00"    # Market close time yesterday

        # Fetch instrument token for the stock
        ltp_data = kite.ltp(f'NSE:{stock_symbol}')
        instrument_token = ltp_data[f'NSE:{stock_symbol}'].get('instrument_token')

        if not instrument_token:
            print(f"Instrument token not found for {stock_symbol}. LTP data: {ltp_data}")
            return  # Exit the function if instrument token is invalid

        # Fetch today's candle data (1-day interval to get open price)
        today_candle_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date_today,
            to_date=to_date_today,
            interval='day'
        )

        # Fetch yesterday's candle data (1-day interval)
        yesterday_candle_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date_yesterday,
            to_date=to_date_yesterday,
            interval='day'
        )

        # Extract today's open price
        today_open = today_candle_data[0]['open']

        # Extract yesterday's high and low
        yesterday_high = yesterday_candle_data[0]['high']
        yesterday_low = yesterday_candle_data[0]['low']

        # Calculate percentage change between today's open and yesterday's high
        percentage_change_high = ((today_open - yesterday_high) / yesterday_high) * 100

        # Calculate percentage change between today's open and yesterday's low
        percentage_change_low = ((today_open - yesterday_low) / yesterday_low) * 100

        if today_open > yesterday_high:
            gapup.append({'symbol': stock_symbol, 'percentage': percentage_change_high})

        if today_open < yesterday_low:
            gapdown.append({'symbol': stock_symbol, 'percentage': percentage_change_low})

    except Exception as e:
        print(f"Error getting price for {stock_symbol}: {str(e)}")


# List of stock symbols to process
stock_symbols = Stock_symbol.stock_symbol

# Use ThreadPoolExecutor for concurrent execution
with ThreadPoolExecutor(max_workers=2) as executor:  # Adjust 'max_workers' as needed
    futures = [executor.submit(gap, symbol) for symbol in stock_symbols]
    
    for future in as_completed(futures):
        try:
            future.result()  # Retrieve the result (if any) to handle exceptions
        except Exception as e:
            print(f"Error in concurrent execution: {e}")

# Sort the gapup and gapdown lists by percentage in descending order
gapup_sorted = sorted(gapup, key=lambda x: x['percentage'], reverse=True)
gapdown_sorted = sorted(gapdown, key=lambda x: x['percentage'], reverse=True)
# print(stock_symbols)
# Write gapup data to a file
with open('gapup.txt', 'a') as file:
    for item in gapup_sorted:
        file.write(f'{item}\n')

# Write gapdown data to a file
with open('gapdown.txt', 'a') as file:
    for item in gapdown_sorted:
        file.write(f'{item}\n')

if __name__ == "__main__":
    authenticate()  
