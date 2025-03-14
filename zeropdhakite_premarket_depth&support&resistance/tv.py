# # from tradingview_ta import TA_Handler, Interval, Exchange
# # import json
# # with open("SR.txt", "r") as file:
# #     for line in file:
# #         line = line.strip()
# #         data = json.loads(line)

# #         symbol = data['symbol']
# #         s2= data['Support2']
# #         r2 = data['Resistance2']

# #         try:
                
# #             Handler = TA_Handler(
# #                 symbol=symbol,
# #                 screener="india",
# #                 exchange="NSE",
# #                 interval=Interval.INTERVAL_1_DAY
# #             )
# #             # print(tesla.get_analysis().summary)

# #             indi =Handler.get_analysis().indicators
# #             # print(indi['volume'])

# #         except:
# #             print(symbol)



# n = {
#     '12': {12, 1,1},
#     '33': {14, 4,4}

# }

# print(n['12'])




# import json

# # Open and load the JSON file
# with open("output_file.json", "r") as file:
#     data = json.load(file)  # Load the JSON content into a Python object (list of dictionaries)

# # Access data for a specific stock
# stock_key = "GREAVESCOT"  # The stock key to look for

# for item in data:
#     if stock_key in item:
#         stock_data = item[stock_key]
#         print(f"Data for {stock_key}:")
#         print(f"Date: {stock_data['date']}")
#         print(f"Pivot: {stock_data['Pivot']}")
#         print(f"Support1: {stock_data['Support1']}")
#         print(f"Resistance1: {stock_data['Resistance1']}")
#         print(f"Support2: {stock_data['Support2']}")
#         print(f"Resistance2: {stock_data['Resistance2']}")
#         break
# else:
#     print(f"Stock {stock_key} not found in the data.")


import json

with open("output_file.json", "r", encoding="utf-8") as file:
    data = json.load(file)
print(data['360ONE'])
