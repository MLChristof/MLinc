#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:51:17 2017

@author: rweegenaar
"""

import oandapyV20
import oandapyV20.endpoints.accounts as accounts
from mlinc.oanda_examples.exampleauth import exampleAuth

accountID, access_token = exampleAuth()

########### Account Setup ###########

api = oandapyV20.API(access_token=access_token)

############# Account Details ##############

r = accounts.AccountDetails(accountID=accountID)
api.request(r)
AccDet = r.response
print(AccDet)
