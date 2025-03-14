import concurrent.futures
from tradingview_ta import TA_Handler, Interval

# Define a dictionary to store the stock symbol and corresponding average volume
average_volumes = {}

# Open the file in read mode and populate average_volumes dictionary
with open('volume14.txt', 'r') as file:
    for line in file:
        # Strip extra spaces and remove surrounding brackets
        line = line.strip().strip('[]')
        
        # Split the line by the comma to separate the symbol and volume
        stock_symbol, average_volume = line.split(',')
        
        # Remove any extra spaces around the stock symbol and volume
        stock_symbol = stock_symbol.strip()
        average_volume = float(average_volume.strip())
        
        # Store the result in the dictionary
        average_volumes[stock_symbol] = average_volume

# Function to calculate percentage volume change for a single stock
def process_stock(stock, average_volume):
    try:
        handler = TA_Handler(
            symbol=stock,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
        indicators = handler.get_analysis().indicators
        current_volume = indicators['volume']
        print(f"Stock: {stock}, Current Volume: {current_volume}")

        # Calculate the percentage change
        percentage_change = ((current_volume - average_volume) / average_volume) * 100

        # Return stock symbol and percentage change
        return (stock, percentage_change)
    
    except Exception as e:
        print(f"Error processing {stock}: {e}")
        return (stock, None)  # Return None for stocks where an error occurred

# List to store percentage changes
volume_changes = []

# Use ThreadPoolExecutor for parallel processing
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks to the executor for each stock and store futures
    futures = [executor.submit(process_stock, stock, volume) for stock, volume in average_volumes.items()]
    
    # Process the results as they complete
    for future in concurrent.futures.as_completed(futures):
        stock, percentage_change = future.result()
        if percentage_change is not None:
            volume_changes.append((stock, percentage_change))

# Sort the list based on percentage change in descending order (highest to lowest)
volume_changes.sort(key=lambda x: x[1], reverse=True)

# Save the sorted results into a text file
with open('volume_change.txt', 'w') as file:
    for stock, change in volume_changes:
        file.write(f"[{stock} , {change:.2f}%]\n")

    print("Sorted volume changes saved to 'volume_change.txt'")
