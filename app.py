#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from flask import Flask
from flask import render_template, send_from_directory, url_for
from flask import request
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


def getText(body):
	tag = re.compile('<.*?>')
	text = re.sub(tag,' ', body)
	cleanText = re.sub('[^\w\s]', ' ',text)
	return cleanText

@app.route('/')
def start():
	return render_template('start.html')

@app.route('/crawling', methods = ['POST'])
def crawling():
	if request.method == 'POST':
		word = {}
		
		url = request.form['url']
		#str = url	
		res = requests.get(url)
		soup = BeautifulSoup(res.content, "html.parser")
		body = soup.find('body').text
		text = getText(body).lower()		
		text = word_tokenize(text)
		
		for i in text:
			if i not in stopwords.words("english"):
				if i not in word.keys:
					word[i]=0
				word[i]+=1;
				
		sortList = sorted(word.items(), key = lambda x:x[1], reverse = True)		
		return render_template('crawling.html', list = sortedList)

# main
if __name__ == '__main__':
	app.run(debug=True);
