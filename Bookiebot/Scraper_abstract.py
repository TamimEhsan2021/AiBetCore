from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import pandas as pd
from tqdm import tqdm
from Databaser import Databaser


class Scraper:
    def __init__(self, url_list: str,attr_labels, attr_list):
        self.url_list = url_list
        self.attr_labels = attr_labels
        self.attr_list = attr_list
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Connection': 'keep-alive'}


    def parse_data(self, url):
        error_log = []
        attr_results = []
        try:
            #self.req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
            self.req = Request(url=url,headers=self.headers)
            self.resp = urlopen(self.req)
            self.html = BeautifulSoup(self.resp, features="lxml")
        except:
            error_log.append(url)
            #self.req = Request(url='https://www.besoccer.com/',headers={'user-agent': 'my-app/0.0.1'})
            self.req = Request(url='https://www.besoccer.com/',headers=self.headers)
            self.resp = urlopen(self.req)
            self.html = BeautifulSoup(self.resp, features="lxml")
        attr_results = []
        for i, attr_path in enumerate(self.attr_list):
            result, error_log = self.scrape_attr(attr_path, self.attr_labels[i], error_log) 
            attr_results.append(result)
        return attr_results, error_log


    def scrape_attr(self, attr_path, attr_label, error_log):
        a = attr_path[0] 
        b = attr_path[1]
        attr = ''
        try:
            attr = self.html.find_all(a,b)[0].text
        except:
            error_log.append('Label: ' + attr_label + ' ; Path:' + str(a) + ' ; ' + str(b))
        return attr, error_log

class Soccer_Scraper(Scraper):
    def dataDict(self):
        self.Data = {}
        self.Data['Link'] = []
        for i, attr in enumerate(self.attr_labels):
            self.Data[attr] = []
        self.Data['Error'] = []
    
    def appendData(self, link, attr_results, error):
        self.Data['Link'].append(link)
        for i, attr in enumerate(self.attr_labels):
            self.Data[attr].append(attr_results[i])
            
        self.Data['Error'].append(error)

    def parse_list(self, soccer_list, season_list):

        for url in tqdm(soccer_list):
            attr_results, error_log = self.parse_data(url+"/analysis")
            self.appendData(url, attr_results, error_log)


if __name__ == "__main__":
    """
    db = Databaser.pass_credentials(*argv)
    dframe = db.pull_from_db('master_input')
    soccer_list = dframe["URL"]

    """
    soccer_list = ['https://www.besoccer.com/match/seleccion-argelia/seleccion-burkina-faso/2020503781', 'https://www.besoccer.com/match/seleccion-camerun/seleccion-costa-marfil/2020503787']
    attr_labels = ['Home_ELO', 'Away_ELO', 'Home_Win', 'Away_Win', 'Draw']
    attr_list = [['td', {'class':'team1-c'}],
                    ['td', {'class':'team2-c'}],
                    ['div', {'class':'elo-label team1-c'}],
                    ['div',{'class':'elo-label team2-c'}],
                    ['div',{'class':'elo-label color-grey2'}]]
    scraper = Soccer_Scraper(soccer_list, attr_labels, attr_list)
    scraper.dataDict()
    scraper.parse_list(soccer_list)
    print(scraper.Data)

    