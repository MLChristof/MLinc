import requests
import pandas as pd
from bs4 import BeautifulSoup


page = requests.get('https://cryptocoincharts.info/arbitrage')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the BodyText div
trade_pair_list = soup.find_all("div", {"class": "table_title container cust_container"})

pair = []
ex1 = []
ex2 = []
time = []

bid = []
ask = []
spread = []
volume = []

for row in trade_pair_list:
    pair.append(row.find_all('span')[0].text)
    ex1.append(row.find_all('span')[1].text)
    ex2.append(row.find_all('span')[2].text)
    time.append(row.find_all('span')[3].text)

dataframe = pd.DataFrame(
    {'Pair': pair,
     'Exchange 1': ex1,
     'Exchange 2': ex2,
     'Time': time
     })

print(dataframe)
