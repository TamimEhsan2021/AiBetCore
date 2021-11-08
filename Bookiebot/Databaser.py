"""
Database initialising class
"""

import sys
import json
import pandas as pd
from sqlalchemy import create_engine
from operator import itemgetter

class Databaser:
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    PORT = 5432
    DATABASE = 'postgres'
    def __init__(self, endpoint, user, password):
        self.ENDPOINT, self.USER, self.PASSWORD = endpoint, user, password
        self.engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DATABASE}")
        self.engine.connect()
        print(str(self.ENDPOINT) + " connected.")

    @staticmethod
    def _load_file(infile: str) -> dict:
        with open(infile,'r+') as file:
            return json.load(file)

    def push_to_db(self, df: pd.DataFrame, db_name: str):
        df.to_sql(db_name, self.engine, if_exists='replace')

    def pull_from_db(self, db_name, engine=None):
        if engine==None:
            engine = self.engine
        return pd.read_SQL(db_name, engine)

    @classmethod
    def pass_credentials(cls, credentials_file: str='db_credentials.json') -> object:
        d = Databaser._load_file(credentials_file)
        return Databaser(*itemgetter('ENDPOINT', 'USER', 'PASSWORD')(d))


def main(argv):
    if len(argv) == 1:
        db = Databaser.pass_credentials(*argv)
    elif len(argv) == 3:
        db = Databaser(*argv)
    else:
        print("usage: python Databaser.py <credentials_file>")
        print("--OR--")
        print("usage: python Databaser.py <ENDPOINT> <USER> <PASSWORD>")

if __name__ == "__main__":
   main(sys.argv[1:])


