"""
@author: rweegenaar
"""

import oandapyV20
import oandapyV20.endpoints.orders as orders


def tsl_order():
    """
    For Oanda Rest V20 API
    This function gives an example order to add a trailing stop loss (TS) to an open trade.
    The TS distance to current price should be reset and the applicable trade ID (ticket) should be given.
    """
    accountid, access_token = ("xxx",
                               "xxx")
    client = oandapyV20.API(access_token=access_token)
    order = {
        "order": {
            "type": "TRAILING_STOP_LOSS",
            "tradeID": "46",
            "timeInForce": "GTC",
            "distance": "0.0008"
                }
            }

    r = orders.OrderCreate(accountID=accountid, data=order)
    client.request(r)
    print(r.response)


tsl_order()

