from sqlalchemy import create_engine
from database.model import Base, Player
from database.api import PUBGDatabaseConnector
from pubg.pubg_api import pubg_api
import json
import pymysql

db_uri = 'mysql+pymysql://pubg_reporting:pubg_reporting@localhost/pubg'

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
