from trader import OandaTrader
import configparser

def from_conf_file(instruments, conf):
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(conf)
    input = {}
    for item in config['OandaTraderInput']:
        input[item] = config['OandaTraderInput'][item]

    return input

if __name__ == '__main__':

    conf_input = from_conf_file('all', r'/home/pi/Documents/ML_conf/conf.ini')

    trader = OandaTrader('all', **conf_input)

    close = trader.close_open_positions()


