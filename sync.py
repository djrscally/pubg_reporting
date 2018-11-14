from database.pubg_reporting_database import pubg_database
from pubg.pubg_api import pubg_api
import json


config = json.load(open('config.json'))

pdb = pubg_database(config)
