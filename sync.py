from database.pubg_reporting_database import pubg_database
from pubg.pubg_api import pubg_api
import json


config = json.load(open('config.json'))
#%%
pdb = pubg_database(config)
#%%
api = pubg_api(config)

#%%
api.get_players()
api.get_matches()
#%%
pdb.insert_players(api.players)
#%%
pdb.insert_matches(api.matches)
#%%
pdb.insert_player_matches(api.players)
