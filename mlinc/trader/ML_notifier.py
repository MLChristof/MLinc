from mlinc.trader.cerebro import Trader
from mlinc.strategies.rsi_strategy import RsiStrategy
from mlinc.notifier import notification

import datetime
import schedule
import time

file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'
file_christof = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_christof.txt'
file_vincent = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_vincent.txt'


with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
    api_key = f.read()

trader_list = []

long_threshold = 35

# Setup traders
ALL = Trader(strategy=RsiStrategy,
             start_date=datetime.datetime(2018, 1, 1),
             end_date=None,
             stock='ALLIANZ',
             api_key=api_key,
             start_cash=10000)
ALL.import_quandl_data(name='ALLIANZ', stock='FSE/ALV_X', close=4, open=1)
DEU = Trader(strategy=RsiStrategy,
             start_date=datetime.datetime(2018, 1, 1),
             end_date=None,
             stock='DEUTSCHE BANK',
             api_key=api_key,
             start_cash=10000)
DEU.import_quandl_data(name='DEUTSCHE BANK', stock='FSE/DBK_X', close=4, open=1)

trader_list.append(ALL)
trader_list.append(DEU)

alerts = {}
for item in trader_list:
    rsi = item.run[0].indicator.array[-8:-1]
    date = []
    for i in [6, 5, 4, 3, 2, 1, 0]:
        date.append(item.run[0].datas[0].datetime.date(0) - datetime.timedelta(i))
    for i, value in enumerate(rsi):
        if value < long_threshold:
            alerts.update({item.stock: {'value': value,
                                        'date': date[i]}})

message = 'Nothing to show...'
if alerts != {}:
    message = ''
    for key, value in alerts.items():
        message += 'RSI value for {} is low ({}). Measured on {}\n'.format(key,
                                                                           value['value'],
                                                                           value['date'])
notification(file_jelle, message)

# for alert in alerts:


# schedule.every().day.at("04:26").do(notifier)
#
# while True:
#     schedule.run_pending()
#     time.sleep(10) # wait one minute





