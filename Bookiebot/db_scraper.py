from Scraper_abstract import Soccer_Scraper
from Databaser import Databaser
import sys
import json
import pandas as pd



def scrape_data(dframe):
    soccer_list = dframe["Link"]
    attr_labels = ['Home_ELO', 'Away_ELO', 'Home_Win', 'Away_Win', 'Draw']
    attr_list = [['td', {'class':'team1-c'}],
                    ['td', {'class':'team2-c'}],
                    ['div', {'class':'elo-label team1-c'}],
                    ['div',{'class':'elo-label team2-c'}],
                    ['div',{'class':'elo-label color-grey2'}]]
    scraper = Soccer_Scraper(soccer_list, attr_labels, attr_list)
    scraper.dataDict()
    scraper.parse_list(soccer_list)
    return scraper.Data

def main(argv):
    db = Databaser.pass_credentials("db_credentials.json")
    #df = pd.read_csv('../combined_clean.csv')

    #db.push_to_db(df, 'master_input')
    dframe = db.pull_from_db('master_input')
    scraped_data = scrape_data(dframe)
    scrapa_frame = pd.DataFrame(scraped_data)
    db.push_to_db(scrapa_frame, 'output1')

if __name__ == "__main__":
    main(sys.argv[1:])
    

    