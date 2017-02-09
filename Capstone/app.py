from flask import Flask, render_template, request, redirect
import json
import requests
import os

app = Flask(__name__)
selector = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
