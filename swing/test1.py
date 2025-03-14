# import yfinance as yf

# import yfinance as yf
# import pandas as pd
# import pandas as pd


# file_path = 'stock_list.xlsx'
# df = pd.read_excel(file_path)
# symbols = df.iloc[:, 1].dropna().tolist()

# # symbols = symbols[0: 5]

# data = []

# for symbol in symbols:
#     try:          
#         # Define the stock ticker (e.g., 'AAPL' for Apple)
#         ticker = f'{symbol}.NS'  # Replace with your stock ticker
#         print(ticker)
#         stock = yf.Ticker(ticker)

#         # Fetch stock price and EPS
#         price = stock.history(period="1d")['Close'].iloc[-1]  # Latest closing price
#         eps = stock.info.get('trailingEps')  # Earnings per share
#         # print(price/eps)
#         data.append({'symbol':symbol , 'eps':eps})

#     except:
#         pass

# # print(data)    

# # Sort the list of dictionaries by 'eps' in ascending order
# sorted_data = sorted(data, key=lambda x: x['eps'])

# # Print the sorted data
# for item in sorted_data:
#     print(f"Symbol: {item['symbol']}, EPS: {item['eps']}")

# # Write the sorted data to a text file
# with open("sorted_eps.txt", "w") as file:  # 'w' mode overwrites the file if it exists
#     for item in sorted_data:
#         file.write(f"Symbol: {item['symbol']}, EPS: {item['eps']}\n")

# print("Data has been written to sorted_eps.txt")    


# from NSEDownload import stocks

# # Gets data without adjustment for events
# df = stocks.get_data(stock_symbol="RELIANCE", start_date='15-9-2021', end_date='1-10-2021')




from datetime import date
from nsepy import get_history
sbin = get_history(symbol='SBIN',
                   start=date(2022,1,1),
                   end=date(2023,1,10))

print(sbin)                   