import bs4 as bs 
import datetime as dt
import os
import pandas as pd 
from pandas_datareader import data as pdr
import pickle
import requests
import yfinance as yf

yf.pdr_override

# saving all s&p 500 data into stock directory files 

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

save_sp500_tickers()
get_data_from_yahoo()




