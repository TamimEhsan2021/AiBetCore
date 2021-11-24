from Scraper_abstract import Soccer_Scraper
from Databaser import Databaser
import sys
import json
import pandas as pd



def scrape_data(soccer_list):
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
    #df = pd.read_csv('../combined_clean_short.csv')

    #db.push_to_db(df, 'master_input_short')
    dframe = db.pull_from_db('master_input')
    result = zip(dframe["Season"], dframe["Link"])
    result_list = list(result)
    season_list,url_list,  = result_list
    for season in dframe["Season"]:
        scraped_data = scrape_data(season)
    scrapa_frame = pd.DataFrame(scraped_data)
    db.push_to_db(scrapa_frame, 'EOL_features')

if __name__ == "__main__":
    main(sys.argv[1:])
    

    