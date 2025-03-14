
# from tradingview_ta import *
# from concurrent.futures import ThreadPoolExecutor


# list_of_stocks = []
# with open("leverage_5x_stocks.txt", "r") as file:
#     for line in file:
#         symbol = line.strip().lower()
#         if symbol != "":
#             list_of_stocks.append(f'nse:{symbol}')

# from tradingview_ta import *

# def analysis_stock(interval)  : 
   
#     analysis = get_multiple_analysis(screener="india", interval=interval, symbols=list_of_stocks)
#     return analysis
  
# top_gainer = []
# indicator_buy_signal_stocks = []

# def data_manipulation():
#     data = analysis_stock(Interval.INTERVAL_1_DAY)
#     for symbol in list_of_stocks:
#         try:
#             stock_analysis = data[symbol.upper()]
#             volume = stock_analysis.indicators['volume']
#             close_price = stock_analysis.indicators["close"]
#             open_price = stock_analysis.indicators["open"]
#             change = close_price - open_price
#             ADX = stock_analysis.indicators['ADX']
#             ADX_plus_DI = stock_analysis.indicators['ADX+DI']
#             ADX_plus_DI_1= stock_analysis.indicators['ADX+DI[1]']
#             ADX_minus_DI_1 = stock_analysis.indicators['ADX-DI[1]']
#             RSI = stock_analysis.indicators['RSI']
#             MACD = stock_analysis.indicators['MACD.macd']
#             MACD_SIGNAL = stock_analysis.indicators['MACD.signal']
#             Stoch_K  = stock_analysis.indicators['Stoch.K']
#             Stoch_D  = stock_analysis.indicators['Stoch.D']
#             CCI20 = stock_analysis.indicators['CCI20']
#             percentage_change = (change / open_price) * 100 if open_price != 0 else 0
#             if change > 0:
#                 top_gainer.append({'symbol': symbol,  'change': change, 'percentage_change': percentage_change,'volume':volume})


#             if (
#             RSI < 30 and  # RSI below 30 indicates oversold
#             ADX > 25 and  # Strong trend exists
#             ADX_plus_DI > ADX_minus_DI_1 and  # Current positive DI is stronger than previous negative DI
#             MACD > MACD_SIGNAL and  # MACD is above the signal line
#             Stoch_K < 20 and Stoch_D < 20 and  # Stochastic indicators are in the oversold range
#             CCI20 < -100  # CCI is oversold
#         ):
#                 print("Strong Buy Signal!")
#                 indicator_buy_signal_stocks.append({'symbol': symbol})
#             else:
#                 print('no signal')
            

        
        
#         except Exception as e:
#             print(e)
#             pass

#     data = {'top_gainer': top_gainer , 'indicator_buy_signal_stocks': indicator_buy_signal_stocks
#     'top_gainer1': top_gainer ,'top_gainer2': top_gainer }




from flask import Flask, render_template, jsonify
from tradingview_ta import get_multiple_analysis, Interval
import time
from datetime import datetime

app = Flask(__name__)

# Load stock symbols from file
list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip().lower()
        if symbol != "":
            list_of_stocks.append(f'nse:{symbol}')

# Function to fetch stock analysis
def analysis_stock(interval):
    return get_multiple_analysis(screener="india", interval=interval, symbols=list_of_stocks)

# Route for fetching and processing data
@app.route('/fetch_data')
def fetch_data():
    try:
        top_gainer = []
        top_gainer_5minute = []
        indicator_buy_signal_stocks = []
        analysis_data = analysis_stock(Interval.INTERVAL_1_DAY)
        analysis_data_5minute = analysis_stock(Interval.INTERVAL_5_MINUTES)

        
        for symbol in list_of_stocks:
            try:
                stock_analysis = analysis_data[symbol.upper()]
                stock_analysis_5minute = analysis_data_5minute[symbol.upper()]
                volume = stock_analysis.indicators['volume']
                close_price = stock_analysis.indicators["close"]
                open_price = stock_analysis.indicators["open"]
                change = close_price - open_price
                ADX = stock_analysis.indicators['ADX']
                ADX_plus_DI = stock_analysis.indicators['ADX+DI']
                ADX_plus_DI_1 = stock_analysis.indicators['ADX+DI[1]']
                ADX_minus_DI_1 = stock_analysis.indicators['ADX-DI[1]']
                RSI = stock_analysis.indicators['RSI']
                MACD = stock_analysis.indicators['MACD.macd']
                MACD_SIGNAL = stock_analysis.indicators['MACD.signal']
                Stoch_K = stock_analysis.indicators['Stoch.K']
                Stoch_D = stock_analysis.indicators['Stoch.D']
                CCI20 = stock_analysis.indicators['CCI20']
                percentage_change = (change / open_price) * 100 if open_price != 0 else 0

                change_5minute = stock_analysis_5minute.indicators["close"] - stock_analysis_5minute.indicators["open"]
                percentage_change_5minute = (change_5minute / stock_analysis_5minute.indicators["open"]) * 100 if open_price != 0 else 0

                # Populate Top Gainers
                if change > 0:
                    top_gainer.append({ 'time':datetime.now().strftime("%d %b %H:%M:%S") ,'symbol': symbol, 'change': change, 'percentage_change': percentage_change, 'volume': volume, 'adx':ADX })
                    
                if change_5minute > 0:
                    top_gainer_5minute.append(
                        {'time':datetime.now().strftime("%d %b %H:%M:%S"),'symbol': symbol, 'change': change_5minute, 'percentage_change': percentage_change_5minute, 'volume': stock_analysis_5minute.indicators["volume"] , 'adx':stock_analysis_5minute.indicators["ADX"] }
                    )

                # Check for Strong Buy Signal
                if (
                    RSI < 30 and
                    ADX > 25 and
                    ADX_plus_DI > ADX_minus_DI_1 and
                    MACD > MACD_SIGNAL and
                    Stoch_K < 20 and Stoch_D < 20 and
                    CCI20 < -100
                ):
                    indicator_buy_signal_stocks.append({'symbol': symbol})
            except Exception as e:
                pass
                # print(f"Error processing {symbol}: {e}")
        
        # top_gainer = sorted(top_gainer, key=lambda x: x['percentage_change'], reverse=True)[:20]
        
        top_gainer_5minute = sorted(top_gainer_5minute, key=lambda x: x['percentage_change'], reverse=True)[:20]
        top_gainer_5minute_1 = sorted(top_gainer_5minute, key=lambda x: x['volume'], reverse=True)[:20]

        # print(top_gainer_5minute_1)
        from concurrent.futures import ThreadPoolExecutor

        def write_to_file(file_name, data):
            with open(file_name, "a") as file:
                file.write("\n".join([f"{entry}" for entry in data]) + "\n")

        files_data = [
            ("text/top_gainers.txt", top_gainer),
            ("text/top_gainer_5minute.txt", top_gainer_5minute),
            ("text/top_gainer_5minute_1.txt", top_gainer_5minute_1)
        ]

        with ThreadPoolExecutor() as executor:
            for file_name, data in files_data:
                executor.submit(write_to_file, file_name, data)


        return jsonify({
            'top_gainer': [],
            # 'indicator_buy_signal_stocks': indicator_buy_signal_stocks,
            'top_gainer1': top_gainer_5minute,
            'top_gainer2': top_gainer_5minute_1
        })
    except Exception as e:
        print(e)
        pass

        # return jsonify({'error': str(e)})

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('adx.html')

if __name__ == '__main__':
    app.run(debug=True)
