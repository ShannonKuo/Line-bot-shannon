#-*- coding=utf8 -*-
import sys
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import datetime

now = datetime.datetime.now()

class parse_zodiac:
    def __init__(self):
        self.result = {}
        
    def constellation(self, astro):
        url = 'http://astro.click108.com.tw/daily_0.php?iAstro=' + str(astro) + '&iAcDay=' + now.strftime("%Y-%m-%d")
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        html2 = soup.find('div', class_='TODAY_CONTENT')
        html2 = str(html2)
        soup = BeautifulSoup(html2)
        
        self.result['overview'] = soup.find_all('span')[0].string
        self.result['overview_cont'] = soup.find_all('p')[1].string
        self.result['love'] = soup.find_all('span')[1].string
        self.result['love_cont'] = soup.find_all('p')[3].string
        self.result['work'] = soup.find_all('span')[2].string
        self.result['work_cont'] = soup.find_all('p')[5].string
        self.result['wealth'] = soup.find_all('span')[3].string
        self.result['wealth_cont'] = soup.find_all('p')[7].string
   
        return self.result
   
if __name__=='__main__':
    zodiac = parse_zodiac()
    zodiac.constellation(1)
