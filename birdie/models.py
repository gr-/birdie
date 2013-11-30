from sqlalchemy import (
    Column,
#    Index,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
#    UniqueConstraint,
    Table,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


from .security import Crypt


follower_table = Table('follower', Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('followee_id', Integer, ForeignKey('user.id'), primary_key=True)
    )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    password = Column(Unicode(20))
    fullname = Column(Unicode(40))
    about = Column(Unicode(255))
    dor = Column(DateTime)   # date of registration

    friends = relationship('User',
                            lazy="dynamic",
                            cascade="all, delete",
                            secondary=follower_table,
                            primaryjoin=id==follower_table.c.follower_id,
                            secondaryjoin=id==follower_table.c.followee_id,
                            backref=backref('followers', lazy='dynamic', cascade="all, delete"))

    def __init__(self, username, password, fullname, about, dor):
        self.username = username
        self.password = Crypt.encode(password)
        self.fullname = fullname
        self.about = about
        self.dor = dor


# class Follower(Base):
#     __tablename__ = 'followers'
#     id = Column(Integer, primary_key=True)
#     follower_id = Column(Integer, ForeignKey('users.id'))
#     follows_id = Column(Integer, ForeignKey('users.id'))
#     
#     follower = relationship(User, cascade='delete', backref='friends')
#     follows = relationship(User, cascade='delete', backref='followers')
#     
#     UniqueConstraint('follower', 'follows', name='uix_1')
# 
#     def __init__(self, follower, follows):
#         self.follower = follower
#         self.follows = follows

class Chirp(Base):
    __tablename__ = 'chirp'
    id = Column(Integer, primary_key=True)
    chirp = Column(Unicode(80))
    timestamp = Column(DateTime)
    author_id = Column(Integer, ForeignKey('user.id'))
    
    author = relationship(User,
                          backref=backref('chirps', order_by="Chirp.timestamp", cascade="all, delete, delete-orphan"),
                          )

    def __init__(self, chirp, author, timestamp):
        self.chirp = chirp
        self.author = author
        self.timestamp = timestamp
        
    def __repr__(self):
        return '<Chirp({!r} from @{} at {})>'.format(self.chirp, self.author.username, self.timestamp)

#Index('my_index', MyModel.name, unique=True, mysql_length=255)