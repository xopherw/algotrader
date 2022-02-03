import time
from algo import *

run = False
is_held = [False, False, False]
ticker = ["best", "job", "mark"]


#--- Main loop to check if market is open, holiday, weekend, and when to execute orders ---#
while True: 
    
    ny_today = caller.dt.datetime.now(caller.pytz.timezone('America/New_York')).replace(tzinfo=None)
    is_market_open = caller.calendar(ny_today.strftime("%Y-%m-%d"), api) == ny_today.date()
    
    market_hours = ny_today.time() >= caller.market_open_time().time() and (ny_today.time() < caller.market_close_time().time())

    # This variable of 'minutes' will change according to stock I decide when to buy and sell
    buying_time = caller.market_close_time() - caller.dt.timedelta(seconds=12)
    
    next_open_time = (caller.next_open_time(api) - ny_today).total_seconds()

    #--- Check if market is on weekday ---#
    if(ny_today.weekday() > 4):
        next = ny_today + caller.dt.timedelta(seconds=next_open_time)
        print(f"Weekend, next open time at {next}") 
        interval = next_open_time
    else:
        #--- Check if market is open ---#
        if(market_hours and is_market_open):
            """MARKET IS OPEN"""
            # Use updated current time to minus next open time to get seconds until next buying time
            interval = (buying_time - caller.dt.datetime.now(caller.pytz.timezone('America/New_York')).replace(tzinfo=None)).seconds
            next = ny_today + caller.dt.timedelta(seconds=interval)
            if((next - ny_today).total_seconds() < 8*3600):
                print(f"Market open, run algorithm time at {next}") 

            if(run):
                print(f"Market is closing soon, running algorithm at {ny_today}")
                # Run algoruthm
                trade(ticker, is_held)
                run = False
                # Use updated current time to minus next open time to get seconds until next open
                interval = next_open_time
                next = ny_today + caller.dt.timedelta(seconds=interval)
                print(f"Algorithm ran, next open time at {next}")
            
            else:
                run = True
            
        elif(market_hours and not is_market_open):
            next = ny_today + caller.dt.timedelta(seconds=interval)
            print(f"Market on holiday, next open time at {next}") 
            interval = next_open_time

        elif(not market_hours and is_market_open):
            next = ny_today + caller.dt.timedelta(seconds=next_open_time)
            print(f"After hours, next run time at {next}") 
            interval =  next_open_time

        #--- When market is definitely closed ---#
        else:
            next = ny_today + caller.dt.timedelta(seconds=next_open_time)
            print(f"Market close, next run time at {next}") 
            interval = next_open_time

    time.sleep(interval)

