import bs4 as bs 
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd 
from pandas_datareader import data as pdr
import pickle
import requests
import yfinance as yf

style.use('ggplot')

yf.pdr_override

# creating correlation table of all s&p 500 stocks 

# function to save sp500 tickers 
def save_sp500_tickers():
	# gets the permission from web link
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

	soup = bs.BeautifulSoup(resp.text, 'lxml')
	# finds the table which is under class wikitable sortable
	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	# for all the available row elemnets in the table, it appends all of the ticker names 
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text.replace('.','-')
		ticker = ticker[:-1]
		tickers.append(ticker)

	# using pickle we can write it into a file sp500tickers.pickle
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers,f)

	return tickers


# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open('sp500tickers.pickle', 'rb') as f:
			tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	start = dt.datetime(2010,1,1)
	end = dt.datetime.now()

	for ticker in tickers:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = pdr.get_data_yahoo(ticker, start, end)
			df.reset_index(inplace=True)
			df.set_index('Date', inplace=True)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))


def compile_data():
	with open('sp500tickers.pickle', 'rb') as f:
		tickers = pickle.load(f)
	main_df = pd.DataFrame()

	for count,ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace=True)
		df.rename(columns = {'Adj Close': ticker}, inplace=True)
		df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how='outer')

		if count % 10 == 0:
			print(count)

	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')


def visualize_data():
	df = pd.read_csv('sp500_joined_closes.csv')
	# df['AAPL'].plot()
	# plt.show()

	# correlates all data to the index ticker names
	df_corr = df.corr()

	# correlated values are saved in variable data
	data = df_corr.values

	# creating  a plot figure
	fig = plt.figure()
	# creating an axis using subplot 
	ax = fig.add_subplot(1,1,1)

	# create a heatmap using Red, Yellow and Green
	heatmap = ax.pcolor(data, cmap = plt.cm.RdYlGn)
	# figure to have a colorbar of the heatmap
	fig.colorbar(heatmap)

	# create ticks at every half mark 
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor = False)
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor = False)

	# inverting y to the bottom and x to the top
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	# creating column and row labels for the graph
	column_labels = df_corr.columns
	row_labels = df_corr.index

	# setting labels of x and y ticks to column and row labels
	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	# plotting x ticks at 90 degrees 
	plt.xticks(rotation=90)
	# color limit of the heatmaps
	heatmap.set_clim(-1,1)

	plt.tight_layout()
	plt.show()

visualize_data()
