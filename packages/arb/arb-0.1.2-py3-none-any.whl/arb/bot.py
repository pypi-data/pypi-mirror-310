from asyncio import gather, run
import time
import ccxt.pro
from delta_neutral_config import *
import ccxt.async_support
import sys
import os
from colorama import Fore, Back, Style,init
import threading
init()
from exchange_config import *

stop_requested = False
data_dir = os.path.abspath(os.sep)
data_dir = os.path.join(data_dir, 'arb_data')
logs_path = os.path.join(data_dir, 'logs/logs.txt')
new_opportunity_path = os.path.join(data_dir, 'logs/opportunities.txt')

def listen_for_exit():
    global stop_requested
    input(" ")
    stop_requested = True

listener_thread = threading.Thread(target=listen_for_exit)
listener_thread.start()

bid_prices = {}
ask_prices = {}
total_change_usd = 0
prec_ask_price = 0
prec_bid_price = 0
i=0
z=0
if len(sys.argv) != 6:
    print(f" \nIncorrect usage, this is what it has to look like: $ {python_command} bot-classic.py [pair] [total_usdt_investment] [stop.delay.minutes] [ex_list]\n ")
    print(f" \n This is the list of args you wrote: {sys.argv}")
    sys.exit(1)
print(" ")
if first_orders_fill_timeout <= 0:
    first_orders_fill_timeout = 3600 # 2.5 days

echanges = [ex[sys.argv[5].split(',')[i]] for i in range(len(sys.argv[5].split(',')))]
echanges_str = [sys.argv[5].split(',')[i] for i in range(len(sys.argv[5].split(',')))]
currentPair = str(sys.argv[1])
criteria_usd = str(criteria_usd)
howmuchusd = float(sys.argv[2])
if delta_neutral:
    usd_to_short = howmuchusd*(1/3)
    howmuchusd = howmuchusd*(2/3)
inputtimeout = int(sys.argv[3])*60
indicatif = str(sys.argv[4])
timeout = time.time() + inputtimeout
endPair = currentPair.split('/')[1]

fees = {n:0 for n in echanges_str}

for ech in fees:
    if ech!='kucoinfutures':
        markets = ex[ech].load_markets()
        fees[ech] = {'base': (0 if markets['BTC/USDT']['feeSide']!='base' else markets['BTC/USDT']['taker']) if list(markets['BTC/USDT'].keys()).count('feeSide')!=0 else 0, 'quote': (markets['BTC/USDT']['taker'] if markets['BTC/USDT']['feeSide']!='base' else 0) if list(markets['BTC/USDT'].keys()).count('feeSide')!=0 else markets['BTC/USDT']['taker']}
    else:
        fees[ech] = {'base':0,'quote':0.0006}

for ech in fees:
    if fees[ech]['base']==None or fees[ech]['quote']==None:
        fees[ech] = {'base':0,'quote':float(input(f"Error while fetching the fees for {ech}. \nPlease input the spot taker fees of {ech} >>> "))}
        
async def fetch_orderbook(exchange_instance, symbol):
    try:
        orderbook = await exchange_instance.watch_order_book(symbol)
    except Exception as e:
        printerror(m=f"Error while fetching orderbook on {exchange_instance.id}. {e}")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        id_ = exchange_instance.id
        await exchange_instance.close()
        new_instance = getattr(ccxt.pro,id_)({'enableRateLimit':True})
        try:
            orderbook = await new_instance.watch_order_book(symbol)
        except Exception as e:
            printerror(m=f"Error while fetching orderbook on {exchange_instance.id}. {e}")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.exit()
    return orderbook
async def execute_trades(ex, max_bid_ex, min_ask_ex, currentPair, crypto_per_transaction, max_bid_price, min_ask_price):
  async def execute_sell_order():
    try:
        market_sell_order = ex[max_bid_ex].createMarketSellOrder(symbol=currentPair, amount=crypto_per_transaction)
        if market_sell_order['price'] is None:
            try:
                new_order = ex[max_bid_ex].fetch_order(id=market_sell_order['id'], symbol=currentPair)
                market_sell_order['price'] = new_order['average']
            except Exception as e:
                try:
                    printandtelegram(f"{get_time()} Filled price couldn't be fetched directly on {max_bid_ex}, and an error occured while fetching the order manually: {e}")
                    new_order = ex[max_bid_ex].fetch_closed_order(id=market_sell_order['id'], symbol=currentPair)
                    market_sell_order['price'] = new_order['average']
                except Exception as e:
                    printerror(m=f"Error while trying another method on {max_bid_ex}: {e}")
                    sys.exit(1)
        actual_max_bid_price = market_sell_order['price']
        printandtelegram(f"{get_time()} Sell market order filled on {max_bid_ex} for {crypto_per_transaction} {currentPair.split('/')[0]} at {market_sell_order['price']}.")
        append_new_line(logs_path,f'{get_time_blank()} INFO: sell market order filled on {max_bid_ex} for {crypto_per_transaction} {currentPair.split("/")[0]} at {market_sell_order["price"]}.')
        return actual_max_bid_price
    except Exception as e:
        printandtelegram(f"Error executing sell order on {max_bid_ex}: {e}")
        append_new_line(logs_path, f'{get_time_blank()} ERROR: {e}')
        sys.exit(1)
        return None

  async def execute_buy_order():
    if 'createMarketBuyOrderRequiresPrice' in list(ex[min_ask_ex].options.keys()):
        if ex[min_ask_ex].options['createMarketBuyOrderRequiresPrice']:
            try:
                market_buy_order = ex[min_ask_ex].createMarketBuyOrder(symbol=currentPair, amount=crypto_per_transaction*min_ask_price, params={'createMarketBuyOrderRequiresPrice':False})
            except Exception as e:
                printerror(m=f"createMarketBuyOrderRequiresPrice on {min_ask_ex} (buy) was true, so tried with amount including price multiplication. Didn't worked. Retrying with price arg. Error: {e}")
                try:
                    market_buy_order = ex[min_ask_ex].create_order(type='market', side='buy', symbol=currentPair, amount=crypto_per_transaction, price=min_ask_price)
                except Exception as e:
                    printerror(m='Error again after retrying with price arg. Exiting...')
                    sys.exit(1)
    else:
        try:
            market_buy_order = ex[min_ask_ex].createMarketBuyOrder(currentPair, crypto_per_transaction)
        except Exception as e:
            printandtelegram(f"{get_time()} Error while creating market buy order on {min_ask_ex}. {e}. Trying again with amount*price in amount argument...")
            try:
                market_buy_order = ex[min_ask_ex].createMarketBuyOrder(symbol=currentPair, amount=crypto_per_transaction*min_ask_price, params={'createMarketBuyOrderRequiresPrice':False})
            except Exception as e:
                printerror(m=f"Buy order on {min_ask_ex} didn't worked with amount*price as amount, retrying with price arg. Error: {e}")
                try:
                    market_buy_order = ex[min_ask_ex].create_order(side='buy',type='market', symbol=currentPair, amount=crypto_per_transaction, price=min_ask_price)
                except Exception as e:
                    printerror(m='Error again after retrying with price arg. Exiting...')
                    sys.exit(1)

    if market_buy_order['price'] is None:
        try:
            new_order = ex[min_ask_ex].fetch_order(id=market_buy_order['id'], symbol=currentPair)
            market_buy_order['price'] = new_order['average']
        except Exception as e:
            try:
                printandtelegram(f"{get_time()} Filled price couldn't be fetched directly on {min_ask_ex}, and an error occured while fetching the order manually: {e}")
                new_order = ex[min_ask_ex].fetch_closed_order(id=market_buy_order['id'], symbol=currentPair)
                market_buy_order['price'] = new_order['average']
            except Exception as e:
                printerror(m=f"Error while trying another method on {min_ask_ex}: {e}")
                sys.exit(1)
    actual_min_ask_price = market_buy_order['price']
    printandtelegram(f"{get_time()} Buy market order filled on {min_ask_ex} for {crypto_per_transaction} {currentPair.split('/')[0]} at {market_buy_order['price']}.")
    append_new_line(logs_path,f"{get_time_blank()} INFO: buy market order filled on {min_ask_ex} for {crypto_per_transaction} {currentPair.split('/')[0]} at {market_buy_order['price']}.")
    return actual_min_ask_price

  # Execute buy and sell orders concurrently
  actual_max_bid_price, actual_min_ask_price = await gather(
      execute_sell_order(), 
      execute_buy_order()
  )

  return actual_max_bid_price, actual_min_ask_price
s=0

ordersFilled = 0

try:
    for n in echanges:
        ticker = n.fetch_ticker(currentPair)
        print(f"Total volume of {currentPair} is {ticker['quoteVolume']}.")

    if minimum_volume > ticker['quoteVolume']:
        print(f"{currentPair}'s volume is less than {minimum_volume} Breaking.")
        append_new_line(logs_path,f"{get_time_blank()} INFO: {currentPair}'s volume is less than {minimum_volume}. Breaking.")
        sys.exit(1)
except Exception as e:
    printerror(m=f"error while fetching base volume of {currentPair}. Error: {e}")
    for exc in echanges_str:
        ex[exc].close()

while ordersFilled != len(echanges):

    for n in echanges_str:
        bal = get_balance(n,endPair)
        if float(bal) < howmuchusd/len(echanges):
            # printandtelegram(f'{Style.DIM}[{time.strftime("%H:%M:%S", time.gmtime(time.time()))}]{Style.RESET_ALL} Not enough balance of {endPair} on {n}. Need {round(float((howmuchusd)/len(echanges))-float(bal),3)} {endPair} more. Current balance on {n}: {round(bal,3)} {endPair}')
            printerror(m=f'not enough balance of {endPair} on {n}. Need {round(float((howmuchusd)/len(echanges))-float(bal),3)} {endPair} more. Current balance on {n}: {round(bal,3)} {endPair}')
            s=1
        else:
            printandtelegram(f'{Style.DIM}[{time.strftime("%H:%M:%S", time.gmtime(time.time()))}]{Style.RESET_ALL} {n} balance OK')
            append_new_line(logs_path,f'{get_time_blank()} INFO: {n} balance OK')

    if s==1:
        sys.exit(1)
    usd = {exchange:(howmuchusd/2)/len(echanges) for exchange in echanges_str}
    usd_real = {exchange:0 for exchange in echanges_str}

    total_usd = 0
    for exc in echanges_str:
        total_usd+=usd[exc]

    all_tickers = []

    try:
        printandtelegram(f"{get_time()} Fetching the global average price for {currentPair}...")
        for n in echanges:
            ticker = n.fetch_ticker(currentPair)
            all_tickers.append(ticker['last'])
        average_first_buy_price = moy(all_tickers)
        total_crypto = (howmuchusd/2)/average_first_buy_price
        printandtelegram(f"{get_time()} Average {currentPair} price in {endPair}: {average_first_buy_price}")
        append_new_line(logs_path,f'{get_time_blank()} INFO: average {currentPair} price in {endPair}: {average_first_buy_price}')

    except Exception as e:
        printerror(m=f"error while fetching average prices. Error: {e}")
        for exc in echanges_str:
            ex[exc].close()

    crypto = {exchange:total_crypto/len(echanges) for exchange in echanges_str}

    crypto_per_transaction = (total_crypto/len(echanges_str))*0.99

    i=0
    for n in echanges:
        n.createLimitBuyOrder(currentPair,total_crypto/len(echanges),average_first_buy_price)
        append_new_line(logs_path,f'{get_time_blank()} INFO: buy limit order of {round(total_crypto/len(echanges),3)} {currentPair.split("/")[0]} at {average_first_buy_price} sent to {echanges_str[i]}.')
        printandtelegram(f'{get_time()} Buy limit order of {round(total_crypto/len(echanges),3)} {currentPair.split("/")[0]} at {average_first_buy_price} sent to {echanges_str[i]}.')
        i+=1

    printandtelegram(f"{get_time()} All orders sent.")

    zz=0
    already_filled = []
    while (zz<=first_orders_fill_timeout*60*0.5 and ordersFilled!=len(echanges)):
        for exc in echanges_str:
            order=ex[exc].fetchOpenOrders(symbol=currentPair)
            if order == [] and already_filled.count(exc) == 0:
                printandtelegram(f"{get_time()} {exc} order filled.")
                append_new_line(logs_path,f'{get_time_blank()} INFO: {exc} order filled.')
                ordersFilled+=1
                already_filled.append(exc)
        time.sleep(1.8)
        zz+=1
    if zz>= first_orders_fill_timeout*60*0.5:
        append_new_line(logs_path,f'{get_time_blank()} INFO: one or more order(s) not filled in approximately {first_orders_fill_timeout} minutes. Cancelling the order(s) and selling the filled amounts.')
        print(f"{get_time()} One or more order(s) not filled in approximately {first_orders_fill_timeout} minutes. Cancelling the order(s) and selling the filled amounts.")
        emergency_convert_list(currentPair,already_filled)
        for exch in echanges_str:
            if already_filled.count(exch) == 0:
                try:
                    print(f"{get_time()} {exc} not compatible with cancelAllOrders. Cancelling manually...")
                    open_orders = ex[exch].fetchOpenOrders(currentPair)
                    ex[exch].cancelOrder(open_orders[len(open_orders)-1]['id'],currentPair)
                    print(f"{get_time()} {exc} order successfully cancelled.")
                    append_new_line(logs_path,f'{get_time_blank()} INFO: {exc} order successfully cancelled.')
                except Exception as e:
                    printerror(m=f"error while cancelling the non-filled orders. Error: {e}")
        already_filled=[]

if delta_neutral:
    api_credentials['options'] = {'defaultType': 'future' if futures_exchange!='mexc3' else 'swap'}
    shex = getattr(ccxt,futures_exchange)(api_credentials)
    bal = get_balance(futures_exchange,endPair)
    if bal<usd_to_short:
        printerror(m=f"not enough {endPair} in {futures_exchange} for the short order, need {usd_to_short-bal} {endPair} more. Current balance: {bal}")
        sys.exit(1)
    order = shex.createMarketSellOder(currentPair+f":{endPair}",usd_to_short)
    print(f"{get_time()} short order successfully placed on {futures_exchange}, pair: {currentPair+f':{endPair}'}, amount: {usd_to_short}, filled price: {order['average']}.")
    append_new_line(logs_path,f"{get_time_blank()} INFO: short order successfully placed on {futures_exchange}, pair: {currentPair+f':{endPair}'}, amount: {usd_to_short}, filled price: {order['average']}.")

printandtelegram(f"{get_time()} Starting the bot with parameters: {[n for n in sys.argv]}")
append_new_line(logs_path,f'{get_time_blank()} INFO: starting program with parameters: {[n for n in sys.argv]}')
prec_time = '0000000'
min_ask_price = 0
if not renewal:
    indexx = sys.argv.index('525600')
    sys.argv[indexx] = 'No renewal'
total_change_usd=0
async def symbol_loop(exchange, symbol):
    global asyncio,total_change_usd,crypto_per_transaction,i,z,prec_time,t,time1,bid_prices,ask_prices,min_ask_price,max_bid_price,prec_ask_price,prec_bid_price,timeout,profit_usd,total_crypto
    while time.time() <= timeout:
        if stop_requested:
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            print(f"{get_time()} Manual rebalance requested. Breaking.")
            await exchange.close()
            append_new_line(logs_path,f"{get_time_blank()} INFO: Manual rebalance requested. Breaking.")
            timeout -= 100000000000
            break
        orderbook = await fetch_orderbook(exchange,symbol)
        now = exchange.milliseconds()
        bid_prices[exchange.id] = orderbook["bids"][0][0]
        ask_prices[exchange.id] = orderbook["asks"][0][0]
        min_ask_ex = min(ask_prices, key=ask_prices.get)
        max_bid_ex = max(bid_prices, key=bid_prices.get)
        for u in echanges_str:
            if crypto[u] < crypto_per_transaction:
                min_ask_ex = u
            if usd[u] <= 0: # should not happen
                max_bid_ex = u
        min_ask_price = ask_prices[min_ask_ex]
        max_bid_price = bid_prices[max_bid_ex]

        theoritical_min_ask_usd_bal = usd[min_ask_ex] - (crypto_per_transaction / (1-fees[min_ask_ex]['quote'])) * min_ask_price * (1+fees[min_ask_ex]['base'])
        theoritical_max_bid_usd_bal = usd[max_bid_ex] + (crypto_per_transaction / (1+fees[max_bid_ex]['base']) * max_bid_price * (1-fees[max_bid_ex]['quote']))

        change_usd = (theoritical_min_ask_usd_bal+theoritical_max_bid_usd_bal)-(usd[max_bid_ex]+usd[min_ask_ex])

        total_usd_balance = 0
        for n in echanges_str:
            total_usd_balance+=usd[n]

        if max_bid_ex != min_ask_ex and change_usd >= float(criteria_usd) and (abs(min_ask_price-max_bid_price))/((max_bid_price+min_ask_price)/2)*100>=criteria_pct and prec_ask_price != min_ask_price and prec_bid_price != max_bid_price:
            await exchange.close()
            i+=1
            
            fees_crypto = crypto_per_transaction * (fees[min_ask_ex]['quote']) + crypto_per_transaction * (fees[max_bid_ex]['base'])
            fees_usd = crypto_per_transaction * max_bid_price * (fees[max_bid_ex]['quote']) + crypto_per_transaction * min_ask_price * (fees[min_ask_ex]['base'])

            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            print("-----------------------------------------------------\n")
            
            ex_balances = ""
            for exc in echanges_str:
                ex_balances+=f"\n{exc}: {round(crypto[exc],3)} {currentPair.split('/')[0]} / {round(usd[exc],2)} {endPair}"
            print(f"{Style.RESET_ALL}Opportunity n°{i} detected! ({min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex})\n \nExcepted profit: +{round(change_usd,4)} {endPair}{Style.RESET_ALL}\n \nSession total profit: {Fore.GREEN}+{round((total_change_usd/100)*howmuchusd,4)} {endPair} {Style.RESET_ALL}\n \nFees paid: {Fore.RED}-{round(fees_usd,4)} {endPair}      -{round(fees_crypto,4)} {currentPair.split('/')[0]}\n \n{Style.RESET_ALL}{Style.DIM} {ex_balances}\n \n{Style.RESET_ALL}Time elapsed since the beginning of the session: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\n \n{Style.RESET_ALL}-----------------------------------------------------\n \n")
            append_new_line(logs_path,f'{get_time_blank()} INFO: new arbitrage opportunity: {min_ask_ex} {min_ask_price} -> {max_bid_price} {max_bid_ex} with an excepted profit of {change_usd} {endPair}')
            send_to_telegram(f"[{indicatif} Trade n°{i}]\n \nOpportunity detected!\n \nExcepted profit: +{round(change_usd,4)} {endPair}\n \n{min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex}\nTime elapsed: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\nSession total profit: {round(total_change_usd,4)} {endPair}\nFees paid: {round(fees_usd,4)} {endPair}      {round(fees_crypto,4)} {currentPair.split('/')[0]}\n \n--------BALANCES---------\n \n {ex_balances}")

            actual_max_bid_price, actual_min_ask_price = await execute_trades(ex,max_bid_ex,min_ask_ex,currentPair,crypto_per_transaction,max_bid_price,min_ask_price)
            
            actual_theoritical_min_ask_usd_bal = usd[min_ask_ex] - (crypto_per_transaction / (1-fees[min_ask_ex]['quote'])) * actual_min_ask_price * (1+fees[min_ask_ex]['base'])
            actual_theoritical_max_bid_usd_bal = usd[max_bid_ex] + (crypto_per_transaction / (1+fees[max_bid_ex]['base']) * actual_max_bid_price * (1-fees[max_bid_ex]['quote']))

            actual_change_usd = (actual_theoritical_min_ask_usd_bal+actual_theoritical_max_bid_usd_bal)-(usd[max_bid_ex]+usd[min_ask_ex])

            if change_usd != actual_change_usd:
                printandtelegram(f"{get_time()} Filled price is different than excepted price (most of the time due to ping-delay). Profit excepted: {(Fore.RED if change_usd < 0 else Fore.GREEN) if change_usd!=0 else Style.RESET_ALL}{change_usd} {endPair}{Style.RESET_ALL} | Actual profit: {(Fore.RED if actual_change_usd < 0 else Fore.GREEN) if actual_change_usd!=0 else Style.RESET_ALL}{actual_change_usd} {endPair}")
                append_new_line(logs_path,f'{get_time_blank()} INFO: Filled price is different than excepted price (most of the time due to ping delay). Profit excepted: {change_usd} {endPair} | Actual profit: {actual_change_usd} {endPair}')

            crypto[min_ask_ex] += crypto_per_transaction
            usd[min_ask_ex] -= (crypto_per_transaction / (1-fees[min_ask_ex]['quote'])) * actual_min_ask_price * (1+fees[min_ask_ex]['base'])
            crypto[max_bid_ex] -= crypto_per_transaction
            usd[max_bid_ex] += crypto_per_transaction / (1+fees[max_bid_ex]['base']) * actual_max_bid_price * (1-fees[max_bid_ex]['quote'])

            prec_ask_price = min_ask_price
            prec_bid_price = max_bid_price

            total_crypto = 0
            for exc in echanges_str:
                total_crypto+=crypto[exc]
            crypto_per_transaction = total_crypto/len(echanges_str)

            ex_balances_after=''
            for exc in echanges_str:
                ex_balances_after+=f"\n{exc}: {round(crypto[exc],3)} {currentPair.split('/')[0]} / {round(usd[exc],2)} {endPair}"

            ex_bal_one_liner = ex_balances.replace('\n', ' || ')
            ex_bal_after_one_liner = ex_balances_after.replace('\n', ' || ')

            append_new_line(new_opportunity_path,f"-----------------------|START|-----------------------\nSymbol: {symbol}\nTimestamp: {time.time()}\nProfit USD: {actual_change_usd}\nExcepted profit USD: {change_usd}\nBuy exchange: {min_ask_ex}\nExcepted buy price: {min_ask_price}\nBuy price: {actual_min_ask_price}\nSell exchange: {max_bid_ex}\nExcepted sell price: {max_bid_price}\nSell price: {actual_max_bid_price}\nExchanges balances (before): {ex_bal_one_liner}\nExchanges balances after: {ex_bal_after_one_liner}\n------------------------|END|------------------------")

        else:
            for count in range(0,1):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
            if change_usd < 0:
                color = Fore.RED
            elif change_usd > 0:
                color = Fore.GREEN
            elif change_usd == 0:
                color = Fore.WHITE
            print(f"{get_time()} Best opportunity: {color}{round(change_usd,4)} {endPair} {Style.RESET_ALL}(with fees)       buy: {min_ask_ex} at {min_ask_price}     sell: {max_bid_ex} at {max_bid_price}")
        time1=exchange.iso8601(exchange.milliseconds())
        if time1[17:19] == "00" and time1[14:16] != prec_time:
            prec_time = time1[11:13]
            await exchange.close()

async def exchange_loop(exchange_id, symbols):
    exchange = getattr(ccxt.pro, exchange_id)()
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

async def main():
    exchanges = {
        echanges_str[i]:[currentPair] for i in range(0,len(echanges))
    }
    loops = [
        exchange_loop(exchange_id, symbols)
        for exchange_id, symbols in exchanges.items()
    ]
    await gather(*loops)

st = time.time()
print(" \n")
run(main())

printandtelegram(f"{get_time()} Selling all {sys.argv[1][:len(sys.argv[1])-5]} for {endPair} on {echanges_str}.")
append_new_line(logs_path,f'{get_time_blank()} INFO: selling all {sys.argv[1][:len(sys.argv[1])-5]} for {endPair} on {echanges_str}.')

for exc in crypto:
    order = ex[exc].createMarketSellOrder(currentPair,crypto[exc])
    balances = ex[exc].fetchBalance()
    usd_real[exc]=balances[endPair]['total']
    crypto[exc]=0

total_usd_balance = 0
for n in echanges_str:
    total_usd_balance += usd_real[n]

total_balance_path = os.path.join(data_dir, "total_balance.txt")

with open(total_balance_path, 'r+') as balance_file:
    old_balance = float(balance_file.read())
    balance_file.seek(0)
    balance_file.write(str(total_usd_balance))

total_session_profit_usd = total_usd_balance-old_balance

total_usd_usable_balance = 0
for exc in usd:
    total_usd_usable_balance+=usd[exc]
total_usd_usable_balance+=total_session_profit_usd

usable_balance_path = os.path.join(data_dir, "usable_balance.txt")

with open(usable_balance_path, 'r+') as balance_file:
    balance_file.seek(0)
    balance_file.write(str(total_usd_usable_balance))

if delta_neutral:
    try:
        shex.createMarketBuyOrder(currentPair+f":{endPair}",usd_to_short,{"reduceOnly": True})
        printandtelegram(f"{get_time()} Successfully closed {shex.id} short order.")
        append_new_line(logs_path,f'{get_time_blank()} INFO: successfully closed {shex.id} short order.')
    except Exception as e:
        printerror(m=f"cannot close short order on {shex.id}: {e}. The bot will continue to run, but please close the short order manually to avoid losses")

printandtelegram(f"{get_time()} Session with {currentPair} finished.\n{get_time()} Total account change since start: {total_session_profit_usd} {endPair}")
append_new_line(logs_path,f'{get_time_blank()} INFO: session ended. Total account change since start: {total_session_profit_usd} {endPair}')
