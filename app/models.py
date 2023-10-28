import os
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from sqlalchemy import create_engine

Base = declarative_base()
basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(basedir, 'db/db.sqlite'))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Permission:
    USE_COMMANDS = 1     # Пользоваться обычными командами.
    SEND_LINKS = 2      # Может отправлять ссылки без удаления.
    MODIFY_QUOTES = 4    # Может добавлять и удалять цитаты.
    MODERATE = 8
    ADMIN = 16       # Может банить юзеров и удалять сообщения.


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    text = Column(String)

    def __repr__(self):
        return f"Quote({self.text=}, {self.chat_id=})"


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    title = Column(String)

    # Settings
    quotes = relationship('Quote', backref='chat', cascade='all, delete')
    antispam = Column(Boolean)
    report = Column(Boolean)
    reminder = Column(Boolean)
    hidden = Column(Boolean)

    def __repr__(self):
        return f'Chat({self.chat_id=}, {self.title=})'
