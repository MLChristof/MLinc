import quandl
import datetime
import numpy as n
import matplotlib.pyplot as plt
import os


quandl.ApiConfig.api_key = 'dY1WTAj3kH6dCSKvzMBw'
""" Open, High, Low, Close, Change, Settle, Volume, Previous Day Open Interest"""


def multiply(numbers):
    total = 1
    for x in numbers:
        total *= x
    return total

file = open(os.getcwd() + "\Data\Jaarmutatie_CPI__van_200218083138.csv"
            , 'r')
lines = file.readlines()
inflation = []
for line in lines:
    inflation.append(float(line.split(';')[1][1:-1]))
inflation = n.array(inflation)/100+1
# From 1984 to 2017
total_inflation = multiply(inflation)


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
    percentage_change_list = []

    for i, row in enumerate(quandl_array):
        try:
            if quandl_array[i+1][0].month != quandl_array[i][0].month:
                rows_of_interest.append(i+1)
        except IndexError:
            pass
        # if row[0].day == 1:
        #     rows_of_interest.append(i)

    account_balance = 0
    for i, row in enumerate(rows_of_interest):
        date_list.append(quandl_array[row][0])
        if i == 0:
            account_balance = start_capital - transaction_fee
            account_balance_list.append(account_balance)
            inlay_list.append(start_capital)
        else:
            close_price_new = quandl_array[rows_of_interest[i]][3]
            close_price_old = quandl_array[rows_of_interest[i-1]][3]
            percentage_change = (close_price_new - close_price_old) / close_price_old
            percentage_change_list.append(percentage_change)
            account_balance = (percentage_change + 1) * account_balance + monthly_investment - transaction_fee
            account_balance_list.append(account_balance)
            inlay_list.append(inlay_list[i-1] + monthly_investment)

    print(n.mean(percentage_change_list))
    print(account_balance_list[-1])
    print(inlay_list[-1])
    print(date_list)

    plt.figure()
    plt.title('S&P 500 investment')
    plt.plot(account_balance_list, label='Account balance')
    plt.plot(inlay_list, label='Inlay')
    plt.xlabel('date')
    plt.ylabel('Kei harde dollars')
    plt.legend()
    plt.show()

    return account_balance


if __name__ == '__main__':
    SP500 = quandl_stocks(symbol='CHRIS/CME_SP1', start_date=(1984, 1, 1), end_date=None)
    SP500 = n.array(SP500.tolist())
    bench_mark(quandl_array=SP500, start_capital=1000., monthly_investment=0, transaction_fee=-2.5)

    # print(SP500)
    # print(SP500[0][0].year)
    # print(SP500[0][0].month)
    # print(SP500[0][0].day)

    # Plot closing prices and diff
    # closing_prices = []
    # for j, i in enumerate(SP500):
    #     closing_prices.append(i[3])
    # closing_prices_change = n.diff(closing_prices)
    #
    # plt.figure()
    # plt.plot(closing_prices_change)
    # plt.show()

    # for i in SP500:
    #     if i[0].month >= 9 or i[0].month <= 5:
    #         print(i[0], i[3])

    # print(bench_mark(quandl_array=SP500, start_capital=1000., monthly_investment=100., transaction_fee=2.5))







