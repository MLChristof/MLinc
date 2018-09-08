"""
author: Robert Weegenaar
description: position size calculator

input: trading instrument, stoploss (SL), current price, total account balance,
        maximum exposure per trade if SL is hit as percentage of total account balance
output: units to trade
"""


def get_trade_volume(sl, current_price, balance, max_exp):
    """

    Parameters
    ----------
    sl
    current_price: float
        EUR
    balance: float
        balance currency (EUR)
    max_exp: float
        percentage

    Returns: units (int)
    -------

    """
    # max exposure in balance currency (e.g. EUR)
    max_exp_cur = balance*max_exp/100

    # difference between price and SL (absolute value)
    sl_diff = 10000*abs(sl - current_price)

    # for EUR_USD
    units = round(10000 * current_price*max_exp_cur/sl_diff)

    return units


print(get_trade_volume(1.17224, 1.15491, 10000, 2))
