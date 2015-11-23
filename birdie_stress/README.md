Birdie stress test suite
---

Tests are powered by [locust.io](http://locust.io).

They are basically a regular python2 app.


The install recipe
---

1. Prepare a python2 virtual env:

        > virtualenv venv
	    > source venv/bin/activate

2. Set up the app with distribution capabilities and more:

	    > python setup.py develop

    Don't forget your own `https_proxy` if any. This step basically install the required dependencies.
    If it fails on C compilation error due to `gevent` dependency, then here is
    one of those miraculous command line that fixes it at least on Mac OS 10.9:

        > CFLAGS='-std=c99' pip install gevent==1.0.2
	
3. Initialize a test database with fake users:

        > initialize_fakedb

4. Run the **locust.io** test suite

        > locust --host=<url-to-the-birdie-website>
	
    Alternatively, with multiple processes:

        > locust --master --host=http://example.com
	    > locust --slave --host=http://example.com

    with as many slaves as you like.

5. Play with the instance

    Go to [http://127.0.0.1:8089](http://127.0.0.1:8089) and follow the online instructions. Enjoy!

	
A couple of more thoughts
---

* The app maintains a small `SQlite` backend for picking at random fake users that connect to the **Birdie** app.
* About dependencies:
    * The `beautifulsoup4` dependency serves the purpose of collecting friends of a given user by scrapping the `myBirdie` HTML page.
    * `loremipsum` is used to generate random sentences as new chirps.