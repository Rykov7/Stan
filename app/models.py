from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


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
    quotes = relationship('Quote', backref='chat')
    antispam = Column(Boolean)
    report = Column(Boolean)
    reminder = Column(Boolean)

    def __repr__(self):
        return f'Chat({self.chat_id=}, {self.title=})'
