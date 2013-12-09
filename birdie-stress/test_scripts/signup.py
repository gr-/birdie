import time

from utils import (
    init_browser,
    add_user,
    )
    
    
class Transaction(object):        
    def __init__(self):
        self.custom_timers={}
 
    def run(self):
        br = init_browser()

        # go straight for sign up
        timer=add_user(br)
        self.custom_timers[ timer[0] ]=timer[1]

#        time.sleep(.2)        
        
        
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    for timer, value in trans.custom_timers.iteritems():
        print '%s: %.5f secs' % (timer, value)