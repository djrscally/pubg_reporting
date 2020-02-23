from sqlalchemy import create_engine
from database.model import Base, Player, PlayerSeasonStats
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
    logging.basicConfig(filename='sync.log', filemode='w', level=numeric_level, format='%(asctime)s:%(levelname)s:%(message)s')

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

    # Player_season_stats is disgustingly slow, so we need to only make calls for
    # the current season and for expired seasons that don't already exist.

    sess = pubgdb.Session()

    # Get the current season, and add in a player-season combo for all players for the
    # current season to the process list
    current_season_id = api.get_current_season()[0]['id']

    process_me = []
    process_me += [(p['id'], current_season_id) for p in api.players]

    # Build a list of player-seasons to check, meaning every possible combo where isCurrentSeason is false
    check_me = [(p['id'], s['id']) for p in api.players for s in [s for s in api.seasons if not s['attributes']['isCurrentSeason']]]
    
    # For each of those possibilities, check if data exist already
    for combo in check_me:
        q = sess.query(PlayerSeasonStats).filter_by(player_id=combo[0], season_id=combo[1])
        # If so, skip it
        if sess.query(q.exists()).one()[0]:
            continue
        # Otherwise, add to the list of things to process
        else:
            process_me.append(combo)

    # Do the actual processing
    for combo in process_me:
        api.get_player_season_stats(combo)

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
