from format_data import get_io_data
# from sklearn import svm
from sklearn import ensemble
import pandas as pd
sentiment_df = pd.read_csv('sentiment.csv', header=0)

i, o = sentiment_df[['stock_num', 'ups', 'sentiment', 'open']], sentiment_df['close']


# supervised machine learning
model = ensemble.RandomForestRegressor()
model.fit(i, o)

def predict(data):
	return model.predict([data])[0]



