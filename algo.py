import caller, api

def trade(ticker, is_held, order):
    # Call API to get a year of historical data till today
    data = caller.twelve_data(ticker, api)

    # Constants (change stock_divider to change the number of stocks to buy and add 1 more to the number of stocks)
    stock_divider = 3 - len(caller.stock_list(api))
    money = caller.money(api)/stock_divider
    qty = int( money / data['close'].iloc[-1])

    # Logics
    buy_logic_1 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
    buy_logic_2 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] > 0)
    sell_logic_1 = (data['ema3'].iloc[-1] < data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
    sell_logic_2 = (data['ema3'].iloc[-1] > data['ema10'].iloc[-1] and data['slope'].iloc[-1] < 0)
        # Buy
    if(not(is_held) and (buy_logic_1 or buy_logic_2)):
        print("Buy")
        is_held = True
        order = not(order)
        caller.order(ticker, qty, order, api)

    # Sell
    elif(is_held and (sell_logic_1 or sell_logic_2)):
        print("Sell")
        is_held = False
        order = not(order)
        qty = caller.qty(ticker, api)
        caller.order(ticker, qty, order, api)

    else:
        print("Hold")
            
    
    return is_held, order
