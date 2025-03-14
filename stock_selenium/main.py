
from tradingview_ta import TA_Handler, Interval
import json
from datetime import datetime
from package.kite_stocks import Kite_stocks
import json
from concurrent.futures import ThreadPoolExecutor, as_completed


Bullish = []
total_stock_list = Kite_stocks()


start_time = datetime.now()


def analyze_stock(item):
    try:
        # Initialize the TA_Handler
        handler = TA_Handler(
            symbol=item['symbol'],
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
        
        # Fetch indicators
        EMA20 = handler.get_analysis().indicators['EMA20']
        EMA10 = handler.get_analysis().indicators['EMA10']

        # Check condition
        if EMA10 > EMA20 and EMA10 > handler.get_analysis().indicators['EMA200']:
            with open('movingstock.txt', 'a') as file:
                file.write(f'{item['symbol']}\n')
            return item['symbol']
    except Exception as e:
        print(f"Error processing {item['symbol']}: {e}")
        return None

# Use ThreadPoolExecutor to process stocks concurrently
with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
    futures = [executor.submit(analyze_stock, item) for item in total_stock_list]
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            Bullish.append(result)

# Print the results
print("Bullish stocks:", Bullish)
print(len(Bullish))     
end_time = datetime.now()
print(f"Start time: {start_time}")
print(f"End time: {end_time}")
print(f"Total time: {end_time - start_time}")