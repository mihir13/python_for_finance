import bs4 as bs 
import pickle
import requests

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
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)

	# using pickle we can write it into a file sp500tickers.pickle
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers,f)

	print (tickers)
	return tickers

save_sp500_tickers()




