import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web 

# create a basic graph using adjusting close 

# plot packaging for graphs
style.use('ggplot')

# reads the csv and uses dates as index 
df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)

# print (df.head())

# open and higgh from datafield
print (df[['Open','High']].head())

# plotting adjusting close in a graph
df['Adj Close'].plot()
plt.show()