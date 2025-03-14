

# # # Define a dictionary to store the stock symbol and corresponding average volume
# # average_volumes = {}

# # # Open the file in read mode and populate average_volumes dictionary
# # with open('volume14.txt', 'r') as file:
# #     for line in file:
# #         # Strip extra spaces and remove surrounding brackets
# #         line = line.strip().strip('[]')
        
# #         # Split the line by the comma to separate the symbol and volume
# #         stock_symbol, average_volume = line.split(',')
        
# #         # Remove any extra spaces around the stock symbol and volume
# #         stock_symbol = stock_symbol.strip()
# #         average_volume = float(average_volume.strip())
        
# #         # Store the result in the dictionary
# #         average_volumes[stock_symbol] = average_volume



# # print(average_volumes)

# # # for i in average_volume:
# # #     print(i)

# # for stock_symbol, avg_volume in average_volumes.items():
# #     print(f'Stock: {stock_symbol}, Average Volume: {avg_volume}')



# import pyodbc

# # Define your connection string (update values as per your SQL Server configuration)
# def get_db_connection():
#     conn = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'  # Ensure the correct ODBC driver is installed
#         'SERVER=DESKTOP-SP7Q1UT\\SQLEXPRESS;'  # Use your server's name or IP address
#         'DATABASE=web_project;'  # The database name you want to connect to
#         'UID=;'  # SQL Server username
#         'PWD=;'  # SQL Server password
#         'Trusted_Connection=yes;'  # Set to 'yes' if using Windows authentication
#     )
#     return conn



# from flask import Flask, jsonify

# app = Flask(__name__)

# li = []
# # Function to connect and fetch data from SQL Server
# def fetch_data():
#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     # Execute your SQL query
#     cursor.execute("SELECT * FROM INDIA")  # Replace with your table name
    
#     # Fetch all rows from the result
#     rows = cursor.fetchall()
#     # print(rows[1])
#     for i in rows :
      
#         if i[3] == 'NSE':
#             li.append(i[1])

#     with open('nse_symbols.txt', 'w') as file:
#         for item in li:
#             file.write(f"{item}\n")
        
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()

#     # # Convert the data into a list of dictionaries
#     # data = []
#     # for row in rows:
#     #     data.append({
#     #         'column1': row[0],  # Replace with actual column names or indices
#     #         'column2': row[1],
#     #         # Add more columns as needed
#     #     })
    
#     # return data

# # Route to fetch data and return as JSON
# @app.route('/getdata', methods=['GET'])
# def getdata():
#     data = fetch_data()  # Fetch the data from SQL Server
#     # return jsonify(data)  # Return the data as JSON
#     pass

# if __name__ == '__main__':
#     app.run(debug=True)



from tradingview_ta import TA_Handler, Interval
import concurrent.futures
import time

def fetch_analysis(symbol):
    """Function to fetch analysis for a given symbol."""
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
        indicators = handler.get_analysis().indicators
        print(indicators['volume'])
        return symbol, indicators
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return symbol, None

# Start measuring time
start_time = time.time()

# Open the file in read mode
with open('nse_symbols.txt', 'r') as file:
    symbols = [line.strip() for line in file]

# Use ThreadPoolExecutor to fetch data concurrently
for i in range(0, 3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Map the fetch_analysis function to the symbols
        results = list(executor.map(fetch_analysis, symbols))

# # Print results
# for symbol, indicators in results:
#     if indicators is not None:
#         print(f"Indicators for {symbol}: {indicators}")

# Calculate and print the time taken
end_time = time.time()
print(f"Time taken to complete: {end_time - start_time:.2f} seconds")
