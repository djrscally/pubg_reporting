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
    default='WARNING',
    help='Level of detail to include in logs')
@click.option(
    '--echo/--no-echo',
    'echo',
    default=False,
    help='Echo SQL Alchemy output to stdout'
)
def sync(loglevel, echo):

    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(filename='sync.log', filemode='w', level=numeric_level)

    user = os.environ.get('PUBGDB_USERNAME')
    password = os.environ.get('PUBGDB_PASSWORD')
    host = os.environ.get('PUBGDB_HOST')
    database = os.environ.get('PUBGDB_DATABASE')

    db_uri = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, database)
    #db_uri = 'sqlite:///:memory:'

    pubgdb = PUBGDatabaseConnector(db_uri, echo)
    Base.metadata.create_all(pubgdb.engine)

    config = json.load(open(os.environ.get('PUBGDB_CONFIG_PATH') + 'config.json'))
    api = pubg_api(config)

    __sync(api, pubgdb)

def __sync(api, pubgdb):
    logging.info("Beginning sync run")

    logging.info("Beginning get_players() call")
    api.get_players()
    logging.info("Beginning upsert_players() call")
    pubgdb.upsert_players(api.players)

    logging.info("Beginning get_seasons() call")
    api.get_seasons()
    logging.info("Beginning upsert_seasons() call")
    pubgdb.upsert_seasons(api.seasons)

    logging.info("Beginning get_matches() call")
    api.get_matches()
    logging.info("Beginning upsert_matches() call")
    pubgdb.upsert_matches(api.matches)

    logging.info("Beginning upsert_player_matches() call")
    pubgdb.upsert_player_matches(api.players)
    logging.info("Beginning upsert_player_match_stats() call")
    pubgdb.upsert_player_match_stats(api.matches, api.players)

    logging.info("Beginning get_player_season_stats() call")
    api.get_player_season_stats()
    logging.info("Beginning upsert_player_season_stats() call")
    pubgdb.upsert_player_season_stats(api.player_season_stats)
    logging.info("Beginning upsert_season_matches() call")
    pubgdb.upsert_season_matches(api.player_season_stats)

    logging.info("Beginning get_player_lifetime_stats() call")
    api.get_player_lifetime_stats()
    logging.info("Beginning upsert_player_lifetime_stats() call")
    pubgdb.upsert_player_lifetime_stats(api.player_lifetime_stats)

    logging.info("Sync run complete")

if __name__=='__main__':

    sync()
