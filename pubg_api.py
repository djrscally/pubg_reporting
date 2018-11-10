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
    payload = {'filter[playerNames]': player_names
    }

    r = requests.get(
        base_url + module,
        headers=headers,
        params=payload
        )

    return r.json()


def insert_players(players, cursor):

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
