from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Attach to existing Chrome session
options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Firefox()
driver.get('https://kite.zerodha.com/chart/web/tvc/NSE/SUZLON/3076609')
import time 

for i in range(0, 100):
    time.sleep(1)
    print(i)


bid_list = []
ask_list = []


# for i in range(1, 20):
#     bid_element = driver.find_element(By.XPATH , f'/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[1]/tbody/tr[{i}]')

#     bid_element = bid_element.text.split()
       
#     bid = float(bid_element[0])  # Convert the first element to float
#     bid_orders = int(bid_element[1])  # Convert the second element to int
#     bid_quantity = int(bid_element[2])  # Convert the third element to int

#     ask_element = driver.find_element(By.XPATH , f'/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[2]/tbody/tr[{i}]')
   

#     ask_element = ask_element.text.split()
#     ask = float(ask_element[0])  # Convert the first element to float
#     ask_orders = int(ask_element[1])  # Convert the second element to int
#     ask_quantity = int(ask_element[2])  # Convert the third e



#     total_bid = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[1]/tfoot/tr')
#     total_ask= driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[2]/tfoot/tr')

    
#     bid_list.append({'bid': bid , 'bid_orders': bid_orders, 'bid_quantity': bid_quantity})
#     ask_list.append({'ask': ask , 'ask_orders': ask_orders, 'ask_quantity': ask_quantity})

#     # print(f'total_bid: {total_bid}')
#     # print(f'total_ask: {total_ask}')



# print(bid_list)

# print(ask_list)


# print(f'total_bid: {total_bid.text}')
# print(f'total_ask: {total_ask.text}')



# Loop to extract bid and ask data
for i in range(1, 20):
    # Extract bid data
    bid_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[1]/tbody/tr[{i}]')
    bid_element = bid_element.text.split()
    
    bid = float(bid_element[0])  # Convert the first element to float
    bid_orders = int(bid_element[1])  # Convert the second element to int
    bid_quantity = int(bid_element[2])  # Convert the third element to int

    # Extract ask data
    ask_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[2]/tbody/tr[{i}]')
    ask_element = ask_element.text.split()
    
    ask = float(ask_element[0])  # Convert the first element to float
    ask_orders = int(ask_element[1])  # Convert the second element to int
    ask_quantity = int(ask_element[2])  # Convert the third element to int

    # Collect data
    bid_list.append({'bid': bid, 'bid_orders': bid_orders, 'bid_quantity': bid_quantity})
    ask_list.append({'ask': ask, 'ask_orders': ask_orders, 'ask_quantity': ask_quantity})

# Total bid and ask values
total_bid = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[1]/tfoot/tr')
total_ask = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/div/div/div[1]/div[1]/table[2]/tfoot/tr')

print(bid_list)
print(ask_list)
print(f'Total Bid: {total_bid.text}')
print(f'Total Ask: {total_ask.text}')

# Apply your trading strategy
def apply_strategy(bid_list, ask_list):
    if not bid_list or not ask_list:
        return

    # Get the highest bid and lowest ask
    highest_bid = max(item['bid'] for item in bid_list)
    lowest_ask = min(item['ask'] for item in ask_list)

    # Define your strategy parameters (thresholds can be adjusted)
    buy_threshold = 74.0  # Example threshold for buying
    sell_threshold = 74.05  # Example threshold for selling

    # Apply strategy
    if highest_bid > buy_threshold:
        print("Buy Signal: Consider buying at or below the highest bid of:", highest_bid)
    if lowest_ask < sell_threshold:
        print("Sell Signal: Consider selling at or above the lowest ask of:", lowest_ask)

# Call the strategy function
apply_strategy(bid_list, ask_list)