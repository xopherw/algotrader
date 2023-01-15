import requests, datetime as dt, numpy as np, pytz, time
from dateutil.relativedelta import relativedelta

# Call for raw data (NASDAQ)
def nsdq_data(ticker, years_frame=5, asset_class="stocks"):
    startTime = time.time()
    try:
        today = dt.datetime.now(pytz.timezone('US/Eastern')).date()
        past = today - relativedelta(years= years_frame)
        price = current_price(ticker.upper(), asset_class)
        new_data = {"date" : today.strftime("%m/%d/%Y"), "open" : price}
        headers = {'user-agent' : "-"}
        url = "https://api.nasdaq.com/api"
        post = f"/quote/{ticker.upper()}/historical"
        params = {
            "assetclass" : asset_class,
            "fromdate"    :   past,
            "limit"      :   '100000',
        }
        r = requests.get(url + post, headers=headers, params=params).json()["data"]["tradesTable"]["rows"][::-1]
        for i in range(len(r)):
            r[i]["open"] = float(r[i]["open"].strip("$"))
            if (i == 0):
                r[i]["emaHigh"], r[i]["emaLow"] = r[i]["open"], r[i]["open"]
            else:
                r[i]["emaLow"] = ema(r, i=i, timeframe=7, ema="emaLow")
                r[i]["emaHigh"] = ema(r, i=i, timeframe=14, ema="emaHigh")
                
        r.append(new_data) # Append latest data (aproaching closing time)
        emaHigh = ema(r, i=-1, timeframe=14, ema="emaHigh")
        emaLow = ema(r, i=-1, timeframe=7, ema="emaLow")
        r[-1]["emaHigh"], r[-1]["emaLow"] = emaHigh, emaLow
        
        # # Calculate slope  data
        slope= np.gradient([i["open"] for i in r])[-1]

        print(time.time() - startTime)
        return {"emaLow" : r[-1]["emaLow"], "emaHigh" : r[-1]["emaHigh"], "slope" : slope}
    except Exception as e:
        print("NSDQ Data Error: ", e)
        pass

# Calculate EWMA
def ema(data, timeframe, ema ,i):
    k = 2/(timeframe + 1.0)
    a = 1-k
    price = data[i]["open"]
    ema_previous = data[i-1][ema]
    ema = price*k + a*ema_previous
    return ema


# Call for current price
def current_price(ticker, asset_class="stocks"):
    try:
        url = f"https://api.nasdaq.com/api/quote/{ticker}/info?assetclass={asset_class}"
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
        d = r[0]["date"]
        return d
    except Exception as e:
        print("Calendar Error:", e)
        pass

# Call for open/close time (params: "Open" or "Clos" only, case senstive and no 'e' for "Clos")
def market_hour(market_time):
    try:
        url = "https://api.nasdaq.com/api/market-info"
        headers = {'user-agent' : "-"}
        r = requests.get(url, headers=headers).json()['data']
        hour = dt.datetime.strptime(r[f'market{market_time}ingTime'].strip(' ET'),"%b %d, %Y %I:%M %p")
        return hour
    except Exception as e:
        print("Market time Error:", e)
        pass

# Call for next open time
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