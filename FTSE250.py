import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader as web
import pickle
import requests


def save_ftse250_tickers():
    resp = requests.get('http://www.hl.co.uk/shares/stock-market-summary/ftse-250')
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'table-styled responsive'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('ftse250.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    tickers = [i if len(i) == 3 or len(i) ==4  else tickers.remove(i )for i in tickers]
    return tickers


def get_data_from_yahoo(reload_ftse250=False):

    if reload_ftse250:
        tickers = save_ftse250_tickers()
    else:
        with open('ftse250.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2017,2,28)

    for ticker in tickers[2:102]:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


get_data_from_yahoo()

