import yfinance as yf
import datetime

# Download historical data
ticker_symbol = "ADANIENT.NS" 
end_date = datetime.datetime.today()
print(end_date)
start_date = end_date - datetime.timedelta(days=60)
data = yf.download(ticker_symbol, start='2024-02-16', end='2024-02-17', interval='1h')

# Calculate typical price
typical_price = (data['High'] + data['Low'] + data['Close']) / 3
volume_price = ( data['Volume'] * typical_price )
# data['typical price'] = typical_price
# data['volume price'] = volume_price
print(data)

excel_file_path = 'stock_data.xlsx'  # Choose your desired file path
data.to_excel(excel_file_path)

print("Data saved to Excel file:", excel_file_path)

# # Calculate volume-price
# vp = data['Volume'] * typical_price

# # Fill NaN in the Typical Price column with values from vp using forward fill
# # typical_price.fillna(method='ffill', inplace=True)
# typical_price = typical_price.ffill(inplace=True)

# # Now calculate the total volume-price by summing up the previous vp and current vp
# total_vp = vp + vp.shift(1)

# data['tp'] = typical_price
# data['vp'] = typical_price * data['Volume']



# if 'vp' in data.columns:
#     # Print values of the 'vp' column
#     print("Values of the 'vp' column:")
#     print(data['vp'])

# print(data['vp'])
# print(data.iloc[1])