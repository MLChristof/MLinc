#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:29:12 2017

@author: rweegenaar
"""

# Script to add a TP to a existing position. Instrument

import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions

########### Account Setup ###########
from mlinc.v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

########## Position Details ############

# Input to create Take Profit
instrument = "USD_JPY"
long_short = 'short'
TP         = "113.3"

# Get order fill ID
r = positions.PositionDetails(accountID=account_id, instrument=instrument)
api.request(r)
Position = r.response
tr_id = str(r.response['position'][long_short]['tradeIDs'])
#format string: remove ['']
tr_id = tr_id[2:-2]

########### Take Profit Order Creation ###############
take_profit = {
        "order": {
                "timeInForce": "GTC",
                "price": TP,
                "type": "TAKE_PROFIT",
                "tradeID": tr_id
                }
        }
        
r = orders.OrderCreate(accountID=account_id, data=take_profit)
api.request(r)
TPResponse = r.response 
print(r.response)