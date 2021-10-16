from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import xlrd
import pandas as pd
from tqdm import tqdm

def scrapingData(url):
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, features="lxml")
    home_EOL = html.find_all('td',{'class':'team1-c'})[0].text
    away_EOL = html.find_all('td',{'class':'team2-c'})[0].text
    home_win = html.find_all('div',{'class':'elo-label team1-c'},'div')[0].text
    away_win = html.find_all('div',{'class':'elo-label team2-c'})[0].text
    draw = html.find_all('div',{'class':'elo-label color-grey2'})[0].text
    return home_EOL,away_EOL, home_win, away_win, draw

Data = {}
Data['Link'] = []
Data['home_EOL'] = []
Data['away_EOL'] = []
Data['home_win'] = []
Data['away_win'] = []
Data['draw'] = []
Data['Error'] = []

home_EOL = ''
away_EOL = ''
home_win = ''
away_win = ''
draw = ''

file_csv = pd.read_csv('big_data.csv')
for d in tqdm(file_csv.values):       
    link = d[4]
    season = d[5]
    if int(season) >= 2015:
        url=link+"/analysis"
    try:
            ScrapedData = scrapingData(url=url)
            home_EOL = ScrapedData[0]
            away_EOL = ScrapedData[1]
            home_win = ScrapedData[2]
            away_win = ScrapedData[3]
            draw = ScrapedData[4]
            Data['Link'].append(link)
            Data['home_EOL'].append(home_EOL)
            Data['away_EOL'].append(away_EOL)
            Data['home_win'].append(home_win)
            Data['away_win'].append(away_win)
            Data['draw'].append(draw)
            Data['Error'].append('')
    except Exception as e:
            Data['Link'].append(link)
            Data['home_EOL'].append(home_EOL)
            Data['away_EOL'].append(away_EOL)
            Data['home_win'].append(home_win)
            Data['away_win'].append(away_win)
            Data['draw'].append(draw)
            Data['Error'].append(e)

df = pd.DataFrame(data=Data)
df.to_csv(path_or_buf="scrapedData.csv", index=False, encoding='utf_8_sig')

    
