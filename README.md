Birdie
==================

The micro-blogging app for educational purpose.

The actual implementation is powered by the *Pyramid* web development framework for Python 3.
Ingredients of the soup are the *Chameleon* template framework, *SQLAlchemy* ORM, *Twitter-bootstrap* for CSS.

Fragments of the actual source code (especially the model) comes from a previous [**Birdie** implementation](https://github.com/cguardia/Pyramid-Tutorial/tree/master/src/stage3) of [cguardia–(https://github.com/cguardia/).

**Birdie** is distributed under the permissive MIT license (see `LICENSE` text for details).

Python package dependencies are listed under the `requires` label in the `setup.py` configuration file.


Getting Started
---------------

First, download the zip file of the birdie project from the [github repos](https://github.com/gr-/birdie).

The following two series of commands are a shorthand for the all install procedure (see below). 
 
Create and set up the python virtual environment:

    $ pyvenv venv
	$ source venv/bin/activate
	$ curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
	$ easy_install pip
	$ pip install -U setuptools
	$ pip install pyramid	

Install **Birdie** requirements (package dependencies) and the app itself in `develop` mode:

	$ unzip birdie-<ver>.zip
	$ cd <path to this README.md file>
	$ python setup.py develop
	$ initialize_birdie_db development.ini
	$ venv/bin/pserve development.ini --reload

Check for successfull installation at [http://localhost:6543](http://localhost:6543)

## INSTALL


### Setting up a virtual environment

To set-up a **Birdie** instance, it is warmly recommended to create a python virtual runtime environment first. This sandbox
isolates python binaries, packages and various settings for **Birdie** and prevent from conflicts with pre-existing settings.

With python3, the-newly-preferred way is the `pyvenv` library and its command-line counterpart:

    $ pyvenv venv
    $ source venv/bin/activate

To check for success, the `which python` command must answer something like `/path/to/venv/venv/bin/python` rather than the
system-wide python binary (`/usr/bin` for most of the *ix boxes). Actually, you are free to set a different name for `venv`
and to put that directory anywhere on your local file system.

Next, it is required to install **setuptools** in this freshly activated environment.
If required, assign first the `https_proxy` variable to the URL of your own proxy server:

    $ export https_proxy=http://<url-of-your-proxy-server>:<port>

Then, download the [ez_setup.py][ez] script and run:

    $ python ez_setup.py

The previous python script serves the purpose of making setup tools (for package building, distribution, and many more) available in the `venv` sandbox.
To check for success of the installation, please ask for

    $ which easy_install

and observes it answers once again `/path/to/venv/venv/bin/easy_install`.  
 
To empower your sandbox, install the super magic `pip` package manager b.t.w. of the [get-pip.py][inst] script:

    $ python get-pip.py 

As an alternative, you might install pip from easy_install itself:

    $ easy_install pip


From now on, you are done with a fully functionnal python3 runtime environment. It is recommended to check for latest version
of **setuptools** and *pip-install* **pyramid** as well, even if **Birdie** app install process is expected to resolve python package dependencies
(it is not as reliable as `pip` anyway).

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


Whatever your decision, the instance of the **Birdie** web app is located at [http://localhost:6543](http://localhost:6543)

Enjoy!

#### Caveats

There are (at least) two known issues you may face when running the **Birdie** app.
 
 - (1) port 6543 is assigned to another app: kill the app or change the port in the `production.ini` and/or `development.ini` file;
 - (2) there is a residual cookie from a previous Birdie installation: delete it within your web browser.  


[ez]:   https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py "ez_setup.py"
[inst]: https://raw.github.com/pypa/pip/master/contrib/get-pip.py       "get-pip.py"
[pip]:  http://www.pip-installer.org/en/latest/index.html       "Pip website"











