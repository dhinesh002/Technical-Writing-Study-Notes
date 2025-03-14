from selenium import webdriver
from selenium.webdriver.common.by import By
# Initialize Chrome WebDriver
# browser = webdriver.Chrome()

from selenium.webdriver.chrome.options import Options
chrome_options = Options()

# Add desired options
chrome_options.add_argument("--headless")  # Example: Run Chrome in headless mode

# Instantiate WebDriver with ChromeOptions
browser = webdriver.Chrome(options=chrome_options)
import time


data_List = [
#     ['adani green', 'https://economictimes.indiatimes.com/adani-green-energy-ltd/stocks/companyid-64847.cms']
# ,
# ['adani ent', 'https://economictimes.indiatimes.com/adani-enterprises-ltd/stocks/companyid-9074.cms']
# ,
# ['adani port', 'https://economictimes.indiatimes.com/adani-ports-special-economic-zone-ltd/stocks/companyid-20316.cms'],

# ['adani power', 'https://economictimes.indiatimes.com/adani-power-ltd/stocks/companyid-23479.cms'],
# ['tata motors', 'https://economictimes.indiatimes.com/tata-motors-ltd/stocks/companyid-12934.cms'],
# ['tata steel', 'https://economictimes.indiatimes.com/tata-steel-ltd/stocks/companyid-12902.cms'],
# ['hdfc life', 'https://economictimes.indiatimes.com/hdfc-life-insurance-company-ltd/stocks/companyid-3068.cms'],

# ['bharathi airtel','https://economictimes.indiatimes.com/bharti-airtel-ltd/stocks/companyid-2718.cms'],
# ['vedanta', 'https://economictimes.indiatimes.com/vedanta-ltd/stocks/companyid-13111.cms'],
# ['hindalco', 'https://economictimes.indiatimes.com/hindalco-industries-ltd/stocks/companyid-13637.cms'],
# ['Bharat Electronics', 'https://economictimes.indiatimes.com/bharat-electronics-ltd/stocks/companyid-11945.cms'],
# ['JINDALSTEL', 'https://economictimes.indiatimes.com/jindal-steel-power-ltd/stocks/companyid-4355.cms'],
# ['PNB', 'https://economictimes.indiatimes.com/punjab-national-bank/stocks/companyid-11585.cms']


['tata motors', 'https://economictimes.indiatimes.com/tata-motors-ltd/stocks/companyid-12934.cms'],
['bharathi airtel','https://economictimes.indiatimes.com/bharti-airtel-ltd/stocks/companyid-2718.cms'],
 ['hdfc life', 'https://economictimes.indiatimes.com/hdfc-life-insurance-company-ltd/stocks/companyid-3068.cms']   ,
['bajaj auto', 'https://economictimes.indiatimes.com/bajaj-auto-ltd/stocks/companyid-21430.cms'],

['PIDILITIND', 'https://economictimes.indiatimes.com/pidilite-industries-ltd/stocks/companyid-10460.cms'],
['HAL','https://economictimes.indiatimes.com/hindustan-aeronautics-ltd/stocks/companyid-9206.cms'],
    ['abb', 'https://economictimes.indiatimes.com/abb-india-ltd/stocks/companyid-14040.cms'],
['ICICIPRULI', 'https://economictimes.indiatimes.com/icici-prudential-life-insurance-company-ltd/stocks/companyid-1898.cms'],
 ['TATAPOWER', 'https://economictimes.indiatimes.com/tata-power-company-ltd/stocks/companyid-12918.cms'],
['ZYDUSLIFE','https://economictimes.indiatimes.com/zydus-lifesciences-ltd/stocks/companyid-3778.cms'],
['TTKHLTCARE','https://economictimes.indiatimes.com/ttk-healthcare-ltd/stocks/companyid-12938.cms'],
['TCPLPACK','https://economictimes.indiatimes.com/tcpl-packaging-ltd/stocks/companyid-2.cms'],
['RICOAUTO','https://economictimes.indiatimes.com/rico-auto-industries-ltd/stocks/companyid-13205.cms'],

['CONTROLPR','https://economictimes.indiatimes.com/control-print-ltd/stocks/companyid-10489.cms'],
    ['CLOUD','https://economictimes.indiatimes.com/varanium-cloud-ltd/stocks/companyid-2095298.cms']



#
# ['tata motors', 'https://economictimes.indiatimes.com/tata-motors-ltd/stocks/companyid-12934.cms'],
# ['tata steel', 'https://economictimes.indiatimes.com/tata-steel-ltd/stocks/companyid-12902.cms'],
# ['bharathi airtel','https://economictimes.indiatimes.com/bharti-airtel-ltd/stocks/companyid-2718.cms'],
# ['bajaj auto', 'https://economictimes.indiatimes.com/bajaj-auto-ltd/stocks/companyid-21430.cms'],
# ['PIDILITIND', 'https://economictimes.indiatimes.com/pidilite-industries-ltd/stocks/companyid-10460.cms'],
# ['HAL','https://economictimes.indiatimes.com/hindustan-aeronautics-ltd/sCONTROLPRCONTROLPRtocks/companyid-9206.cms'],
# ['VEDL', 'https://economictimes.indiatimes.com/vedanta-ltd/stocks/companyid-13111.cms'],
# ['hindalco', 'https://economictimes.indiatimes.com/hindalco-industries-ltd/stocks/companyid-13637.cms'],
# ['INDUSINDBK', 'https://economictimes.indiatimes.com/indusind-bank-ltd/stocks/companyid-9196.cms'],
# ['abb', 'https://economictimes.indiatimes.com/abb-india-ltd/stocks/companyid-14040.cms'],
# ['BEL', 'https://economictimes.indiatimes.com/bharat-electronics-ltd/stocks/companyid-11945.cms'],
# ['ICICIPRULI', 'https://economictimes.indiatimes.com/icici-prudential-life-insurance-company-ltd/stocks/companyid-1898.cms'],
# ['TATAPOWER', 'https://economictimes.indiatimes.com/tata-power-company-ltd/stocks/companyid-12918.cms'],
# ['JINDALSTEL', 'https://economictimes.indiatimes.com/jindal-steel-power-ltd/stocks/companyid-4355.cms'],
# ['PNB' ,'https://economictimes.indiatimes.com/punjab-national-bank/stocks/companyid-11585.cms'],
# ['ZYDUSLIFE','https://economictimes.indiatimes.com/zydus-lifesciences-ltd/stocks/companyid-3778.cms'],
# ['MONTECARLO','https://economictimes.indiatimes.com/monte-carlo-fashions-ltd/stocks/companyid-58299.cms'],
# ['TCPLPACK','https://economictimes.indiatimes.com/tcpl-packaging-ltd/stocks/companyid-2.cms'],
# ['MARATHON','https://economictimes.indiatimes.com/marathon-nextgen-realty-ltd/stocks/companyid-13280.cms'],
# ['STEELXIND', 'https://economictimes.indiatimes.com/steel-exchange-india-ltd/stocks/companyid-16459.cms'],
# ['GENESYS','https://economictimes.indiatimes.com/genesys-international-corporation-ltd/stocks/companyid-4114.cms'],
# ['NELCO','https://economictimes.indiatimes.com/nelco-ltd/stocks/companyid-13370.cms'],
# ['VALIANTORG','https://economictimes.indiatimes.com/valiant-organics-ltd/stocks/companyid-65108.cms'],
# ['RICOAUTO','https://economictimes.indiatimes.com/rico-auto-industries-ltd/stocks/companyid-13205.cms'],
# ['UTTAMSUGAR','https://economictimes.indiatimes.com/uttam-sugar-mills-ltd/stocks/companyid-15290.cms'],
# ['CONTROLPR','https://economictimes.indiatimes.com/control-print-ltd/stocks/companyid-10489.cms'],
# ['INDNIPPON','https://economictimes.indiatimes.com/india-nippon-electricals-ltd/stocks/companyid-11709.cms'],
# ['BODALCHEM','https://economictimes.indiatimes.com/bodal-chemicals-ltd/stocks/companyid-10710.cms'],
# ['ATULAUTO','https://economictimes.indiatimes.com/atul-auto-ltd/stocks/companyid-5864.cms'],
# ['CHEVIOT','https://economictimes.indiatimes.com/cheviot-company-ltd/stocks/companyid-12406.cms'],
# ['JUBLINDS','https://economictimes.indiatimes.com/jubilant-industries-ltd/stocks/companyid-33078.cms'],
# ['SMSPHARMA','https://economictimes.indiatimes.com/sms-pharmaceuticals-ltd/stocks/companyid-15744.cms'],
# ['WINDLAS','https://economictimes.indiatimes.com/windlas-biotech-ltd/stocks/companyid-2013610.cms'],
# ['ASAL','https://economictimes.indiatimes.com/automotive-stampings-and-assemblies-ltd/stocks/companyid-10371.cms'],
# ['NAHARCAP','https://economictimes.indiatimes.com/nahar-capital-financial-services-ltd/stocks/companyid-18395.cms']




]



while True:

    for data in data_List:

        try:
            browser.get(data[1])
            import time
            # time.sleep(10)
            current_price = browser.find_element(By.XPATH, '//*[@id="stockHeader"]/div/div[1]/div[1]/span[1]/ul/li[1]/span[1]/span')
            # time.sleep(10)
            vwap = browser.find_element(By.XPATH, '//*[@id="nonprimemetrics"]/table[1]/tbody/tr[9]/td[2]')
            # time.sleep(10)

            current_price_without_commas = current_price.text.replace(',', '')
            current_vwap_price_without_commas = vwap.text.replace(',', '')

            current_stock_price = float(current_price_without_commas)
            vwap_price = float(current_vwap_price_without_commas)


            vwap_3_percentage_less = vwap_price* 0.99

            # import datetime
            from datetime import datetime

            # Get current time
            # current_time = datetime.datetime.now()
            current_time = datetime.now()

            # Format the time as "hhmm"
            formatted_time = current_time.strftime("%H%M")

            # Extract minute and hour from current time
            # current_minute = current_time.minute
            # current_hour = current_time.hour
            print(current_stock_price, data[0])
            print(vwap_price)

            if current_stock_price <= vwap_3_percentage_less:
                with open('./text.txt', 'a') as output_file:
                    output_file.write(f"{data[0]},{formatted_time} \n")

            # print(current_stock_price)
            # print(vwap_price)

            # browser.close()

        except:
            pass    
