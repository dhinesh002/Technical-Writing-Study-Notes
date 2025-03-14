
# # # import yfinance as yf
# # # import pandas as pd
# # # import time
# # # import ta

# # # # Download data
# # # data = yf.download("RVNL.NS", start="2024-12-11", end="2024-12-12", interval="1m")

# # # # Convert the index (Datetime) from UTC to IST
# # # data.index = data.index.tz_convert('Asia/Kolkata')
# # # data['EMA_10'] = ta.trend.ema_indicator(data['Close'], window=10)
# # # data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
# # # # Print the adjusted data
# # # print(data)



# # # # for index, row in data.iterrows():
# # # #     print(row)



# # import yfinance as yf
# # import ta

# # # Download the data
# # data = yf.download("RVNL.NS", start="2024-12-11", end="2024-12-12", interval="1m")

# # # Convert the index (Datetime) from UTC to IST
# # data.index = data.index.tz_convert('Asia/Kolkata')

# # # Ensure 'Close' is a 1-dimensional array (Series)
# # data['EMA_10'] = ta.trend.ema_indicator(data['Close'], window=10)
# # data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)

# # # Print the adjusted data
# # print(data)


# # from blueshift.api import(    symbol,
# #                             order_target_percent,
# #                             schedule_function,
# #                             date_rules,
# #                             time_rules,
# #                        )

# # import blueshift
# # print(dir(blueshift))


# import os

# # Define the search term (e.g., "#1m")
# search_term = "1m"

# # Define the directory where your Python files are located
# # directory = "C:\Users\Intel\Desktop>" # For Windows
# # directory = r"C:\Users\Intel\Desktop"
# directory = "C:/Users/Intel/Desktop"

# # directory = "/path/to/your/directory"  # For macOS/Linux

# # Loop through all Python files in the directory
# for root, dirs, files in os.walk(directory):
#     for file in files:
#         if file.endswith(".py"):
#             file_path = os.path.join(root, file)
#             with open(file_path, 'r') as f:
#                 lines = f.readlines()
#                 for i, line in enumerate(lines):
#                     if search_term in line:
#                         print(f"Found '{search_term}' in {file_path}, line {i + 1}: {line.strip()}")




# import yfinance as yf
# symbol = 'TCS.NS'
# interval = '1m'
# stock = yf.Ticker(symbol)
# data = stock.history(period='1d', interval=interval)
# data['20_Day_MA'] = data['Close'].rolling(window=20).mean()
# # print(f"Intraday Data for {symbol} (Interval: {interval})")
# # print(intraday_data)

# print(data)




import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt

symbol = 'TCS.NS'
start_date = '2024-12-10'
end_date = '2024-12-12'
interval = '1m'
stock = yf.Ticker(symbol)
data = stock.history(start=start_date, end=end_date,interval=interval)
data = data.drop(columns=['Dividends', 'Stock Splits'])

data['10_Day_MA'] = data['Close'].rolling(window=10).mean()
data['20_Day_MA'] = data['Close'].rolling(window=20).mean()

# data['Daily_Return'] = data['Close'].pct_change() * 100

data = data.tail(362)
# print(data.tail(362))

# Assuming 'data' is your DataFrame
for i in range(1, len(data)):
    # Check for a crossover where 10-day EMA crosses above 20-day EMA
    if data['10_Day_MA'].iloc[i-1] < data['20_Day_MA'].iloc[i-1] and data['10_Day_MA'].iloc[i] > data['20_Day_MA'].iloc[i]:
        print(f"10-Day EMA crossed above 20-Day EMA at {data.index[i]}")
    # Check for a crossover where 10-day EMA crosses below 20-day EMA
    elif data['10_Day_MA'].iloc[i-1] > data['20_Day_MA'].iloc[i-1] and data['10_Day_MA'].iloc[i] < data['20_Day_MA'].iloc[i]:
        print(f"10-Day EMA crossed below 20-Day EMA at {data.index[i]}")
