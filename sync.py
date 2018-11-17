from database.pubg_reporting_database import pubg_database
from pubg.pubg_api import pubg_api
import json

print("Loading config...")
config = json.load(open('config.json'))

print("Initialising database and api classes")
try:
    pdb = pubg_database(config)
except Exception as e:
    print("Error initialising database: ", e)

try:
    api = pubg_api(config)
except Exception as e:
    print("Error initialising api:",  e)

try:
    print("------ Beginning GET block ------")
    print("Fetching seasons...")
    api.get_seasons()
    print("Fetching players...")
    api.get_players()
    print("Fetching matches...")
    api.get_matches()
    print("Fetching player\'s lifetime stats...")
    api.get_player_lifetime_stats()
    print("Fetching player\'s season stats...")
    api.get_player_season_stats()

except Exception as e:
    print("Error fetching data from the API: ", e)

try:
    print("------ Flushing Database ------")
    pdb.flush_db()
    print("------ Beginning INSERT block ------")
    print("Inserting players...")
    pdb.insert_players(api.players)
    print("Inserting matches...")
    pdb.insert_matches(api.matches)
    print("Inserting seasons...")
    pdb.insert_seasons(api.seasons)
    print("Inserting player\'s matches...")
    pdb.insert_player_matches(api.players)
    print("Inserting player\'s season stats...")
    pdb.insert_player_season_stats(api.player_season_stats)
    print("Inserting player\'s lifetime stats...")
    pdb.insert_player_lifetime_stats(api.player_lifetime_stats)
except Exception as e:
    print("Error inserting data to the database: ", e)

# Exit nicely, no matter what.
pdb.disconnect()
