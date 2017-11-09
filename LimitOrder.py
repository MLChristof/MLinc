#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 21:06:29 2017

@author: rweegenaar, based on code from ratnadeepb on GitHub
"""

import oandapyV20
import oandapyV20.endpoints.orders as orders

########### Account Setup ###########
from v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

Instrument = 'USD_JPY'
OrderPrice = 113.00
SLPrice    = 112.50
Units      = 100 #positive number is long and negative is short


########## Sell Limit Order Creation ############
# The stop is set within the order
# Client Extensions are also set
data = {
        "order": {
                "price": OrderPrice,
                "stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": SLPrice
                },
                "timeInForce": "GTC",
                "instrument": Instrument,
                "units": Units,
                "clientExtensions": {
                        "comment": "Tryout API",
                        "tag": "beginner",
                        "id": "my_test_order"
                        },
                "type": "LIMIT",
                "positionFill": "DEFAULT"
                }
        }

r = orders.OrderCreate(accountID=account_id, data=data)
api.request(r)
LOResponse = r.response
print(r.response)