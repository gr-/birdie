#import weakref
import random
import time
import uuid
import sys
from loremipsum import get_sentence
from locust import HttpLocust, TaskSet, task
from sqlalchemy.orm import sessionmaker

import logging

from models import FakeUser
import settings
from utils import initialize_db, get_friends, fakeuser_factory


class BirdieTaskSet(TaskSet):
    # TODO: fix social network distribution and post distribution and their correlation
    def on_start(self):
        """Pick a registered user at random and log in"""
        Session = initialize_db()
        self.session = Session()
        self.user = FakeUser(self.session)
#        logging.info('User is {!s}'.format(self.user))
        self.logged_in = False

    def _login(self):
        if not self.logged_in:
            response = self.client.post(settings.BASE_URL+'/login',
                                        {'form.submitted': True, 'login': self.user.username, 'password': self.user.password},
                                        name="/{username}")
            self.logged_in=True
            # HTML parsing of the mybirdie page defined by template mybirdie-bootstrap.pt
            self.friends = set(get_friends(response.text))
            

    def _logout(self):
        self.client.get(settings.BASE_URL+'/logout', name='/logout')
        self.user = None
        self.logged_in = False
        
        
    @task(3)
    def index(self):
        self.client.get('/')

    @task(1)
    def about(self):
        self.client.get('/about')
        
    @task(5)
    def view(self):
        # log in
        self._login()
        # pick any registered user at random
        buddy = FakeUser(self.session)
        # view her/him profile
        self.client.get(settings.BASE_URL+'/'+buddy.username+'/view', name="/{username}/view")

    @task(3)
    def follow(self):
        # log in
        self._login()
        # pick a candidate friend at random
        friend = FakeUser(self.session)
        if friend.username not in self.friends:
            # then view her/him profile
            self.client.get(settings.BASE_URL+'/'+friend.username+'/view', name="/{username}/view")
            # finally follow
            self.client.get(settings.BASE_URL+'/'+friend.username+'/follow', name="/{username}/follow")
            self.friends.add(friend.username)
        

    @task(1)
    def unfollow(self):
        # log in
        self._login()
        if len(self.friends)>0:
            # then pick a borrying friend at random
            old_friend = self.friends.pop()
            # finally unfollow
            self.client.get(settings.BASE_URL+'/'+old_friend+'/unfollow', name="/{username}/unfollow")


    @task(10)
    def post(self):
        # log in
        self._login()
        # post a chirp from a lorem ipsum sentence
        self.client.post(settings.BASE_URL+'/'+self.user.username,
                        {'form.submitted': True, 'chirp': get_sentence()},
                        name="/{username}[post]")
                        

    @task(1)
    def sign_on(self):
        """Logout, then sign on and log out a fresh new user. The next registered user is finally picked at random."""
        # log out current user
        self._logout()
        # generate a brand new user at random
        fuf=fakeuser_factory()
        data=fuf.next()
        # prepare data to fill the sign on form
        data['confirm']=data['password']
        data['form.submitted']=True
        # sign on
        self.client.post(settings.BASE_URL+'/join', data, name='/join')
        # log out the new user
        self._logout()
        # prepare the next task with a new user
        self.user = FakeUser(self.session)
        
        

class BirdieUser(HttpLocust):
        
    host = settings.BASE_URL
    weight = 1
    task_set = BirdieTaskSet 
    min_wait = 2000
    max_wait = 10000
