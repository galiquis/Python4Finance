import bs4 as bs
import pickle
import requests
## import ep6
import os # needed to create directories and work with file structure in the OS
import pandas as pd
import datetime as dt
import pandas_datareader as web
## import ep8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

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

def compile_data():
    with open('FTSE100_Tickers.pickle', 'rb') as f: #open the pickle for reading
        tickers = pickle.load(f) # set tickers to content
    main_df = pd.DataFrame() # set main_df to a blank dataframe
    for count, ticker in enumerate(tickers): # enumerate adds a count as loop itterates
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker)) #reads each csv ticker into df
        df.set_index('Date', inplace=True) # set indexto date
        df.rename(columns={'Adj Close': ticker}, inplace=True) # rename the adj close to company ticker
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True) #drop everything we dont need

        if main_df.empty: # if main_df is empty
            main_df = df # set to the first df
        else:
            main_df = main_df.join(df, how='outer') # otherwise join the new df to the existing main_df

        if count % 10 == 0:
            print(count) # pring out every 10
    print(main_df.head())
    main_df.to_csv('FTSE_100_Index_joined_closes.csv') # save it off at the end

def visualise_data():
    df = pd.read_csv('FTSE_100_Index_joined_closes.csv')
    #df['RDSA'].plot()
    #plt.show()
    df_corr = df.corr()
    print(df_corr.head())
    data1 = df_corr.values
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap1)
    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap1.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()

## get_data_yahoo()
## compile_data()
visualise_data()