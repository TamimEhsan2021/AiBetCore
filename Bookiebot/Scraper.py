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
    
def dataDict():
    Data = {}
    Data['Link'] = []
    Data['home_EOL'] = []
    Data['away_EOL'] = []
    Data['home_win'] = []
    Data['away_win'] = []
    Data['draw'] = []
    Data['Error'] = []
    Data['Retry'] = []
    Data['Status'] = []
    return Data

def appendData(Data, link, home_EOL, away_EOL,home_win, away_win,draw,error,retry,status):
    Data['Link'].append(link)
    Data['home_EOL'].append(home_EOL)
    Data['away_EOL'].append(away_EOL)
    Data['home_win'].append(home_win)
    Data['away_win'].append(away_win)
    Data['draw'].append(draw)
    Data['Error'].append(error)
    Data['Retry'].append(retry)
    Data['Status'].append(status)


file_csv = pd.read_csv('big_data.csv')
dataInit = dataDict()
Data=dataDict()
for d in tqdm(file_csv.values):     
    link = d[4]
    season = d[5]
    if int(season) >= 2020:
        url=link+"/analysis"
        retryList = []
        try:    
                initScraper = Scraper(url=url)
                ScrapedData = initScraper.scrapingEOL()
                home_EOL = ScrapedData[0]
                away_EOL = ScrapedData[1]
                home_win = ScrapedData[2]
                away_win = ScrapedData[3]
                draw = ScrapedData[4]
                error =''
                retry =False
                status='Success'
                appendData(Data, link, home_EOL, away_EOL,home_win, away_win,draw,error,retry,status)
        except Exception as e:
                if url in retryList:
                    retry = False
                else:
                    retry = True
                home_EOL = ''
                away_EOL = ''
                home_win = ''
                away_win = ''
                draw = ''
                status='Retry'
                error=e
                appendData(Data, link, home_EOL, away_EOL,home_win, away_win,draw,error,retry,status)
                retryList.append(url)

for i in retryList:
    retryList = []
    try:    
            initScraper = Scraper(url=i)
            ScrapedData = initScraper.scrapingEOL()

            home_EOL = ScrapedData[0]
            away_EOL = ScrapedData[1]
            home_win = ScrapedData[2]
            away_win = ScrapedData[3]
            draw = ScrapedData[4]
            error =''
            retry =False
            status='Success'
            appendData(Data, link, home_EOL, away_EOL,home_win, away_win,draw,error,retry,status)
    except Exception as e:
            error=e
            home_EOL = ''
            away_EOL = ''
            home_win = ''
            away_win = ''
            draw = ''
            retry=False
            status='Failed'
            appendData(Data, link, home_EOL, away_EOL,home_win, away_win,draw,error,retry,status)


df = pd.DataFrame(data=Data)
df.to_csv(path_or_buf="scrapedData.csv", index=False, encoding='utf_8_sig')

    
