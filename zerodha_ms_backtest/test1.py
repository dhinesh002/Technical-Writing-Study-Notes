from datetime import datetime, timedelta

total_candles = 0
date = datetime.now()  # Start with the current date

while total_candles < 5:
    # print(date.strftime("%Y-%m-%d"))  
    date = date - timedelta(days=1) 
    print(date)
    total_candles += 1
