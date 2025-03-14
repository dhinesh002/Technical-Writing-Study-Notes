from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Attach to existing Chrome session
options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome()
driver.get('https://kite.zerodha.com/chart/web/tvc/NSE/SUZLON/3076609')
import time 

# time.sleep(120)
for i in range(0, 100):
    time.sleep(1)
    print(i)
try:
    for i in range(1, 20):
        bid_element = driver.find_element(By.XPATH , f'/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[4]/div[2]/div[1]/div[1]/table[1]/tbody/tr[{i}]')
        # bid_element = bid_element.text.split()
        # # print(bid_element.text)
        # bid = float(bid_element[0])  # Convert the first element to float
        # bid_orders = int(bid_element[1])  # Convert the second element to int
        # bid_quantity = int(bid_element[2])  # Convert the third element to int

        total_bid = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[7]/div[2]/div[1]/div[1]/table[1]/tfoot/tr')
        total_bid = total_bid.text

        ask_element = driver.find_element(By.XPATH , f'/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[4]/div[2]/div[1]/div[1]/table[2]/tbody/tr[{i}]')
        # ask_element = ask_element.text.split()
        # ask = float(ask_element[0])  # Convert the first element to float
        # ask_orders = int(ask_element[1])  # Convert the second element to int
        # ask_quantity = int(ask_element[2])  # Convert the third e
                
        total_ask = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[7]/div[2]/div[1]/div[1]/table[2]/tfoot/tr')
        total_ask = total_ask.text

        # print(f'buy: {bid},{bid_orders},{bid_quantity}, {total_bid} , sell : {ask}, {ask_orders}, {ask_quantity}, {total_ask}')


except Exception as e:
    print(f"Error occurred: {e}")
