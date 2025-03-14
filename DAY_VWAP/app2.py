# import pandas as pd
# import logging
# import time

# logging.basicConfig(filename='trading.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# # Read the Excel file
# df = pd.read_excel("stock_list.xlsx")

# # Extract data from the second column
# # second_column_data = df.iloc[:, 1]
# second_column_data = df.iloc[:200, 1]
# # Convert the data into a Python list
# stock_symbol_list = second_column_data.tolist()

# from tradingview_ta import TA_Handler, Interval, Exchange
# from datetime import datetime

# while True:
#     for symbol in stock_symbol_list:
#         try:
#             handler = TA_Handler(
#             symbol=symbol,
#             screener="india",
#             exchange="NSE",
#             interval=Interval.INTERVAL_1_DAY
#             )

#             high = handler.get_analysis().indicators['high']
#             low = handler.get_analysis().indicators['low']
#             close = handler.get_analysis().indicators['close']

#             vwap = (high+low+close)/3
#             vwap_3per_high = (vwap * 1.01)
#             vwap_3per_low = (vwap * 0.99)


#             # print(symbol)
#             logging.info(f"Symbol: {symbol}, VWAP: {vwap}, Close: {close}")

#             if close < vwap_3per_low:
#                 current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#                 # Write close price and current time to a text file
#                 with open("/close_prices.txt", "a") as file:
#                     file.write(f" {symbol} , Close Price: {close}, Time: {current_time}\n")


#             time.sleep(2)
           
#         except:
#             pass
#     time.sleep(60)     




import datetime

# Get current time
current_time = datetime.datetime.now()

# Extract minute and hour from current time
current_minute = current_time.minute
current_hour = current_time.hour

# Print minute followed by hour
print("Current minute:", current_minute)
print("Current hour:", current_hour)