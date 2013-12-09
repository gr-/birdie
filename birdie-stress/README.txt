Birdie stress test suite
---

Tests are powered by multi-mechanize :
http://testutils.org/multi-mechanize/


They are basically a regular Python 2 app.


INSTALL

1) prepare a python 2 (>=2.7) virtual environment with virtualenv

2) pip-install the multi-mechanize package :
http://testutils.org/multi-mechanize/setup.html

Among the tricky dependencies are 
	- freetype and libpng system libraries, and
	- matplotlib python library. 

3) run a local instance (http://localhost:6543) of Birdie in production mode

4) from then root directory of the test suite, run
	$ python birdie-stress/test_scripts/initialize_db.py
	
It will create 500 fake users in the Birdie database
	
5) run
	 $ multimech-run birdie-stress/

and grab the results in the directory birdie-stress/results/results_<timestamp>
