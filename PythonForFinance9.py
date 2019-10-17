from collections import Counter
import numpy as np
import pandas as pd 
import pickle
from sklearn import svm, model_selection, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.model_selection import cross_validate, train_test_split


# processing data for Machine Learning
# groups of companies are likely to move together, some are going to move first 
# pricing data to % change - will be our features and labels will find target (buy,sell or hold)
# ask question to data based on the price changes - within 7 days did the price go up or not (buy if yes, sell if no)

# each model is going to be on per company basis 
def process_data_for_labels(ticker):
	# next 7 days if price goes up or down
	hm_days = 7 
	df = pd.read_csv('sp500_joined_closes.csv', index_col = 0)
	tickers = df.columns.values.tolist()
	df.fillna(0, inplace = True)

	for i in range(1, hm_days+1):
		# price in 2 days from now - todays price / todays price * 100 
		df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker] # (shift (-i) to move future prices up in table)

	df.fillna(0, inplace = True)
	return tickers, df

# function to detect buy,sell or hold stocks
def buy_sell_hold(*args):
	cols = [c for c in args]
	requirement = 0.02
	for col in cols:
		if col > requirement: # buy 
			return 1
		if col < -requirement: # sell 
			return -1
		
	return 0 # hold


def extract_featuresets(ticker):
	tickers, df = process_data_for_labels(ticker)
	# creating maps of either buy, sell or hold for 7 days 
	df['{}_target'.format(ticker)] = list(map( buy_sell_hold, 
		df['{}_1d'.format(ticker)],
		df['{}_2d'.format(ticker)],
		df['{}_3d'.format(ticker)],
		df['{}_4d'.format(ticker)],
		df['{}_5d'.format(ticker)],
		df['{}_6d'.format(ticker)],
		df['{}_7d'.format(ticker)],
		))
	# values are assigned to a list 
	vals = df['{}_target'.format(ticker)].values.tolist()
	str_vals = [str(i) for i in vals]
	# Data spread to see the spreads in value and filling spreads in list 
	print ('Data spread: ', Counter(str_vals))
	df.fillna(0, inplace=True)

	# replaces any infinite increase since it may be an IPO to a NaN
	df = df.replace([np.inf,-np.inf], np.nan)
	# dropping NaN
	df.dropna(inplace=True)

	# values are normalised in % change from yesterday
	df_vals = df[[ticker for ticker in tickers ]].pct_change()
	df_vals = df_vals.replace([np.inf,-np.inf], 0)
	df_vals.fillna(0, inplace=True)

	# x feature sets, y are labels 
	X = df_vals.values
	y = df['{}_target'.format(ticker)].values

	return X,y, df


def do_ml(ticker):
	# where x is our target values and y is the value from buy_sell_hold() either 0,1,-1
	X, y, df = extract_featuresets(ticker)

	# training x and y using train_test_split with test_size of 25%
	X_train, X_test,  y_train, y_test = train_test_split(X, y, 
		test_size = 0.25)

	# creating a classifier 
	# clf = neighbors.KNeighborsClassifier()

	clf = VotingClassifier([('lsvc',svm.LinearSVC()), ('knn', neighbors.KNeighborsClassifier()),
		('rfor', RandomForestClassifier(n_estimators=100))])


	# fit x and y train into classifier
	clf.fit(X_train, y_train)

	# to know confidence of the data 
	confidence = clf.score(X_test, y_test)
	
	print('Accuracy: ', confidence)
	# predictions predicts x_test(futuresets)
	predictions = clf.predict(X_test)

	print('Predicted spread:', Counter(predictions))

	return confidence

do_ml('TWTR')



