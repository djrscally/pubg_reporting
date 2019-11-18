"""
Utility to build the config.json file for people so they don't have to make
it themselves.
"""

import json
import getpass

def buildconfig():

	# First we'll collect the info we need to generate the config

	dbhost = input('Enter the Database host (probably localhost): ')
	dbuser = input('Enter the Database user: ')
	dbpass = getpass.getpass('Enter the Database password: ')
	shard = input('Enter the PUBG shard you play in: ')
	api_key = input('Paste in your PUBG API key: ')

	players = []

	# Players is a little complex as there could be any number. We'll do a simple
	# while loop to check if the person running the script is done adding their
	# players or whether to continue.

	players.append(input('Enter the first player\'s name: '))

	more_players = input('Are there any more players to add? (y/n): ')

	while more_players == "y":
		players.append(input('Enter the next player\'s name: '))
		more_players = input('Are there any more players to add? (y/n): ')

	# Info collected so we just build the json

	config = {}

	config['players'] = players
	config['api_key'] = api_key
	config['db_host'] = dbhost
	config['db_name'] = 'pubg_reporting'
	config['db_un'] = dbuser
	config['db_pw'] = dbpass
	config['shard'] = shard

	# And write it to file, job done.

	f = open('config.json','w')
	f.write(json.dumps(config, indent=4))

	print('Config file created successfully')

	return None

buildconfig()
