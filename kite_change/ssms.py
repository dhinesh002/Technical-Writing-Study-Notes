
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


# -----------------------------------------
# -------------------------------------------


from flask import Flask, render_template, jsonify
from tradingview_ta import get_multiple_analysis, Interval
import time
from datetime import datetime
import pyodbc

# Connection configuration
server = r'DESKTOP-SP7Q1UT\SQLEXPRESS'  # Use a raw string for the server name
database = 'moving_average_project'  # Replace with your database name

# Connection string for Windows Authentication
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)


from tradingview_ta import *
from concurrent.futures import ThreadPoolExecutor
import time 

while True:


    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")

        handler = TA_Handler(
                symbol='TCS',
                screener="india",
                exchange="NSE",
                interval=Interval.INTERVAL_1_DAY,
            )
        analysis = handler.get_analysis()
        # print(analysis.indicators)

        values = {}
        symbol="NSE:TCS"
        quote_data = kite.quote([symbol])
        # print(quote_data)
        buy_quantity= quote_data[symbol]['buy_quantity']
        sell_quantity= quote_data[symbol]['sell_quantity']
        market_depth = quote_data[symbol]["depth"]

        values['buy_quantity'] = buy_quantity
        values['sell_quantity'] = sell_quantity

        # Initialize empty lists to store values
        buy_side = []  # For buy-side (bids)
        sell_side = []  # For sell-side (asks)

        # Extract buy-side data
        for bid in market_depth["buy"]:
            buy_side.append({
                "price": bid["price"],
                "quantity": bid["quantity"],
                "orders": bid["orders"]
            })

        # Extract sell-side data
        for ask in market_depth["sell"]:
            sell_side.append({
                "price": ask["price"],
                "quantity": ask["quantity"],
                "orders": ask["orders"]
            })

        # Remove the duplicated assignments for buy-side
        values['level1_price'] = buy_side[0]['price']
        values['level1_quantity'] = buy_side[0]['quantity']
        values['level1_orders'] = buy_side[0]['orders']

        values['level2_price'] = buy_side[1]['price']
        values['level2_quantity'] = buy_side[1]['quantity']
        values['level2_orders'] = buy_side[1]['orders']

        values['level3_price'] = buy_side[2]['price']
        values['level3_quantity'] = buy_side[2]['quantity']
        values['level3_orders'] = buy_side[2]['orders']

        values['level4_price'] = buy_side[3]['price']
        values['level4_quantity'] = buy_side[3]['quantity']
        values['level4_orders'] = buy_side[3]['orders']

        values['level5_price'] = buy_side[4]['price']
        values['level5_quantity'] = buy_side[4]['quantity']
        values['level5_orders'] = buy_side[4]['orders']
        values['symbol'] = 'TCS'
        values['time'] = datetime.now()

        cursor = conn.cursor()

        # SQL: Insert data
        insert_query = """
        INSERT INTO TradeData (
            buy_quantity, sell_quantity, level1_price, level1_quantity, level1_orders, 
            level2_price, level2_quantity, level2_orders, level3_price, level3_quantity, 
            level3_orders, level4_price, level4_quantity, level4_orders, level5_price, 
            level5_quantity, level5_orders, symbol, time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cursor.execute(insert_query, *values.values())
            conn.commit()
            print("Data inserted successfully!")
        except pyodbc.Error as e:
            print(f"Error inserting data: {e}")

        # Close the connection
        cursor.close()
        conn.close()
        time.sleep(1)
        # print(values)


    except Exception as e:
        print("Error connecting to the database:", e)

