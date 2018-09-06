# -*- coding: utf-8 -*-
"""Streaming price data.

demonstrate the PricingStream request.

Example:
    streaming_prices.py --nice --count 10 --inst EUR_USD --inst EUR_JPY
"""
import argparse
import json
from oandapyV20 import API
from oandapyV20.exceptions import V20Error, StreamTerminated
from oandapyV20.endpoints.pricing import PricingStream
from exampleauth import exampleAuth
from requests.exceptions import ConnectionError

# create the top-level parser
parser = argparse.ArgumentParser(prog='steaming_prices')
parser.add_argument('--nice', action='store_true', help='json indented')
parser.add_argument('--timeout', default=0, type=float,
                    help='timeout in secs., default no timeout')
parser.add_argument('--count', default=0, type=int,
                    help='# of records to receive, default = unlimited.')
parser.add_argument('--instruments', type=str, nargs='?',
                    action='append', help='instruments')


def stream(count, instruments, nice, timeout=None):
    accountID, access_token = exampleAuth()

    request_params = {}
    if timeout:
        request_params = {"timeout": timeout}

    # fetch MAXREC stream records
    MAXREC = count

    api = API(access_token=access_token,
              environment="practice",
              request_params=request_params)

    # setup the stream request
    r = PricingStream(accountID=accountID,
                      params={"instruments": ",".join(instruments)})

    n = 0
    R_list = list()
    while True:
        try:
            for R in api.request(r):
                if nice:
                    R = json.dumps(R, indent=2)
                print('Collecting Data.. Please wait..')
                R_list.append(R)
                n += 1
                if MAXREC and n >= MAXREC:
                    r.terminate("maxrecs received: {}".format(MAXREC))

        except V20Error as e:
            # catch API related errors that may occur
            with open("LOG", "a") as LOG:
                LOG.write("V20Error: {}\n".format(e))
            break
        except ConnectionError as e:
            with open("LOG", "a") as LOG:
                LOG.write("Error: {}\n".format(e))
        except StreamTerminated as e:
            with open("LOG", "a") as LOG:
                LOG.write("Stopping: {}\n".format(e))
            break
        except Exception as e:
            with open("LOG", "a") as LOG:
                LOG.write("??? : {}\n".format(e))
            break

    return R_list



if __name__ == '__main__':
    x = stream(2, ['EUR_USD'], True, timeout=5)
    print(x)



