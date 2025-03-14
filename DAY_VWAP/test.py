from tradingview_ta import TA_Handler, Interval, Exchange

handler = TA_Handler(
    symbol="ADANIGREEN",
    screener="india",
    exchange="NSE",
    interval=Interval.INTERVAL_1_DAY
)
# print(handler.get_analysis().indicators)

high = handler.get_analysis().indicators['high']
low = handler.get_analysis().indicators['low']
close = handler.get_analysis().indicators['close']


vwap = (high+low+close)/3

vwap_3per_high = (vwap * 1.01)
vwap_3per_low = (vwap * 0.99)


print(vwap)
print(vwap_3per_high)
print(vwap_3per_low)


