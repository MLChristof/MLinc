import sys
sys.path.append(r'/home/pi/Documents/ML_conf/conf.ini')

from mlinc.oanda.trader import OandaTrader
from mlinc.oanda.instruments_list import instrument_list
from datetime import datetime
import configparser


instruments = instrument_list()

config = configparser.RawConfigParser(allow_no_value=True)
config.read('conf.ini')
input = {}
for item in config['BaconBuyer']:
    input[item] = config['BaconBuyer'][item]

trader = OandaTrader(instruments=instruments, granularity=input['granularity'], rsi_window=int(input['rsi_window']),
                     hma_window=int(input['hma_window']),
                     rrr=float(input['rrr']), rsi_max=float(input['rsi_max']),
                     rsi_min=float(input['rsi_min']),
                     max_margin_closeout_percent=float(input['max_margin_closeout_percent']),
                     max_exposure_percent=float(input['max_exposure_percent']),
                     notify_who=input['notify_who'])

trader.result_summary(datetime.now())
