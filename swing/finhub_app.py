
# # #pip install finnhub-python

# # api='crikc5pr01qqt33saeogcrikc5pr01qqt33saep0'


# # import finnhub
# # finnhub_client = finnhub.Client(api_key=api)

# # print(finnhub_client.market_holiday(exchange='NSE'))
# # # import finnhub

# # # finnhub_client = finnhub.Client(api_key=api)

# # # # Example for NSE stocks
# # # data = finnhub_client.stock_candles('INFY.BSE', '1', 1700000000, 1700086400)
# # # print(data)


# import yfinance as yf

# def fetch_intraday_data(symbol, interval, start, end):
#     ticker = yf.Ticker(symbol)
#     data = ticker.history(interval=interval, start=start, end=end)
#     return data

# # Example usage
# symbol = "ITC.NS"  # NSE stocks use `.NS` suffix on Yahoo Finance
# start_date = "2023-12-10"
# end_date = "2023-12-11"
# interval = "1m"  # 1-minute interval

# data = fetch_intraday_data(symbol, interval, start_date, end_date)
# print(data)


import yfinance as yf
import pandas as pd
import time

# Download data
data = yf.download("ITC.NS", start="2024-12-12", end="2024-12-15", interval="1m")

# Convert the index (Datetime) from UTC to IST
data.index = data.index.tz_convert('Asia/Kolkata')

# Print the adjusted data
print(data.tail(10))

# for index, row in data.iterrows():
    # print(row)
