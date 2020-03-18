from mlinc.oanda.trader import OandaTrader
import configparser

def from_conf_file(instruments, conf):
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(conf)
    input = {}
    for item in config['OandaTraderInput']:
        input[item] = config['OandaTraderInput'][item]

    return input

if __name__ == '__main__':

    conf_input = from_conf_file('all', r'C:\Data\2_Personal\Python_Projects\MLinc\mlinc\oanda\conf_files\conf.ini')

    trader = OandaTrader('all', **conf_input)

    close = trader.close_open_positions()


