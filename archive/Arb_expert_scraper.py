import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.python.org")
html = driver.page_source

# Create a BeautifulSoup object
soup = BeautifulSoup(html)
print(soup.prettify())

# Pull all text from the BodyText div
trade_pair_list = soup.find_all("div", {"class": "head"})

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
