"""
author: Robert Weegenaar
description: position size calculator
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
output: units to trade
"""

import oandapyV20
import oandapyV20.endpoints.pricing as pricing
from mlinc.oanda_examples.exampleauth import exampleAuth

def get_price():

    accountID, access_token = exampleAuth()
    api = oandapyV20.API(access_token=access_token)
    params = {
        "instruments": "USD_JPY,USD_INR,GBP_USD,EUR_USD"
    }
    r = pricing.PricingInfo(accountID=accountID, params=params)
    api.request(r)
    pricing = r.response['prices']
    return(pricing)

def get_trade_volume1(SL, current_price, balance, max_exp):
    """
    Parameters
    ----------
    SL
    current_price: float
        EUR
    balance: float
        account currency
    max_exp: float
        percentage
    ----------
    Returns units (int)
    """

    # max exposure in balance currency (e.g. EUR)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL in pips (absolute value)
    SL_diff = 10000*abs(SL - current_price)

    # for e.g. SILVER/EUR
    units = round(10000 * max_exp_cur/SL_diff)

    return units


def get_trade_volume2(SL, current_price, balance, max_exp):
    """
    calculate trading volume with account currency equal to base currency of instrument
    for example: account currency is EUR and trading instrument is EUR/USD
    Parameters
    ----------
    SL
    current_price: float
        EUR
    balance: float
        account currency
    max_exp: float
        percentage
    ----------
    Returns units (int)
    """

    # max exposure in account currency (e.g. EUR)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL (absolute value)
    SL_diff = 10000*abs(SL - current_price)

    # for e.g. EUR
    units = round(10000 * current_price*max_exp_cur/SL_diff)

    return units


def get_trade_volume3(SL, current_price, balance, max_exp, inst, account_cur='EUR'):
    """
    calculate trading volume with account currency  is not in the
    trading instrument pair, but the same as the conversion pair’s counter currency
    for example: account currency is USD and trading instrument is EUR/GBP
    The conversion pair is GBP/USD
    Parameters
    ----------
    SL
    current_price: float
        EUR
    balance: float
        account currency
    max_exp: float
        percentage
    account_cur: string
        account currency (default set to EUR)
    ----------
    Returns units (int)
    """
    # exchange rate conversion pair
    conv_pair = inst[4:]+'_'+account_cur

    # exhange rate GBP/USD

    price_conv_pair = 1.75

    # max exposure in account currency (e.g. USD)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL (absolute value)
    SL_diff = 10000*abs(SL - current_price)

    # for e.g. EUR/GBP
    units = round(10000 * (1/price_conv_pair)*max_exp_cur/SL_diff)

    return units


# print(get_trade_volume1(SL=12.00000, current_price=12.31031, balance=10000, max_exp=2))
# print(get_trade_volume2(SL=1.15, current_price=1.15551, balance=10000, max_exp=2))
print(get_trade_volume3(SL=0.87475, current_price=0.89475, balance=5000, max_exp=1, inst='EUR_GBP', account_cur='USD'))

