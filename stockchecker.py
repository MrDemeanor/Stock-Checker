import os
from dotenv import load_dotenv
import requests
from operator import itemgetter
import time

# Load the .env file
load_dotenv()

# Load the stock ticker file
stock_tickers = open(os.getenv("STOCK_TICKER_FILE"))

# Initialize empty list of stocks
stocks_of_interest = list()

query_strings = list()

ticker_string = ""

count = 0

for ticker in stock_tickers:

    count += 1

    if ticker_string is "":
        ticker_string += ticker.rstrip('\n')
    else:
        ticker_string += ",{}".format(ticker.rstrip('\n'))
    
    if count == 100:
        count = 0
        query_strings.append(ticker_string)
        ticker_string = ""

if(len(ticker_string.split(','))) > 0:
    query_strings.append(ticker_string)

num_stocks = 0

print(len(query_strings))

for query_string in query_strings:

    time.sleep(1)
    
    res = requests.get("https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=quote&changeFromClose=true&filter=latestPrice,changePercent,previousClose&token={}".format(query_string, os.getenv("API_KEY"))).json()

    for key in res:

        num_stocks += 1

        print(key)
        
        try:
            latest_price = float(res["{}".format(key)]["quote"]["latestPrice"])
            change_percent = float(res["{}".format(key)]["quote"]["changePercent"]) * 100

            if latest_price >= float(os.getenv("MIN_PRICE")) and latest_price <= float(os.getenv("MAX_PRICE")) and change_percent <= float(os.getenv("PERCENT_CHANGE")):
                stocks_of_interest.append([key, latest_price, change_percent])
        except:
            continue

stocks_of_interest.sort(key = lambda x: x[2])

print("Checked {} stocks!".format(num_stocks))

for stocks in stocks_of_interest:
    print(stocks)