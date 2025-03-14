from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
from flask import Flask, render_template, jsonify
from concurrent.futures import ThreadPoolExecutor

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
            interval=Interval.INTERVAL_1_DAY,
        )
        analysis = handler.get_analysis()
        close_price = analysis.indicators["close"]
        open_price = analysis.indicators["open"]
        volume = analysis.indicators["volume"]

        change = close_price - open_price

        # Calculate percentage change
        percentage_change = (change / open_price) * 100 if open_price != 0 else 0

        if change > 0:
            up_side.append({
                'symbol': symbol,
                'change': change,
                'percentage_change': percentage_change,
                'price': close_price,
                'volume': volume
            })
        else:
            down_side.append({
                'symbol': symbol,
                'change': change,
                'percentage_change': percentage_change,
                'price': close_price,
                'volume': volume
            })
    except:
        print(symbol, 'not found')

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
