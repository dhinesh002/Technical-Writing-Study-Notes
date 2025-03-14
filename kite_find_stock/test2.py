

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

def calculate_rsi(data, period=14):
    """Calculates the Relative Strength Index (RSI) for a given dataset.

    Args:
        data (pd.DataFrame): A pandas DataFrame containing the candle data.
        period (int): The number of periods to use for the RSI calculation (default: 14).

    Returns:
        pd.Series: A pandas Series containing the RSI values.
    """

    # Calculate price changes
    data['Change'] = data['close'].diff()

    # Calculate upward and downward price changes
    data['Upward Change'] = data['Change'].clip(lower=0)
    data['Downward Change'] = data['Change'].clip(upper=0).abs()

    # Calculate average gain and loss (using Wilder's smoothing)
    average_gain = data['Upward Change'].ewm(alpha=1/period, min_periods=period).mean()
    average_loss = data['Downward Change'].ewm(alpha=1/period, min_periods=period).mean()

    # Calculate RSI
    rsi = 100 - 100 / (1 + (average_gain / average_loss))

    return rsi

import talib  

def day_before_data():
    # today = datetime.now().strftime('%Y-%m-%d')
    today = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
    from_date = f"{today} 09:15:00"  # Start time for today (market open time)
    to_date = f"{today} 15:30:00"    # End time for today (market close time)


            # Get the instrument token for the stock symbol
    instrument_token = kite.ltp(f'NSE:TATAPOWER')[f'NSE:TATAPOWER']['instrument_token']

            # Fetch historical 3-minute candle data
    candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval='3minute'
    )
    return candle_data    


buy_order = []
sell_order = []

buy_active = False
sell_active = False


def main(kite):
    # today = datetime.now().strftime('%Y-%m-%d')
    today = (datetime.now() - timedelta(9)).strftime('%Y-%m-%d')
    from_date = f"{today} 09:15:00"  # Start time for today (market open time)
    to_date = f"{today} 15:30:00"    # End time for today (market close time)

            # Get the instrument token for the stock symbol
    instrument_token = kite.ltp(f'NSE:TATAPOWER')[f'NSE:TATAPOWER']['instrument_token']

            # Fetch historical 3-minute candle data
    candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval='3minute'
    )

    daybefore_data = day_before_data()
    data= daybefore_data + candle_data
    
    # df = pd.DataFrame(candle_data)
    df = pd.DataFrame(data)
    df['ADX_14'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)  # Default time period is 14
    df['DMI_+DI'] = talib.PLUS_DI(df['high'], df['low'], df['close'], timeperiod=14)  # +DI (DMI Up)
    df['DMI_-DI'] = talib.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14)  # -DI (DMI Down)
    # df['SMA_50'] = df['close'].rolling(window=50).mean()
    # df['RSI_14'] = calculate_rsi(df.copy())  # Avoid modifying original DataFrame
    df['PSAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)

    current_day_df = df[125:]
    previous_row = None 

    df = df[125:]
    # print(df)
        # Initialize variables
    parabolic_up = []
    parabolic_down = []
    current_trend = None  # Track the current trend ('up' or 'down')
    trend_data = []  # Store all trends

    for i, row in df.iterrows():
        psar = row['PSAR']
        high = row['high']
        low = row['low']
        # print(psar)
        
        # Check if PSAR is above the high (bearish signal)
        if psar > high:
            if current_trend != 'down':
                # Save the previous trend data if trend changed
                if current_trend == 'up' and parabolic_up:
                    trend_data.append({'trend': 'up', 'data': parabolic_up})
                    parabolic_up = []  # Reset the up trend array
                current_trend = 'down'
            parabolic_down.append(row)
        
        # Check if PSAR is below the low (bullish signal)
        elif psar < low:
            if current_trend != 'up':
                # Save the previous trend data if trend changed
                if current_trend == 'down' and parabolic_down:
                    trend_data.append({'trend': 'down', 'data': parabolic_down})
                    parabolic_down = []  # Reset the down trend array
                current_trend = 'up'
            parabolic_up.append(row)

    # Append the last trend data
    if current_trend == 'up' and parabolic_up:
        trend_data.append({'trend': 'up', 'data': parabolic_up})
        
    elif current_trend == 'down' and parabolic_down:
        trend_data.append({'trend': 'down', 'data': parabolic_down})



    for trend in trend_data:
        if len(trend['data']) > 1:
            # Get the first and last row
            first_row = trend['data'][0]
            last_row = trend['data'][-1]

            buy_entry = trend['data'][1]['open']
            buy_exit = trend['data'][-1]['close']

            DMI_plus = trend['data'][0]['DMI_+DI']
            DMI_minus = trend['data'][0]['DMI_-DI']
            ADX = trend['data'][0]['ADX_14']


            start = datetime.strptime(str(first_row['date']), '%Y-%m-%d %H:%M:%S%z').strftime('%d %B %Y, %I:%M %p')
            end = datetime.strptime(str(last_row['date']), '%Y-%m-%d %H:%M:%S%z').strftime('%d %B %Y, %I:%M %p')

          
            signal = None
            if first_row['PSAR'] > first_row['high']  and DMI_plus < DMI_minus and ADX > 25:
                signal = 'SELL'
                print(f'SELL at : {start} to {end}  ,,,, {buy_entry} to {buy_exit}')
            elif first_row['PSAR'] < first_row['low'] and DMI_plus > DMI_minus and ADX > 25:
                signal = 'BUY'
                print(f'BUY at : {start} to {end}  ,,,, {buy_entry} to {buy_exit}')
              
        else:
            single_row = trend['data'][0]
          

authenticate()
main(kite=authenticate())
