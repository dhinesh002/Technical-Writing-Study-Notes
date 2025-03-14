# import logging
# import os
# import json
# from kiteconnect import KiteConnect, KiteTicker
# from datetime import datetime, timedelta
# import pandas as pd
# import time
# from concurrent.futures import ThreadPoolExecutor
# import json


# api_key = ''
# secret = ''

# kite = KiteConnect(api_key=api_key)

# TOKEN_FILE = "access_token.json"

# def save_access_token(token):
#     with open(TOKEN_FILE, 'w') as f:
#         json.dump({"access_token": token}, f)

# def load_access_token():
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, 'r') as f:
#             data = json.load(f)
#             return data.get("access_token")
#     return None

# from datetime import datetime, timedelta

# def authenticate():
#     access_token = load_access_token()
#     if access_token:
#         kite.set_access_token(access_token)
#         try:
#             kite.margins() 
#         except Exception as e:
#             logging.warning("Access token may be invalid, re-authenticating...")
#             return get_access_token() 
#     else:
#         return get_access_token()

# def get_access_token():
#     print("Go to the following URL to authorize:")
#     print(kite.login_url())
#     request_token = input("Enter the request token: ")
#     data = kite.generate_session(request_token, api_secret=secret)
#     kite.set_access_token(data["access_token"])
#     save_access_token(data["access_token"])
  

# authenticate()



# data = kite.historical_data(
#             instrument_token=kite.ltp("NSE:" + 'WIPRO')["NSE:" + 'WIPRO']["instrument_token"],
#             from_date='2024-11-01',
#             to_date='2025-01-01',
#             interval='2minute',
#         )

# df = pd.DataFrame(data)
# print(df)
# # Optionally, save the data to a CSV file for further analysis
# df.to_csv('wipro_2min_historical_data.csv', index=False)

# # price_data = data['Close']
# # print(price_data)


# # --------------------------

# # data = kite.historical_data(
# #             instrument_token=kite.ltp("NSE:" + 'WIPRO')["NSE:" + 'WIPRO']["instrument_token"],
# #             from_date='2024-11-01',
# #             to_date='2025-01-01',
# #             interval='2minute',
# #         )

# # df = pd.DataFrame(data)
# # print(df)
# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt

# # # Assuming you have the `df` DataFrame populated with your data

# # # Convert the date column to pandas datetime
# # df['date'] = pd.to_datetime(df['date'])

# # # Set the date column as the index for easier time-based operations
# # df.set_index('date', inplace=True)

# # # Calculate 50-period and 200-period Simple Moving Averages (SMA)
# # df['SMA50'] = df['close'].rolling(window=50).mean()
# # df['SMA200'] = df['close'].rolling(window=200).mean()

# # # Initialize columns for Buy/Sell signals and position tracking
# # df['Signal'] = 0  # 0 means no position, 1 means buy, -1 means sell
# # df['Position'] = 0  # This will hold the strategy position (1 = long, 0 = no position, -1 = short)

# # # Define strategy logic:
# # # Buy when the close price crosses above the 50-period SMA
# # # Sell when the close price crosses below the 50-period SMA
# # for i in range(1, len(df)):
# #     if df['close'].iloc[i] > df['SMA50'].iloc[i] and df['close'].iloc[i-1] <= df['SMA50'].iloc[i-1]:
# #         df.at[df.index[i], 'Signal'] = 1  # Buy signal
# #     elif df['close'].iloc[i] < df['SMA50'].iloc[i] and df['close'].iloc[i-1] >= df['SMA50'].iloc[i-1]:
# #         df.at[df.index[i], 'Signal'] = -1  # Sell signal

# # # Track positions and calculate returns
# # initial_balance = 100000  # Starting balance for the backtest
# # balance = initial_balance
# # positions = []
# # entry_price = 0
# # position_size = 0
# # wins = 0
# # losses = 0
# # max_win = 0
# # max_loss = 0

# # # Backtest logic with entry and exit conditions for both buy and sell
# # for i in range(1, len(df)):
# #     if df['Signal'].iloc[i] == 1 and balance > 0:  # Buy entry condition
# #         entry_price = df['close'].iloc[i]
# #         position_size = balance / entry_price
# #         positions.append({'Date': df.index[i], 'Action': 'Buy', 'Price': entry_price, 'Amount': position_size})
# #         balance = 0  # Funds used to buy
# #     elif df['Signal'].iloc[i] == -1 and len(positions) > 0 and balance == 0:  # Stop buy and sell condition
# #         sell_price = df['close'].iloc[i]
# #         balance += position_size * sell_price  # Close the buy position
# #         positions.append({'Date': df.index[i], 'Action': 'Sell', 'Price': sell_price, 'Amount': position_size})
# #         profit_or_loss = (sell_price - entry_price) * position_size
        
# #         # Track wins/losses and max win/loss
# #         if profit_or_loss > 0:
# #             wins += 1
# #             max_win = max(max_win, profit_or_loss)
# #         else:
# #             losses += 1
# #             max_loss = min(max_loss, profit_or_loss)
            
# #         position_size = 0  # Position is closed
# #     elif df['Signal'].iloc[i] == -1 and balance == 0:  # Sell entry condition
# #         entry_price = df['close'].iloc[i]
# #         position_size = balance / entry_price
# #         positions.append({'Date': df.index[i], 'Action': 'Sell', 'Price': entry_price, 'Amount': position_size})
# #         balance = 0  # Funds used to sell
# #     elif df['Signal'].iloc[i] == 1 and len(positions) > 0 and balance == 0:  # Stop sell and buy condition
# #         buy_price = df['close'].iloc[i]
# #         balance += position_size * buy_price  # Close the sell position
# #         positions.append({'Date': df.index[i], 'Action': 'Buy', 'Price': buy_price, 'Amount': position_size})
# #         profit_or_loss = (buy_price - entry_price) * position_size
        
# #         # Track wins/losses and max win/loss
# #         if profit_or_loss > 0:
# #             wins += 1
# #             max_win = max(max_win, profit_or_loss)
# #         else:
# #             losses += 1
# #             max_loss = min(max_loss, profit_or_loss)
            
# #         position_size = 0  # Position is closed

# # # Evaluate performance
# # final_balance = balance + (position_size * df['close'].iloc[-1])
# # profit_or_loss = final_balance - initial_balance
# # win_loss_ratio = wins / (losses if losses > 0 else 1)

# # # Print performance metrics
# # print(f"Initial Balance: {initial_balance}")
# # print(f"Final Balance: {final_balance}")
# # print(f"Profit/Loss: {profit_or_loss}")
# # print(f"Number of Trades: {len(positions)//2}")
# # print(f"Number of Wins: {wins}")
# # print(f"Number of Losses: {losses}")
# # print(f"Max Win: {max_win}")
# # print(f"Max Loss: {max_loss}")
# # print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")
# # print(f"Total Profit: {profit_or_loss}")

# # # Optionally, you could save the positions to a CSV file for further analysis
# # positions_df = pd.DataFrame(positions)
# # positions_df.to_csv('trading_positions.csv', index=False)


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Load the historical data into a DataFrame
data = pd.read_csv('wipro_2min_historical_data.csv')  # Example

# Select the price type (Close for simplicity)
price_data = data['close']
print(price_data)

# -----------------------

# Normalize data to range [0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_data = scaler.fit_transform(price_data.values.reshape(-1, 1))

# ------------------

# Sigmoid function for logistic regression
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# ------------------

# Define logistic regression function with additional arguments
def logistic_regression(X, Y, p, lr, iterations):
    w = np.zeros(X.shape[1])  # Initialize weights based on number of features in X
    loss = 0.0
    for i in range(iterations):
        hypothesis = sigmoid(np.dot(X, w))  # Prediction
        loss = -1.0 / len(X) * np.sum(Y * np.log(hypothesis) + (1.0 - Y) * np.log(1.0 - hypothesis)) 
        gradient = np.dot(X.T, (hypothesis - Y)) / len(X)  # Gradient calculation
        w = w - lr * gradient  # Update weights
    
    # Return both loss and prediction
    return loss, sigmoid(np.dot(X, w))  # Return both loss and prediction

# -----------------

# Generate synthetic data as features (similar to `synth_ds` in Pine Script)
X = np.log(np.abs(np.power(normalized_data, 2) - 1) + 0.5)

# Ensure X is a 2D array, since we need it to have shape (n_samples, n_features)
X = X.reshape(-1, 1)  # Make sure X is a 2D array (n_samples, 1)

# Label generation: 1 for 'BUY', 0 for 'SELL'
y = (price_data.shift(-1) > price_data).astype(int)  # Buy if next day's close is higher

# -----------------------

# Set the parameters for logistic regression
p = 1  # This seems to represent some parameter for your dot product or loss calculation
lr = 0.0009  # Learning rate
iterations = 1000  # Number of iterations for training

# Train logistic regression model
loss, model_predictions = logistic_regression(X[:-1], y[:-1], p, lr, iterations)

# ------------------

# Fit the logistic regression model using sklearn for comparison
model = LogisticRegression(max_iter=iterations, solver='lbfgs', C=1/lr)
model.fit(X[:-1], y[:-1])  # Fit the logistic regression model

# Predict the probabilities using the sklearn model
predictions = model.predict_proba(X[-1].reshape(-1, 1))[:, 1]

# -------------- 

# Assuming scaled_loss is a calculated threshold for buy/sell signals
scaled_loss = np.mean(model_predictions)  # Example placeholder for scaled_loss calculation

# Generate buy/sell signals for the entire dataset
buy_signal = price_data > scaled_loss  # Buy signal when price is greater than scaled_loss
sell_signal = price_data < scaled_loss  # Sell signal when price is lower than scaled_loss

# ------------

holding_period = 5  # Example holding period
position = None  # Start with no position
entry_time = None  # Variable to keep track of the entry time

for i in range(len(data)):
    if buy_signal[i]:
        position = 'long'
        entry_price = data['close'][i]
        entry_time = i  # Store the entry time
    elif sell_signal[i] and position == 'long' and i - entry_time >= holding_period:
        position = None
        exit_price = data['close'][i]
        profit = exit_price - entry_price
        print(f"Profit: {profit}")

# -----------

# # Plot the loss and predictions
# plt.plot(loss)
# plt.plot(model_predictions)
# plt.show()

# ------------

# Calculate cumulative returns
returns = np.diff(price_data)  # Assuming returns are calculated as price changes
cumulative_returns = np.cumsum(returns)  # Total return after each trade

# Calculate win rate
wins = np.sum(returns > 0)  # Count of winning trades
total_trades = len(returns)  # Total number of trades
win_rate = wins / total_trades
print(f"Win Rate: {win_rate:.2f}")
