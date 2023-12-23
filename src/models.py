from pathlib import Path

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
    hidden = Column(Boolean)

    def __repr__(self):
        return f'Chat({self.chat_id=}, {self.title=})'


def is_antispam_enabled(chat_id: int) -> bool:
    try:
        return session.query(Chat.antispam).filter_by(chat_id=chat_id).first()[0]
    except TypeError:
        return False


def is_quote_in_chat(text: str, chat_id: int) -> bool:
    result = session.query(Quote.text).filter_by(text=text, chat_id=chat_id).first()
    return bool(result)


def delete_quote_in_chat(text: str, chat_id: int):
    session.execute(delete(Quote).filter_by(text=text, chat_id=chat_id))
    session.commit()


def all_chat_quotes(chat_id: int) -> list:
    return session.query(Quote.text).filter(Quote.chat_id == chat_id).all()


def add_quote(chat_id: int, text: str):
    session.add(Quote(chat_id=chat_id, text=text))
    session.commit()
