from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import \
    Column\
    , Integer\
    , Float\
    , String\
    , Boolean\
    , DateTime\
    , ForeignKey\
    , Table
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

class SystemInformation(Base):
    """
    Key-Value table storing metadata about the sync process
    """

    __tablename__ = 'system_information'
    key = Column(String(512), primary_key=True)
    value = Column(String(512))

    def __repr__(self):
        return "<SystemInformation(key={0}, value={1})>".format(self.key, self.value)

class SyncPlayers(Base):
    """
    Manually administered table that defines which player-shards to sync.
    Users enter player IGNs and shards here and the script syncs their data
    """

    __tablename__ = 'sync_players'

    player_ign = Column(String(256), primary_key=True)
    shard = Column(String(32), primary_key=True)

    def __repr__(self):
        return "<SyncPlayers(player_ign={0}, shard={1})>".format(player_ign, shard)

class PlayerMatches(Base):
    """
    Association table linking players to the matches they have played in
    """

    __tablename__ = 'player_matches'

    player_id = Column(String(256), ForeignKey('players.player_id'), primary_key=True)
    player = relationship("Player", back_populates='matches')

    match_id = Column(String(256), ForeignKey('matches.match_id'), primary_key=True)
    match = relationship("Match", back_populates="players")

    def __repr__(self):
        return "<PlayerMatches(player_id={0}, match_id={1})>".format(self.player_id, self.match_id)

class SeasonMatches(Base):
    """
    Association table linking seasons to the matches that occurred in them.
    """

    __tablename__ = 'season_matches'

    season_id = Column(String(256), ForeignKey('seasons.season_id'), primary_key=True)
    season = relationship('Season', back_populates='matches')

    match_id = Column(String(256), ForeignKey('matches.match_id'), primary_key=True)
    match = relationship('Match', back_populates='season')

    def __repr__(self):
        return "<SeasonMatch(season_id={0}, match_id={1})>".format(season_id, match_id)

class Player(Base):
    """
    Base class for Players. Basic info plus relationships to stats, matches and seasons
    """

    __tablename__ = 'players'

    player_id = Column(String(256), primary_key=True, nullable=False)
    player_name = Column(String(256), nullable=False)
    shard_id = Column(String(256), nullable=False)

    matches = relationship(
        'PlayerMatches',
        back_populates='player'
    )

    seasons= relationship(
        'PlayerSeasonStats',
        back_populates='player'
    )

    lifetime_stats = relationship(
        'PlayerLifetimeStats',
        uselist=False,
        back_populates='player'
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

    season_id = Column(String(256), primary_key=True, nullable=False)
    is_current_season = Column(Boolean, nullable=False)
    is_off_season = Column(Boolean, nullable=False)

    players = relationship(
        'PlayerSeasonStats',
        back_populates='season'
    )

    matches = relationship(
        'SeasonMatches',
        back_populates='season'
    )

    def __repr__(self):
        return "<Season(season_id={0})".format(self.season_id)

class Match(Base):
    """
    Base class for individual matches, details about the actual rounds
    played (although not any stats which is weird)
    """

    __tablename__ = 'matches'

    match_id = Column(String(256), primary_key=True, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    gameMode = Column(String(256), nullable=False)
    mapName = Column(String(256), nullable=False)
    isCustomMatch = Column(Boolean, nullable=False)
    seasonState = Column(String(256), nullable=False)
    shardId = Column(String(256), nullable=False)

    players = relationship(
        'PlayerMatches',
        back_populates='match'
    )

    season = relationship(
        'SeasonMatches',
        back_populates='match'
    )

    def __repr__(self):
        return "<Match(match_id={0}, gameMode={1}, mapName={2})".format(
            self.match_id,
            self.gameMode,
            self.mapName
        )

class PlayerMatchStats(Base):
    """
    Stats for a single match per player
    """

    __tablename__ = 'player_match_stats'

    player_id = Column(String(256), primary_key=True)

    match_id = Column(String(256), ForeignKey('matches.match_id'), primary_key=True)

    DBNOs = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    boosts = Column(Integer, nullable=False)
    damageDealt = Column(Float, nullable=False)
    deathType = Column(String(64), nullable=False)
    headshotKills = Column(Integer, nullable=False)
    heals = Column(Integer, nullable=False)
    killPlace = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    longestKill = Column(Float, nullable=False)
    revives = Column(Integer, nullable=False)
    rideDistance = Column(Float, nullable=False)
    roadKills = Column(Integer, nullable=False)
    swimDistance = Column(Float, nullable=False)
    teamKills = Column(Integer, nullable=False)
    timeSurvived = Column(Float, nullable=False)
    vehicleDestroys = Column(Integer, nullable=False)
    walkDistance = Column(Float, nullable=False)
    weaponsAcquired = Column(Integer, nullable=False)
    winPlace = Column(Integer, nullable=False)

    def __repr__(self):
        return "<PlayerMatchStats(player_id={0}, match_id={1})>".format(
            self.player_id,
            self.match_id
        )



class PlayerSeasonStats(Base):
    """
    Stats for a single season, per player and game mode. I.E. there's a row for
    each player, for each season they have played in, for each game-mode that
    exists in PUBG
    """

    __tablename__ = 'player_season_stats'

    season_id = Column(String(256), ForeignKey('seasons.season_id'))
    season = relationship('Season', back_populates='players')

    player_id = Column(String(256), ForeignKey('players.player_id'))
    player = relationship('Player', back_populates='seasons')

    game_mode = Column(String(256))

    game_mode = Column(String(256), nullable=False)
    assists = Column(Integer, nullable=False)
    boosts = Column(Integer, nullable=False)
    dBNOs = Column(Integer, nullable=False)
    dailyKills = Column(Integer, nullable=False)
    damageDealt = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    dailyWins = Column(Integer, nullable=False)
    headshotKills = Column(Integer, nullable=False)
    heals = Column(Integer, nullable=False)
    killPoints = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    longestKill = Column(Float, nullable=False)
    longestTimeSurvived = Column(Float, nullable=False)
    losses = Column(Integer, nullable=False)
    maxKillStreaks = Column(Integer, nullable=False)
    mostSurvivalTime = Column(Integer, nullable=False)
    rankPoints = Column(Integer, nullable=False)
    revives = Column(Integer, nullable=False)
    rideDistance = Column(Float, nullable=False)
    roadKills = Column(Integer, nullable=False)
    roundMostKills = Column(Integer, nullable=False)
    roundsPlayed = Column(Integer, nullable=False)
    suicides = Column(Integer, nullable=False)
    swimDistance = Column(Float, nullable=False)
    teamKills = Column(Integer, nullable=False)
    timeSurvived = Column(Float, nullable=False)
    top10s = Column(Integer, nullable=False)
    vehicleDestroys = Column(Integer, nullable=False)
    walkDistance = Column(Float, nullable=False)
    weaponsAcquired = Column(Integer, nullable=False)
    weeklyKills = Column(Integer, nullable=False)
    weeklyWins = Column(Integer, nullable=False)
    winPoints = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)

    def __repr__(self):
        return "<PlayerSeasonStats(season_id={0}, player_id={1}, game_mode={2})>".format(
            self.season_id,
            self.player_id,
            self.game_mode
        )

    # have to move the PK definition to table args or SQL Alchemy only seems
    # to keep the first two.
    __table_args__ = (
        PrimaryKeyConstraint('player_id', 'season_id', 'game_mode'),
        {},
    )

class PlayerLifetimeStats(Base):
    """
    Stats for a player's entire in-game lifetime, per game mode.
    """

    __tablename__ = 'player_lifetime_stats'

    player_id = Column(String(256), ForeignKey('players.player_id'), primary_key=True)
    game_mode = Column(String(256), nullable=False, primary_key=True)

    player = relationship('Player', back_populates='lifetime_stats')

    assists = Column(Integer, nullable=False)
    boosts = Column(Integer, nullable=False)
    dBNOs = Column(Integer, nullable=False)
    dailyKills = Column(Integer, nullable=False)
    damageDealt = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    dailyWins = Column(Integer, nullable=False)
    headshotKills = Column(Integer, nullable=False)
    heals = Column(Integer, nullable=False)
    killPoints = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    longestKill = Column(Float, nullable=False)
    longestTimeSurvived = Column(Float, nullable=False)
    losses = Column(Integer, nullable=False)
    maxKillStreaks = Column(Integer, nullable=False)
    mostSurvivalTime = Column(Float, nullable=False)
    rankPoints = Column(Float, nullable=False)
    revives = Column(Integer, nullable=False)
    rideDistance = Column(Float, nullable=False)
    roadKills = Column(Integer, nullable=False)
    roundMostKills = Column(Integer, nullable=False)
    roundsPlayed = Column(Integer, nullable=False)
    suicides = Column(Integer, nullable=False)
    swimDistance = Column(Float, nullable=False)
    teamKills = Column(Integer, nullable=False)
    timeSurvived = Column(Float, nullable=False)
    top10s = Column(Integer, nullable=False)
    vehicleDestroys = Column(Integer, nullable=False)
    walkDistance = Column(Float, nullable=False)
    weaponsAcquired = Column(Integer, nullable=False)
    weeklyKills = Column(Integer, nullable=False)
    weeklyWins = Column(Integer, nullable=False)
    winPoints = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)

    def __repr__(self):
        return "<PlayerLifetimeStats(player_id={0}, game_mode={1})>".format(
            self.player_id,
            self.game_mode
        )
