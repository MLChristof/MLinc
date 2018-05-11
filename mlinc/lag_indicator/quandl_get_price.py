import quandl


# x = quandl.get('LME/PR_AL', start_date='2018-01-01', end_date='2018-01-13')
# x = quandl.get('CHRIS/ICE_B1', start_date='2018-01-01', end_date='2018-01-13')
x = quandl.get('EIA/PET_RBRTE_D', start_date='2018-01-01', end_date='2018-01-13')
# x = quandl.get('WIKI/AAPL', start_date='2017-10-01', end_date='2018-01-13')
print(x)

