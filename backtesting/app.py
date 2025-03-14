

from tradingview_ta import TA_Handler, Interval, Exchange

handler = TA_Handler(
                        symbol= 'ITC',
                        screener="india",
                        exchange="NSE",
                        interval=Interval.INTERVAL_1_DAY,
                        )
                    
indicator  = handler.get_analysis().indicators
rsi = indicator['RSI']
# print(rsi)
current_price = indicator['close']
print(indicator)