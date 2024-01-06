import requests as req, numpy as np, pandas as pd, pytz, datetime as dt, os
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

#### Constant
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
alpaca_url = "https://api.alpaca.markets/v2"
headers = {"accept": "application/json", "APCA-API-KEY-ID": api_key, "APCA-API-SECRET-KEY": api_secret}

# Calculate EWMA
def ema(data, timeframe, ema ,i):
    k = 2/(timeframe + 1.0)
    a = 1-k
    price = data[i]["open"]
    ema_previous = data[i-1][ema]
    ema = price*k + a*ema_previous
    return ema


# Call for current price
def current_price(symbol):
    try:
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"
        r = req.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print("Current Price Error:", e)
        pass

# Call for historical data
def historical_data(symbol):
    try:
        today = dt.today().replace(tzinfo=pytz.timezone('US/Eastern')).date()
        start = today - relativedelta(years=10)
        url = "https://data.alpaca.markets/v2"
        end = today
        params = {
            "start" : start,
            "timeframe" : "1Day",
            "limit" : 10000
        }
        r = req.get(url + f"/stocks/{symbol.upper()}/bars", headers=headers, params=params)
        return r.json()["bars"]
    except Exception as e:
        print("Historical Data Error:", e)
        pass

# Call for order
def orders(symbol, qty, order):
    try:
        side = "buy" if order else "sell"
        post = "/v2/orders"
        params = {
            "symbol"        :   symbol.upper(),
            "qty"           :   str(qty),
            "side"          :   side,
            "type"          :   "market",
            "time_in_force" :   "day"
        }
        r = req.post(alpaca_url + post, headers=headers, json=params)
        print("Status Code:", r.status_code)
    except Exception as e:
        print("Order Error:", e)
        pass

# Call to list bought stocks
def positions():
    try:
        r = req.get(alpaca_url + "/positions", headers=headers)
        return r.json()
    except Exception as e:
        print("Positions Error:", e)
        pass

# Call for stock quantity bought
def qty(ticker, api):
    try:
        url = alpaca_url
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
def buying_power():
    try:
        r = req.get(alpaca_url + "/account", headers=headers)
        return float(r.json()['cash'])
    except Exception as e:
        print("Buying Power Error:", e)
        pass

# Call for clock
def clock():
    try:
        r = req.get(alpaca_url + "/clock", headers=headers)
        return r.json()
    except Exception as e:
        print("Clock Error:", e)
        pass