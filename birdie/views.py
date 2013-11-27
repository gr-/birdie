from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.renderers import get_renderer
from pyramid.security import (
    remember, 
    forget, 
    authenticated_userid,
    )
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from pyramid.url import route_url

from sqlalchemy.exc import DBAPIError

from repoze.timeago import get_elapsed
from datetime import datetime

from .models import (
    DBSession,
    Chirp,
    User,
    Follower,
    check_login,
    )


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_birdie_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


class BirdieViews(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout-bootstrap.pt")
        self.layout = renderer.implementation().macros['layout']
        self.logged_in = authenticated_userid(request)
        self.username = request.params.get('username')
        self.app_url = request.application_url
        self.static_url = request.static_url

    @view_config(route_name='about',
                renderer='templates/about-bootstrap.pt')
    def about_page(self):
        return {}            
                
    @view_config(route_name='home',
                renderer='templates/birdie-bootstrap.pt')
    def birdie_view(self):
        username = self.logged_in
        user = None
        follows = None
        chirps = None
        friends = []
        try:
            if username:        
                user = DBSession.query(User).filter_by(username=username).one()
                follows = DBSession.query(Follower).filter(Follower.follower==user.id)
                friends = [friend.id for friend in follows]
            chirps = DBSession.query(Chirp).order_by(Chirp.timestamp.desc()).limit(15)
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        
        return {'elapsed': get_elapsed,
            'user': user,
            'follows': friends,
            'chirps': chirps}

    @view_config(route_name='mybirdie',
                permission='registered',
                renderer='templates/mybirdie-bootstrap.pt')
    def my_birdie_view(self):
        username = self.logged_in
        
        user = DBSession.query(User).filter_by(username=username).one()
        
        if 'form.submitted' in self.request.params:
            chirp = self.request.params.get('chirp')
            author = user
            timestamp = datetime.utcnow()
            DBSession.add( Chirp(chirp, author, timestamp) )
                
            url = self.request.route_url('mybirdie', username=username)
            return HTTPFound(url)

        follows = DBSession.query(User).join(Follower, User.id==Follower.follows).\
                                        filter_by(follower=user.id)
#       follows = follows.order_by(Follower.timestamp.asc()).limit(10)
        followers = DBSession.query(User).join(Follower, User.id==Follower.follower).\
                                       filter_by(follows=user.id)
#       followers = followers.order_by(Follower.follower.asc()).limit(10)
        chirpers = [friend.id for friend in follows] # projection of a user on column id
        chirps = DBSession.query(Chirp).filter(Chirp.author_id.in_(chirpers))
        chirps = chirps.order_by(Chirp.timestamp.desc()).limit(15)
        
        my_chirps = DBSession.query(Chirp).filter_by(author_id=user.id)
        my_chirps = my_chirps.order_by(Chirp.timestamp.desc()).limit(6)

        return {'elapsed': get_elapsed,
                'user': user,
                'follows': follows,
                'followers': followers,
                'chirps': chirps,
                'my_chirps': my_chirps}

    @view_config(route_name='login',
                renderer='templates/login-bootstrap.pt')
    @forbidden_view_config(renderer='birdie:templates/login-bootstrap.pt')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        join_url = request.route_url('join')
        came_from = request.params.get('came_from')
        print('came_from={!r}\n'.format(request.params.get('came_from')))
        if came_from is None : # first time it enters the login page
            came_from = request.referer
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            if check_login(login, password):
                headers = remember(request, login)
                if (came_from == login_url or came_from == join_url or came_from == self.app_url or came_from == ''):
                    came_from = request.route_url('mybirdie', username=login)  # never use login form itself as came_from
                return HTTPFound(location=came_from,
                                 headers=headers)
            message = 'Failed login'

        return {'message': message,
                'came_from': came_from,
                'login': login,
                'password': password}
                

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        url = self.request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)

    @view_config(route_name='join',
                renderer='birdie:templates/join-bootstrap.pt')
    def join(self):

        request = self.request
        join_url = request.route_url('join')
        login_url = request.route_url('login')
        came_from = request.params.get('came_from')
        if came_from is None: # first time it enters the join page
            came_from = request.referer
        
        if 'form.submitted' in request.params:
        # registration form has been submitted
            username = request.params.get('username')
            password = request.params.get('password')
            confirm = request.params.get('confirm')
            fullname = request.params.get('fullname')
            about = request.params.get('about')
            message = ''

            user = DBSession.query(User).filter_by(username=username).first()
            
            if username is '':
                message = "The username is required."
            elif (password is '' and confirm is ''):
                message = "The password is required."
            elif user:
                message = "The username {} already exists.".format(username)
            elif confirm != password:
                message = "The passwords don't match."
            elif len(password) < 6:
                message = "The password is too short."

            if message:
                return {'message': message,
                    'came_from': came_from,
                    'username': username,
                    'fullname': fullname,
                    'about': about}
           
           # register new user
            dor = datetime.utcnow()
            DBSession.add( User(username, password, fullname, about, dor) )
            headers = remember(request, username)
            if (came_from == join_url or came_from == login_url or came_from == self.app_url):
                came_from = request.route_url('mybirdie', username=username)  # never use login form itself as came_from
            return HTTPFound(location = came_from,
                             headers = headers)

        # default - prepare empty sign in form
        return {'message': '',
                'came_from': came_from,
                'username': '',
                'fullname': '',
                'about': ''}


    @view_config(route_name='profile',
                 permission='registered',
                 renderer='birdie:templates/user-bootstrap.pt')
    def profile_view(self):
        auth_username = self.logged_in
        username = self.request.matchdict['username']
        if auth_username==username:
            return HTTPFound(location = self.request.route_url('mybirdie', username=username))

        auth_user = DBSession.query(User).filter_by(username=auth_username).one()
        auth_user_follows = DBSession.query(Follower).filter_by(follower=auth_user.id)
        auth_user_friends = [friend.id for friend in auth_user_follows] # projection
        user = DBSession.query(User).filter_by(username=username).one()
        
        follows = DBSession.query(Follower).filter_by(follower=user.id)
#        follows = follows.order_by(Follower.follows.asc()).limit(10)
        followers = DBSession.query(Follower).filter_by(follows=user.id)
#        followers = followers.order_by(Follower.follower.asc()).limit(10)
        chirps = DBSession.query(Chirp).filter_by(author_id=user.id)
        chirps = chirps.order_by(Chirp.timestamp.desc()).limit(6)
        return {'elapsed': get_elapsed,
                'auth_user_follows': auth_user_friends,
                'user': user,
                'follows': follows,
                'followers': followers,
                'chirps': chirps}
                

    @view_config(route_name='follow',
                 permission="registered",
                 renderer='birdie:templates/fake.pt')
    def follow(self):
        username = self.logged_in
        user = DBSession.query(User).filter_by(username=username).one()
        friend_username = self.request.matchdict.get('username')
        friend = DBSession.query(User).filter_by(username=friend_username).one()
        follower = user.id
        follows = friend.id
        
        DBSession.add( Follower(follower, follows ))
        return HTTPFound(location = self.request.referer)


    @view_config(route_name='unfollow',
                 permission="registered",
                 renderer='birdie:templates/fake.pt')
    def unfollow(self):
        username = self.logged_in
        user = DBSession.query(User).filter_by(username=username).one()
        friend_username = self.request.matchdict.get('username')
        friend = DBSession.query(User).filter_by(username=friend_username).one()
        follower = user.id
        follows = friend.id
        
        DBSession.query(Follower).filter(Follower.follower==follower).filter(Follower.follows==follows).delete()
        return HTTPFound(location = self.request.referer)



    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'birdie'}


