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
df = web.DataReader("RDSB.L", 'yahoo', start, end)
print(df.head())
print(df.tail())
