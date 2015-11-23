#import weakref
import random
from sqlalchemy import (
    Column,
    Integer,
    String,
    )
from sqlalchemy.ext.declarative import declarative_base

import settings


Base = declarative_base()

class User(Base):
    """SQLAlchemy user model"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(username='%s', password='%s')>" % (
                self.username, self.password)


class FakeUser(object):
    def __init__(self, session):
        rand = random.randrange(0, settings.MAX_USERS) 
        row = session.query(User.id, User.username, User.password)[rand]
            
        self.id = row.id
        self.username = row.username
        self.password = row.password
#        self.logged_in = False

    def __str__(self):
        return "FakeUser<id=%s, user=%s, password=%s>" % (self.id, self.username, self.password)
