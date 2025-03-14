from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
data = []


def Kite_stocks():
    driver.get('https://zerodha.com/margin-calculator/Equity/')
    for i in range(1, 501):
            
        test =driver.find_element(By.XPATH , f'//*[@id="entry-{i}"]')

        # print(test.text)    
        split_text = test.text.split()
        if split_text[2]== "5x":
            data.append({"symbol":split_text[0], "leverage": split_text[2]})

    return data

