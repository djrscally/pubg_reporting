from sqlalchemy import create_engine
from database.model import Base, Player
from database.api import PUBGDatabaseConnector
from pubg.pubg_api import pubg_api
import json
import pymysql
import os

user = os.environ.get('PUBGDB_USERNAME')
password = os.environ.get('PUBGDB_PASSWORD')
host = os.environ.get('PUBGDB_HOST')
database = os.environ.get('PUBGDB_DATABASE')

db_uri = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, database)
#db_uri = 'sqlite:///:memory:'

pubgdb = PUBGDatabaseConnector(db_uri, echo=True)
Base.metadata.create_all(pubgdb.engine)


config = json.load(open('config.json'))

api = pubg_api(config)

api.get_players()
pubgdb.upsert_players(api.players)

api.get_seasons()
pubgdb.upsert_seasons(api.seasons)

api.get_matches()
pubgdb.upsert_matches(api.matches)

pubgdb.upsert_player_matches(api.players)

api.get_player_season_stats()
pubgdb.upsert_player_season_stats(api.player_season_stats)
