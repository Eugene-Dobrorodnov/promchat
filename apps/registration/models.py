import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from apps.settings import Settings


engine = create_engine(Settings.DB_PATCH)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User('%s')>" % (self.username)


users_table = User.__table__
metadata = Base.metadata


def create_user():
    metadata.create_all(engine)
