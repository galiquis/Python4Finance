import bs4 as bs
import pickle
import requests
## import ep6
import os # needed to create directories and work with file structure in the OS
import pandas as pd
import datetime as dt
import pandas_datareader as web


def save_FTSE100_tickers():
    ## Define the page we want to scrape
    resp = requests.get('https://en.wikipedia.org/wiki/FTSE_100_Index')
    ## use BS to pull the source
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table',{'id':'constituents'}).find('tbody')
    tickers = []
    for rows in table.find_all('tr')[1:]:
        ticker = rows.find_all('td')
        tickers.append(ticker[1].text)
    with open('FTSE100_Tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers


#save_FTSE100_tickers()


def get_data_yahoo(reload_FTSE100=False):
    if reload_FTSE100:
        tickers = save_FTSE100_tickers()
    else:
        with open('FTSE100_Tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2000,1,1)
    end = dt.datetime.today().strftime('%Y-%m-%d')

    for ticker in tickers:
        if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker+".L", 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            #df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_yahoo()
