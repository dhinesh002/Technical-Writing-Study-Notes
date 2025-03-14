from flask import Flask, jsonify, render_template
from tradingview_ta import TA_Handler, Interval
from concurrent.futures import ThreadPoolExecutor
import threading
import time

app = Flask(__name__)

# Global variable to store stock data
data = []
lock = threading.Lock()


# Function to fetch stock data for a single symbol
def fetch_stock_data(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol.strip(),
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )

        volume = handler.get_analysis().indicators['volume']
        price = handler.get_analysis().indicators['close']
        change = handler.get_analysis().indicators['change']
        change_percentage = (change / handler.get_analysis().indicators['open']) * 100
        change_percentage = f"{change_percentage:.2f}"

        return {
            "symbol": symbol,
            "volume": volume,
            "price": price,
            "change": change,
            "change_percentage": change_percentage,
        }
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None


# Function to update stock data
def update_stock_data():
    global data
    while True:
        with open("movingstock.txt", "r") as file:
            symbols = [line.strip() for line in file]

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:  # Use up to 10 workers
            future_to_symbol = {executor.submit(fetch_stock_data, symbol): symbol for symbol in symbols}
            for future in future_to_symbol:
                result = future.result()
                if result:
                    # print(result)
                    results.append(result)

        with lock:
            data = results

        time.sleep(120)  # Refresh every 2 minutes


# API to fetch stock data
@app.route("/data")
def get_data():
    with lock:
        return jsonify(data)


# Frontend route
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # Start the data updating thread
    threading.Thread(target=update_stock_data, daemon=True).start()
    app.run(debug=True)
