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
from konlpy.tag import Kkma


app = Flask(__name__)

def hfilter(s):
	return re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+','',s)

@app.route('/')
def start():
	return render_template('start.html')

@app.route('/crawling', methods = ['POST'])
def crawling():
	if request.method == 'POST':
		
		kkma = Kkma()		
		word_d = {}
		url = request.form['url']
		req = requests.get(url)
		html = req.text
		soup = BeautifulSoup(html, 'html.parser')
		my_para = soup.select('#articleBodyContents')
		for para in my_para:
			hsent = hfilter(para.getText())
			wlist = kkma.pos(hsent)
			for w in wlist:
				if w[1] == "NNG":
					if w[0] not in word_d:
						word_d[w[0]]=0
					word_d[w[0]] += 1			
		sortedList = sorted(word_d.items(), key = lambda x:x[1], reverse = True)		
		return render_template('crawling.html', list = sortedList)

# main
if __name__ == '__main__':
	app.run(debug=True);
