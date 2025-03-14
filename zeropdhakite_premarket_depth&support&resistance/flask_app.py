from flask import Flask, render_template, jsonify
import time
import concurrent.futures
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



app = Flask(__name__)

import json

support1_level = []
support2_level = []
resistance1_level =[]
resistance2_level =[]


# Load JSON data
with open("output_file.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Load stock list
list_of_stocks = []
with open("leverage_5x_stocks.txt", "r") as file:
    for line in file:
        symbol = line.strip()
        if symbol != "":
            list_of_stocks.append(symbol)

# list_of_stocks = ['TCS', 'WIPRO']
li = []  # Shared list for storing stock data


def fetch_data(symbol):
    """Fetch high and low data for a stock symbol."""
    try:
        token = kite.ltp("NSE:" + symbol)["NSE:" + symbol]["instrument_token"]
        data = kite.historical_data(
            instrument_token=token,
            from_date='2025-01-01',
            to_date='2025-01-01',
            interval='3minute'
        )
        # print(json_data[symbol])
        Pivot=json_data[symbol]['Pivot']
        Support1=json_data[symbol]['Support1']
        Support2=json_data[symbol]['Support2']
        Resistance1=json_data[symbol]['Resistance1']
        Resistance2=json_data[symbol]['Resistance2']
        # print(Pivot,Support1,Support2,Resistance1,Resistance2)
        # print(data[-1]['low'])
        if data[-1]['low'] <= Support2 :
            support2_level.append({'symbol': symbol,'price':data[-1]['close'],'volume': data[-1]['volume'],'Support2': Support2, 'time':data[-1]['date']})

        if data[-1]['low'] <= Support1 and  data[-1]['low'] >  Support2:
            support1_level.append({'symbol': symbol,'price':data[-1]['close'],'volume': data[-1]['volume'],'Support1': Support1, 'time':data[-1]['date']})

        if data[-1]['high'] >= Resistance2:
            resistance2_level.append({'symbol': symbol,'price':data[-1]['close'],'volume': data[-1]['volume'],'Resistance2': Resistance2, 'time':data[-1]['date']})

        if data[-1]['high'] >= Resistance1 and data[-1]['high'] <Resistance1:
            resistance2_level.append({'symbol': symbol,'price':data[-1]['close'],'volume': data[-1]['volume'],'Resistance1': Resistance1, 'time':data[-1]['date']})

        return symbol, data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return symbol, None


def fetch_all_stocks(symbols):
    """Fetch data for all stocks using threads."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(fetch_data, symbols))
    return results


@app.route('/')
def index():
    """Render the HTML template."""
    # fetch_all_stocks(list_of_stocks)

    return render_template('index.html')

@app.route('/data')
def get_data():
    """Fetch data for all stocks and return as JSON."""
    # Clear previous data to avoid duplication
    support1_level.clear()
    support2_level.clear()
    resistance1_level.clear()
    resistance2_level.clear()


    fetch_all_stocks(list_of_stocks)

    # Prepare response
    response_data = {
        'support1_level':support1_level,
        'support2_level':support2_level,
        'resistance1_level':resistance1_level,
        'resistance2_level':resistance2_level

    }
    print(datetime.now())
    print('*******************************************')
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True,port=5002)
