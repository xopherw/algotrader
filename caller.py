import requests, datetime as dt, numpy as np, pandas as pd, pytz
from dateutil.relativedelta import relativedelta


# Call for raw data (NASDAQ)
def nsdq_data(ticker, api):
    try:
        today = dt.datetime.now(pytz.timezone('US/Eastern')).date()
        past = today - relativedelta(years= 5)
        price = current_price(ticker.upper())
        new_data = {"date" : today.strftime("%m/%d/%Y"), "close" : price}
        headers = {'user-agent' : "-"}
        url = "https://api.nasdaq.com/api"
        post = f"/quote/{ticker.upper()}/historical"
        params = {
            "assetclass" : "stocks",
            "fromdate"    :   past,
            "limit"      :   '100000',
        }
        r = requests.get(url + post, headers=headers, params=params).json()

        # data cleaning and formatting
        # Remove unnecessary data and reverse order
        data = pd.DataFrame(r["data"]["tradesTable"]["rows"][::-1]).drop(columns=['volume', 'high', 'low', 'open'], axis=1) 
        data[['close']] = data[['close']].replace('\$|,', '', regex=True).astype(float) # Convert 'close' to float type
        data = data.append(new_data, ignore_index=True) # Append latest data (aproaching closing time)

        # Calculate and add ema3, ema10, and slope to data
        ema3 = data['close'].ewm(span=3, adjust=False).mean() 
        ema10 = data['close'].ewm(span=10, adjust=False).mean() 
        slope= np.gradient(data['close']) 
        data['ema3'] = ema3 
        data['ema10'] = ema10 
        data['slope'] = slope

        return data
    except Exception as e:
        print("NSDQ Data Error: ", e)
        pass


# Call for raw data (past data) 
# NOTE: THIS CODE IS UNUSABLE PLEASE USE NASDAQ API.
# def twelve_data(ticker, api):
#     try:
#         today = dt.datetime.now(pytz.timezone('US/Eastern')).date()
#         price = current_price(ticker.upper())
#         new_data = {"datetime" : today, "close" : price}
#         past = today - relativedelta(months = 12)
#         params = {
#             "symbol"        :   ticker.upper(),
#             "interval"      :   "1day",
#             "start_date"    :   str(past),
#             "end_date"      :   str(today),
#             "apikey"        :   api.twelve_data
#         }
#         # Retrieve
#         url = f"https://api.twelvedata.com/time_series"
#         r = requests.get(url, params=params).json()
        
#         # Clean
#         data = pd.DataFrame(r['values'][::-1]).drop(columns=['volume', 'high', 'low', 'open'], axis=1) # Reverse and convert to DataFrame
#         data[['close']] = data[['close']].astype(float) # Convert 'close' to float type
#         data = data.append(new_data, ignore_index=True) # Append latest data (aproaching closing time)

#         # Calculate and add ema3, ema10, and slope to data
#         ema3 = data['close'].ewm(span=3, adjust=False).mean() 
#         ema10 = data['close'].ewm(span=10, adjust=False).mean() 
#         slope= np.gradient(data['close']) 
#         data['ema3'] = ema3 
#         data['ema10'] = ema10 
#         data['slope'] = slope

#         return data
#     except Exception as e:
#         print("12 Data Error:", e)
#         pass

# Call for current price
def current_price(ticker):
    try:
        url = f"https://api.nasdaq.com/api/quote/{ticker}/info?assetclass=stocks"
        headers = {'user-agent' : "-"}
        r = requests.get(url, headers=headers).json()['data']
        return round(float(r['primaryData']['lastSalePrice'].strip('$')), 2)
    except Exception as e:
        print("Current Price Error:", e)
        pass

# Call for order
def order(ticker, qty, order, api):
    try:
        side = "buy" if order else "sell"
        url = "https://paper-api.alpaca.markets"
        post = "/v2/orders"
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        params = {
            "symbol"        :   ticker.upper(),
            "qty"           :   str(qty),
            "side"          :   side,
            "type"          :   "market",
            "time_in_force" :   "day"
        }
        r = requests.post(url + post, headers=headers, json=params)
        print("Status Code:", r.status_code)
    except Exception as e:
        print("Order Error:", e)
        pass

# Call to list bought stocks
def stock_list(api):
    try:
        url = "https://paper-api.alpaca.markets"
        post = "/v2/positions"
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        r = requests.get(url + post, headers=headers).json()
        return r
    except Exception as e:
        print("Stock List Error:", e)
        pass

# Call for stock quantity bought
def qty(ticker, api):
    try:
        url = "https://paper-api.alpaca.markets"
        post = "/v2/positions/" + ticker.upper()
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        r = requests.get(url + post, headers=headers)
        return r.json()["qty"] if(r.status_code == 200) else None
    except Exception as e:
        print("Quantity Error:", e)
        pass

# Call for buying power
def money(api):
    try:
        url = "https://paper-api.alpaca.markets"
        post = "/v2/account"
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        r = requests.get(url + post, headers=headers).json()["buying_power"]
        money = round(float(r), 2)
        return money
    except Exception as e:
        print("Buying Power Error:", e)
        pass

# Call for calendar (check if holiday)
def calendar(date, api):
    try:
        url = "https://paper-api.alpaca.markets"
        post = f"/v2/calendar"
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        params = {
            "start"     :   date,
            "end"       :   date,
        }
        r = requests.get(url + post, headers=headers, params=params).json()
        d = dateconvert(r[0]["date"])
        return d
    except Exception as e:
        print("Calendar Error:", e)
        pass

# Call for opening hour
def market_open_time():
    try:
        url = "https://api.nasdaq.com/api/market-info"
        headers = {'user-agent' : "-"}
        r = requests.get(url, headers=headers).json()['data']
        open = dt.datetime.strptime(r['marketOpeningTime'].strip(' ET'),"%b %d, %Y %I:%M %p")
        return open
    except Exception as e:
        print("Market open time Error:", e)
        pass

# Call for closing hour
def market_close_time():
    try:
        url = "https://api.nasdaq.com/api/market-info"
        headers = {'user-agent' : "-"}
        r = requests.get(url, headers=headers).json()['data']
        close = dt.datetime.strptime(r['marketClosingTime'].strip(' ET'),"%b %d, %Y %I:%M %p")
        return close
    except Exception as e:
        print("Market close time Error:", e)
        pass

# Call for next closing time
def next_open_time(api):
    try:
        url = "https://paper-api.alpaca.markets"
        post = f"/v2/clock"
        headers = {
            "APCA-API-KEY-ID" : api.alpaca_api,
            "APCA-API-SECRET-KEY" : api.alpaca_secret,
        }
        r = requests.get(url + post, headers=headers).json()
        next_open = dt.datetime.strptime(r['next_open'][:-6],"%Y-%m-%dT%H:%M:%S")
        return next_open
    except Exception as e:
        print("Next open time Error:", e)
        pass

# Convert string date to date object
def dateconvert(date):
    d = dt.datetime.strptime(date, "%Y-%m-%d")
    return d.date()