import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web 


# creating a database stored in .csv or .xslx of a stock history 

# special import where future warnings are ignored
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

# plot packaging for graphs
style.use('ggplot')

# start and end dates for timeline of a company stock
start = dt.datetime(2010,1,1)
end = dt.datetime(2019,10,1)

# dataframe to read Tesla stocks from Yahoo using start and end dates
df = web.DataReader('TSLA', 'yahoo', start, end)

# prints the latest stock data 
print (df.tail(6))

# data file converted to csv
df.to_csv('tsla.csv')

