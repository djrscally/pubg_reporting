"""
Class to manage the connection and transactional functions for the MySQL
database.
"""

from .model import Player, Match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

class PUBGDatabaseConnector:

    def __init__(self, engine_uri, echo=False):
        """
        Define connection parameters for the MySQL connection, and that's
        more or less it.
        """

        self.engine = create_engine(engine_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)

        return None

    def flush_db(self):

        cursor = self.connect()

        cursor.execute(
            'call pFlushData;'
        )

        self.commit()
        self.disconnect()

        return None

    def insert_players(self, players):
        """
        Drop all the players into the players table.
        """

        session = self.Session()

        session.add_all(
            [Player(
                player_id=player['id'],
                player_name=player['attributes']['name'],
                shard_id=player['attributes']['shardId']
            ) for player in players]
        )

        session.commit()

        return True

    def insert_matches(self, matches):
        """
        Takes matches from the API output and adds them as Match() objects to
        the ORM.
        """

        session = self.Session()

        session.add_all(
            [Match(
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
            ) for match in matches]
        )

        session.commit()

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

    def insert_seasons(self, seasons):

        cursor = self.connect()

        for season in seasons:
            cursor.execute(
                'insert into seasons values (%s, %s, %s);',
                (
                    season['id'],
                    season['attributes']['isCurrentSeason'],
                    season['attributes']['isOffseason']
                )
            )

        self.commit()
        self.disconnect()

        return True

    def select_season_updated_on(self):
        """
        This fetches the date the season was last updated from the databases
        administration table, just so we can check if it's less than a month
        old to avoid angering the API people.
        """

        return None

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
