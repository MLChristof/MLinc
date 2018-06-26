import json
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream

from v20conf import *

accountID = account_id
access_token= account_key

api = API(access_token=access_token, environment="practice")

instruments = "DE30_EUR,EUR_USD,EUR_JPY"
s = PricingStream(accountID=accountID, params={"instruments":instruments})
try:
    n = 0
    for R in api.request(s):
        print(json.dumps(R, indent=2))
        n += 1
        if n > 10:
            s.terminate("maxrecs received: {}".format(MAXREC))

except V20Error as e:
    print("Error: {}".format(e))