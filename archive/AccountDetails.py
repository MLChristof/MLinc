#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:51:17 2017

@author: rweegenaar
"""

import oandapyV20
import oandapyV20.endpoints.accounts as accounts

########### Account Setup ###########
from archive.v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

############# Account Details ##############

r = accounts.AccountDetails(accountID=account_id)
api.request(r)
AccDet = r.response
