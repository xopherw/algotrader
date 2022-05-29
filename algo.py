import caller, api, time

def trade(ticker):

    for i in ticker:

        # Call API to get a year of historical data till today
        data = caller.nsdq_data(i)

        # Constants (change stock_divider to change the number of stocks to buy and add 1 more to the number of stocks)
        stock_divider = 4 - len(caller.stock_list(api))
        money = round(caller.money(api)/stock_divider,2)
        

        # Logics
        buy_logic_1 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        buy_logic_2 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        sell_logic_1 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
        sell_logic_2 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
            
        # Buy
        if(not(ticker[i]) and (buy_logic_1 or buy_logic_2)):
            print(f"Buy {i}")
            ticker[i] = True
            qty = int( money / data['close'].iloc[-1])
            caller.order(i, qty, True, api)

        # Sell
        elif(ticker[i] and (sell_logic_1 or sell_logic_2)):
            print(f"Sell {i}")
            ticker[i] = False
            qty = caller.qty(i, api)
            caller.order(i, qty, False, api)

        else:
            print(f"Hold {i}")
                
        time.sleep(2.05)