from pytrends.request import TrendReq

# Create a pytrends object
pytrends = TrendReq(hl='en-US', tz=360)

# Define your keywords
keywords = ['nse']

# Fetch data for a specific region or globally
pytrends.build_payload(keywords, cat=0, timeframe='today 1-m', geo='', gprop='')

# Get interest over time
data = pytrends.interest_over_time()
print(data)

# Get interest by region
region_data = pytrends.interest_by_region()
print(region_data)

# You can save the result as CSV if needed
# region_data.to_csv('search_data.csv')
