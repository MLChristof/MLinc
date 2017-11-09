#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 21:06:29 2017

@author: rweegenaar
"""

# Market order (position entry at current price) with SL & TP
# Market orders can also be used to immediately close a position
# Developer Guide: http://developer.oanda.com/rest-live-v20/transaction-df/

import oandapyV20
import oandapyV20.endpoints.orders as orders

########### Account Setup ###########
from v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

Instrument = 'USD_DKK'
SLPrice    = 6.4428
TPPrice    = 6.3776
Units      = -100 # positive number is long, negative short

########## Market Order Creation ############
# The SL and TP are set within the order
# Client Extensions are also set
data = {
        "order": {
                "stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": SLPrice
                },
                "takeProfitOnFill": {
                        "timeInForce": "GTC",
                        "price": TPPrice
                },
                "timeInForce": "FOK", # FOK = Fill or Kill; IOC = Immediate Or Cancel
                "instrument": Instrument,
                "units": Units,
                "clientExtensions": {
                        "comment": "Tryout API",
                        "tag": "beginner",
                        "id": "My first market order"
                        },
                "type": "MARKET",
                "positionFill": "DEFAULT"
                }
        }

r = orders.OrderCreate(accountID=account_id, data=data)
api.request(r)
MOResponse = r.response
print(r.response)