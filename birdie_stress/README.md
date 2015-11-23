Birdie stress test suite
---

Tests are powered by [locust.io](http://locust.io).

They are basically a regular python2 app.


The install recipe
---

1. Prepare a python2 virtual env:

    > virtualenv venv
	> source venv/bin/activate

2. Install `locust.io`:

	> pip install locustio

If it fails on C compilation error due to `gevent` dependency, then here is
one of those miraculous command line that fixes it at least on Mac OS 10.9:

    > CFLAGS='-std=c99' pip install gevent==1.0.2


3. Add distribution capabilities

    > pip install pyzmq
	

4. Run the locust.io `test` suite

    > locust --host=<url-to-the-birdie-website>
	
Alternatively, with multiple processes:

    > locust --master --host=http://example.com
	> locust --slave --host=http://example.com

with as many slaves as you like.

5. Play with the instance

Go to http://127.0.0.1:8089 and follow the online instructions. Enjoy!