import yfinance as yf
import datetime

# Download historical data
ticker_symbol = "ADANIENT.NS" 
end_date = datetime.datetime.today()
print(end_date)
start_date = end_date - datetime.timedelta(days=60)
data = yf.download(ticker_symbol, start="2024-02-16", end="2024-02-17", interval='1h')
data['VWAP'] = (((data['High'] + data['Low'] + data['Close']) / 3) * data['Volume']).cumsum() / data['Volume'].cumsum()


print(data.tail())
# print(data)
# # Remove timezone information from the datetime index
# data.index = data.index.tz_localize(None)

# # Calculate typical price
# typical_price = (data['High'] + data['Low'] + data['Close']) / 3
# volume_price = ( data['Volume'] * typical_price )

# # Add the calculated values to the DataFrame
# data['Typical Price'] = typical_price
# data['Volume Price'] = volume_price

# # # Save data to Excel
# excel_file_path = 'stock_data.xlsx'  # Choose your desired file path
# data.to_excel(excel_file_path)

# print("Data saved to Excel file:", excel_file_path)



# from stock_indicators import indicators

# # This method is NOT a part of the library.
# quotes = get_history_from_feed("SPY")

# # Calculate
# results = indicators.get_vwap(quotes)