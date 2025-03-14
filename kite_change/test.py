# # from tradingview_ta import TA_Handler, Interval, Exchange



# # import logging
# # import os
# # import json
# # from kiteconnect import KiteConnect, KiteTicker
# # from datetime import datetime, timedelta
# # import pandas as pd
# # import time
# # from concurrent.futures import ThreadPoolExecutor
# # import json


# # api_key = ''
# # secret = ''

# # kite = KiteConnect(api_key=api_key)

# # TOKEN_FILE = "access_token.json"

# # def save_access_token(token):
# #     with open(TOKEN_FILE, 'w') as f:
# #         json.dump({"access_token": token}, f)

# # def load_access_token():
# #     if os.path.exists(TOKEN_FILE):
# #         with open(TOKEN_FILE, 'r') as f:
# #             data = json.load(f)
# #             return data.get("access_token")
# #     return None

# # from datetime import datetime, timedelta

# # def authenticate():
# #     access_token = load_access_token()
# #     if access_token:
# #         kite.set_access_token(access_token)
# #         try:
# #             kite.margins() 
# #         except Exception as e:
# #             logging.warning("Access token may be invalid, re-authenticating...")
# #             return get_access_token() 
# #     else:
# #         return get_access_token()

# # def get_access_token():
# #     print("Go to the following URL to authorize:")
# #     print(kite.login_url())
# #     request_token = input("Enter the request token: ")
# #     data = kite.generate_session(request_token, api_secret=secret)
# #     kite.set_access_token(data["access_token"])
# #     save_access_token(data["access_token"])
  

# # authenticate()

# #         # Function to calculate total buy and sell quantities
# # def get_total_depth(buy_depth, sell_depth):
# #     total_buy_quantity = sum([level['quantity'] for level in buy_depth if level['quantity'] > 0])
# #     total_sell_quantity = sum([level['quantity'] for level in sell_depth if level['quantity'] > 0])
# #     return total_buy_quantity, total_sell_quantity


# # # Function to calculate the "sell : buy" ratio
# # def get_sell_buy_ratio(buy_depth, sell_depth):
# #     ratio_list = []
    
# #     # Iterate over the levels of buy and sell orders
# #     for sell, buy in zip(sell_depth, buy_depth):
# #         sell_quantity = sell['quantity']
# #         buy_quantity = buy['quantity']
        
# #         # If there's no buy quantity, assume 0 for buy side
# #         if buy_quantity == 0:
# #             ratio_list.append(f"sell: {sell_quantity} : buy: 0")
# #         else:
# #             ratio_list.append(f"sell: {sell_quantity} : buy: {buy_quantity}")
    
# #     return ratio_list

# # def process_stock(symbol):
# #     try:
# #         handler = TA_Handler(
# #             symbol=symbol,
# #             screener="india",
# #             exchange="NSE",
# #             interval=Interval.INTERVAL_1_DAY,
# #         )
# #         analysis = handler.get_analysis()
# #         # print(analysis.indicators)
# #         # print(analysis.time)
# #         # print(analysis.oscillators['RECOMMENDATION'])

# #         data = kite.historical_data(
# #             instrument_token=kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"],
# #             from_date=datetime.now(),
# #             to_date=datetime.now(),
# #             interval='day',
# #         )
# #         market_depth = kite.quote("NSE:" + symbol)
# #         print(market_depth[f'NSE:{symbol}'])
# #         print(123)
# #         buy_depth = market_depth[f'NSE:{symbol}']['depth']['buy']
# #         sell_depth = market_depth[f'NSE:{symbol}']['depth']['sell']

# #         # print(buy_depth)


# #         # Extract buy and sell depth
# #         # buy_depth = market_depth[F'NSE:{symbol}']['depth']['buy']
# #         # sell_depth = market_depth[F'NSE:{symbol}']['depth']['sell']
# #         # print(buy_depth , sell_depth)


# #         # # Calculate total buy and sell quantities
# #         total_buy_quantity, total_sell_quantity = get_total_depth(buy_depth, sell_depth)
# #         # print(total_buy_quantity)
# #         # print(total_sell_quantity)
# #         # # Calculate imbalance
# #         imbalance = total_buy_quantity - total_sell_quantity

# #         # # Print results
# #         print(f"Total Buy Quantity: {total_buy_quantity}")
# #         print(f"Total Sell Quantity: {total_sell_quantity}")
# #         print(f"Market Imbalance (Buy - Sell): {imbalance}")

# #         n = 100000 / 80000
# #         print(n)
# #         # sell_buy_ratios = get_sell_buy_ratio(20, 10)

# #         # Print the market imbalance ratios
# #         # for ratio in sell_buy_ratios:
# #             # print(ratio)

# #             # # print(data)
# #     except:
# #         pass   



# # process_stock('NLCINDIA')   


# from tradingview_ta import *
# analysis = get_multiple_analysis(screener="america", interval=Interval.INTERVAL_1_HOUR, symbols=["nasdaq:tsla", "nyse:docn", "nasdaq:aapl"])

# # print(analysis.indicators())

# for i in analysis:
#     print(i.indicators())


# from tradingview_ta import *

# # Fetch multiple analyses
# analysis = get_multiple_analysis(
#     screener="america",
#     interval=Interval.INTERVAL_1_HOUR,
#     symbols = [
#     "nasdaq:tsla",  # Tesla
#     "nasdaq:aapl",  # Apple
#     "nasdaq:amzn",  # Amazon
#     "nasdaq:msft",  # Microsoft
#     "nasdaq:nvda",  # NVIDIA
#     "nyse:ba",      # Boeing
#     "nyse:dis",     # Disney
#     "nyse:v",       # Visa
#     "nyse:jpm",     # JPMorgan Chase
#     "nasdaq:googl", # Alphabet (Google)
#     "nasdaq:fb",    # Meta Platforms (Facebook)
#     "nyse:ko",      # Coca-Cola
#     "nyse:pg",      # Procter & Gamble
#     "nasdaq:adbe",  # Adobe
#     "nyse:xom",     # Exxon Mobil
#     "nasdaq:intc",  # Intel
#     "nasdaq:pypl",  # PayPal
#     "nyse:hd",      # Home Depot
#     "nasdaq:csco",  # Cisco Systems
#     "nyse:nee"      # NextEra Energy
# ]

# )

# # Iterate through the analysis results
# for symbol, result in analysis.items():
#     if isinstance(result, Analysis):  # Check if the result is a valid Analysis object
#         print(f"Indicators for {symbol}:")
#         print(result.indicators)
#     else:

#         print(f"Error for {symbol}: {result}")



from tradingview_ta import *
from concurrent.futures import ThreadPoolExecutor

# Load stock list
list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip()
        if symbol != "":
            list_of_stocks.append(symbol)

def process_stock(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
        analysis = handler.get_analysis()

        # Get required indicators
        bb_lower = analysis.indicators['BB.lower']
        pivot_s1 = analysis.indicators['Pivot.M.Classic.S1']
        close_price = analysis.indicators['close']

        # Check the condition
        # if close_price <= bb_lower or close_price <= pivot_s1:
        #     print(f"Symbol: {symbol}")
        #     print(f"Close Price: {close_price}")
        #     print(f"BB.lower: {bb_lower}")
        #     print(f"Pivot.M.Classic.S1: {pivot_s1}")
        #     print("-" * 50)
        if  close_price <= pivot_s1:
            print(f"Symbol: {symbol}")
            print(f"Close Price: {close_price}")
            # print(f"BB.lower: {bb_lower}")
            print(f"Pivot.M.Classic.S1: {pivot_s1}")
            print("-" * 50)        

    except Exception as e:
        # Handle exceptions silently or print them for debugging
        print(f"Error processing {symbol}: {e}")

# Use ThreadPoolExecutor for multithreading
max_workers = 5  # You can adjust this based on your system's capacity
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_stock, list_of_stocks)
