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
from mlinc.oanda_examples.exampleauth import exampleAuth

# TODO: create if statements to determine which case is applicable, in one function.
# TODO: After this, write this new function into the oanda trader class.

def get_bid_price(instrument):
    import oandapyV20.endpoints.pricing as pricing
    accountID, access_token = exampleAuth()
    api = oandapyV20.API(access_token=access_token)
    params = {"instruments": instrument}
    r = pricing.PricingInfo(accountID=accountID, params=params)
    api.request(r)
    pricing = r.response['prices']
    bid_price = pricing[0]['bids'][0]['price']
    return bid_price

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
    inst: basestring
        trading instrument (e.g. EUR_GBP)
    account_cur: string
        account currency (default set to EUR)
    ----------
    Returns units (int)
    """
    # conversion pair
    conv_pair = inst[4:]+'_'+account_cur

    # conversion pair exchange rate GBP/USD
    # price_conv_pair = 1.75 # baby pips example
    price_conv_pair = float(get_bid_price(conv_pair))

    # max exposure in account currency (e.g. USD)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL (absolute value)
    SL_diff = 10000*abs(SL - current_price)

    # for e.g. EUR/GBP
    units = round(10000 * (1/price_conv_pair)*max_exp_cur/SL_diff)

    return units


def get_trade_volume4(SL, current_price, balance, max_exp, inst, account_cur='EUR'):
    """
    calculate trading volume with account currency  is not in the
    trading instrument pair, but the same as the conversion pair’s base currency
    for example: account currency is CHF and trading instrument is USD/JPY
    The conversion pair is CHF/JPY
    Parameters
    ----------
    SL
    current_price: float
        EUR
    balance: float
        account currency
    max_exp: float
        percentage
    inst: basestring
        trading instrument
    account_cur: string
        account currency (default set to EUR)
    ----------
    Returns units (int)
    """
    # conversion pair
    conv_pair = account_cur+'_'+inst[4:]

    # conversion pair exchange rate CHF/JPY
    # price_conv_pair = 85.00 # baby pips example
    price_conv_pair = float(get_bid_price(conv_pair))

    # max exposure in account currency (e.g. USD)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL in pips (absolute value)
    SL_diff = 10000*abs(SL - current_price)

    # for e.g. USD/JPY
    units = round(10000 * price_conv_pair*max_exp_cur/SL_diff)

    return units


# print(get_trade_volume1(SL=12.00000, current_price=12.31031, balance=10000, max_exp=2))
# print(get_trade_volume2(SL=1.15, current_price=1.15551, balance=10000, max_exp=2))
# print(get_trade_volume3(SL=1.27319, current_price=1.29319, balance=5000, max_exp=1, inst='EUR_GBP', account_cur='USD'))
# print(get_trade_volume4(SL=110.049, current_price=111.049, balance=5000, max_exp=1, inst='USD_JPY', account_cur='CHF'))

