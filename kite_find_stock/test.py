# Sample data: A list of dictionaries with buy and sell depth values
data = [
    {'item': 'Stock A', 'buy_depth': 100, 'sell_depth': 50},
    {'item': 'Stock B', 'buy_depth': 200, 'sell_depth': 100},
    {'item': 'Stock C', 'buy_depth': 150, 'sell_depth': 300},
    {'item': 'Stock D', 'buy_depth': 250, 'sell_depth': 250},
]

# Function to calculate the ratios in the desired format
def calculate_ratios(data):
    ratios = []
    for entry in data:
        item = entry['item']
        buy_depth = entry['buy_depth']
        sell_depth = entry['sell_depth']
        
        # Check for valid depths to avoid division by zero
        if buy_depth > 0 and sell_depth > 0:
            if buy_depth > sell_depth:
                ratio = f"1 : {sell_depth / buy_depth:.2f}"
            else:
                ratio = f"{buy_depth / sell_depth:.2f} : 1"
        else:
            ratio = "undefined (buy or sell depth is zero)"  # Handling zero depths
        
        ratios.append({'item': item, 'ratio': ratio})
    return ratios

# Calculate ratios
ratios = calculate_ratios(data)

# Output the results
for result in ratios:
    item = result['item']
    ratio = result['ratio']
    print(f'The buy/sell ratio for {item} is {ratio}.')
