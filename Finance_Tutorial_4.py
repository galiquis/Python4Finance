import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

## import candlestick
## matplotlib.finance hasdepreciated - now mplfinance
## also as the API has changed there needs to be a change to how candlestick_ohlc is ref'd
from mplfinance.original_flavor import candlestick_ohlc # .original_flavor allows access to old methods
import matplotlib.dates as mdates



style.use('ggplot')
df = pd.read_csv('RDSB.csv', index_col=0, parse_dates=True)

## Going to resample the data into a new data frame
## (Resampling is aggrigating data up)
## looking to pull out Open, High, Low, CLose across each 10 day segment
df_ohlc = df['Adj Close'].resample('10D').ohlc()
## along with the sum'd volume for the 10 days
df_Vol = df['Volume'].resample('10D').sum()
## next we need to reset the index column on df_olhc so that it's not using the Date column
df_ohlc.reset_index(inplace=True) # sets the frame to all being dataframe
## and convert the date to an mdates number
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
## check the DFs
# print(df_ohlc.head())
# print(df_Vol.head())

## Build the chart
## define the axis and plot area
## ax1 - top chart
ax1 =  plt.subplot2grid((6,1), (0,0), rowspan=5,colspan=1)
## ax2 - bottom chart
ax2 =plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=ax1)
## define X axis as dates
ax1.xaxis_date()
## Draw candlesticks
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

## and plot the volume on the bottom chart
ax2.fill_between(df_Vol.index.map(mdates.date2num), df_Vol.values, 0) # fill_between(x_cord, y_cord, from 0)

plt.show()
