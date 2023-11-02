from flask import Flask, jsonify
from ai import predict
from stocks import check_exist, stocks
from api import get_stock_info, get_stock_tweets
from apscheduler.schedulers.background import BackgroundScheduler
from get_info import update_info
import pandas as pd

#Backend app with endpoints to get specific information
app = Flask(__name__)

@app.route('/')
def home():
  return {'state': 'It is working!'}

@app.route('/search/<name>')
def search(name):
  search = check_exist(name)
  return f'{search}'


@app.route('/stock_info/<name>')
def stock_info(name):
  info = get_stock_info(name).drop(columns=['ticker'])
  info = info.values.tolist()
  return info

@app.route('/tweet_info/<name>')
def tweet_info(name):
  info = get_stock_tweets(name).drop(columns=['ticker'])
  info = info.values.tolist()
  return info

@app.route('/reddit_info/<ticker_num>')
def get_reddit_info(ticker_num):    
	reddit_df = pd.read_csv('sentiment.csv', header=0)
	print(reddit_df[reddit_df['stock_num'] == int(ticker_num)].tail(1)['ups'])
	ups = reddit_df[reddit_df['stock_num'] == int(ticker_num)].tail(1)['ups'].values[0]
	sentiment = reddit_df[reddit_df['stock_num'] == int(ticker_num)].tail(1)['sentiment'].values[0]
	return jsonify({
		"ticker_num": ticker_num,
		"ups": ups,
		"sentiment": sentiment,
	})

@app.route('/predict/<name>')
def getPrediction(name):
	ticker_num = stocks[name.upper()]
	reddit_df = pd.read_csv('sentiment.csv', header=0)
	ups = reddit_df[reddit_df['stock_num'] == ticker_num].tail(1)['ups'].values[0]
	sentiment = reddit_df[reddit_df['stock_num'] == ticker_num].tail(1)['sentiment'].values[0]
	info = get_stock_info(name).drop(columns=['ticker'])
	info = info.values.tolist()
	data = [ticker_num, ups, sentiment, info[-1][0]]
	prediction = predict(data)
	return f'{prediction}'


sched = BackgroundScheduler()
sched.add_job(update_info,'interval',hours=12)
sched.start()

app.run(host = "0.0.0.0")