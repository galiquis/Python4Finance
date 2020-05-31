import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
#import pandas_datareader.data as web
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()
# Yahoo API seems to work for UK stocks :)
# check Yahoo Finance for the codes
#df = web.DataReader("RDSB.L", 'yahoo', start, end)

# Writing and reading DataFrames
#df.to_csv('RDSB.csv') # converts the dataframe to CSV
df = pd.read_csv('RDSB.csv', parse_dates=True, index_col=0)
#print(df.head())

df[['Open','Close','High']].plot()
plt.show()
