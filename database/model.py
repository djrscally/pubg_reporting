from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import \
    Column\
    , Integer\
    , String\
    , Boolean\
    , DateTime\
    , ForeignKey\
    , Table
from sqlalchemy.orm import relationship

Base = declarative_base()

player_matches = Table(
    'player_matches',
    Base.metadata,
    Column('player_id', String, ForeignKey('players.player_id')),
    Column('match_id', String, ForeignKey('matches.match_id'))
)

season_matches = Table(
    'season_matches',
    Base.metadata,
    Column('season_id', String, ForeignKey('seasons.season_id')),
    Column('match_id', String, ForeignKey('matches.match_id'))
)

class Player(Base):
    """
    Defines the players
    """

    __tablename__ = 'players'

    player_id = Column(String, primary_key=True, nullable=False)
    player_name = Column(String, nullable=False)
    shard_id = Column(String, nullable=False)

    matches = relationship(
        'Match',
        secondary=player_matches,
        back_populates='players'
    )

    player_season_stats = relationship(
        'PlayerSeasonStats',
        back_populates='players'
    )

    def __repr__(self):
        return "<Player(player_id={0}, player_name={1})>".format(
            self.player_id,
            self.player_name
        )

class Season(Base):
    """
    Base class for Seasons, which are like a bucket of matches that are very
    inconsistent lengths. Originally once per month, then they went to much
    longer and lately semi-permanent
    """

    __tablename__ = 'seasons'

    season_id = Column(String, primary_key=True, nullable=False)
    is_current_season = Column(Boolean, nullable=False)
    is_off_season = Column(Boolean, nullable=False)

    player_season_stats = relationship('PlayerSeasonStats', back_populates='seasons')

    def __repr__(self):
        return "<Season(season_id={0})".format(self.season_id)

class Match(Base):
    """
    Base class for individual matches, details about the actual rounds
    played (although not any stats which is weird)
    """

    __tablename__ = 'matches'

    match_id = Column(String, primary_key=True, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    gameMode = Column(String, nullable=False)
    mapName = Column(String, nullable=False)
    isCustomMatch = Column(Boolean, nullable=False)
    seasonState = Column(String, nullable=False)
    shardId = Column(String, nullable=False)

    players = relationship(
        'Player',
        secondary=player_matches,
        back_populates='matches'
    )

    def __repr__(self):
        return "<Match(match_id={0}, gameMode={1}, mapName={2})".format(
            self.match_id,
            self.gameMode,
            self.mapName
        )

class PlayerSeasonStats(Base):
    """
    Stats for a single season for a player
    """

    __tablename__ = 'player_season_stats'

    season_stats_id = Column(Integer, primary_key=True, autoincrement=True)

    season_id = Column(String, ForeignKey('seasons.season_id'), nullable=False)
    seasons = relationship('Season', back_populates='seasons')

    player_id = Column(String, ForeignKey('players.player_id'), nullable=False)
    players = relationship('Player', back_populates='players')

    game_mode = Column(String, nullable=False)

    game_mode = Column(String, nullable=False)
    assists = Column(Integer, nullable=False)
    bestRankPoint = Column(Integer, nullable=False)
    boosts = Column(Integer, nullable=False)
    dBNOs = Column(Integer, nullable=False)
    dailyKills = Column(Integer, nullable=False)
    damageDealt = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    dailyWins = Column(Integer, nullable=False)
    headshotKills = Column(Integer, nullable=False)
    heals = Column(Integer, nullable=False)
    killPoints = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    longestKill = Column(Integer, nullable=False)
    longestTimeSurvived = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    maxKillStreaks = Column(Integer, nullable=False)
    mostSurvivalTime = Column(Integer, nullable=False)
    rankPoints = Column(Integer, nullable=False)
    revives = Column(Integer, nullable=False)
    rideDistance = Column(Integer, nullable=False)
    roadKills = Column(Integer, nullable=False)
    roundMostKills = Column(Integer, nullable=False)
    roundsPlayed = Column(Integer, nullable=False)
    suicides = Column(Integer, nullable=False)
    swimDistance = Column(Integer, nullable=False)
    teamKills = Column(Integer, nullable=False)
    timeSurvived = Column(Integer, nullable=False)
    top10s = Column(Integer, nullable=False)
    vehicleDestroys = Column(Integer, nullable=False)
    walkDistance = Column(Integer, nullable=False)
    weaponsAcquired = Column(Integer, nullable=False)
    weeklyKills = Column(Integer, nullable=False)
    weeklyWins = Column(Integer, nullable=False)
    winPoints = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)

    def __repr__(self):
        return "<PlayerSeasonStats(season_id={0}, player_id={1})>".format(self.season_id, self.player_id)

class PlayerLifetimeStates(Base):
    """
    Placeholder
    """

    __tablename__ = 'player_lifetime_stats'

    lifetime_stats_id = Column(Integer, primary_key=True, autoincrement=True)

    player_id = Column(String, ForeignKey('players.player_id'), nullable=False)
    players = relationship('Player', back_populates='players')

    assists = Column(Integer, nullable=False)
    bestRankPoint = Column(Integer, nullable=False)
    boosts = Column(Integer, nullable=False)
    dBNOs = Column(Integer, nullable=False)
    dailyKills = Column(Integer, nullable=False)
    damageDealt = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    dailyWins = Column(Integer, nullable=False)
    headshotKills = Column(Integer, nullable=False)
    heals = Column(Integer, nullable=False)
    killPoints = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    longestKill = Column(Integer, nullable=False)
    longestTimeSurvived = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    maxKillStreaks = Column(Integer, nullable=False)
    mostSurvivalTime = Column(Integer, nullable=False)
    rankPoints = Column(Integer, nullable=False)
    revives = Column(Integer, nullable=False)
    rideDistance = Column(Integer, nullable=False)
    roadKills = Column(Integer, nullable=False)
    roundMostKills = Column(Integer, nullable=False)
    roundsPlayed = Column(Integer, nullable=False)
    suicides = Column(Integer, nullable=False)
    swimDistance = Column(Integer, nullable=False)
    teamKills = Column(Integer, nullable=False)
    timeSurvived = Column(Integer, nullable=False)
    top10s = Column(Integer, nullable=False)
    vehicleDestroys = Column(Integer, nullable=False)
    walkDistance = Column(Integer, nullable=False)
    weaponsAcquired = Column(Integer, nullable=False)
    weeklyKills = Column(Integer, nullable=False)
    weeklyWins = Column(Integer, nullable=False)
    winPoints = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
