#Created on Tue Nov  7 06:23:03 2017

#@author: Robert Weegenaar, based on code from ratnadeepb on GitHub

import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.trades as trades
from os import environ
import json

########### Account Setup ###########
from v20conf import account_id, account_key
api = oandapyV20.API(access_token=account_key)

# ############# Account Details ##############
#
# r = accounts.AccountDetails(accountID=account_id)
# api.request(r)
# print(r.response)

# ############# Account Summary #############
# r = accounts.AccountSummary(accountID=account_id)
# api.request(r)
# print(r.response['account'])
# print(r.response['lastTransactionID'])
#
# ########## Limit Order Creation ############
#
# # This is a stop loss order (short) of 1 unit on the EUR_USD pair
# # The stop is set within the order
# # Client Extensions are also set
# data = {
#         "order": {
#                 "price": "1.1560",
#                 "stopLossOnFill": {
#                         "timeInForce": "GTC",
#                         "price": "1.1570"
#                 },
#                 "timeInForce": "GTC",
#                 "instrument": "EUR_USD",
#                 "units": "-1",
#                 "clientExtensions": {
#                         "comment": "Trying the API out",
#                         "tag": "beginner",
#                         "id": "my_test_order"
#                         },
#                 "type": "LIMIT",
#                 "positionFill": "DEFAULT"
#                 }
#         }
#
# r = orders.OrderCreate(accountID=account_id, data=data)
# api.request(r)
# print(r.response)
#
# ############ Take Profit Order Creation ###############
#
# # Get ID of the last order
# tr_id = r.response['orderFillTransaction']['id']
#
# take_profit = {
#         "order": {
#                 "timeInForce": "GTC",
#                 "price": "1.1545",
#                 "type": "TAKE_PROFIT",
#                 "tradeID": tr_id
#                 }
#         }
# r = orders.OrderCreate(accountID=account_id, data=take_profit)
# api.request(r)
# print(r.response)
#
# ############## Trailing Stop Order Creation ###############
#
# trailing_SL = {
#         "order": {
#                 "timeInForce": "GTC",
#                 "distance": "0.001",
#                 "type": "TRAILING_STOP_LOSS",
#                 "tradeID": tr_id
#                 }
#         }
# r = orders.OrderCreate(accountID=account_id, data=trailing_SL)
# api.request(r)
# print(r.response)
#
# ############### Cancel an Order ################
#
# r = orders.OrderCancel(accountID=account_id, orderID=tr_id)
# api.request(r)
# print(r.response)
#
# ############### Get Order List ################
#
# r = orders.OrderList(accountID=account_id)
# api.request(r)
# print(r.response)
# trade_ids = r.response['orders']
#
# print(trade_ids)
#
# ############### Get Order Detail ################
#
# for order in trade_ids:
#     r = orders.OrderDetails(accountID=account_id, orderID=order['id'])
#     api.request(r)
#     print(r.response)
#
# ########### Get Pending Orders #############
#
# r = orders.OrdersPending(accountID=account_id)
# api.request(r)
# print(r.response)
#
########### Get all open positions ############

r = positions.OpenPositions(accountID=account_id)
api.request(r)
print(r.response)
all_positions = r.response['positions']
#
# ########## Closing an open position ###########
#
# instrument = "EUR_USD"
# data = {
#         "logUnits": "10",
#         "longClientExtensions": "Close 10 units of long positions in {}".format(instrument)
#         }
# r = positions.PositionClose(accountID=account_id,
#                             instrument=instrument,
#                             data=data)
# api.request(r)
# print(r.response)
#
# ########## Position Details ############
#
# instrument = "EUR_USD"
# r = positions.PositionDetails(accountID=account_id, instrument=instrument)
# api.request(r)
# print(r.response)
#
# ########## List of all positions ##########
#
# r = positions.PositionList(accountID=account_id)
# api.request(r)
# print(r.response)
# #
# ######## Get Pricing info for a list of instruments within an account #######
#
# params = {
#         "instruments": "USD_JPY,USD_INR,GBP_USD,EUR_USD"
#         }
# r = pricing.PricingInfo(accountID=account_id, params=params)
# api.request(r)
# print(r.response)
# pricing = r.response['prices']

# ####### Get realtime pricing on instruments #########
#
# r = pricing.PricingStream(accountID=account_id, params=params)
# rv = api.request(r)
# maxrecs = 10
# for tick in rv:
#     print(json.dumps(tick, indent=4), ",")
#     maxrecs -= 1
#     if maxrecs == 0:
#         try:
#             r.terminate("Max records received")
#         except oandapyV20.exceptions.StreamTerminated as e:
#             print(e)


