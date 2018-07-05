#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:27:42 2017

@author: rweegenaar
"""

# Close Position

import oandapyV20
import oandapyV20.endpoints.positions as positions

########### Account Setup ###########
from archive.v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

instrument = "EUR_USD"
long_short = 'long'
units = "1000"


########## Closing an open position ###########

data = {
        "longUnits": units   
        }

r = positions.PositionClose(accountID=account_id,
                             instrument=instrument,
                             data=data)
api.request(r)
COResponse = r.response
print(r.response)