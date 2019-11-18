from sqlalchemy import create_engine
from database.model import Base, Player
from database.api import PUBGDatabaseConnector
from pubg.pubg_api import pubg_api
import json

db_uri = 'sqlite:////home/djrscally/Coding/pubg_reporting/pubg.db'

pubgdb = PUBGDatabaseConnector(db_uri, echo=True)
Base.metadata.create_all(pubgdb.engine)


config = json.load(open('config.json'))

api = pubg_api(config)

api.get_players()
pubgdb.insert_players(api.players)

api.get_matches()
pubgdb.insert_matches(api.matches)

pubgdb.insert_player_matches(api.players)
