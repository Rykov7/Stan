import logging
import os
from pathlib import Path
from typing import Type

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

root = Path(__file__).parent.parent
data_folder = root / "data"
db_path = data_folder / "db.sqlite"
engine = create_engine(f'sqlite:///{db_path}')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Permission:
    USE_COMMANDS = 1  # Пользоваться обычными командами.
    SEND_LINKS = 2  # Может отправлять ссылки без удаления.
    MODIFY_QUOTES = 4  # Может добавлять и удалять цитаты.
    MODERATE = 8
    ADMIN = 16  # Может банить юзеров и удалять сообщения.


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

    def __repr__(self):
        return f'Chat({self.chat_id=}, {self.title=})'


class BadWord(Base):
    __tablename__ = 'bad_words'
    id = Column(Integer, primary_key=True)
    word = Column(String)

    def __repr__(self):
        return f'BadWord({self.id}: {self.word=})'


CACHE: dict[int, Type[Chat]] = {}


def _fill_cache():
    if os.environ.get("testing", "FALSE") == "FALSE":
        for chat in session.query(Chat).all():
            CACHE[chat.chat_id] = chat


def is_antispam_enabled(chat_id: int) -> bool:
    if chat_id not in CACHE:
        return False
    return CACHE[chat_id].antispam


def is_quote_in_chat(text: str, chat_id: int) -> bool:
    return text in all_chat_quotes(chat_id)


def delete_quote_in_chat(text: str, chat_id: int):
    session.execute(delete(Quote).filter_by(text=text, chat_id=chat_id))
    session.commit()
    _reload_chat(chat_id)


def all_chat_quotes(chat_id: int) -> list:
    if chat_id not in CACHE:
        return []
    return [quote.text for quote in CACHE[chat_id].quotes]


def is_chat_exists(chat_id: int) -> bool:
    return chat_id in CACHE


def add_quote(chat_id: int, text: str):
    session.add(Quote(chat_id=chat_id, text=text))
    session.commit()
    _reload_chat(chat_id)


def add_spam(chat_id: int, text: str):
    session.add(BadWord(word=text))
    session.commit()
    _reload_chat(chat_id)


def chat_by_id(chat_id: int) -> None | Chat:
    return CACHE.get(chat_id)


def add_chat(chat_id: int, chat_title: str):
    session.add(Chat(chat_id=chat_id, title=chat_title, antispam=1, report=0, reminder=1))
    session.commit()
    _reload_chat(chat_id)


def update_chat(chat_id: int, antispam: int = 1, rep: int = 0, rem: int = 1):
    session.query(Chat).filter_by(chat_id=chat_id).update({"antispam": antispam, "report": rep, "reminder": rem})
    session.commit()
    _reload_chat(chat_id)


def delete_chat(chat_id: int) -> str:
    """
    Удаляем чат из БД вместе с его цитатами, возвращаем его название для логирования
    """
    chat = session.query(Chat).filter_by(chat_id=chat_id).first()
    session.delete(chat)
    session.commit()
    del CACHE[chat_id]
    return chat.title


def _reload_chat(chat_id: int):
    chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    CACHE[chat_id] = chat


_fill_cache()
logging.warning("[START] Load data from db to cache")
