
import pandas as pd

# Read the Excel file
df = pd.read_excel("stock_list.xlsx")

# Extract data from the second column
# second_column_data = df.iloc[:, 1]
second_column_data = df.iloc[:200, 1]


# Convert the data into a Python list
stock_symbol_list = second_column_data.tolist()

# Print the list
# print(len(stock_symbol_list))