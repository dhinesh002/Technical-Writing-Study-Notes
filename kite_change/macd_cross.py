from tradingview_ta import TA_Handler, Interval, Exchange
import time

# Load stock symbols from a file
# list_of_stocks = ['TCS']

# Load stock symbols from file
list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip().lower()
        list_of_stocks.append(symbol)


# Configure TradingView TA and fetch indicators
for stock in list_of_stocks:
    try:
        analysis = TA_Handler(
            symbol=stock,
            screener="india",  # Screener for NASDAQ stocks
            exchange="NSE",   # Exchange where the stock is listed
            interval=Interval.INTERVAL_1_MINUTE  # 1-day interval
        )
        result = analysis.get_analysis()
        ADX_plus_DI =result.indicators['ADX+DI']
        ADX_minus_DI =result.indicators['ADX-DI']

        ADX_plus_DI_1 =result.indicators['ADX+DI[1]']
        ADX_minus_DI_1 =result.indicators['ADX-DI[1]']

        if ADX_plus_DI > ADX_minus_DI and ADX_plus_DI_1 < ADX_minus_DI_1:
            print(stock)


        # print(result.indicators)
        # print(result.indicators.keys())
        # for key in result.indicators.keys():
            # print(key)


        # volume = result.indicators['volume']
   
        # if 0 < result.indicators['MACD.macd'] <= 0.10 and 0 < result.indicators['MACD.signal'] <= 0.10 and   result.indicators['ADX'] < 20:
        #     print(stock)

    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
