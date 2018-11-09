import requests
import json

# Load the config file
config = json.load(open('config.json'))

# Build the authorization headers so the API will accept our calls. Also define
# the base URL for the api

headers = {
    'Authorization':config['api_key'],
    'Accept':'application/vnd.api+json'
}

base_url = 'https://api.pubg.com/shards/{0}'.format(config['shard'])

# And make an iterator of the player names to search
player_names = config['players']

def get_players(player_names=player_names, headers=headers):
    module = '/players'
    payload = {'filter[playerNames]':player_names
    }
    r = requests.get(base_url + module,
                    headers=headers,
                    params=payload)

    return r.json()

#%%

p = get_players()

#%%
p
#%%

import mysql.connector as mariadb
db_user = config['db_user']
db_pw = config['db_pw']
db_host = config['db_host']
db_name = config['db_name']

mdb = mariadb.connect(user=db_user, password=db_pw, database=db_name)
cursor = mdb.cursor()
