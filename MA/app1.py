
import concurrent.futures
# from some_ta_module import TA_Handler  # Replace with actual import
import pandas as pd
import time 
from tradingview_ta import TA_Handler, Interval, Exchange
import smtplib
from datetime import datetime
from datetime import datetime
import os
import pywhatkit as kit
import pyautogui
import pyperclip


# Define the file path where symbols will be stored
file_path = 'stored_stock.txt'

# Function to check if a symbol is already stored
def is_symbol_stored(symbol):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            stored_symbols = file.read().splitlines()
            return symbol in stored_symbols
    return False

# Function to store a new symbol
def store_symbol(symbol):
    with open(file_path, 'a') as file:
        file.write(symbol + '\n')



def get_current_price(symbol):
    try:
        # print(1)
        # print(symbol)
        
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_15_MINUTES,
        )
        indicators = handler.get_analysis().indicators
        # print(indicators)
       
        data = {'symbol': symbol,'current_price': indicators['close'], 'open':indicators['open'],
                'high':indicators['high'], 'low':indicators['low']
                 ,'sma10': handler.get_indicators()['SMA10']}
        return data
    except:
        return None

filtered_list = [...]  # Your filtered list
# df = pd.read_excel("stock_list.csv")

df = pd.read_csv("stock_list.csv")
filtered_list = df.values.tolist()
print(filtered_list)
# print(len(filtered_list))
# filtered_list= filtered_list[0:2]
# Using ThreadPoolExecutor for concurrent execution

while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_symbol = {executor.submit(get_current_price, item[2]): item for item in filtered_list}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                data = future.result()
                # print(data)
                stock_symbol = data['symbol']
                sma10 = data['sma10']
                current_price = data['current_price']

                open = data['open']
                high = data['high']
                low = data['low']

                ten_percent_low = open * 0.9
                ten_percent_high = open * 1.1

                                # Calculate high values
                high_2_percent = sma10 * 1.02  # 2% high
                high_3_percent = sma10 * 1.03  # 3% high
                high_4_percent = sma10 * 1.04  # 4% high
                high_5_percent = sma10 * 1.05  # 5% high

                # Calculate low values
                low_2_percent = sma10 * 0.98   # 2% low
                low_3_percent = sma10 * 0.97   # 3% low
                low_4_percent = sma10 * 0.96   # 4% low
                low_5_percent = sma10 * 0.95   # 5% low


                # print(data)

                if current_price >= high_5_percent:
                    with open('high_5_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol} , {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)
                elif current_price >= high_4_percent:
                    with open('high_4_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)
                elif current_price >= high_3_percent:
                    with open('high_3_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)
                elif current_price >= high_2_percent:
                    with open('high_2_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)


                if current_price <= low_5_percent:
                    with open('low_5_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)
                elif current_price <= low_4_percent:
                    with open('low_4_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file                    
                        print(stock_symbol)
                if current_price <= low_3_percent:
                    with open('low_3_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)
                elif current_price <= low_2_percent:
                    with open('low_2_percent.txt', 'a') as text:  # Open in append mode
                        text.write(f'{stock_symbol}, {current_price}\n')  # Write the stock symbol to the file
                        print(stock_symbol)

                # if high >=ten_percent_high:
                #     with open('high_10_percent.txt', 'a') as text:  # Open in append mode
                #         text.write(f'{stock_symbol}, {ten_percent_high}\n')  # Write the stock symbol to the file
                #         print(stock_symbol)


                # if low <= ten_percent_low:
                #     with open('low_10_percent.txt', 'a') as text:  # Open in append mode
                #         text.write(f'{stock_symbol}, {ten_percent_low}\n')  # Write the stock symbol to the file
                #         print(stock_symbol)        




                



        
                # Calculate high values
                high_2_percent = sma10 * 1.02  # 2% high
                high_3_percent = sma10 * 1.03  # 3% high
                high_4_percent = sma10 * 1.04  # 4% high
                high_5_percent = sma10 * 1.05  # 5% high

                # Calculate low values
                low_2_percent = sma10 * 0.98   # 2% low
                low_3_percent = sma10 * 0.97   # 3% low
                low_4_percent = sma10 * 0.96   # 4% low
                low_5_percent = sma10 * 0.95   # 5% low

              
            except Exception as exc:
                print(f'{symbol[1]} generated an exception: {exc}')

