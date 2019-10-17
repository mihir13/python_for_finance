import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web 

# plotting adjusted close and moving averages along with volume 

# special import where future warnings are ignored
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

# plot packaging for graphs
style.use('ggplot')

# reads the csv and 
df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)

# takes today and 49 days prior prices to calculate all averages as moving averages
df['50ma'] = df['Adj Close'].rolling(window = 50, min_periods = 0). mean()

# # Keeps the DataFrame with valid entries in the same variable.
# df.dropna(inplace = True)

# subplots using subplot2grid (6 rows 1 column), (x,y), row and col span, share with ax1 of x axis
ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 5, colspan = 1, sharex = ax1)


#plotting the three datafields using plots and bar for Volume 
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['50ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
