import bs4 as bs
import pickle
import requests

def save_FTSE100_tickers():
    ## Define the page we want to scrape
    resp = requests.get('https://en.wikipedia.org/wiki/FTSE_100_Index')
    ## use BS to pull the source
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table',{'id':'constituents'}).find('tbody')
    tickers = []
    for rows in table.find_all('tr')[1:]:
        ticker = rows.find_all('td')
        if not ticker[1].text == 'BT.A':
            tickers.append(ticker[1].text)
    with open('FTSE100_Tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers


save_FTSE100_tickers()
