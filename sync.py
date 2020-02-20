from sqlalchemy import create_engine
from database.model import Base, Player
from database.api import PUBGDatabaseConnector
from pubg.pubg_api import pubg_api
import json
import pymysql
import os
import click
import logging

@click.command()
@click.option(
    '--log-level',
    'loglevel',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
    default='Warning',
    help='Level of detail to include in logs')
def sync(loglevel):

    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(filename='sync.log', filemode='w', level=numeric_level)

    user = os.environ.get('PUBGDB_USERNAME')
    password = os.environ.get('PUBGDB_PASSWORD')
    host = os.environ.get('PUBGDB_HOST')
    database = os.environ.get('PUBGDB_DATABASE')

    db_uri = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, database)
    #db_uri = 'sqlite:///:memory:'

    pubgdb = PUBGDatabaseConnector(db_uri, echo=True)
    Base.metadata.create_all(pubgdb.engine)

    config = json.load(open(os.environ.get('PUBGDB_CONFIG_PATH') + 'config.json'))
    api = pubg_api(config)

    __sync(api, pubgdb)

def __sync(api, pubgdb):
    logging.debug("Beginning get_players() call")
    api.get_players()
    logging.debug("Completed get_players() call")
    pubgdb.upsert_players(api.players)

    api.get_seasons()
    pubgdb.upsert_seasons(api.seasons)

    api.get_matches()
    pubgdb.upsert_matches(api.matches)

    pubgdb.upsert_player_matches(api.players)
    print("""
    ============= Player Match Stats Start ===============
    """)
    pubgdb.upsert_player_match_stats(api.matches, api.players)

    api.get_player_season_stats()
    pubgdb.upsert_player_season_stats(api.player_season_stats)
    pubgdb.upsert_season_matches(api.player_season_stats)

    api.get_player_lifetime_stats()
    pubgdb.upsert_player_lifetime_stats(api.player_lifetime_stats)

if __name__=='__main__':

    sync()
