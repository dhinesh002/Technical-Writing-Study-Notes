
from tradingview_ta import TA_Handler, Interval, Exchange

class Get_current_price:
    def get_current_price(symbol):
        try:
        
            handler = TA_Handler(
                symbol=symbol,
                screener="india",
                exchange="NSE",
                interval=Interval.INTERVAL_1_DAY,
            )
            indicators = handler.get_analysis().indicators
          
        
            data = {
                'symbol': symbol,
                    'open': indicators['open'],
                    'high': indicators['high'],
                    'current_price': indicators['close'],
                    'volume': indicators['volume'],
                    'low': indicators['low'],
                    'volume': indicators['volume']

            }
            # print(data)
     
            return data
        except Exception as e:
            print(f"Error getting price for {symbol}: {e}")
          
            return None
