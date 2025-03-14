
# import logging
# import os
# import json
# from kiteconnect import KiteConnect, KiteTicker
# from datetime import datetime, timedelta
# import pandas as pd
# import time
# from concurrent.futures import ThreadPoolExecutor
# import json


# api_key = ''
# secret = ''

# kite = KiteConnect(api_key=api_key)

# TOKEN_FILE = "access_token.json"

# def save_access_token(token):
#     with open(TOKEN_FILE, 'w') as f:
#         json.dump({"access_token": token}, f)

# def load_access_token():
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, 'r') as f:
#             data = json.load(f)
#             return data.get("access_token")
#     return None

# from datetime import datetime, timedelta

# def authenticate():
#     access_token = load_access_token()
#     if access_token:
#         kite.set_access_token(access_token)
#         try:
#             kite.margins() 
#         except Exception as e:
#             logging.warning("Access token may be invalid, re-authenticating...")
#             return get_access_token() 
#     else:
#         return get_access_token()

# def get_access_token():
#     print("Go to the following URL to authorize:")
#     print(kite.login_url())
#     request_token = input("Enter the request token: ")
#     data = kite.generate_session(request_token, api_secret=secret)
#     kite.set_access_token(data["access_token"])
#     save_access_token(data["access_token"])
  

# authenticate()


# stock_list=['TCS']
# for symbol in stock_list:
#     try:
#         # Fetch historical data
#         data = kite.historical_data(
#             instrument_token=kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"],
#             from_date='2025-01-01',
#             to_date='2025-01-01',
#             interval='2minute',
#         )
#         # import pandas_ta as ta
#         df = pd.DataFrame(data)
#         import talib
#         # Calculate ADX
#         df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
#         # Calculate MACD
#         df['MACD'], df['MACD_signal'], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
#         df['EMA9'] = talib.EMA(df['close'], timeperiod=9)

# # Calculate EMA20
#         df['EMA20'] = talib.EMA(df['close'], timeperiod=20)

#         # Identify Bullish (EMA9 crosses above EMA20)
#         df['Bullish_Crossover'] = (df['EMA9'] > df['EMA20']) & (df['EMA9'].shift(1) < df['EMA20'].shift(1))

#         # Identify Bearish (EMA9 crosses below EMA20)
#         df['Bearish_Crossover'] = (df['EMA9'] < df['EMA20']) & (df['EMA9'].shift(1) > df['EMA20'].shift(1))

#         # Filter crossover points
#         crossover_points = df[(df['Bullish_Crossover']) | (df['Bearish_Crossover'])]
#         print(crossover_points[['date', 'ADX','EMA9', 'EMA20', 'Bullish_Crossover', 'Bearish_Crossover']])
  
#         # print(df)
# # 
#     except Exception as e:
#         print(e)
#         # pass    



# from datetime import datetime


# # Format the time as '01 Jan 09:30:60'
# formatted_time = datetime.now().strftime("%d %b %H:%M:%S")

# print(formatted_time)
