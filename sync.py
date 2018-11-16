from database.pubg_reporting_database import pubg_database
from pubg.pubg_api import pubg_api
import json


config = json.load(open('config.json'))

pdb = pubg_database(config)

api = pubg_api(config)

api.get_seasons()

api.get_players()

api.get_matches()

api.get_player_lifetime_stats()

api.get_player_season_stats()

pdb.flush_db()

pdb.insert_players(api.players)

pdb.insert_matches(api.matches)

pdb.insert_seasons(api.seasons)

pdb.insert_player_matches(api.players)

pdb.insert_player_season_stats(api.player_season_stats)

pdb.insert_player_lifetime_stats(api.player_lifetime_stats)

# TODO: Insert season_matches
#%%
pdb.disconnect()
