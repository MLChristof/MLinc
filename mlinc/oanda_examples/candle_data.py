# -*- coding: utf-8 -*-
"""Retrieve candle data.

For complete specs of the endpoint, please check:

    http://developer.oanda.com/rest-live-v20/instrument-ep/

Specs of InstrumentsCandles()

    http://oanda-api-v20.readthedocs.io/en/latest/oandapyV20.endpoints.html

"""
import argparse
import json
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.definitions.instruments import CandlestickGranularity
# from mlinc.oanda_examples.exampleauth import exampleAuth
import re

price = ['M', 'B', 'A', 'BA', 'MBA']
granularities = CandlestickGranularity().definitions.keys()
# create the top-level parser
parser = argparse.ArgumentParser(prog='candle-data')
parser.add_argument('--nice', action='store_true', help='json indented')
parser.add_argument('--count', default=0, type=int,
                    help='num recs, if not specified 500')
parser.add_argument('--granularity', choices=granularities, required=True)
parser.add_argument('--price', choices=price, default='M', help='Mid/Bid/Ask')
parser.add_argument('--from', dest="From", type=str,
                    help="YYYY-MM-DDTHH:MM:SSZ (ex. 2016-01-01T00:00:00Z)")
parser.add_argument('--to', type=str,
                    help="YYYY-MM-DDTHH:MM:SSZ (ex. 2016-01-01T00:00:00Z)")
parser.add_argument('--instruments', type=str, nargs='?',
                    action='append', help='instruments')


def candles(inst, granularity, count, From, to, price, nice, access_token):
    api = API(access_token=access_token)

    def check_date(s):
        dateFmt = "[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}Z"
        if not re.match(dateFmt, s):
            raise ValueError("Incorrect date format: ", s)

        return True

    if inst:
        params = {}
        if granularity:
            params.update({"granularity": granularity})
        if count:
            params.update({"count": count})
        if From and check_date(From):
            params.update({"from": From})
        if to and check_date(to):
            params.update({"to": to})
        if price:
            params.update({"price": price})
        for i in inst:
            r = instruments.InstrumentsCandles(instrument=i, params=params)
            rv = api.request(r)
            kw = {}
            if nice:
                kw = {"indent": nice}
            # print("{}".format(json.dumps(rv, **kw)))
            return rv



if __name__ == "__main__":
    try:
        test = candles(inst=['EUR_USD'], granularity=['H1'], count=[2], From=None, to=None, price=['BA'], nice=True)
        print(test)
    except V20Error as v20e:
        print("ERROR {} {}".format(v20e.code, v20e.msg))
    except ValueError as e:
        print("{}".format(e))
    except Exception as e:
        print("Unkown error: {}".format(e))
