import subprocess
import time
import sys,ccxt
import os
from colorama import Style, init, Fore
init()
from exchange_config import *
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print('''
                                                                                                                     
                                                                                                                     
 A    RRRR   BBBB  
A A   R   R  B   B 
AAA   RRRR   BBBB  
A A   R  R   B   B  
A A   R   R  BBBB  
                                                                                                                     
                                                                                                                     ''')
args = sys.argv
mode = args[1]
data_dir = os.path.abspath(os.sep)
data_dir = os.path.join(data_dir, 'arb_data')
usable_balance_path = os.path.join(data_dir, "usable_balance.txt")
total_balance_path = os.path.join(data_dir, "total_balance.txt")

current_dir = os.path.dirname(os.path.abspath(__file__))
fake_money_path = os.path.join(current_dir, "bot-fake-money.py")
bot_path = os.path.join(current_dir, "bot.py")
main_path = os.path.join(current_dir, "main.py")

if renewal:
    balance = args[3]
    symbol=args[4]
    renew=args[2]
    ex_list=args[5]
else:
    balance = args[2]
    symbol=args[3]
    renew="525600"
    ex_list=args[4]
i=0
if mode!='fake-money':
    with open(usable_balance_path,"w") as f:
        f.write(str(balance))
    real_balance=0
    for ex_str in ex_list.split(','):
        bal = ex[ex_str].fetchBalance()
        real_balance+=float(bal[symbol.split('/')[1]]['total'])
    with open(total_balance_path,"w") as f:
        f.write(str(real_balance))
else:
    with open(total_balance_path,"w") as f:
        f.write(str(balance))

while True:
    with open(usable_balance_path,"r") as f:
        balance = str(f.read())
    if i>=1 and p.returncode==1:
        sys.exit(1)
    if mode == "fake-money":
        p=subprocess.run([python_command,fake_money_path,symbol,balance,renew,symbol,ex_list])
    elif mode == "real":
        p=subprocess.run([python_command,bot_path,symbol,balance,renew,symbol,ex_list])
    else:
        printerror(m=f"mode input is incorrect.")
        sys.exit(1)
    i+=1
