import numpy as np
import pandas as pd
import pickle

def process_data_for_lables(ticker):
    hm_days = 7
    df = pd.read_csv('FTSE_100_Index_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    # replace NAs with 0
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]

    df.fillna(0, inplace=True)

    return tickers, df

def buy_sell_hold(*args): # args allows the passing of colomns to function
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < requirement:
            return -1
    return 0        
