from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    """
    Defines the players
    """

    __tablename__ = 'players'

    player_id = Column(String, primary_key=True, nullable=False)
    player_name = Column(String, nullable=False)
    shard_id = Column(String, nullable=False)

    matches = relationship('Match')

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

class PlayerMatch(Base):
    """
    relational table tying players to the matches they have been
    in, but again no stats.
    """

    __tablename__ = 'player_matches'

    player_match_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    player_id = Column(String, ForeignKey('players.player_id'))
    player = relationship('Player', back_populates='player_matches')
    match_id = Column(String, ForeignKey('matches.match_id'))
    match = relationship('Match', back_populates='player_matches')
