from sqlalchemy import (
    Column,
#    Index,
    Integer,
#    Text,
    Unicode,
    ForeignKey,
    UniqueConstraint,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    password = Column(Unicode(20))
    fullname = Column(Unicode(40))
    about = Column(Unicode(255))
    dor = Column(TIMESTAMP())   # date of registration

    def __init__(self, username, password, fullname, about, dor):
        self.username = username
        self.password = crypt.encode(password)
        self.fullname = fullname
        self.about = about
        self.dor = dor

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    follower = Column(Integer, ForeignKey('users.id'))
    follows = Column(Integer, ForeignKey('users.id'))
    
    UniqueConstraint('follower', 'follows', name='uix_1')

    def __init__(self, follower, follows):
        self.follower = follower
        self.follows = follows

class Chirp(Base):
    __tablename__ = 'chirps'
    id = Column(Integer, primary_key=True)
    chirp = Column(Unicode(80))
    timestamp = Column(TIMESTAMP())
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship(User, cascade='delete', backref='chirps')

    def __init__(self, chirp, author, timestamp):
        self.chirp = chirp
        self.author = author
        self.timestamp = timestamp

#Index('my_index', MyModel.name, unique=True, mysql_length=255)