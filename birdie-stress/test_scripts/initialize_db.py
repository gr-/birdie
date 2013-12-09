from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    )

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.ext.declarative import declarative_base

from birdie_settings import DB_FILE

engine = create_engine(DB_FILE, echo=False, echo_pool=False)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(username='%s', password='%s')>" % (
                self.username, self.password)


# create the schema                
Base.metadata.create_all(engine)    

# prepare a db session
session_factory = sessionmaker(bind=engine)
#                                autoflush=True,
#                                autocommit=False,
#                                )
DBSession = scoped_session(session_factory)


if __name__ == '__main__':
    from utils import populate_db
    
    # insert birdie_settings.MAX_USERS users into the db
    populate_db()