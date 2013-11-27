from pyramid.security import Authenticated
from pyramid.security import Allow

from .models import (
    DBSession,
    User,
    )
    
from cryptacular.bcrypt import BCRYPTPasswordManager

Crypt = BCRYPTPasswordManager()


class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'registered')
    ]
    def __init__(self, request):
        pass
        

def check_login(login, password):
    session = DBSession()
    user = session.query(User).filter_by(username=login).first()
    if user is not None:
        hashed_password = user.password
        if Crypt.check( hashed_password, password ):
            return True
    return False
