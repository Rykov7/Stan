import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(basedir, 'db/db.sqlite'))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
