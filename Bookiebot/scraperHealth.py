from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import pandas as pd
from tqdm import tqdm


class Scraper:
    def __init__(self,url: str):
        self.url = url
        self.req = Request(url=self.url,headers={'user-agent': 'my-app/0.0.1'})
        self.resp = urlopen(self.req)
        self.html = BeautifulSoup(self.resp, features="lxml")
        # self.url = url

    def scrapingEOL(self):
        home_EOL = self.html.find_all('td',{'class':'team1-c'})[0].text
        away_EOL = self.html.find_all('td',{'class':'team2-c'})[0].text
        home_win = self.html.find_all('div',{'class':'elo-label team1-c'},'div')[0].text
        away_win = self.html.find_all('div',{'class':'elo-label team2-c'})[0].text
        draw = self.html.find_all('div',{'class':'elo-label color-grey2'})[0].text
        
        return home_EOL,away_EOL, home_win, away_win, draw
