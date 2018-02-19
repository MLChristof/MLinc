import quandl
import datetime
import numpy as n
import matplotlib.pyplot as plt


quandl.ApiConfig.api_key = 'dY1WTAj3kH6dCSKvzMBw'
""" Open, High, Low, Close, Change, Settle, Volume, Previous Day Open Interest"""


def quandl_stocks(symbol, start_date=(2000, 1, 1), ticker=None, end_date=None):
    """
    symbol is a string representing a stock symbol, e.g. 'AAPL'

    start_date and end_date are tuples of integers representing the year, month,
    and day

    end_date defaults to the current date when None
    """

    # query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]
    query_list = [symbol]
    # print(query_list)

    start_date = datetime.date(*start_date)

    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()

    return quandl.get(query_list,
                      returns='numpy',
                      start_date=start_date,
                      end_date=end_date,
                      collapse='daily',
                      order='asc',
                      ticker=ticker
                      )


def bench_mark(quandl_array, start_capital, monthly_investment, transaction_fee):
    rows_of_interest = []
    account_balance_list = []
    inlay_list = []
    date_list = []

    for i, row in enumerate(quandl_array):
        month = row[0][i+1].month
        if row[0][i+1].month != row[0][i].month:

        if row[0].day == 1:
            rows_of_interest.append(i)

    for i, row in enumerate(rows_of_interest):
        date_list.append(quandl_array[row][0])
        if i == 0:
            account_balance = start_capital - transaction_fee
            account_balance_list.append(account_balance)
            inlay_list.append(start_capital)
        else:
            close_price = quandl_array[row][3]
            percentage_change = (quandl_array[rows_of_interest[i-1]][3] - close_price) / close_price
            account_balance = (percentage_change + 1) * account_balance + monthly_investment - transaction_fee
            account_balance_list.append(account_balance)
            inlay_list.append(inlay_list[i-1] + monthly_investment)

    print(account_balance_list[-1])
    print(inlay_list[-1])
    print(date_list)

    plt.figure()
    plt.plot(account_balance_list)
    plt.hold
    plt.plot(inlay_list)
    plt.show()

    return account_balance


if __name__ == '__main__':
    SP500 = quandl_stocks(symbol='CHRIS/CME_SP1', start_date=(1984, 1, 1), end_date=None)
    SP500 = n.array(SP500.tolist())
    # print(SP500[0])
    # print(SP500[0][0].year)
    # print(SP500[0][0].month)
    # print(SP500[0][0].day)

    # for i in SP500:
    #     if i[0].month >= 9 or i[0].month <= 5:
    #         print(i[0], i[3])

    # print(bench_mark(quandl_array=SP500, start_capital=1000., monthly_investment=100., transaction_fee=2.5))
    bench_mark(quandl_array=SP500, start_capital=1000., monthly_investment=100, transaction_fee=0)






