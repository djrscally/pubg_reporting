from sqlalchemy import create_engine
from database.model import Base, Player, PlayerSeasonStats, Match, SystemInformation
from database.api import PUBGDatabaseConnector
from pubg.pubg_api import pubg_api
import json
import datetime
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
    '--echo',
    'echo',
    is_flag=True,
    help='Echo SQL Alchemy output to stdout'
)
@click.option(
    '--build-only',
    'buildonly',
    is_flag=True,
    help='Set flag to only build the database structure but not perform a sync'
)
def sync(loglevel, echo, buildonly):

    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(filename='sync.log', filemode='w', level=numeric_level, format='%(asctime)s:%(levelname)s:%(message)s')
    # Turn SQL Alchemy logging to the entered value
    logging.getLogger('sqlalchemy.engine').setLevel(logging.getLevelName(loglevel))
    

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

    if not buildonly:
        __sync(api, pubgdb)

def __sync(api, pubgdb):
    logging.info("Beginning sync run")

    # Get the last sync datetime, for use later on. Check that this isn't the first sync
    # and if it is, treat the current time as the last_sync time
    sess = pubgdb.Session()
    
    q = sess.query(SystemInformation).filter_by(key="Last Sync Datetime").one_or_none()
    if q is None:
        last_sync_datetime = datetime.datetime.now()
        logging.debug("Last Sync Datetime not found in DB, setting to {0}".format(last_sync_datetime))
    else:
        last_sync_datetime = datetime.datetime.strptime(q.value, '%Y-%m-%d %H:%M:%S')
        logging.debug("Last Sync Datetime selected from DB as {0}".format(last_sync_datetime))

    logging.info("Beginning get_players() call")
    api.get_players()
    logging.info("Beginning upsert_players() call")
    pubgdb.upsert_players(api.players)

    logging.info("Beginning get_seasons() call")
    api.get_seasons()
    logging.info("Beginning upsert_seasons() call")
    pubgdb.upsert_seasons(api.seasons)

    logging.info("Beginning get_matches() call")

    # get_matches is slow because it syncs a lot. We're going to check the database
    # to only make calls for matches that we don't already hold data for (since those)
    # data will never change after the fact. Additionally, we need to make sure we 
    # only sync each match a single time.

    process_matches = []

    for player in api.players:
        for match in player['relationships']['matches']['data']:
            q = sess.query(Match).filter_by(match_id=match['id'])
            # If we already added it, or it already exists in the database
            if (match['id'] in process_matches) or (sess.query(q.exists()).one()[0]):
                continue
            else:
                process_matches.append(match['id'])

    api.get_matches(process_matches)
    logging.info("Beginning upsert_matches() call")
    pubgdb.upsert_matches(api.matches)

    logging.info("Beginning upsert_player_matches() call")
    pubgdb.upsert_player_matches(api.players)
    logging.info("Beginning upsert_player_match_stats() call")
    pubgdb.upsert_player_match_stats(api.matches, api.players)

    logging.info("Beginning get_player_season_stats() call")

    # Player_season_stats and lifetime_stats are disgustingly slow due to rate limited endpoints,
    # so we need to only make calls for the current season and for expired seasons that don't already exist as
    # well as only for players who've played a match since the last sync.

    # First, build a table of when matches were played

    match_datetimes = [{match['data']['id']:datetime.datetime.strptime(match['data']['attributes']['createdAt'][:-2],'%Y-%m-%dT%H:%M:%S')} for match in api.matches]

    # Next, build a list of players who've played since the last sync
    # [season for season in self.seasons if season['attributes']['isCurrentSeason']]
    
    process_players = [p['id'] for p in api.players if max([match_datetimes[m['id']] for m in p['relationships']['matches']['data']]) >= last_sync_datetime]
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

    # Update the last updated time in the db. Remember to check that it 
    # exists first (to avoid writing upsert logic...)
    q = sess.query(SystemInformation).filter_by(key='Last Sync Datetime').one_or_none()
    if q is not None:
        q.update({SystemInformation.value:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    else:
        lsdt = SystemInformation(key='Last Sync Datetime', value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sess.add(lsdt)

    sess.commit()

    logging.info("Sync run complete")

if __name__=='__main__':

    sync()
