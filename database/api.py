"""
Class to manage the connection and transactional functions for the MySQL
database.
"""

from .model import Player, Match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from .model import\
    Player\
    , Match\
    , Season\
    , PlayerMatches\
    , PlayerSeasonStats\
    , PlayerLifetimeStats
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

    def upsert_player_matches(self, players):
        """
        Drops the link between players and matches into the association table.
        """

        conn = self.engine.connect()
        trans = conn.begin()

        try:
            for player in players:
                for match in player['relationships']['matches']['data']:
                    insert_stmt = insert(PlayerMatches).values(
                        player_id=player['id'],
                        match_id=match['id']
                    )

                    merge_stmt = insert_stmt.on_duplicate_key_update(
                        player_id=insert_stmt.inserted.player_id,
                        match_id=insert_stmt.inserted.match_id
                    )

                    conn.execute(merge_stmt)

            trans.commit()
        except:
            trans.rollback()

        conn.close()

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

    def upsert_player_season_stats(self, player_season_stats):
        """
        The SQL Statement here is irritatingly long-ass but it's a big table
        and I don't know how else to let the season_stats_id primary key do its
        auto-increment thing so "ASCII SHRUG"
        """

        conn = self.engine.connect()
    #    trans = conn.begin()

        try:
            for player_season in player_season_stats:
                for game_mode in player_season['attributes']['gameModeStats'].keys():
                    trans = conn.begin()
                    insert_stmt = insert(PlayerSeasonStats).values(
                        player_id=player_season['relationships']['player']['data']['id'],
                        season_id=player_season['relationships']['season']['data']['id'],
                        game_mode=game_mode,
                        assists=player_season['attributes']['gameModeStats'][game_mode]['assists'],
#                        bestRankPoint=player_season['attributes']['gameModeStats'][game_mode]['bestRankPoint'],
                        boosts=player_season['attributes']['gameModeStats'][game_mode]['boosts'],
                        dBNOs=player_season['attributes']['gameModeStats'][game_mode]['dBNOs'],
                        dailyKills=player_season['attributes']['gameModeStats'][game_mode]['dailyKills'],
                        damageDealt=player_season['attributes']['gameModeStats'][game_mode]['damageDealt'],
                        days=player_season['attributes']['gameModeStats'][game_mode]['days'],
                        dailyWins=player_season['attributes']['gameModeStats'][game_mode]['dailyWins'],
                        headshotKills=player_season['attributes']['gameModeStats'][game_mode]['headshotKills'],
                        heals=player_season['attributes']['gameModeStats'][game_mode]['heals'],
                        killPoints=player_season['attributes']['gameModeStats'][game_mode]['killPoints'],
                        kills=player_season['attributes']['gameModeStats'][game_mode]['kills'],
                        longestKill=player_season['attributes']['gameModeStats'][game_mode]['longestKill'],
                        longestTimeSurvived=player_season['attributes']['gameModeStats'][game_mode]['longestTimeSurvived'],
                        losses=player_season['attributes']['gameModeStats'][game_mode]['losses'],
                        maxKillStreaks=player_season['attributes']['gameModeStats'][game_mode]['maxKillStreaks'],
                        mostSurvivalTime=player_season['attributes']['gameModeStats'][game_mode]['mostSurvivalTime'],
                        rankPoints=player_season['attributes']['gameModeStats'][game_mode]['rankPoints'],
                        revives=player_season['attributes']['gameModeStats'][game_mode]['revives'],
                        rideDistance=player_season['attributes']['gameModeStats'][game_mode]['rideDistance'],
                        roadKills=player_season['attributes']['gameModeStats'][game_mode]['roadKills'],
                        roundMostKills=player_season['attributes']['gameModeStats'][game_mode]['roundMostKills'],
                        roundsPlayed=player_season['attributes']['gameModeStats'][game_mode]['roundsPlayed'],
                        suicides=player_season['attributes']['gameModeStats'][game_mode]['suicides'],
                        swimDistance=player_season['attributes']['gameModeStats'][game_mode]['swimDistance'],
                        teamKills=player_season['attributes']['gameModeStats'][game_mode]['teamKills'],
                        timeSurvived=player_season['attributes']['gameModeStats'][game_mode]['timeSurvived'],
                        top10s=player_season['attributes']['gameModeStats'][game_mode]['top10s'],
                        vehicleDestroys=player_season['attributes']['gameModeStats'][game_mode]['vehicleDestroys'],
                        walkDistance=player_season['attributes']['gameModeStats'][game_mode]['walkDistance'],
                        weaponsAcquired=player_season['attributes']['gameModeStats'][game_mode]['weaponsAcquired'],
                        weeklyKills=player_season['attributes']['gameModeStats'][game_mode]['weeklyKills'],
                        weeklyWins=player_season['attributes']['gameModeStats'][game_mode]['weeklyWins'],
                        winPoints=player_season['attributes']['gameModeStats'][game_mode]['winPoints'],
                        wins=player_season['attributes']['gameModeStats'][game_mode]['wins']
                    )

                    merge_stmt = insert_stmt.on_duplicate_key_update(
#                        player_id=insert_stmt.inserted.player_id,
#                        season_id=insert_stmt.inserted.season_id,
#                        game_mode=insert_stmt.inserted.game_mode,
                        assists=insert_stmt.inserted.assists,
#                        bestRankPoint=insert_stmt.inserted.bestRankPoint,
                        boosts=insert_stmt.inserted.boosts,
                        dBNOs=insert_stmt.inserted.dBNOs,
                        dailyKills=insert_stmt.inserted.dailyKills,
                        damageDealt=insert_stmt.inserted.damageDealt,
                        days=insert_stmt.inserted.days,
                        dailyWins=insert_stmt.inserted.dailyWins,
                        headshotKills=insert_stmt.inserted.headshotKills,
                        heals=insert_stmt.inserted.heals,
                        killPoints=insert_stmt.inserted.killPoints,
                        kills=insert_stmt.inserted.kills,
                        longestKill=insert_stmt.inserted.longestKill,
                        longestTimeSurvived=insert_stmt.inserted.longestTimeSurvived,
                        losses=insert_stmt.inserted.losses,
                        maxKillStreaks=insert_stmt.inserted.maxKillStreaks,
                        mostSurvivalTime=insert_stmt.inserted.mostSurvivalTime,
                        rankPoints=insert_stmt.inserted.rankPoints,
                        revives=insert_stmt.inserted.revives,
                        rideDistance=insert_stmt.inserted.rideDistance,
                        roadKills=insert_stmt.inserted.roadKills,
                        roundMostKills=insert_stmt.inserted.roundMostKills,
                        roundsPlayed=insert_stmt.inserted.roundsPlayed,
                        suicides=insert_stmt.inserted.suicides,
                        swimDistance=insert_stmt.inserted.swimDistance,
                        teamKills=insert_stmt.inserted.teamKills,
                        timeSurvived=insert_stmt.inserted.timeSurvived,
                        top10s=insert_stmt.inserted.top10s,
                        vehicleDestroys=insert_stmt.inserted.vehicleDestroys,
                        walkDistance=insert_stmt.inserted.walkDistance,
                        weaponsAcquired=insert_stmt.inserted.weaponsAcquired,
                        weeklyKills=insert_stmt.inserted.weeklyKills,
                        weeklyWins=insert_stmt.inserted.weeklyWins,
                        winPoints=insert_stmt.inserted.winPoints,
                        wins=insert_stmt.inserted.wins
                    )

                    conn.execute(merge_stmt)
                    trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()

        conn.close()

        return True

    def upsert_player_lifetime_stats(self, player_lifetime_stats):

        conn = self.engine.connect()
        trans = conn.begin()

        try:
            for lifetime_stats in player_lifetime_stats:
                for game_mode in lifetime_stats['attributes']['gameModeStats'].keys():
                    insert_stmt = insert(PlayerLifetimeStats).values(
                        player_id=lifetime_stats['relationships']['player']['data']['id'],
                        game_mode=game_mode,
                        assists=lifetime_stats['attributes']['gameModeStats'][game_mode]['assists'],
                        boosts=lifetime_stats['attributes']['gameModeStats'][game_mode]['boosts'],
                        dBNOs=lifetime_stats['attributes']['gameModeStats'][game_mode]['dBNOs'],
                        dailyKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['dailyKills'],
                        damageDealt=lifetime_stats['attributes']['gameModeStats'][game_mode]['damageDealt'],
                        days=lifetime_stats['attributes']['gameModeStats'][game_mode]['days'],
                        dailyWins=lifetime_stats['attributes']['gameModeStats'][game_mode]['dailyWins'],
                        headshotKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['headshotKills'],
                        heals=lifetime_stats['attributes']['gameModeStats'][game_mode]['heals'],
                        killPoints=lifetime_stats['attributes']['gameModeStats'][game_mode]['killPoints'],
                        kills=lifetime_stats['attributes']['gameModeStats'][game_mode]['kills'],
                        longestKill=lifetime_stats['attributes']['gameModeStats'][game_mode]['longestKill'],
                        longestTimeSurvived=lifetime_stats['attributes']['gameModeStats'][game_mode]['longestTimeSurvived'],
                        losses=lifetime_stats['attributes']['gameModeStats'][game_mode]['losses'],
                        maxKillStreaks=lifetime_stats['attributes']['gameModeStats'][game_mode]['maxKillStreaks'],
                        mostSurvivalTime=lifetime_stats['attributes']['gameModeStats'][game_mode]['mostSurvivalTime'],
                        rankPoints=lifetime_stats['attributes']['gameModeStats'][game_mode]['rankPoints'],
                        revives=lifetime_stats['attributes']['gameModeStats'][game_mode]['revives'],
                        rideDistance=lifetime_stats['attributes']['gameModeStats'][game_mode]['rideDistance'],
                        roadKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['roadKills'],
                        roundMostKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['roundMostKills'],
                        roundsPlayed=lifetime_stats['attributes']['gameModeStats'][game_mode]['roundsPlayed'],
                        suicides=lifetime_stats['attributes']['gameModeStats'][game_mode]['suicides'],
                        swimDistance=lifetime_stats['attributes']['gameModeStats'][game_mode]['swimDistance'],
                        teamKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['teamKills'],
                        timeSurvived=lifetime_stats['attributes']['gameModeStats'][game_mode]['timeSurvived'],
                        top10s=lifetime_stats['attributes']['gameModeStats'][game_mode]['top10s'],
                        vehicleDestroys=lifetime_stats['attributes']['gameModeStats'][game_mode]['vehicleDestroys'],
                        walkDistance=lifetime_stats['attributes']['gameModeStats'][game_mode]['walkDistance'],
                        weaponsAcquired=lifetime_stats['attributes']['gameModeStats'][game_mode]['weaponsAcquired'],
                        weeklyKills=lifetime_stats['attributes']['gameModeStats'][game_mode]['weeklyKills'],
                        weeklyWins=lifetime_stats['attributes']['gameModeStats'][game_mode]['weeklyWins'],
                        winPoints=lifetime_stats['attributes']['gameModeStats'][game_mode]['winPoints'],
                        wins=lifetime_stats['attributes']['gameModeStats'][game_mode]['wins']
                    )

                    merge_stmt = insert_stmt.on_duplicate_key_update(
                        game_mode=insert_stmt.inserted.game_mode,
                        assists=insert_stmt.inserted.assists,
                        boost=insert_stmt.inserted.boosts,
                        dBNOs=insert_stmt.inserted.dBNOs,
                        dailyKills=insert_stmt.inserted.dailyKills,
                        damageDealt=insert_stmt.inserted.damageDealt,
                        days=insert_stmt.inserted.days,
                        dailyWins=insert_stmt.inserted.dailyWins,
                        headshotKills=insert_stmt.inserted.headshotKills,
                        heals=insert_stmt.inserted.heals,
                        killPoints=insert_stmt.inserted.killPoints,
                        kills=insert_stmt.inserted.kills,
                        longestKill=insert_stmt.inserted.longestKill,
                        longestTimeSurvived=insert_stmt.inserted.longestTimeSurvived,
                        losses=insert_stmt.inserted.losses,
                        maxKillStreaks=insert_stmt.inserted.maxKillStreaks,
                        mostSurvivalTime=insert_stmt.inserted.mostSurvivalTime,
                        rankPoints=insert_stmt.inserted.rankPoints,
                        revives=insert_stmt.inserted.revives,
                        rideDistance=insert_stmt.inserted.rideDistance,
                        roadKills=insert_stmt.inserted.roadKills,
                        roundMostKills=insert_stmt.inserted.roundMostKills,
                        roundsPlayed=insert_stmt.inserted.roundsPlayed,
                        suicides=insert_stmt.inserted.suicides,
                        swimDistance=insert_stmt.inserted.swimDistance,
                        teamKills=insert_stmt.inserted.teamKills,
                        timeSurvived=insert_stmt.inserted.timeSurvived,
                        top10s=insert_stmt.inserted.top10s,
                        vehicleDestroys=insert_stmt.inserted.vehicleDestroys,
                        walkDistance=insert_stmt.inserted.walkDistance,
                        weaponsAcquired=insert_stmt.inserted.weaponsAcquired,
                        weeklyKills=insert_stmt.inserted.weeklyKills,
                        weeklyWins=insert_stmt.inserted.weeklyWins,
                        winPoints=insert_stmt.inserted.winPoints,
                        wins=insert_stmt.inserted.wins
                    )

                    conn.execute(merge_stmt)
            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()

        conn.close()

        return True
