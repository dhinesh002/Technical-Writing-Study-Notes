import logging
import os
import json
from kiteconnect import KiteConnect, KiteTicker
from datetime import datetime, timedelta
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
import json


api_key = ''
secret = ''

kite = KiteConnect(api_key=api_key)

TOKEN_FILE = "access_token.json"

def save_access_token(token):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({"access_token": token}, f)

def load_access_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get("access_token")
    return None

from datetime import datetime, timedelta

def authenticate():
    access_token = load_access_token()
    if access_token:
        kite.set_access_token(access_token)
        try:
            kite.margins() 
        except Exception as e:
            logging.warning("Access token may be invalid, re-authenticating...")
            return get_access_token() 
    else:
        return get_access_token()

def get_access_token():
    print("Go to the following URL to authorize:")
    print(kite.login_url())
    request_token = input("Enter the request token: ")
    data = kite.generate_session(request_token, api_secret=secret)
    kite.set_access_token(data["access_token"])
    save_access_token(data["access_token"])
  

authenticate()



from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
from flask import Flask, render_template, jsonify
from concurrent.futures import ThreadPoolExecutor
import csv


# Load stock list
list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip()
        if symbol != "":
            list_of_stocks.append(symbol)

# print(list_of_stocks)

up_side = []
down_side = []

def process_stock(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_5_MINUTES,
        )
        analysis = handler.get_analysis()
        close_price = analysis.indicators["close"]
        open_price = analysis.indicators["open"]
        volume = analysis.indicators["volume"]
        oscillators_recommendation = analysis.oscillators['RECOMMENDATION']
        recommendation = analysis.summary['RECOMMENDATION']
        analysis_time = analysis.time

        change = close_price - open_price
        # print(analysis.summary['RECOMMENDATION'])
        # Calculate percentage change
        percentage_change = (change / open_price) * 100 if open_price != 0 else 0

        if change > 0:
            up_side.append({
                'symbol': symbol,
                'change': change,
                'percentage_change': percentage_change,
                'price': close_price,
                'volume': volume , 
                'oscillators_recommendation': oscillators_recommendation ,
                'analysis_time': analysis_time ,
                'recommendation': recommendation
            })
        else:
            down_side.append({
                'symbol': symbol,
                'change': change,
                'percentage_change': percentage_change,
                'price': close_price,
                'volume': volume ,
                'oscillators_recommendation': oscillators_recommendation ,
                'analysis_time': analysis_time,
                'recommendation': recommendation
            })
    except:
        # print(symbol, 'not found')
        pass

def get_total_depth(buy_depth, sell_depth):
    total_buy_quantity = sum([level['quantity'] for level in buy_depth if level['quantity'] > 0])
    total_sell_quantity = sum([level['quantity'] for level in sell_depth if level['quantity'] > 0])
    return total_buy_quantity, total_sell_quantity


def get_change():
    # Clear the previous data
    global up_side, down_side
    up_side = []
    down_side = []
    with ThreadPoolExecutor(max_workers=5) as executor:  # Set max_workers as desired
        executor.map(process_stock, list_of_stocks)
    # Sort up_side by 'percentage_change' in descending order and get top 20
    up_side_sortedby_percentage = sorted(up_side, key=lambda x: x['percentage_change'], reverse=True)[:20]
    up_side_sortedby_volume = sorted(up_side, key=lambda x: x['volume'], reverse=True)[:20]
    # Sort down_side by 'percentage_change' in ascending order and get top 20
    down_side_sortedby_percentage = sorted(down_side, key=lambda x: x['percentage_change'], reverse=False)[:20]
    down_side_sortedby_volume = sorted(down_side, key=lambda x: x['volume'], reverse=True)[:20]

    # print(up_side_sortedby_percentage)
    buyside_imabalance_ratio = 0
    imbalance = 0

    for data in up_side_sortedby_percentage:
        try:    
            market_depth = kite.quote("NSE:" + data['symbol'])
            buy_depth = market_depth[f'NSE:{data['symbol']}']['depth']['buy']
            sell_depth = market_depth[f'NSE:{data['symbol']}']['depth']['sell']
            total_buy_quantity, total_sell_quantity = get_total_depth(buy_depth, sell_depth)
            imbalance = total_buy_quantity - total_sell_quantity
            buyside_imabalance_ratio = 0

            if total_buy_quantity != 0 and  total_sell_quantity !=0:
                buyside_imabalance_ratio =  round((total_buy_quantity /total_sell_quantity) , 2)
            data['imbalance'] = imbalance
            data['buyside_imabalance_ratio'] = buyside_imabalance_ratio
        
        except:
            data['imbalance'] = imbalance
            data['buyside_imabalance_ratio'] = buyside_imabalance_ratio

    sellside_imabalance_ratio = 0
    imbalance = 0

    for data in down_side_sortedby_percentage:
        try:
            market_depth = kite.quote("NSE:" + data['symbol'])
            buy_depth = market_depth[f'NSE:{data['symbol']}']['depth']['buy']
            sell_depth = market_depth[f'NSE:{data['symbol']}']['depth']['sell']
            total_buy_quantity, total_sell_quantity = get_total_depth(buy_depth, sell_depth)
            imbalance = total_buy_quantity - total_sell_quantity
            
            if total_buy_quantity != 0 and  total_sell_quantity !=0:
                sellside_imabalance_ratio =  round((total_sell_quantity /total_buy_quantity) , 2)
            data['imbalance'] = imbalance
            data['sellside_imabalance_ratio'] = sellside_imabalance_ratio

        except:
            pass

    print(up_side_sortedby_percentage)

    # Open the CSV file in write mode
    with open('up_side_sortedby_percentage.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['symbol', 'change', 'percentage_change', 'price', 'volume','oscillators_recommendation', 'analysis_time', 'recommendation',
    'imbalance', 'buyside_imabalance_ratio'])
        # Write the header
        writer.writeheader()        
        # Loop through your data and write each dictionary as a row
        for item in up_side_sortedby_percentage:  # Assuming 'your_data' contains dictionaries like the ones you posted
            writer.writerow(item)

# -----------------------------------

    # Open the CSV file in write mode
    with open('down_side_sortedby_percentage.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['symbol', 'change', 'percentage_change', 'price', 'volume','oscillators_recommendation', 'analysis_time', 'recommendation',
    'imbalance', 'sellside_imabalance_ratio'])
        # Write the header
        writer.writeheader()        
        # Loop through your data and write each dictionary as a row
        for item in down_side_sortedby_percentage:  # Assuming 'your_data' contains dictionaries like the ones you posted
            writer.writerow(item)            

# ---------------------

    data = {
        'up_side_sortedby_percentage': up_side_sortedby_percentage,
        'up_side_sortedby_volume': up_side_sortedby_volume,
        'down_side_sortedby_percentage': down_side_sortedby_percentage,
        'down_side_sortedby_volume': down_side_sortedby_volume
    }

    return data

app = Flask(__name__)

@app.route('/')
def index():
    """Render the HTML template."""
    return render_template('index.html')

@app.route('/data')
def get_data():
    data = get_change()
    response_data = {'data': data}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True , port=5001)
