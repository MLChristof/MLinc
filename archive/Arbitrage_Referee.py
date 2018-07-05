"""
This is the master file for arbitrage trading
Date: 25-02-2018

""""""
This is the master file for arbitrage trading
Date: 25-02-2018

 - Validation, 25-02-2018

"""

import pandas as pd

class ValidateChance(object):
    def __init__(self, input_database):
        """
        Parameters
        ----------
        input_database: str
            input_database contains all the obtained chances form the arbitrage website
        """
        db_chances = pd.read_csv(input_database, names=['ID', 'Date', 'Exchange Buy', 'Exchange Sell', 'Currency',
                                                        'Fund', 'Volume', 'Ask Price', 'Bid Price', 'Spread',
                                                        'Predicted Profit'])
        self.ID = db_chances['ID']
        self.currency = db_chances['Currency']
        self.fund = db_chances['Fund']
        self.exchange_buy = db_chances['Exchange Buy']
        self.exchange_sell = db_chances['Exchange Sell']
        self.date = db_chances['Date']
        self.price_bid = db_chances['Bid Price']
        self.price_ask = db_chances['Ask Price']
        self.spread = db_chances['Spread']
        self.volume = db_chances['Volume']
        self.predicted_profit = db_chances['Predicted Profit']

        print(self.predicted_profit)
        if self.predicted_profit[0] >= 0:
            self.advice = 'true'

        print(self.advice)

    def buy_check(self):
        #TODO: use webscrape on the exchange website
        self.advice.append = 'true'

    def sell_check(self):
       #TODO: confirm the selling party, use webscrape on the exchange website

        self.advice.append = 'true'

    def trade_performance_index(self):

        #TODO: calculated the TPI
        revenue = self.spread * self.volume
        tpi_predicted = self.predicted_profit / revenue
        print(tpi_predicted)

        self.advice.append = 'true'

    def trade_decision(self):
        #TODO: maak de afweging

        if self.advice == 'true':
            print('KOPEN')
        else:
            print('NIET KOPEN')

if __name__ == '__main__':
    test = ValidateChance('C:\Local\99-Off_topic\MLtrading\Python\MLinc\mlinc\Data\Input_web_database.csv')
