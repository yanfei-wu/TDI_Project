from flask import Flask, render_template, request, redirect
from pandas import DataFrame, to_datetime
import json
import requests
import time
from datetime import datetime, timedelta
from bokeh.plotting import figure, output_file, show
from bokeh import embed

app = Flask(__name__)
selector = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

def plot_data():
    # get user input
    ticker = request.form['ticker']
    features = request.form.getlist('feature')

    # get data from quandl API & put in pandas
    now = datetime.now()
    start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=MLsrd2_dG3A495syK-tM'
    r = requests.get(URL)

    request_df = DataFrame(r.json())
    df = DataFrame(request_df.ix['data','dataset'], columns = request_df.ix['column_names','dataset'])
    df.columns = [x.lower() for x in df.columns]
    df = df.set_index(['date'])
    df.index = to_datetime(df.index)

    # plot stock price with bokeh
    p = figure(x_axis_type = "datetime")
    if 'cp' in features:
        p.line(df.index, df['close'], color='blue', legend='close price', line_width=2)
    if 'acp' in features:
        p.line(df.index, df['adj. close'], color='black', legend='adjusted close price', line_width=2)
    if 'op' in features:
        p.line(df.index, df['open'], color='red', legend='open price', line_width=2)
    if 'aop' in features:
        p.line(df.index, df['adj. open'], color='green', legend='adjusted open price', line_width=2)
    return p

@app.route('/plot_page',methods=['GET','POST'])
def plot_page():
	plot = plot_data()
	script, div = embed.components(plot)
	return render_template('bokeh.html',script=script,div=div)


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
