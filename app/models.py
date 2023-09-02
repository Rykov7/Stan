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


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     tg_id = Column(Integer, unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     username = Column(String)
#     permissions = Column(Integer)
#
#     def __repr__(self):
#         return f'User({self.first_name} {self.last_name} {self.username})'
#
# class Role(Base):
#     __tablename__ = 'roles'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), unique=True)
#     default = Column(Boolean, default=False, index=True)
#     permissions = Column(Integer)
#     users = relationship('User', backref='role', lazy='dynamic')
#
#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm
#
#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm
#
#     def reset_permissions(self):
#         self.permissions = 0
#
#     def has_permission(self, perm):
#         return self.permissions & perm == perm
#
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#             "User": [Permission.USE_COMMANDS],
#             "Moderator": [Permission.USE_COMMANDS, Permission.SEND_LINKS,
#                           Permission.MODIFY_QUOTES, Permission.MODERATE],
#             "Administrator": [Permission.USE_COMMANDS, Permission.SEND_LINKS,
#                               Permission.MODIFY_QUOTES, Permission.MODERATE,
#                               Permission.ADMIN],
#         }
#         default_role = 'User'
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.reset_permissions()
#             for perm in roles[r]:
#                 role.add_permission(perm)
#             role.default = (role.name == default_role)
#             session.add(role)
#         session.commit()