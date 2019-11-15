from sqlalchemy import create_engine
from database.model import Base, Player
from database.api import PUBGDatabaseConnector

db_uri = 'sqlite:///:memory:'

pubgdb = PUBGDatabaseConnector(db_uri, echo=True)

Base.metadata.create_all(pubgdb.engine)

sess = pubgdb.Session()

dan = Player(player_id='12345', player_name='Dan', shard_id='sdfsf')
session.add(dan)
session.commit()
