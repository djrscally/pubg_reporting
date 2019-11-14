from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class Player(base):
    """
    Defines the players
    """

    __tablename__ = 'users'

    player_id = Column(String, primary_key=True, nullable=False)
    player_name = Column(String, nullable=False)
    shard_id = Column(String, nullable=False)

    def __repr__(self):
        return "<Player(player_id={0}, player_name={1})>".format(
            self.player_id,
            self.player_name
        )

class Season(base):
    """
    Base class for Seasons, which are like a bucket of matches that are very
    inconsistent lengths. Originally once per month, then they went to much
    longer and lately semi-permanent
    """

    __tablename__ = 'seasons'

    season_id = Column(String, primary_key=True, nullable=False)
    , is_current_season = Column(Boolean, nullable=False)
    , is_off_season = Column(Boolean, nullable=False)
