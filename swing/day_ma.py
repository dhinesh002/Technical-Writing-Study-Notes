import yfinance as yf
import pandas as pd
import pandas as pd


file_path = 'stock_list.xlsx'
df = pd.read_excel(file_path)
symbols = df.iloc[:, 1].dropna().tolist()

# symbols = ['TCS']
symbol = 'TCS.NS'
start_date = '2024-9-13'
end_date = '2024-12-13'
interval = '1d'

for symbol in symbols :
    try:
        stock = yf.Ticker(f'{symbol}.NS')
        data = stock.history(start=start_date, end=end_date,interval=interval)
        data = data.drop(columns=['Dividends', 'Stock Splits'])

        data['9EMA'] = data['Close'].rolling(window=9).mean()
        data['20EMA'] = data['Close'].rolling(window=20).mean()

        last_2_days_data = data.tail(2)

        current_day = last_2_days_data.iloc[-1]
        last_before_day = last_2_days_data.iloc[-2]

        current_day_ema9 = float(current_day['9EMA'])
        current_day_ema20 = float(current_day['20EMA'])

        last_before_day_ema9 = float(last_before_day['9EMA'])
        last_before_day_ema20 = float(last_before_day['20EMA'])

        if  current_day_ema9 >=current_day_ema20 and last_before_day_ema9 <= last_before_day_ema20 :
            print(symbol)

    except:
        pass    