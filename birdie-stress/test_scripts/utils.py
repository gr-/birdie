import cookielib
import mechanize
#import weakref
import random
import time
import uuid
import sys
from loremipsum import get_sentence

from birdie_settings import *
from initialize_db import (
    User,
    DBSession,
    )
        

class FakeUser(object):
    def __init__(self, browser):
        rand = random.randrange(0, MAX_USERS) 
        row = DBSession.query(User.id, User.username, User.password)[rand]
            
        self.id = row.id
        self.username = row.username
        self.password = row.password

        self.br = browser
        self.logged_in = False

    def log_in(self):
        timer = ()
        if not self.logged_in:
            timer = _login(self.br, self.username, self.password)
            if timer[0] == 'Login':
                self.logged_in = True
        return timer
        
        
    def post_chirp(self):
        latency=0
        timer = ()
        br = self.br
        
        _ = br.open(BASE_URL+'/'+self.username)    
    
#        chirps_count=random.randrange(1, MAX_CHIRPS)
#        for i in range(chirps_count):
    
        br.select_form(nr=0)
        br.form[ 'chirp' ] = get_sentence()
        
        start_timer = time.time()
        resp = br.submit() 
        resp.read()
        latency += time.time() - start_timer
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        # assert ('my birdie' in resp.get_data()), 'Text Assertion Failed'

        timer = 'Chirp', latency       
        return timer
        

    def follow(self):
        
        br=self.br
        # randomly pick a friend - may be myself or a friend of mine, don't care
        friend = FakeUser(self.br)
        
        start_timer = time.time()
        resp = br.open(BASE_URL+'/'+friend.username+'/follow')
        resp.read()
        latency = time.time() - start_timer
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        # assert ('my birdie' in resp.get_data()), 'Text Assertion Failed'

        timer = 'Follow', latency        
        return timer


    def unfollow(self):
        
        br=self.br
        # randomly pick a friend - may be myself or not an actual friend of mine, don't care
        old_friend = FakeUser(self.br)
        
        start_timer = time.time()
        resp = br.open(BASE_URL+'/'+old_friend.username+'/unfollow')
        resp.read()
        latency = time.time() - start_timer
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        # assert ('my birdie' in resp.get_data()), 'Text Assertion Failed'

        timer = 'Unfollow', latency        
        return timer


    def view(self):
        
        br=self.br
        # randomly pick a user - may be myself or a friend of mine, don't care
        buddy = FakeUser(self.br)
        
        start_timer = time.time()
        resp = br.open(BASE_URL+'/'+buddy.username+'/view')
        resp.read()
        latency = time.time() - start_timer
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        # assert ('my birdie' in resp.get_data()), 'Text Assertion Failed'

        timer = 'View_profile', latency        
        return timer

    

    def __str__(self):
        return "FakeUser<user=%s,logged_in=%s>" % (self.username, self.logged_in)

# utility functions
def init_browser():
    """Returns an initialized browser and associated cookie jar."""
    br = mechanize.Browser()

    br.set_handle_equiv(True)
#    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # add a custom header to declare "Believe me, I am not a robot"
    br.addheaders = [('User-agent', 'Mozilla/5.0')]

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return br

def _login(br, u, p):
    timer = ()
    
    _ = br.open(BASE_URL+'/login')

    br.select_form(nr=0)
    br.form[ 'login' ] = u
    br.form[ 'password' ] = p
    
    start_timer = time.time()
    resp = br.submit()
    resp.read()
    latency = time.time() - start_timer

    assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code

    if 'Failed login' in resp.get_data(): 
        timer= 'Login_failed', latency                     
    else:
        timer = 'Login', latency
         
    return timer
    
    
def add_user(br):
    timer=()
    # build a brand new fake user
    random_uid = str(uuid.uuid4())
    
    fullname = random_uid
    username = BASE_USERNAME+random_uid[:8]
    password = random_uid[:8]

    _ = br.open(BASE_URL+'/join')

    br.select_form(nr=0)
    br.form[ 'fullname' ] = fullname
    br.form[ 'username' ] = username
    br.form[ 'password' ] = password
    br.form[ 'confirm' ] = password
    br.form[ 'about' ] = ABOUT

    start_time = time.time()
    resp = br.submit()
    resp.read()
    latency = time.time() - start_time
    # verify responses are valid
    assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
    
    if resp.geturl() == BASE_URL+'/join':
        timer = 'Failed_registration', latency
    else:
        timer = 'Register_new_user', latency
        # add user in the local db (for future retrieval)
        DBSession.add( User (username=username, password=password) )
        
        # logout and reset cookie
        resp = br.open(BASE_URL+'/logout')
#        resp.read()
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        assert ('Public Timeline' in resp.get_data()), 'Text Assertion Failed'  
        
    return timer
    
    
def populate_db(br=None, size=MAX_USERS):
    if not br:
        br = init_browser()        
    print ''
    
    for index in range(size):    
        sys.stdout.write('\rPopulating the database with {} new users over {}'.format(index+1, MAX_USERS))
        sys.stdout.flush()
        add_user(br)
    DBSession.commit()
    print ''    
