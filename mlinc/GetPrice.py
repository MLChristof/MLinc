#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 21:17:19 2017

@author: rweegenaar
"""

import oandapyV20
import oandapyV20.endpoints.pricing as pricing


########### Account Setup ###########
from mlinc.v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)


####### Get Pricing info for a list of instruments within an account #######

params = {
        "instruments": "USD_JPY,USD_INR,GBP_USD,EUR_USD"
        }
r = pricing.PricingInfo(accountID=account_id, params=params)
api.request(r)
pricing = r.response['prices']