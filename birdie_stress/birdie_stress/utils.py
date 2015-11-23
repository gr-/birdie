import uuid
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import requests
from bs4 import BeautifulSoup
import re

from models import Base, User, FakeUser
import settings


"""
This module contains utility fonctions such like database connection or fake user generator. 

"""


def fakeuser_factory():
    """factory (generator) of fake users to populate the database"""
    while True:
        random_uid = str(uuid.uuid4())
        # build a brand new fake user
        yield {'fullname': random_uid,
                'username': settings.BASE_USERNAME+random_uid[:8],
                'password': random_uid[:8],
                'about': settings.ABOUT}


def get_friends(page):
    """parse MyBirdie HTML page to get friend's usernames."""
    soup=BeautifulSoup(page, 'html.parser')
    f_context=soup.find(string=re.compile("Follows:")).parent.parent.parent.find_all('p', class_='list-group-item-text')
    friends = []
    for f in f_context:
        friends.append(f.small.text.strip()[1:])
    return friends
    

def initialize_db():
    """
    Initializes database connection and sessionmaker.
    Creates user table.
    """
    engine = db_connect()
    create_user_table(engine)
    return sessionmaker(bind=engine)


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE), echo=False, echo_pool=False)


def create_user_table(engine):
    """"""
    Base.metadata.create_all(engine)


def add_user(session, fullname, username, password, about):
    data = {'form.submitted': True,
            'fullname': fullname,
            'username': username,
            'password': password,
            'confirm': password,
            'about': about}

    response = requests.post(settings.BASE_URL+'/join', data=data)
    session.add( User (username=data['username'], password=data['password']) )
    requests.get(settings.BASE_URL+'/logout')
    
    
def populate_db(size=settings.MAX_USERS):
    Session = initialize_db()
    db_session = Session()
    print ''
    fuf = fakeuser_factory()
    for index in range(size):
        user = fuf.next()
        sys.stdout.write('\rPopulating the database: {}/{} new users created'.format(index+1, size))
        sys.stdout.flush()
        add_user(db_session, **user)
    print ''    
    db_session.commit()
    db_session.close()
    
    

    
if __name__=='__main__':
    populate_db()
    # import logging
    # from bs4 import BeautifulSoup
    # import re
    # Session = initialize_db()
    # session = Session()
    # user = FakeUser(session)
    # print('user is {!r}'.format(user))
    # response=requests.post(settings.BASE_URL+'/login', data={'form.submitted': True, 'login': user.username, 'password': user.password})
    # soup=BeautifulSoup(response.text, 'html.parser')
    # f_context=soup.find(string=re.compile("Follows:")).parent.parent.parent.find_all('p', class_='list-group-item-text')
    # friends = []
    # for f in f_context:
    #     friends.append(f.small.text.strip()[1:])
    # print(friends)