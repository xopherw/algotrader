import caller, time

def trade(ticker):

    for i in ticker:

        # Call API to get a year of historical data till today
        data = caller.nsdq_data(i)

        # Constants
        stock_divider = len(ticker) + 1 - len(caller.stock_list(api))
        money = int(caller.money(api)/len(ticker))
        
        print("ema Low: " + str(data['emaLow']) + " | ema High: " + str(data['emaHigh']) + " | slope: " + str(data['slope']))

        # # Logics (discontinue)
        # buy_logic_1 = (data['ema7'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        # buy_logic_2 = (data['ema7'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        # sell_logic_1 = (data['ema7'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
        # sell_logic_2 = (data['ema7'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)

        buy_logic = (data["emaLow"] > data["emaHigh"] or data["slope"] > 0)
        sell_logic = (data["emaLow"] < data["emaHigh"] and data["slope"] < 0)

        # Buy
        if(not(ticker[i]) and (buy_logic)):
            print(f"Buy {i}")
            ticker[i] = True
            qty = int( money / data['open'])
            caller.order(i, qty, True, api)

        # Sell
        elif(ticker[i] and (sell_logic)):
            print(f"Sell {i}")
            ticker[i] = False
            qty = caller.qty(i, api)
            caller.order(i, qty, False, api)

        else:
            print(f"Hold {i}")