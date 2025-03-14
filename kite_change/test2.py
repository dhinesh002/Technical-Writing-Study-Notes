
# from tradingview_ta import *
# from concurrent.futures import ThreadPoolExecutor

# # Load stock list
# list_of_stocks = []
# with open("leverage_5x_stocks.txt", "r") as file:
#     for line in file:
#         symbol = line.strip()
#         if symbol != "":
#             list_of_stocks.append(symbol)

# list_of_stocks =['TCS']

# def process_stock(symbol):
#     try:
#         handler = TA_Handler(
#             symbol=symbol,
#             screener="india",
#             exchange="NSE",
#             interval=Interval.INTERVAL_1_DAY,
#         )
#         analysis = handler.get_analysis()
#         print(analysis.indicators)
#         print(analysis.indicators['Pivot.M.Demark.R1'])
#         print(analysis.indicators['Pivot.M.Demark.Middle'])
#         print(analysis.indicators['Pivot.M.Demark.S1'])

#         print('---------------')
#         print(analysis.indicators['Pivot.M.Classic.R1'])
#         print(analysis.indicators['Pivot.M.Classic.Middle'])
#         print(analysis.indicators['Pivot.M.Classic.S1'])



#         # Pivot.M.Demark.R1
#         # Pivot.M.Demark.Middle
#         # Pivot.M.Demark.S1
#         # Pivot.M.Woodie.R3
#         # Pivot.M.Woodie.R2
#         # Pivot.M.Woodie.R1
#         # Pivot.M.Woodie.Middle
#         # Pivot.M.Woodie.S1
#         # Pivot.M.Woodie.S2
#         # Pivot.M.Woodie.S3
#         # Pivot.M.Camarilla.R3
#         # Pivot.M.Camarilla.R2
#         # Pivot.M.Camarilla.R1
#         # Pivot.M.Camarilla.Middle
#         # Pivot.M.Camarilla.S1
#         # Pivot.M.Camarilla.S2
#         # Pivot.M.Camarilla.S3
#         # Pivot.M.Fibonacci.R3
#         # Pivot.M.Fibonacci.R2
#         # Pivot.M.Fibonacci.R1
#         # Pivot.M.Fibonacci.Middle
#         # Pivot.M.Fibonacci.S1
#         # Pivot.M.Fibonacci.S2
#         # Pivot.M.Fibonacci.S3
#         # Pivot.M.Classic.R3
#         # Pivot.M.Classic.R2
#         # Pivot.M.Classic.R1
#         # Pivot.M.Classic.Middle
#         # Pivot.M.Classic.S1
#         # Pivot.M.Classic.S2
#         # Pivot.M.Classic.S3




#         # print(analysis.summary['RECOMMENDATION'])
         
#         # print(analysis.oscillators['RECOMMENDATION'])
#         # print(analysis.moving_averages['RECOMMENDATION'])
#         # STRONG_BUY
#         # if analysis.moving_averages['RECOMMENDATION']  == "NEUTRAL":
#             # print(symbol)        
#         # if analysis.summary['RECOMMENDATION'] == analysis.oscillators['RECOMMENDATION'] == analysis.moving_averages['RECOMMENDATION'] == "STRONG_BUY":
#         #     print(symbol)

         

#         # macd = analysis.indicators['MACD.signal']
#         # ADX = analysis.indicators['ADX']
#         # macd_signal = analysis.indicators['MACD.macd']

#         # if -0.10 <= macd <= 0.10 and -0.10 <= macd_signal <= 0.10 and ADX < 20:
#         #     print(f"Symbol: {symbol}")
#         #     print(f"MACD.signal: {macd}")
#         #     print(f"MACD.macd: {macd_signal}")
#         #     print("-" * 50)
#         # print(macd)
#         # print(macd_signal)

#         # MACD.signal
#         # MACD.macd
#         # Get required indicators
#         # bb_lower = analysis.indicators['BB.lower']
#         # pivot_s1 = analysis.indicators['Pivot.M.Classic.S1']
#         # close_price = analysis.indicators['close']
#         # print(analysis.indicators)

#     except Exception as e:
#         # Handle exceptions silently or print them for debugging
#         print(f"Error processing {symbol}: {e}")

# # Use ThreadPoolExecutor for multithreading
# max_workers = 5  # You can adjust this based on your system's capacity
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
#     executor.map(process_stock, list_of_stocks)


# # from tradingview_ta import TA_Handler, Interval

# # def process_stock(symbol):
# #     try:
# #         handler = TA_Handler(
# #             symbol=symbol,              # BTCUSD for Bitcoin/US Dollar
# #             screener="crypto",          # Screener is set to crypto for cryptocurrencies
# #             exchange="COINBASE",         # Use your preferred exchange (e.g., BINANCE, COINBASE, etc.)
# #             interval=Interval.INTERVAL_1_MINUTE,  # Set your desired time interval
# #         )
# #         analysis = handler.get_analysis()

# #         # Retrieve indicators for analysis
# #         macd = analysis.indicators['MACD.signal']
# #         ADX = analysis.indicators['ADX']
# #         macd_signal = analysis.indicators['MACD.macd']
# #         print(analysis.indicators['close'])

# #         # # Example condition for MACD and ADX
# #         # if -0.10 <= macd <= 0.10 and -0.10 <= macd_signal <= 0.10 and ADX < 20:
# #         #     print(f"Symbol: {symbol} meets the criteria")
# #         #     print(f"MACD.signal: {macd}")
# #         #     print(f"MACD.macd: {macd_signal}")
# #         #     print(f"ADX: {ADX}")
# #         #     print("-" * 50)

# #     except Exception as e:
# #         print(f"Error processing {symbol}: {e}")


# # for i in range(0 , 100000):
# # # Call the function for BTC/USD
# #     process_stock("BTCUSD")


# import pyodbc

# # Connection configuration
# server = r'DESKTOP-SP7Q1UT\SQLEXPRESS'  # Use a raw string for the server name
# database = 'moving_average_project'  # Replace with your database name

# # Connection string for Windows Authentication
# connection_string = (
#     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#     f"SERVER={server};"
#     f"DATABASE={database};"
#     f"Trusted_Connection=yes;"
# )

# connection = pyodbc.connect(connection_string)
# cursor = connection.cursor()

# # Create the table with the necessary columns
# create_table_query = """
# CREATE TABLE market_data (
#     Recommend_Other FLOAT,
#     Recommend_All FLOAT,
#     Recommend_MA FLOAT,
#     RSI FLOAT,
#     RSI_1 FLOAT,
#     Stoch_K FLOAT,
#     Stoch_D FLOAT,
#     Stoch_K_1 FLOAT,
#     Stoch_D_1 FLOAT,
#     CCI20 FLOAT,
#     CCI20_1 FLOAT,
#     ADX FLOAT,
#     ADX_DI FLOAT,
#     ADX_DI_1 FLOAT,
#     ADX_DI_1_1 FLOAT,
#     AO FLOAT,
#     AO_1 FLOAT,
#     Mom FLOAT,
#     Mom_1 FLOAT,
#     MACD_macd FLOAT,
#     MACD_signal FLOAT,
#     Rec_Stoch_RSI INT,
#     Stoch_RSI_K FLOAT,
#     Rec_WR INT,
#     W_R FLOAT,
#     Rec_BBPower INT,
#     BBPower FLOAT,
#     Rec_UO INT,
#     UO FLOAT,
#     close FLOAT,
#     EMA5 FLOAT,
#     SMA5 FLOAT,
#     EMA10 FLOAT,
#     SMA10 FLOAT,
#     EMA20 FLOAT,
#     SMA20 FLOAT,
#     EMA30 FLOAT,
#     SMA30 FLOAT,
#     EMA50 FLOAT,
#     SMA50 FLOAT,
#     EMA100 FLOAT,
#     SMA100 FLOAT,
#     EMA200 FLOAT,
#     SMA200 FLOAT,
#     Rec_Ichimoku INT,
#     Ichimoku_BLine FLOAT,
#     Rec_VWMA INT,
#     VWMA FLOAT,
#     Rec_HullMA9 INT,
#     HullMA9 FLOAT,
#     Pivot_M_Classic_S3 FLOAT,
#     Pivot_M_Classic_S2 FLOAT,
#     Pivot_M_Classic_S1 FLOAT,
#     Pivot_M_Classic_Middle FLOAT,
#     Pivot_M_Classic_R1 FLOAT,
#     Pivot_M_Classic_R2 FLOAT,
#     Pivot_M_Classic_R3 FLOAT,
#     Pivot_M_Fibonacci_S3 FLOAT,
#     Pivot_M_Fibonacci_S2 FLOAT,
#     Pivot_M_Fibonacci_S1 FLOAT,
#     Pivot_M_Fibonacci_Middle FLOAT,
#     Pivot_M_Fibonacci_R1 FLOAT,
#     Pivot_M_Fibonacci_R2 FLOAT,
#     Pivot_M_Fibonacci_R3 FLOAT,
#     Pivot_M_Camarilla_S3 FLOAT,
#     Pivot_M_Camarilla_S2 FLOAT,
#     Pivot_M_Camarilla_S1 FLOAT,
#     Pivot_M_Camarilla_Middle FLOAT,
#     Pivot_M_Camarilla_R1 FLOAT,
#     Pivot_M_Camarilla_R2 FLOAT,
#     Pivot_M_Camarilla_R3 FLOAT,
#     Pivot_M_Woodie_S3 FLOAT,
#     Pivot_M_Woodie_S2 FLOAT,
#     Pivot_M_Woodie_S1 FLOAT,
#     Pivot_M_Woodie_Middle FLOAT,
#     Pivot_M_Woodie_R1 FLOAT,
#     Pivot_M_Woodie_R2 FLOAT,
#     Pivot_M_Woodie_R3 FLOAT,
#     Pivot_M_Demark_S1 FLOAT,
#     Pivot_M_Demark_Middle FLOAT,
#     Pivot_M_Demark_R1 FLOAT,
#     open FLOAT,
#     P_SAR FLOAT,
#     BB_lower FLOAT,
#     BB_upper FLOAT,
#     AO_2 FLOAT,
#     volume INT,
#     change FLOAT,
#     low FLOAT,
#     high FLOAT,
#     summary VARCHAR(10),
#     moving_averages VARCHAR(10),
#     oscillators VARCHAR(10),
#     buy_quantity INT,
#     sell_quantity INT,
#     level1_price FLOAT,
#     level1_quantity INT,
#     level1_orders INT,
#     level2_price FLOAT,
#     level2_quantity INT,
#     level2_orders INT,
#     level3_price FLOAT,
#     level3_quantity INT,
#     level3_orders INT,
#     level4_price FLOAT,
#     level4_quantity INT,
#     level4_orders INT,
#     level5_price FLOAT,
#     level5_quantity INT,
#     level5_orders INT,
#     symbol VARCHAR(20),
#     time_retrived DATETIME
# );
# """

# # Execute the create table query
# cursor.execute(create_table_query)
# connection.commit()
# print("Table created successfully.")





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

# Establishing the connection
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Create the table with the necessary columns
create_table_query = """
CREATE TABLE market_data (
    Recommend_Other FLOAT,
    Recommend_All FLOAT,
    Recommend_MA FLOAT,
    RSI FLOAT,
    RSI_1 FLOAT,
    Stoch_K FLOAT,
    Stoch_D FLOAT,
    Stoch_K_1 FLOAT,
    Stoch_D_1 FLOAT,
    CCI20 FLOAT,
    CCI20_1 FLOAT,
    ADX FLOAT,
    ADX_DI FLOAT,
    ADX_DI_1 FLOAT,
    ADX_DI_1_1 FLOAT,
    AO FLOAT,
    AO_1 FLOAT,
    Mom FLOAT,
    Mom_1 FLOAT,
    MACD_macd FLOAT,
    MACD_signal FLOAT,
    Rec_Stoch_RSI INT,
    Stoch_RSI_K FLOAT,
    Rec_WR INT,
    W_R FLOAT,
    Rec_BBPower INT,
    BBPower FLOAT,
    Rec_UO INT,
    UO FLOAT,
  [close] FLOAT,
    EMA5 FLOAT,
    SMA5 FLOAT,
    EMA10 FLOAT,
    SMA10 FLOAT,
    EMA20 FLOAT,
    SMA20 FLOAT,
    EMA30 FLOAT,
    SMA30 FLOAT,
    EMA50 FLOAT,
    SMA50 FLOAT,
    EMA100 FLOAT,
    SMA100 FLOAT,
    EMA200 FLOAT,
    SMA200 FLOAT,
    Rec_Ichimoku INT,
    Ichimoku_BLine FLOAT,
    Rec_VWMA INT,
    VWMA FLOAT,
    Rec_HullMA9 INT,
    HullMA9 FLOAT,
    Pivot_M_Classic_S3 FLOAT,
    Pivot_M_Classic_S2 FLOAT,
    Pivot_M_Classic_S1 FLOAT,
    Pivot_M_Classic_Middle FLOAT,
    Pivot_M_Classic_R1 FLOAT,
    Pivot_M_Classic_R2 FLOAT,
    Pivot_M_Classic_R3 FLOAT,
    Pivot_M_Fibonacci_S3 FLOAT,
    Pivot_M_Fibonacci_S2 FLOAT,
    Pivot_M_Fibonacci_S1 FLOAT,
    Pivot_M_Fibonacci_Middle FLOAT,
    Pivot_M_Fibonacci_R1 FLOAT,
    Pivot_M_Fibonacci_R2 FLOAT,
    Pivot_M_Fibonacci_R3 FLOAT,
    Pivot_M_Camarilla_S3 FLOAT,
    Pivot_M_Camarilla_S2 FLOAT,
    Pivot_M_Camarilla_S1 FLOAT,
    Pivot_M_Camarilla_Middle FLOAT,
    Pivot_M_Camarilla_R1 FLOAT,
    Pivot_M_Camarilla_R2 FLOAT,
    Pivot_M_Camarilla_R3 FLOAT,
    Pivot_M_Woodie_S3 FLOAT,
    Pivot_M_Woodie_S2 FLOAT,
    Pivot_M_Woodie_S1 FLOAT,
    Pivot_M_Woodie_Middle FLOAT,
    Pivot_M_Woodie_R1 FLOAT,
    Pivot_M_Woodie_R2 FLOAT,
    Pivot_M_Woodie_R3 FLOAT,
    Pivot_M_Demark_S1 FLOAT,
    Pivot_M_Demark_Middle FLOAT,
    Pivot_M_Demark_R1 FLOAT,
   [open] FLOAT,
    P_SAR FLOAT,
    BB_lower FLOAT,
    BB_upper FLOAT,
    AO_2 FLOAT,
    volume INT,
    change FLOAT,
    low FLOAT,
    high FLOAT,
    summary VARCHAR(10),
    moving_averages VARCHAR(10),
    oscillators VARCHAR(10),
    buy_quantity INT,
    sell_quantity INT,
    level1_price FLOAT,
    level1_quantity INT,
    level1_orders INT,
    level2_price FLOAT,
    level2_quantity INT,
    level2_orders INT,
    level3_price FLOAT,
    level3_quantity INT,
    level3_orders INT,
    level4_price FLOAT,
    level4_quantity INT,
    level4_orders INT,
    level5_price FLOAT,
    level5_quantity INT,
    level5_orders INT,
    symbol VARCHAR(20),
    time_retrived DATETIME
);
"""

# Execute the create table query
cursor.execute(create_table_query)
connection.commit()
print("Table created successfully.")

# Close the cursor and connection
cursor.close()
connection.close()
