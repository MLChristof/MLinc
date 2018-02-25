"""
This is the master file for arbitrage trading
Date: 25-02-2018

"""
import pandas as pd


class TradeEngine(object):

    def __init__(self, db_name):
        """
        Parameters
        ----------
        DB_name = str
            DB_name is the name of the validated database.
        """
        self.db_name = db_name

    def get_trade_arguments(self, priority_spec):

        database = pd.read_csv(self.db_name, names=['ID', 'Date', 'ex_buy', 'coin_buy', 'coin_sell', 'volume', 'ex_sell'
                                                    , 'priority'])
        database.
        if priority_spec == 'chance':
            database.sort()
            pass
        elif priority_spec == 'date':
            #TODO: Define to sort on date
            pass


if __name__ == '__main__':
    test = TradeEngine('SQL_database')