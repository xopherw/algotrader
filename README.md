# algotrader (DEPRECIATED)

An algorithm for auto trading (USE AT YOUR OWN RISK).
This is obviously a hobby projec to play around with using technical indication to justify when to buy and sell. There is absolutely no ML model being used.

The algorithm uses Exponential Moving Averages (both highs and lows) and slope to decide if the stock is good buy or sell. Result may be vary on all stocks.

You may fork it and update the code as your own repo but I am not responsible for any financial advice.

# **NOTE:**

In order to use APIs in this project, you must have an alpaca account with API secret key and key saved in `api.py`.

The `caller.py` is run in https://paper-api.alpaca.markets by default for paper trading testing purposes. For real time trading please replace to https://api.alpaca.markets at `alpaca_url` inside of `caller.py`
