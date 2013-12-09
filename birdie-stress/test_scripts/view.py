import time

from utils import (
    init_browser,
    FakeUser,
    )

class Transaction(object):

    def __init__(self):
        self.custom_timers={}        

        self.br = init_browser()
        
        while True:
            self.user = FakeUser(self.br)
            timer=self.user.log_in()        
            self.custom_timers[ timer[0] ]=timer[1]
            if self.user.logged_in:
                break
        
        
    def run(self):
            
        timer=self.user.view()
        self.custom_timers[ timer[0] ]=timer[1]

        # # close session
        # resp = br.open(BASE_URL+'/logout')
        # resp.read()
        # # verify responses are valid
        # assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        # assert ('Public Timeline' in resp.get_data()), 'Text Assertion Failed'

#        time.sleep(.5)

        
if __name__ == '__main__':
    trans = Transaction()
    trans.run()

    for timer, value in trans.custom_timers.iteritems():
        print '%s: %.5f secs' % (timer, value)       