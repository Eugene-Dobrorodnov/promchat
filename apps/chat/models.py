import datetime
import re
import metadata_parser

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine, event, Boolean
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
    is_link = Column(Boolean, unique=False, default=False)
    title = Column(String(250), nullable=True)
    image = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship(User, backref="messages")


room_table = Room.__table__
message_table = Message.__table__
metadata = Base.metadata


@event.listens_for(Message, "after_insert")
def after_insert_listener(mapper, connection, instance):
    """
    Verification link
    """
    url_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', instance.messages)

    if url_list:
        url_resource = metadata_parser.MetadataParser(url=url_list[0])
        page = url_resource.metadata.get('page')
        title = page.get('title', None),
        image = page.get('image', None),

        connection.execute(
            message_table.update().
            where(message_table.c.id==instance.id).
            values(is_link=True, image=image, title=title)
        )


def create_all():
    metadata.create_all(engine)
