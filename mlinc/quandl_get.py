import quandl
import os
import datetime


class QuandlGet(object):
    def __init__(self, quandl_key, api_key, start_date, end_date):
        self.quandl_key = quandl_key
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date

        self.quandl_data = quandl.get(self.quandl_key, start_date=self.start_date, end_date=self.end_date,
                                      authtoken=api_key)

    def save_to_csv(self, path):
        self.quandl_data.to_csv(path)


if __name__ == '__main__':
    cwd = os.getcwd()
    with open("C:\\Users\Jelle\Desktop\quandl_api.txt", 'r') as f:
        api_key = f.read()

    x = QuandlGet('CHRIS/ICE_B1', api_key, start_date=datetime.datetime(2017, 10, 1), end_date=datetime.datetime(2018, 1, 13))
    x.save_to_csv(path=cwd + '\\lag_indicator\\data\\' + 'ICE_B1')

