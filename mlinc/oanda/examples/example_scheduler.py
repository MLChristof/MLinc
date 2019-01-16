
def oanda_to_csv_live(oanda_output):
    delta_data_frame = oanda_to_dataframe(oanda_output)
    delta_dataframe.to_csv(os.getcwd() + '\\oanda_data\\' + oanda_output['instrument'],
                           sep=',',
                           columns=['time', 'open', 'high', 'low', 'close', 'volume'],
                           index=False)

    dataframe.append(delta_dataframe)

    schedule.every(60).minutes.do(oanda_to_csv(df.to_csv))


 def main():
     para = {'inst': 'EUR_USD',
             'granularity': 'H1',
             'count': 100}

     test_data = candles(inst=[para['inst']], granularity=[para['granularity']], count=[para['count']], From=None,
                         to=None, price=None, nice=True)

     df = oanda_baconbuyer(test_data, hma_window=14, rsi_window=14)
     print(df)

     df_name = para['inst'] + '_' + para['granularity'] + '_Count' + str(para['count']) + '_' + str(dt.today())

     df_path = os.path.dirname(__file__) + r'\trader\data\\'

     df.to_csv(df_path + df_name + '.csv')



 if __name__ == '__main__':
     main()
