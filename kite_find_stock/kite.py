from datetime import datetime, timedelta
from kiteconnect import KiteConnect
import logging
from scrap import FindDepth

class Get_3min_candle_data:
  
    def get_3min_candle_data(kite, stock_symbol):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            # today = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
            from_date = f"{today} 09:15:00"  # Start time for today (market open time)
            to_date = f"{today} 15:30:00"    # End time for today (market close time)

            day_before = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')
            fd = f"{day_before} 09:15:00"  # Start time for today (market open time)
            td = f"{day_before} 15:30:00"    # End time for today (market close time)

            print(today)
            print(day_before)

            # Get the instrument token for the stock symbol
            instrument_token = kite.ltp(f'NSE:{stock_symbol}')[f'NSE:{stock_symbol}']['instrument_token']

            # Fetch historical 3-minute candle data
            candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval='3minute'
            )

            # before_candle_data = kite.historical_data(
            #     instrument_token=instrument_token,
            #     from_date=fd,
            #     to_date=td,
            #     interval='3minute'
            # )
            # before_candle_data_last_candle = before_candle_data[-1]
            # last_high = before_candle_data_last_candle['high']

            first_3m_candle = candle_data[0]
            first_3m_candle_open = first_3m_candle['open']
            first_3m_candle_close = first_3m_candle['close']
            first_3m_candle_high = first_3m_candle['high']
            first_3m_candle_low = first_3m_candle['low']
            volume = first_3m_candle['volume']


            # Fetch market depth (order book) for the stock
            market_depth = kite.quote([f'NSE:{stock_symbol}'])

            # Access the depth data
            depth = market_depth[f'NSE:{stock_symbol}']['depth']

            # Best bid (buy) and ask (sell) prices and quantities
            best_bid_price = depth['buy'][0]['price']
            best_bid_qty = depth['buy'][0]['quantity']
            best_ask_price = depth['sell'][0]['price']
            best_ask_qty = depth['sell'][0]['quantity']
           
            data = {
              
                'first_3m_candle_open': first_3m_candle_open,
                'first_3m_candle_close': first_3m_candle_close,
                'first_3m_candle_high': first_3m_candle_high,
                'first_3m_candle_low': first_3m_candle_low,
                'volume': volume, 
                'stock_symbol': stock_symbol,
                'bid': depth['buy'] ,
                'sell': depth['sell'] , 
                # 'last_high': last_high
            }
            return data
        except Exception as e:
            print(f"Error getting price for {stock_symbol}: {e}")
            return None





    def gap(kite, stock_symbol):
        gapup = []
        gapdown = []
        try:

            # Today's date
            today = datetime.now().strftime('%Y-%m-%d')

            # Yesterday's date
            yesterday = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')

            # Define the date and time range for today and yesterday
            from_date_today = f"{today} 09:15:00"   # Market open time today
            to_date_today = f"{today} 15:30:00"     # Market close time today

            from_date_yesterday = f"{yesterday} 09:15:00"  # Market open time yesterday
            to_date_yesterday = f"{yesterday} 15:30:00"    # Market close time yesterday

            # Fetch instrument token for the stock
            instrument_token = kite.ltp(f'NSE:{stock_symbol}')[f'NSE:{stock_symbol}']['instrument_token']

            # Fetch today's candle data (3-minute interval to get the open price)
            today_candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date_today,
                to_date=to_date_today,
                interval='day'  # 'day' for daily candles, first candle will be today's open
            )

            # Fetch yesterday's candle data (1-day interval)
            yesterday_candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date_yesterday,
                to_date=to_date_yesterday,
                interval='day'  # 'day' for daily candles
            )

            # Extract today's open price
            today_open = today_candle_data[0]['open']

            # Extract yesterday's high and low
            yesterday_high = yesterday_candle_data[0]['high']
            yesterday_low = yesterday_candle_data[0]['low']

                        # Calculate percentage change between today's open and yesterday's high
            percentage_change_high = ((today_open - yesterday_high) / yesterday_high) * 100

            # Calculate percentage change between today's open and yesterday's low
            percentage_change_low = ((today_open - yesterday_low) / yesterday_low) * 100

            if today_open > yesterday_high:
               
                gapup.append({'symbol': stock_symbol , 'percentage':percentage_change_high })

            if today_open < yesterday_low:
              
                gapdown.append({'symbol': stock_symbol , 'percentage':percentage_change_low })               


        except Exception as e:
            print(f"Error getting price for {stock_symbol}: {e}")




  
    def get_1month_candle_data(kite, stock_symbol):
        try:
            today = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
            from_date = f"{today} 09:15:00"  # Start time for today (market open time)
            to_date = f"{today} 15:30:00"    # End time for today (market close time)

            # Get the instrument token for the stock symbol
            instrument_token = kite.ltp(f'NSE:{stock_symbol}')[f'NSE:{stock_symbol}']['instrument_token']

            # Fetch historical 3-minute candle data
            candle_data = kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval='3minute'
            )

            first_3m_candle = candle_data[0]
            first_3m_candle_open = first_3m_candle['open']
            first_3m_candle_close = first_3m_candle['close']
            first_3m_candle_high = first_3m_candle['high']
            first_3m_candle_low = first_3m_candle['low']
            volume = first_3m_candle['volume']


            # Fetch market depth (order book) for the stock
            market_depth = kite.quote([f'NSE:{stock_symbol}'])

            # Access the depth data
            depth = market_depth[f'NSE:{stock_symbol}']['depth']

            # Best bid (buy) and ask (sell) prices and quantities
            best_bid_price = depth['buy'][0]['price']
            best_bid_qty = depth['buy'][0]['quantity']
            best_ask_price = depth['sell'][0]['price']
            best_ask_qty = depth['sell'][0]['quantity']

            # avg_volume = get_1month_candle_data(kite, stock_symbol)
           
            data = {
                #  'avg_volume': 12 ,
                'first_3m_candle_open': first_3m_candle_open,
                'first_3m_candle_close': first_3m_candle_close,
                'first_3m_candle_high': first_3m_candle_high,
                'first_3m_candle_low': first_3m_candle_low,
                # 'volume': volume, 
                'stock_symbol': stock_symbol,
                'bid': depth['buy'] ,
                'sell': depth['sell'] , 
               
            }
            return data
        except Exception as e:
            print(f"Error getting price for {stock_symbol}: {e}")
            return None



def get_1month_candle_data(kite, stock_symbol):
    try:
        # Get today's date
        today = datetime.now().date()

        # Define the start date (30 days ago from today)
        start_date = today - timedelta(days=30)
        
        # Format dates for the API (3-minute candle data for the last 30 days)
        from_date = start_date.strftime('%Y-%m-%d 09:15:00')
        to_date = today.strftime('%Y-%m-%d 15:30:00')

        # Get the instrument token for the stock symbol
        instrument_token = kite.ltp(f'NSE:{stock_symbol}')[f'NSE:{stock_symbol}']['instrument_token']

        # Fetch historical 3-minute candle data for the last 30 days
        candle_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval='3minute'
        )

        # Extract the first 3-minute candle for each day
        first_candles = []
        current_day = None

        for candle in candle_data:
            candle_time = candle['date']
            # Check if this candle is the first of the day
            if current_day != candle_time.date():
                current_day = candle_time.date()
                first_candles.append(candle)

        # Calculate the average volume of the first 3-minute candle for the last 30 days
        if first_candles:
            total_volume = sum(candle['volume'] for candle in first_candles)
            average_volume = total_volume / len(first_candles)
        else:
            average_volume = 0

        # Return data including the calculated average volume
        data = {
            'stock_symbol': stock_symbol,
            'average_first_3m_candle_volume_last_30_days': average_volume,
            'first_candles': first_candles,  # Optional: to inspect the first candles
        }

        return data

    except Exception as e:
        print(f"Error getting price for {stock_symbol}: {e}")
        return None
