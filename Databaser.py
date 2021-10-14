"""
Database initialising class
"""

import json
import pandas as pd
from sqlalchemy import create_engine
from operator import itemgetter

class Databaser:
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    PORT = 5432
    DATABASE = 'postgres'
    def __init__(self):
        d = self._load_file('dotaproscraper/db_credentials.json')
        self.ENDPOINT, self.USER, self.PASSWORD = itemgetter('ENDPOINT', 'USER', 'PASSWORD')(d)
        self.engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DATABASE}")
        self.engine.connect()

    def _load_file(self, infile: str) -> dict:
        with open(infile,'r+') as file:
            return json.load(file)

    def push_to_db(self, df: pd.DataFrame, db_name: str):
        df.to_sql(db_name, self.engine, if_exists='replace')