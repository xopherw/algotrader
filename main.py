import time
from algo import *

run = False
tickers = {'SNDL' : False, 'ALNA' : False, 'VERB' : False}
asset = caller.stock_list(api)

#--- Check asset for continuitiy ---#
if asset != []:
    for i in asset:
        if(i['symbol'] in tickers):
            tickers[i['symbol']] = True

#--- Main loop to check if market is open, holiday, weekend, and when to execute orders ---#
while True: 
    
    ny_today = caller.dt.datetime.now(caller.pytz.timezone('America/New_York')).replace(tzinfo=None)
    is_market_open = caller.calendar(ny_today, api) == ny_today.date()
    
    market_hours = ny_today.time() >= caller.market_hour("Open").time() and (ny_today.time() < caller.market_hour("Clos").time())

    # This variable of 'minutes' will change according to stock I decide when to buy and sell
    buying_time = caller.market_hour("Clos") - caller.dt.timedelta(seconds=8.75)
    
    next_open_time = (caller.next_open_time(api) - ny_today).total_seconds()

    #--- Check if market is on weekday ---#
    if(ny_today.weekday() > 4):
        next = ny_today + caller.dt.timedelta(seconds=next_open_time)
        print(f"Weekend, next open time at {next}") 
        interval = next_open_time
    else:
        #--- Check if market is open ---#
        print("marker_hours: " + str(market_hours) + "\nis_market_open: " + str(is_market_open))     
        if(market_hours):
            """MARKET IS OPEN"""
            # Use updated current time to minus next open time to get seconds until next buying time
            interval = (buying_time - caller.dt.datetime.now(caller.pytz.timezone('America/New_York')).replace(tzinfo=None)).seconds
            next = ny_today + caller.dt.timedelta(seconds=interval)
            if((next - ny_today).total_seconds() < 8*3600):
                print(f"Market open, run algorithm time at {next}") 

            if(run):
                print(f"Market is closing soon, running algorithm at {ny_today}")
                # Run algorithm
                trade(tickers)
                run = False
                # Use updated current time to minus next open time to get seconds until next open
                interval = next_open_time
                next = ny_today + caller.dt.timedelta(seconds=interval)
                print(f"Algorithm ran, next open time at {next}")
            
            else:
                run = True
            
        # elif(market_hours and not is_market_open):
        #     next = ny_today + caller.dt.timedelta(seconds=interval)
        #     print(f"Market on holiday, next open time at {next}") 
        #     interval = next_open_time

        # elif(not market_hours and is_market_open):
        #     next = ny_today + caller.dt.timedelta(seconds=next_open_time)
        #     print(f"After hours, next run time at {next}") 
        #     interval =  next_open_time

        #--- When market is definitely closed ---#
        else:
            next = ny_today + caller.dt.timedelta(seconds=next_open_time)
            print(f"Market close, next run time at {next}") 
            interval = next_open_time

    time.sleep(interval)

