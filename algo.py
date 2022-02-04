import caller, api, time

def trade(ticker, is_held):

    for i in range(len(ticker)):

        # Call API to get a year of historical data till today
        data = caller.twelve_data(ticker[i], api)

        # Constants (change stock_divider to change the number of stocks to buy and add 1 more to the number of stocks)
        stock_divider = 3 - len(caller.stock_list(api))
        money = caller.money(api)/stock_divider
        

        # Logics
        buy_logic_1 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        buy_logic_2 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
        sell_logic_1 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
        sell_logic_2 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
            
        # Buy
        if(not(is_held[i]) and (buy_logic_1 or buy_logic_2)):
            print(f"Buy {ticker[i]}")
            is_held[i] = True
            qty = int( money / data['close'].iloc[-1])
            caller.order(ticker[i], qty, True, api)

        # Sell
        elif(is_held[i] and (sell_logic_1 or sell_logic_2)):
            printf("Sell {ticker[i]}")
            is_held[i] = False
            qty = caller.qty(ticker, api)
            caller.order(ticker, qty, False, api)

        else:
            print(f"Hold {ticker[i]}")
                
        time.sleep(3.5)