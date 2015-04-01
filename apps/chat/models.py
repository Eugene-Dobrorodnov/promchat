import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from apps.registration.models import User


engine = create_engine('postgresql+psycopg2:///prom_chat')
Base = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Room('%s')>" % (self.title)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    messages = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship(User, backref="messages")


room_table = Room.__table__
message_table = Message.__table__
metadata = Base.metadata


def create_all():
    metadata.create_all(engine)
