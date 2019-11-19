"""
Class to manage the connection and transactional functions for the MySQL
database.
"""

from .model import Player, Match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from .model import Player, Match, Season
from sqlalchemy.dialects.mysql import insert

class PUBGDatabaseConnector:

    def __init__(self, engine_uri, echo=False):
        """
        Define connection parameters for the MySQL connection, and that's
        more or less it.
        """

        self.engine = create_engine(engine_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)

        return None

    def upsert_players(self, players):
        """
        Inserts or Updates Players
        """

        conn = self.engine.connect()
        trans = conn.begin()

        try:
            for player in players:
                insert_stmt = insert(Player).values(
                    player_id=player['id'],
                    player_name=player['attributes']['name'],
                    shard_id=player['attributes']['shardId']
                )

                merge_stmt = insert_stmt.on_duplicate_key_update(
                    player_id=insert_stmt.inserted.player_id,
                    player_name=insert_stmt.inserted.player_name,
                    shard_id=insert_stmt.inserted.shard_id,
                    status='U'
                )

                conn.execute(merge_stmt)
            trans.commit()
        except:
            trans.rollback()

        conn.close()

        return True

    def upsert_matches(self, matches):
        """
        Takes matches from the API output and adds them as Match() objects to
        the ORM.
        """

        conn = self.engine.connect()
        trans = conn.begin()

        try:
            for match in matches:
                insert_stmt = insert(Match).values(
                    match_id=match['id'],
                    createdAt=datetime.datetime.strptime(
                        match['attributes']['createdAt'][:-2],
                        '%Y-%m-%dT%H:%M:%S'
                    ),
                    duration=match['attributes']['duration'],
                    gameMode=match['attributes']['gameMode'],
                    mapName=match['attributes']['mapName'],
                    isCustomMatch=match['attributes']['isCustomMatch'],
                    seasonState=match['attributes']['seasonState'],
                    shardId=match['attributes']['shardId']
                )

                merge_stmt = insert_stmt.on_duplicate_key_update(
                    match_id=insert_stmt.inserted.match_id,
                    createdAt=insert_stmt.inserted.createdAt,
                    duration=insert_stmt.inserted.duration,
                    gameMode=insert_stmt.inserted.gameMode,
                    mapName=insert_stmt.inserted.mapName,
                    isCustomMatch=insert_stmt.inserted.isCustomMatch,
                    seasonState=insert_stmt.inserted.seasonState,
                    shardId=insert_stmt.inserted.shardId
                )

                conn.execute(merge_stmt)
            trans.commit()
        except:
            trans.rollback()

        conn.close()

        return True

    def insert_player_matches(self, players):
        """
        Drops the link between players and matches into the association table.
        """

        session = self.Session()

        for player in players:
            for match in player['relationships']['matches']['data']:


                cursor.execute(
                    'insert into player_matches (player_id, match_id)\
                    values (%s, %s);',
                    (player['id'], match['id'])
                )
        self.commit()
        self.disconnect()

        return True

    def upsert_seasons(self, seasons):
        """
        Insert season data
        """

        conn = self.engine.connect()
        trans = conn.begin()

        try:
            for season in seasons:
                insert_stmt = insert(Season).values(
                    season_id=season['id'],
                    is_current_season=season['attributes']['isCurrentSeason'],
                    is_off_season=season['attributes']['isOffseason']
                )

                merge_stmt = insert_stmt.on_duplicate_key_update(
                    season_id=insert_stmt.inserted.season_id,
                    is_current_season=insert_stmt.inserted.is_current_season,
                    is_off_season=insert_stmt.inserted.is_off_season
                )

                conn.execute(merge_stmt)
            trans.commit()
        except:
            trans.rollback()

        conn.close()

        return True

    def insert_player_season_stats(self, player_season_stats):
        """
        The SQL Statement here is irritatingly long-ass but it's a big table
        and I don't know how else to let the season_stats_id primary key do its
        auto-increment thing so "ASCII SHRUG"
        """

        cursor = self.connect()

        for player_season in player_season_stats:
            for game_mode in player_season['attributes']['gameModeStats'].keys():
                cursor.execute(
                    'insert into player_season_stats \
                        (\
                            season_id\
                            , player_id\
                            , game_mode\
                            , assists\
                            , bestRankPoint\
                            , boosts\
                            , dBNOs\
                            , dailyKills\
                            , damageDealt\
                            , days\
                            , dailyWins\
                            , headshotKills\
                            , heals\
                            , killPoints\
                            , kills\
                            , longestKill\
                            , longestTimeSurvived\
                            , losses\
                            , maxKillStreaks\
                            , mostSurvivalTime\
                            , rankPoints\
                            , revives\
                            , rideDistance\
                            , roadKills\
                            , roundMostKills\
                            , roundsPlayed\
                            , suicides\
                            , swimDistance\
                            , teamKills\
                            , timeSurvived\
                            , top10s\
                            , vehicleDestroys\
                            , walkDistance\
                            , weaponsAcquired\
                            , weeklyKills\
                            , weeklyWins\
                            , winPoints\
                            , wins\
                        ) values (\
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                            , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                            , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                            , %s\
                        );', (
                            player_season['relationships']['season']['data']['id'],
                            player_season['relationships']['player']['data']['id'],
                            game_mode,
                            player_season['attributes']['gameModeStats'][game_mode]['assists'],
                            player_season['attributes']['gameModeStats'][game_mode]['bestRankPoint'],
                            player_season['attributes']['gameModeStats'][game_mode]['boosts'],
                            player_season['attributes']['gameModeStats'][game_mode]['dBNOs'],
                            player_season['attributes']['gameModeStats'][game_mode]['dailyKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['damageDealt'],
                            player_season['attributes']['gameModeStats'][game_mode]['days'],
                            player_season['attributes']['gameModeStats'][game_mode]['dailyWins'],
                            player_season['attributes']['gameModeStats'][game_mode]['headshotKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['heals'],
                            player_season['attributes']['gameModeStats'][game_mode]['killPoints'],
                            player_season['attributes']['gameModeStats'][game_mode]['kills'],
                            player_season['attributes']['gameModeStats'][game_mode]['longestKill'],
                            player_season['attributes']['gameModeStats'][game_mode]['longestTimeSurvived'],
                            player_season['attributes']['gameModeStats'][game_mode]['losses'],
                            player_season['attributes']['gameModeStats'][game_mode]['maxKillStreaks'],
                            player_season['attributes']['gameModeStats'][game_mode]['mostSurvivalTime'],
                            player_season['attributes']['gameModeStats'][game_mode]['rankPoints'],
                            player_season['attributes']['gameModeStats'][game_mode]['revives'],
                            player_season['attributes']['gameModeStats'][game_mode]['rideDistance'],
                            player_season['attributes']['gameModeStats'][game_mode]['roadKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['roundMostKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['roundsPlayed'],
                            player_season['attributes']['gameModeStats'][game_mode]['suicides'],
                            player_season['attributes']['gameModeStats'][game_mode]['swimDistance'],
                            player_season['attributes']['gameModeStats'][game_mode]['teamKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['timeSurvived'],
                            player_season['attributes']['gameModeStats'][game_mode]['top10s'],
                            player_season['attributes']['gameModeStats'][game_mode]['vehicleDestroys'],
                            player_season['attributes']['gameModeStats'][game_mode]['walkDistance'],
                            player_season['attributes']['gameModeStats'][game_mode]['weaponsAcquired'],
                            player_season['attributes']['gameModeStats'][game_mode]['weeklyKills'],
                            player_season['attributes']['gameModeStats'][game_mode]['weeklyWins'],
                            player_season['attributes']['gameModeStats'][game_mode]['winPoints'],
                            player_season['attributes']['gameModeStats'][game_mode]['wins']
                        )
                )
                self.commit()
        self.disconnect()

        return None

    def insert_player_lifetime_stats(self, player_lifetime_stats):

        cursor = self.connect()

        for lifetime_stats in player_lifetime_stats:
            for game_mode in lifetime_stats['attributes']['gameModeStats'].keys():
                try:
                    cursor.execute(
                        'insert into player_lifetime_stats \
                            (\
                                player_id\
                                , game_mode\
                                , assists\
                                , bestRankPoint\
                                , boosts\
                                , dBNOs\
                                , dailyKills\
                                , damageDealt\
                                , days\
                                , dailyWins\
                                , headshotKills\
                                , heals\
                                , killPoints\
                                , kills\
                                , longestKill\
                                , longestTimeSurvived\
                                , losses\
                                , maxKillStreaks\
                                , mostSurvivalTime\
                                , rankPoints\
                                , revives\
                                , rideDistance\
                                , roadKills\
                                , roundMostKills\
                                , roundsPlayed\
                                , suicides\
                                , swimDistance\
                                , teamKills\
                                , timeSurvived\
                                , top10s\
                                , vehicleDestroys\
                                , walkDistance\
                                , weaponsAcquired\
                                , weeklyKills\
                                , weeklyWins\
                                , winPoints\
                                , wins\
                                ) values (\
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                                , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                                , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
                                , %s\
                                );', (
                                lifetime_stats['relationships']['player']['data']['id'],
                                game_mode,
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['assists'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['bestRankPoint'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['boosts'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['dBNOs'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['dailyKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['damageDealt'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['days'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['dailyWins'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['headshotKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['heals'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['killPoints'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['kills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['longestKill'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['longestTimeSurvived'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['losses'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['maxKillStreaks'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['mostSurvivalTime'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['rankPoints'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['revives'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['rideDistance'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['roadKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['roundMostKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['roundsPlayed'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['suicides'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['swimDistance'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['teamKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['timeSurvived'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['top10s'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['vehicleDestroys'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['walkDistance'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['weaponsAcquired'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['weeklyKills'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['weeklyWins'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['winPoints'],
                                lifetime_stats['attributes']['gameModeStats'][game_mode]['wins']
                                )
                            )
                except Exception as e:
                    print(cursor.statement)
                    print(e)
        self.commit()
        self.disconnect()

        return None
