import concurrent.futures
import pandas as pd
from tradingview_ta import TA_Handler, Interval

import os

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
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
        indicators = handler.get_analysis().indicators
        data = {
            'symbol': symbol,
            'current_price': indicators['close'],
            'open': indicators['open'],
            'high': indicators['high'],
            'low': indicators['low'],
            'sma10': handler.get_indicators()['SMA10'],
            'volume': indicators['volume'],
        }
        return data
    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return None

# Read stock list from CSV
df = pd.read_csv("stock_list.csv")

df = pd.read_excel('stock_list1.xlsx')
filtered_list = df.values.tolist()

# Using ThreadPoolExecutor for concurrent execution
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_symbol = {executor.submit(get_current_price, item[1]): item for item in filtered_list}
    for future in concurrent.futures.as_completed(future_to_symbol):
        symbol = future_to_symbol[future]
        try:
            data = future.result()
            if data:
                stock_symbol = data['symbol']
                sma10 = data['sma10']
                current_price = data['current_price']
                open_price = data['open']  # Don't overwrite built-in names
                high = data['high']
                low = data['low']
                volume = int(data['volume'])

                # Handling large volume stocks
                if volume >= 1000000:
                    print(True)
                    with open('onem.txt', 'a') as text:  # Correct file path
                        text.write(f'{stock_symbol}\n')
                        print(stock_symbol)

                # Handling medium volume stocks
                if 500000 <= volume < 1000000:
                    with open('fivel.txt', 'a') as text:
                        text.write(f'{stock_symbol}\n')
                        print(stock_symbol)

        except Exception as exc:
            print(f'{symbol[1]} generated an exception: {exc}')
