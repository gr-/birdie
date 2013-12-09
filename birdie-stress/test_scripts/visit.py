import mechanize
import time

from utils import (
    init_browser,
    )
    
from birdie_settings import BASE_URL

    
class Transaction(object):        
    def __init__(self):
        self.custom_timers={}
 
    def run(self):
        br = init_browser()

        start_time = time.time()
        resp = br.open(BASE_URL)
        resp.read()
        latency=time.time() - start_time
        # verify responses are valid
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code
        assert ('Public Timeline' in resp.get_data()), 'Text Assertion Failed'

        self.custom_timers[ 'Home' ]=latency

#        time.sleep(.2)        
        
        
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    for timer, value in trans.custom_timers.iteritems():
        print '%s: %.5f secs' % (timer, value)