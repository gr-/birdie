Birdie
==================

The micro-blogging app for educational purpose.

The actual implementation is powered by the *Pyramid* web development framework for Python 3.
Ingredients of the soup are the *Chameleon* template framework, *SQLAlchemy* ORM, *Twitter-bootstrap* for CSS.

Birdie is distributed under the permissive MIT license (see `LICENSE` text for details).

Python package dependencies are listed under the `requires` label in the `setup.py` configuration file.


Getting Started
---------------

First, create and set up the python virtual environment:

    $ pyvenv venv
	$ source venv/bin/activate
	$ curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
	$ easy_install pip
	$ pip install -U setuptools
	$ pip install pyramid	

Then install Birdie requirements (package dependencies) and the app itself in `develop` mode:

	$ cd <path to this README.md file>
	$ python setup.py develop
	$ initialize_birdie_db development.ini
	$ venv/bin/pserve development.ini --reload

Enjoy at [http://localhost:6543](http://localhost:6543)

## INSTALL


### Setting up a virtual environment

To set-up a Birdie instance, it is warmly recommended to create a python virtual runtime environment first. This sandbox
isolate python binaries, variables, packages and settings for Birdie and prevent from conflicts with pre-existing settings.

With python3, the-newly-preferred way is the pyvenv library and its command-line counterpart:

    $ pyvenv venv
        $ source venv/bin/activate

To check for success, the `which python` command must answer something like `path-to-env/env/bin/python` rather than the
system-wide python binary (`/usr/bin` for most of the *ix boxes).

Next, it is required to install **setuptools** in this freshly activated environment.
If required, assign previously the `https_proxy` variable to the URL of your own proxy server:

    export https_proxy=http://<url-of-my-proxy>:<port>

Then, download the [ez_setup.py][ez] script and run:

    $ python ez_setup.py


To finilize your sandbox, install the super magic `pip` package manager b.t.w. of the [get-pip.py][inst] script:

    $ python get-pip.py 

From now on, you are done with a fully functionnal python3 runtime environment. It is recommended to check for latest version
of setuptools and pip install pyramid as well, even if Birdie app install process is expected to resolve python package dependencies
(it is not as reliable as pip).

    $ pip install -U setuptools
	$ pip install pyramid


To play further with `pip`, please refer to
the documentation on the [official pip website](http://www.pip-installer.org/en/latest/index.html "pip website")


### Birdie install

Install procedure is fairly easy. You have to decide for development or (limited) production instance and follow the directions below.

#### Production instance

    $ python setup.py develop
	$ initialize_birdie_db development.ini
    $ pserve development.ini --reload


#### Development instance

    $ python setup.py install
	$ initialize_birdie_db production.ini
    $ pserve production.ini


Whatever your decision, the instance of the Birdie web app is located at [http://localhost:6543](http://localhost:6543)

#### Caveats

There are (at least) two known issues you may face when running the Birdie app.
 
 - (1) port 6543 is assigned to another app: kill the app or change the port in the `production.ini` and/or `development.ini` file;
 - (2) there is a residual cookie from a previous Birdie installation: delete it within your web browser.  

Enjoy!


[ez]:   https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py "ez_setup.py"
[inst]: https://raw.github.com/pypa/pip/master/contrib/get-pip.py       "get-pip.py"
[pip]:  http://www.pip-installer.org/en/latest/index.html       "Pip website"











