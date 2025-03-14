import concurrent.futures
import os
from datetime import datetime, timedelta
import logging
from kiteconnect import KiteConnect
from kite import Get_3min_candle_data
from stocks import Stock_symbol
from tradingview import Get_current_price
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrap import FindDepth

# Your API key and secret
api_key = ''
secret = ''
access_token_file = "access_token.txt"  # File to store access token


# Initialize the Kite Connect API
kite = KiteConnect(api_key=api_key)
kite.reqsession.timeout = (10, 30)  # (connect_timeout, read_timeout)

start_time = datetime.now()

def authenticate():
    """ Authenticate and generate a new session if no valid token exists. """
    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as file:
            access_token = file.read().strip()
            kite.set_access_token(access_token)
            try:
                # Try fetching user details to check if the token is still valid
                kite.profile()
                logging.info("Access token is valid. No need to reauthenticate.")
                return kite  # Return authenticated Kite instance
            except Exception as e:
                logging.warning(f"Token might have expired: {e}")

    # If token doesn't exist or is invalid, authenticate again
    print("Go to the following URL to authorize:")
    print(kite.login_url())
    request_token = input("Enter the request token: ")
    data = kite.generate_session(request_token, api_secret=secret)
    
    # Set and store the access token
    access_token = data["access_token"]
    kite.set_access_token(access_token)
    
    # Save the access token for future use
    with open(access_token_file, "w") as file:
        file.write(access_token)
    
    logging.info("Access token set and saved successfully.")
    return kite  # Return authenticated Kite instance

def main(kite):
    list_of_stocks = Stock_symbol.stock_symbol
    filtered_stocks = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_symbol = {executor.submit(Get_current_price.get_current_price, stock_symbol): stock_symbol for stock_symbol in list_of_stocks}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            data = future.result()  # Wait for the result only if needed
            if data:
                stock_symbol = data['symbol']
                high = data['high']
                open_price = data['open']
                low = data['low']
                volume = data['volume']
                current_price = data['current_price']
                percentage_change = ((current_price - open_price) / open_price) * 100
                if low == open_price and abs(percentage_change > 0.40):
                    filtered_stocks.append(stock_symbol)

    return filtered_stocks

def main1(kite, filtered_stocks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_symbol = {executor.submit(Get_3min_candle_data.get_3min_candle_data, kite, stock_symbol): stock_symbol for stock_symbol in filtered_stocks}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            data = future.result()  # Wait for the result only if needed
            if data:
                # print(data)
                Open = data['first_3m_candle_open']
                low = data['first_3m_candle_low']
                high = data['first_3m_candle_high']
                close = data['first_3m_candle_close']
                volume = data['volume']
                stock_symbol = data['stock_symbol']
                # best_bid_price = data['best_bid_price']
                # best_bid_qty= data['best_bid_qty']
                # best_ask_price = data['best_ask_price']
                # best_ask_qty=data['best_ask_qty']
                # avg_volume = data['avg_volume']

                bid=data['bid']
                sell=data['sell']
                # last_high = data['last_high']

                percentage_change = ((high - low) / low) * 100
                percentage_change = round(percentage_change , 2)
                # Open == low and  volume >=30000
                if Open == low  and  volume >=30000:
                    body_size = abs(Open - close)
                    upper_wick_size = high - max(Open, close)
                    if upper_wick_size < (body_size / 2):
                        # print(f'Good candle: {stock_symbol}')
                        i = 'Good'
                    else:
                        i = 'Normal'    

                        with open('watchlist.txt', 'a') as file:
                            file.write(f"""symbol: {stock_symbol}  - ({i}), sl: {Open}   , volume: {volume},  percentage_change: {percentage_change}, bid: {bid} , sell : {sell} , time: {datetime.now()}\n""")
                        
                        with open('orderlist.txt', 'a') as file:
                            file.write(f"""symbol: {stock_symbol} , {volume}\n""")

                    # pass

def calculate_trade_parameters(symbol):
    """
    Calculate trade entry, stop loss, and target based on market depth from Zerodha API.
    
    Parameters:
    - symbol: Stock symbol (e.g., 'AEROFLEX')
    
    Returns:
    - Dictionary containing 'symbol', 'entry', 'sl', and 'target'
    """
    
    try:
        # Fetch market depth (order book) for the stock
        market_depth = kite.quote([f'NSE:{symbol}'])

        # Access the depth data
        depth = market_depth[f'NSE:{symbol}']['depth']

        # Get the highest bid price (best entry price)
        entry_price = depth['buy'][0]['price']  # Highest bid price (entry)
        best_bid_below_entry = depth['buy'][1]['price']  # Second best bid price (potential SL)

        # Get the lowest sell price (for target calculation)
        target_price = depth['sell'][0]['price']  # Lowest sell price (target)
        
    except Exception as e:
        return f"Error fetching market depth: {str(e)}"
    
    # Stop loss set at the second highest bid price
    sl_price = best_bid_below_entry

    # Calculate the potential gain and risk
    potential_gain = target_price - entry_price  # Difference between target and entry
    risk = entry_price - sl_price  # Difference between entry and stop loss

    # Win rate calculation based on potential gain and risk (optional, depends on strategy)
    win_rate = (potential_gain / risk) if risk != 0 else None  # Risk/reward ratio

    # Return the trade parameters
    trade_parameters = {
        "symbol": symbol,
        "entry": round(entry_price, 2),
        "sl": round(sl_price, 2),
        "target": round(target_price, 2),
        "potential_gain": round(potential_gain, 2),
        "risk": round(risk, 2),
        "win_rate": round(win_rate, 2) if win_rate else "Undefined"
    }

    return trade_parameters


def place_trade_order(symbol, entry_price, sl_price, target_price, quantity):
    """
    Place a buy order, stop loss (SL), and target order using Zerodha API.

    Parameters:
    - symbol: Stock symbol (e.g., 'NSE:WIPRO')
    - entry_price: The price at which to enter the trade
    - sl_price: Stop loss price
    - target_price: Target price
    - quantity: Quantity of the order (default: 1)
    
    Returns:
    - Dictionary containing order responses
    """
    try:
        # Place a limit buy order at the entry price
        buy_order = kite.place_order(
            tradingsymbol=symbol,
            exchange='NSE',
            transaction_type='BUY',
            quantity=quantity,
            order_type='LIMIT',
            price=entry_price,
            product='MIS',  # 'MIS' for intraday or 'CNC' for delivery
            variety='regular'  # Regular order
        )
        import time
        time.sleep(20)
        print(f"Buy order placed successfully at {entry_price} , {datetime.now()}")
        buy_order_id =  buy_order['order_id']
        time.sleep(10) 
        order_history = kite.order_history(buy_order_id)
        print(buy_order_id)
        print(order_history)

                # Monitor the order status
        # while True:
        #     # Fetch the order history to get the current status
        #     order_history = kite.order_history(buy_order_id)
        #     print(order_history)
            
        #     # Check the most recent status
        #     if order_history:
        #         current_status = order_history[-1]['status']
        #         print(f"Current order status: {current_status}, {datetime.now()}")

        #         if current_status == 'COMPLETE':
        #             print("Order has been completed successfully.", datetime.now())
        #             break
        #     else:
        #         print("No order history found.", datetime.now())
        
        return {
            'buy_order': buy_order,
            # 'sl_order': sl_order,
            # 'target_order': target_order
        }

    except Exception as e:
        return f"Error placing order: {str(e)}"




gapup = []
gapdown = []

def gap(stock_symbol):
    try:
        # Today's date
        today = datetime.now().strftime('%Y-%m-%d')
        # today = (datetime.now() - timedelta(4)).strftime('%Y-%m-%d')


        # Yesterday's date
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        # Define the date and time range for today and yesterday
        from_date_today = f"{today} 09:15:00"   # Market open time today
        to_date_today = f"{today} 15:30:00"     # Market close time today

        from_date_yesterday = f"{yesterday} 09:15:00"  # Market open time yesterday
        to_date_yesterday = f"{yesterday} 15:30:00"    # Market close time yesterday

        # Fetch instrument token for the stock
        ltp_data = kite.ltp(f'NSE:{stock_symbol}')
        instrument_token = ltp_data[f'NSE:{stock_symbol}'].get('instrument_token')

        if not instrument_token:
            print(f"Instrument token not found for {stock_symbol}. LTP data: {ltp_data}")
            return  # Exit the function if instrument token is invalid

        # Fetch today's candle data (1-day interval to get open price)
        today_candle_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date_today,
            to_date=to_date_today,
            interval='day'
        )

        # Fetch yesterday's candle data (1-day interval)
        yesterday_candle_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date_yesterday,
            to_date=to_date_yesterday,
            interval='day'
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
            print({'symbol': stock_symbol, 'percentage': percentage_change_high})
            gapup.append({'symbol': stock_symbol, 'percentage': percentage_change_high})

        if today_open < yesterday_low:
            print({'symbol': stock_symbol, 'percentage': percentage_change_low})
            gapdown.append({'symbol': stock_symbol, 'percentage': percentage_change_low})

    except Exception as e:
        print(f"Error getting price for {stock_symbol}: {str(e)}")


# Stock_symbol.stock_symbol
import re
def extract_symbols(file_path):
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Use regex to find all symbols in the format 'symbol: SYMBOL_NAME'
        symbols = re.findall(r'symbol:\s*([A-Za-z0-9]+)', file_content)

        # Print the symbols as a list
        # print(symbols)
        return symbols

    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    kite = authenticate()  # Authenticate and get the Kite instance
    v1 = input('Authentication success. Do you want to continue (Y/N)? ')
    if v1.capitalize() == 'Y':
        filtered_stocks = main(kite)
    v2 = input('Filteration completed. Do you want to continue (Y/N)? ')
    if v2.capitalize() == 'Y':
        main1(kite, Stock_symbol.stock_symbol)
        # main1(kite, filtered_stocks)



#         kite_ticker = KiteTicker("your_api_key", access_token)

# # Assign callbacks
#         kite_ticker.on_ticks = on_ticks

#         # Subscribe to instrument
#         instrument_token = "your_instrument_token"  # Replace with your instrument token
#         kite_ticker.subscribe([instrument_token])
#         kite_ticker.connect(threaded=True)


        # # List of stock symbols to process
        # stock_symbols = Stock_symbol.stock_symbol

        #     # Use ThreadPoolExecutor for concurrent execution
        # with ThreadPoolExecutor(max_workers=2) as executor:  # Adjust 'max_workers' as needed
        #         futures = [executor.submit(gap, symbol) for symbol in stock_symbols]
                
        #         for future in as_completed(futures):
        #             try:
        #                 future.result()  # Retrieve the result (if any) to handle exceptions
        #             except Exception as e:
        #                 print(f"Error in concurrent execution: {e}")

        #     # Sort the gapup and gapdown lists by percentage in descending order
        # gapup_sorted = sorted(gapup, key=lambda x: x['percentage'], reverse=True)
        # gapdown_sorted = sorted(gapdown, key=lambda x: x['percentage'], reverse=True)
        # print(stock_symbols)
        #     # Write gapup data to a file
        # with open('gapup.txt', 'a') as file:
        #         for item in gapup_sorted:
        #             file.write(f'{item}\n')

        #     # Write gapdown data to a file
        # with open('gapdown.txt', 'a') as file:
        #         for item in gapdown_sorted:
        #             file.write(f'{item}\n')




    
     



# Log end time
end_time = datetime.now()
print(f"Start time: {start_time}")
print(f"End time: {end_time}")
print(f"Total time: {end_time - start_time}")

