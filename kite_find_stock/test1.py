# # Example data (based on what you provided)
# data = [
#     {
#         "symbol": "AEROFLEX", 
#         "sl": 191.15, 
#         "volume": 32085, 
#         "percentage_change": 1.44,
#         "bid": [
#             {'price': 192.75, 'quantity': 193, 'orders': 1},
#             {'price': 192.74, 'quantity': 14, 'orders': 1},
#             {'price': 192.72, 'quantity': 14, 'orders': 1}
#         ],
#         "sell": [
#             {'price': 192.99, 'quantity': 1, 'orders': 1},
#             {'price': 193, 'quantity': 899, 'orders': 3}
#         ]
#     },
#     {
#         "symbol": "AGSTRA", 
#         "sl": 93.52, 
#         "volume": 38054, 
#         "percentage_change": 4.57,
#         "bid": [
#             {'price': 95.19, 'quantity': 13, 'orders': 1},
#             {'price': 95.15, 'quantity': 112, 'orders': 1}
#         ],
#         "sell": [
#             {'price': 95.81, 'quantity': 17, 'orders': 1},
#             {'price': 95.85, 'quantity': 115, 'orders': 3}
#         ]
#     },
#     {
#         "symbol": "ALANKIT", 
#         "sl": 22.14, 
#         "volume": 36902, 
#         "percentage_change": 1.13,
#         "bid": [
#             {'price': 22.18, 'quantity': 418, 'orders': 1},
#             {'price': 22.17, 'quantity': 1, 'orders': 1},
#             {'price': 22.16, 'quantity': 418, 'orders': 1}
#         ],
#         "sell": [
#             {'price': 22.29, 'quantity': 780, 'orders': 2},
#             {'price': 22.30, 'quantity': 3413, 'orders': 2}
#         ]
#     },
#     {
#         "symbol": "DEN", 
#         "sl": 52.13, 
#         "volume": 53025, 
#         "percentage_change": 0.67,
#         "bid": [
#             {'price': 52.19, 'quantity': 279, 'orders': 1},
#             {'price': 52.17, 'quantity': 174, 'orders': 1}
#         ],
#         "sell": [
#             {'price': 52.22, 'quantity': 12224, 'orders': 5},
#             {'price': 52.24, 'quantity': 329, 'orders': 1}
#         ]
#     },
#     {
#         "symbol": "SUBEXLTD", 
#         "sl": 26.59, 
#         "volume": 48243, 
#         "percentage_change": 0.68,
#         "bid": [
#             {'price': 26.67, 'quantity': 1862, 'orders': 5},
#             {'price': 26.66, 'quantity': 2724, 'orders': 7}
#         ],
#         "sell": [
#             {'price': 26.69, 'quantity': 4053, 'orders': 2},
#             {'price': 26.70, 'quantity': 1158, 'orders': 4}
#         ]
#     },
#     {
#         "symbol": "WIPRO", 
#         "sl": 541.55, 
#         "volume": 1275015, 
#         "percentage_change": 0.73,
#         "bid": [
#             {'price': 542.4, 'quantity': 27, 'orders': 1},
#             {'price': 542.35, 'quantity': 45, 'orders': 4}
#         ],
#         "sell": [
#             {'price': 542.55, 'quantity': 677, 'orders': 4},
#             {'price': 542.6, 'quantity': 401, 'orders': 3}
#         ]
#     }
# ]

# # Now you have all the symbol data in a list of dictionaries!

# def analyze_trade(symbol_data):
#     symbol = symbol_data['symbol']
#     sl = symbol_data['sl']
#     highest_bid = symbol_data['bid'][0]['price']  # highest bid price
#     lowest_sell = symbol_data['sell'][0]['price']  # lowest ask price

#     # Buy-to-Sell Scenario
#     buy_to_sell_reward = lowest_sell - highest_bid
#     buy_to_sell_risk = highest_bid - sl
#     buy_to_sell_ratio = buy_to_sell_reward / buy_to_sell_risk if buy_to_sell_risk != 0 else 0

#     # Sell-to-Buy Scenario (short sell)
#     sell_to_buy_reward = highest_bid - lowest_sell
#     sell_to_buy_risk = lowest_sell - sl
#     sell_to_buy_ratio = sell_to_buy_reward / sell_to_buy_risk if sell_to_buy_risk != 0 else 0

#     # Determine best trade option
#     if buy_to_sell_ratio > sell_to_buy_ratio and buy_to_sell_reward > 0:
#         entry = highest_bid
#         target = lowest_sell
#         stop_loss = sl
#         trade = "Buy-to-Sell"
#         ratio = buy_to_sell_ratio
#     elif sell_to_buy_reward > 0:
#         entry = lowest_sell
#         target = highest_bid
#         stop_loss = sl
#         trade = "Sell-to-Buy"
#         ratio = sell_to_buy_ratio
#     else:
#         trade = "No Trade"
#         entry = target = stop_loss = ratio = None

#     return {
#         "symbol": symbol,
#         "trade": trade,
#         "entry": entry,
#         "target": target,
#         "stop_loss": stop_loss,
#         "risk_reward_ratio": ratio
#     }

# # Analyze all symbols
# for stock in data:
#     result = analyze_trade(stock)
#     print(f"Symbol: {result['symbol']}, Trade: {result['trade']}, "
#           f"Entry: {result['entry']}, Target: {result['target']}, "
#           f"Stop Loss: {result['stop_loss']}, Risk/Reward Ratio: {result['risk_reward_ratio']:.2f}")

#     print('_______________________________________________________________')      



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
api_key = 'dq9l8jfk6x54izb2'
secret = '1jyvug1ogvot5nxvx817l3n1xo4ko96r'
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
    data['Change'] = data['HA_Close'].diff()

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
    today = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    from_date = f"{today} 09:15:00"  # Start time for today (market open time)
    to_date = f"{today} 15:30:00"    # End time for today (market close time)


            # Get the instrument token for the stock symbol
    instrument_token = kite.ltp(f'NSE:IDFCFIRSTB')[f'NSE:IDFCFIRSTB']['instrument_token']

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
    today = datetime.now().strftime('%Y-%m-%d')
            # today = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
    from_date = f"{today} 09:15:00"  # Start time for today (market open time)
    to_date = f"{today} 15:30:00"    # End time for today (market close time)


            # Get the instrument token for the stock symbol
    instrument_token = kite.ltp(f'NSE:IDFCFIRSTB')[f'NSE:IDFCFIRSTB']['instrument_token']

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

 


    df['HA_Open'] = 0.0
    df['HA_Close'] = 0.0
    df['HA_High'] = 0.0
    df['HA_Low'] = 0.0

    # Loop through the data and calculate Heikin-Ashi values
    for i in range(0, len(df)):
        # Heikin-Ashi Close
        df.at[i, 'HA_Close'] = (df.at[i, 'open'] + df.at[i, 'high'] + df.at[i, 'low'] + df.at[i, 'close']) / 4

        # Heikin-Ashi Open
        if i == 0:
            # The first Heikin-Ashi Open is the same as the standard candle open
            df.at[i, 'HA_Open'] = (df.at[i, 'open'] + df.at[i, 'close']) / 2
        else:
            df.at[i, 'HA_Open'] = (df.at[i-1, 'HA_Open'] + df.at[i-1, 'HA_Close']) / 2

        # Heikin-Ashi High
        df.at[i, 'HA_High'] = max(df.at[i, 'high'], df.at[i, 'HA_Open'], df.at[i, 'HA_Close'])

        # Heikin-Ashi Low
        df.at[i, 'HA_Low'] = min(df.at[i, 'low'], df.at[i, 'HA_Open'], df.at[i, 'HA_Close'])
 
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['RSI_14'] = calculate_rsi(df.copy())  # Avoid modifying original DataFrame
    # df['PSAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)
    df['PSAR'] = talib.SAR(df['HA_High'], df['HA_Low'], acceleration=0.02, maximum=0.2)

    # print(df[125:])

    current_day_df = df[125:]
    previous_row = None 

        # Loop through the rows and print each one
    for index, row in current_day_df.iterrows():
        if previous_row is None:
            previous_row = row

        else:
            current_row = row

            if current_row['HA_Close'] < current_row['PSAR'] and previous_row['HA_Close'] > previous_row['PSAR']:
                print(current_row['date'])






        # print(f"Index: {index}")
        # if previous_row is not None:
        #     # You can now access both previous_row and current_row
        #     # print("Previous row date:", previous_row['date'])
        #     # print("Current row date:", row['date'])
        #     current_row = row
        
        # # After processing, set the current row as the previous row for the next iteration
        # else:
        #     previous_row = row
        #     # current_row = 

        # heikin_aski_open = round((row['HA_Open']), 2)
        # heikin_aski_close =round( (row['HA_Close']), 2)
        # heikin_aski_high = round((row['HA_High']), 2)
        # heikin_aski_low = round((row['HA_Low']), 2)
        # heikin_aski_sma50 =round((row['SMA_50']), 2)
        # heikin_aski_rsi14 = round((row['RSI_14']), 2)
        # heikin_aski_psar = round((row['PSAR']), 2)
        # print(heikin_aski_open,heikin_aski_close,heikin_aski_high, heikin_aski_low,heikin_aski_sma50, heikin_aski_rsi14, heikin_aski_psar)
        # print(row['date'].strftime('%Y-%m-%d %I:%M %p') ) # Blank line between rows

        # if heikin_aski_open < heikin_aski_close and heikin_aski_rsi14 > 50 and heikin_aski_open > heikin_aski_sma50 :
            # buy_order.append(row)
            # pass


        # current_candle = current_day_df.iloc[index]['date']
        # previous_candle =     

            

        # print(current_candle)



# print(buy_order)
# print(len(buy_order))


authenticate()
main(kite=authenticate())
