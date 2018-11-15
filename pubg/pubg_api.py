import requests
import json
import mysql.connector as mysql

# Load the config file
config = json.load(open('config.json'))

# Build the authorization headers so the API will accept our calls. Also define
# the base URL for the api

headers = {
    'Authorization': config['api_key'],
    'Accept': 'application/vnd.api+json'
}

base_url = 'https://api.pubg.com/shards/{0}'.format(config['shard'])

class pubg_api:

    self.matches = []
    self.matches_json = []

    def __init__(self, config):
        self.headers = {
            'Authorization': config['api_key'],
            'Accept': 'application/vnd.api+json'
        }

        self.base_url = 'https://api.pubg.com/shards/{0}'.format(
            config['shard']
        )

        self.players = config['players']

        return None

    def get_players_and_matches(self):

        module = '/players'
        payload = {'filter[playerNames]': ','.join(self.players)
        }

        r = requests.get(
            base_url + module,
            headers=self.headers,
            params=payload
            )

        for player in r.json()['data']:
            for match in player['relationships']['matches']['data']:
                if match['id'] in matches:
                    continue
                else:
                    self.matches.append(match['id'])
                    self.matches_json.append(self.get_match(match['id']))

        return r.json()

    def get_match(self, match_id):

        module = '/matches/{0}'.format(match_id)

        r = requests.get(
            base_url + module,
            headers=self.headers
        )

        return r.json()


# And make an iterator of the player names to search
player_names = config['players']

# Now build the connection to the database for the insert statements

mdb = mysql.connect(
    host=config['db_host'],
    user=config['db_un'],
    password=config['db_pw'],
    database=config['db_name']
    )

cursor = mdb.cursor()


def get_players(player_names=player_names, headers=headers):

    module = '/players'
    players = ','.join(player_names)
    payload = {'filter[playerNames]': players
    }

    r = requests.get(
        base_url + module,
        headers=headers,
        params=payload
        )

    return r.json()


def get_match(match_id, headers=headers):

    module = '/matches/{0}'.format(match_id)

    r = requests.get(
        base_url + module,
        headers=headers
    )

    return r.json()

def insert_players(players, cursor):
    """
    Drop all the players into the players table.
    """

    for player in players['data']:
        cursor.execute('insert into players\
                        values (\
                            %s,\
                            %s,\
                            %s);', (
                                player['id'],
                                player['attributes']['name'],
                                player['attributes']['shardId']
                                ))

    return None

def insert_matches(players, cursor):
    """
    Because of the way the API is structured, this actually inserts data
    to both the matches and player_matches tables. Matches first otherwise
    the foreign keys will get upset, and we wouldn't want that now would we?
    """

    matches = []

    for player in players['data']:
        for match in player['relationships']['matches']['data']:

            if match['id'] in matches:
                continue
            else:
                m = get_match(match['id'])
                cursor.execute('insert into matches\
                                values (\
                                    %s,\
                                    %s,\
                                    %s,\
                                    %s,\
                                    %s,\
                                    %s,\
                                    %s,\
                                    %s);', (
                                        match['id'],
                                        m['data']['attributes']['createdAt'][:-2],
                                        m['data']['attributes']['duration'],
                                        m['data']['attributes']['gameMode'],
                                        m['data']['attributes']['mapName'],
                                        m['data']['attributes']['isCustomMatch'],
                                        m['data']['attributes']['seasonState'],
                                        m['data']['attributes']['shardId']
                                    )
                                )
                print(cursor.statement)
                mdb.commit()
                matches.append(match['id'])

            try:
                cursor.execute('insert into player_matches (player_id, match_id)\
                    values (\
                    %s,\
                    %s);', (player['id'], match['id'])
                )
            except:
                print(cursor.statement)
                raise

    return None
"""

#%%
p = get_players()

#%%

insert_players(p, cursor)

#%%
insert_matches(p, cursor)
#%%
mdb.close()
#%%
# Let's drop the players into the database.
insert_players(
    get_players(
        player_names,
        headers
    ),
    cursor
)

mdb.commit()
mdb.close()
"""
