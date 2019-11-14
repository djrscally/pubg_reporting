from sqlalchemy import create_engine
from database.model import Base

eng = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(eng)
