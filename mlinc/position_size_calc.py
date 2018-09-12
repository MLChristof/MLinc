"""
author: Robert Weegenaar
description: position size calculator for Oanda
Also see: https://www.babypips.com/learn/forex/calculating-position-sizes
Four cases possible:
1) account currency equals counter currency of trading instrument
2) account currency equals base currency of trading instrument
3) account currency is different from trading instruments, but the same
    as the conversion's pair counter currency.
4) account currency is different from trading instruments, but the same
    as the conversion's pair base currency.

input: trading instrument, stoploss (SL), current price, total account balance,
        maximum exposure per trade if SL is hit as percentage of total account balance
output: volume (units) to trade
"""

import oandapyV20
from mlinc.oanda_examples.exampleauth import exampleAuth
from mlinc.oanda_examples.instruments_list import instrument_list

# TODO: Write get_trade_volume function into the oanda trader class(?).


def get_mid_price(instrument, api):
    import oandapyV20.endpoints.pricing as pricing
    accountID, access_token = exampleAuth()
    # api = oandapyV20.API(access_token=access_token)
    params = {"instruments": instrument}
    r = pricing.PricingInfo(accountID=accountID, params=params)
    api.request(r)
    pricing = r.response['prices']
    bid_price = float(pricing[0]['bids'][0]['price'])
    ask_price = float(pricing[0]['asks'][0]['price'])
    return (bid_price+ask_price)/2


def get_trade_volume(SL, current_price, balance, max_exp, inst, api, account_cur='EUR'):
    # max exposure in balance currency (e.g. EUR)
    max_exp_cur = balance * max_exp / 100
    # difference between price and SL in pips (absolute value)
    SL_diff = 10000 * abs(SL - current_price)

    # case nr.1
    if account_cur == inst[-3:]:
        # for e.g. SILVER/EUR
        units = round(10000 * max_exp_cur / SL_diff)

    # case nr.2
    elif account_cur == inst[:3]:
        # for e.g. EUR
        units = round(10000 * current_price * max_exp_cur / SL_diff)

    # case nr.3
    elif account_cur not in inst and inst[4:] + '_' + account_cur in instrument_list():
        # test case inst='EUR_GBP', account_cur='USD'
        # conversion pair
        conv_pair = inst[4:] + '_' + account_cur
        # conversion pair exchange rate GBP/USD
        # price_conv_pair = 1.75 # baby pips example
        price_conv_pair = get_mid_price(conv_pair, api)
        # for e.g. EUR/GBP
        units = round(10000 * (1 / price_conv_pair) * max_exp_cur / SL_diff)

    # case nr.4
    elif account_cur not in inst and account_cur + '_' + inst[-3:] in instrument_list():
        # test case inst='USD_JPY', account_cur='CHF'
        # conversion pair
        conv_pair = account_cur + '_' + inst[-3:]
        # conversion pair exchange rate CHF/JPY
        # price_conv_pair = 85.00 # baby pips example
        price_conv_pair = get_mid_price(conv_pair, api)
        # for e.g. USD/JPY
        units = round(10000 * price_conv_pair * max_exp_cur / SL_diff)

    else:
        return 'Oops, could not determine trade volume, ' \
               'check if your instrument is tradable and conversion pair exists. \n' \
               '(e.g. USD_CNH is not possible, since conversion pair EUR_CNH or CNH_EUR does not exist in Oanda)\n' \
               'Please determine trading volume in web interface.'

    return units

# case nr.1
# print(get_trade_volume(SL=12.00000, current_price=12.31031, balance=10000, max_exp=2, inst='XAG_EUR'))

# case nr.2
# print(get_trade_volume(SL=1.15, current_price=1.15551, balance=10000, max_exp=2, inst='EUR_USD'))

# case nr.3
# print(get_trade_volume(SL=1.27319, current_price=1.29319, balance=5000, max_exp=1, inst='EUR_GBP', account_cur='USD'))

# case nr.4
# print(get_trade_volume(SL=110.049, current_price=111.049, balance=5000, max_exp=1, inst='USD_JPY', account_cur='CHF'))

# test Brent Crude Oil
# print(get_trade_volume(SL=76, current_price=77.212, balance=10000, max_exp=2, inst='BCO_USD'))

# HK33_HKD
# print(get_trade_volume(SL=26250, current_price=26139.5, balance=10000, max_exp=2, inst='HK33_HKD'))

# SPX500_USD
# print(get_trade_volume(SL=2900, current_price=2881.1, balance=10000, max_exp=2, inst='SPX500_USD'))

# USD_CNH (gives error)
# print(get_trade_volume(SL=6.68, current_price=6.87456, balance=10000, max_exp=2, inst='USD_CNH'))


