Birdie
==================

The micro-blogging app for educational purpose.

The current implementation is powered by the *Pyramid* web development framework for Python.
Ingredients of the soup are the *Chameleon* template framework, *SQLAlchemy* ORM, *Twitter-bootstrap* for CSS.

Fragments of the source code comes from a previous [**Birdie** implementation](https://github.com/cguardia/Pyramid-Tutorial/tree/master/src/stage3) of [Carlos de la Guardia](https://github.com/cguardia/). Actually, it essentially remains the original idea and terms (**Birdie** and *chirp*) in the project.

**Birdie** is distributed under the permissive MIT license (see `LICENSE` text for details).

Python package dependencies are listed under the `requires` label in the `setup.py` configuration file.


Getting Started
---------------

First, download the zip file of the birdie project from the [github repos](https://github.com/gr-/birdie).

If required, don't forget to assign the `https_proxy` variable to the URL of your own proxy server:

    > export https_proxy=http://<url-of-your-proxy-server>:<port>


## INSTALL FOR PEOPLE IN A HURRY

The following two series of commands are a shorthand for the all install procedure (see below). 

Create and set up the python virtual environment:

    > pyvenv venv
	> source venv/bin/activate

Install **Birdie** requirements (package dependencies) and the app itself in `develop` mode:

	> unzip birdie-<ver>.zip
	> cd <path to this README.md file>
	> python setup.py develop
	> initialize_birdie_db development.ini
	> pserve development.ini --reload

Check for successful installation at [http://localhost:6543](http://localhost:6543)

## INSTALL FOR THE OTHERS

Birdie was developed with the python 3.3+ interpreter. It is then fully compliant with any python 3 branch.
As the cherry on top, some users report that they have successfully experienced python 2.7+ environments.


### Setting up a virtual environment

To set-up a **Birdie** instance, it is warmly recommended to create a python virtual runtime environment first. This sandbox
isolates python binaries, packages and various settings for **Birdie** and prevent from conflicts with pre-existing settings.

For any python <=3.2 box, it requires the `virtualenv` command. The almost out-of-the-box virtualenv is provided [there](https://pypi.python.org/pypi/virtualenv). You have to deploy a virtualenv this way:

    > virtualenv -p /path/to/python3 venv
    > source venv/bin/activate

Then, you can directly jump to the Birdie Install section.

Otherwise, with python3.3+ the-newly-preferred way is the `pyvenv` library and its command-line counterpart:

    > pyvenv venv
    > source venv/bin/activate

To check for success, the `which python` command must answer something like `/path/to/venv/venv/bin/python` rather than the
system-wide python binary (`/usr/bin` for most of the *ix boxes). Actually, you are free to set a different name for `venv`
and to put that directory anywhere on your local file system.


Next, the **setuptools** utility suite is required in this freshly activated environment. Depending on your bare metal python version,
either you already have it in your virtual environment (with virtualenv or pyvenv from python>=3.4), or you could follow the
instructions from the [PyPi repos entry](https://pypi.python.org/pypi/setuptools) (with python<3.4).

From now on, you are done with a fully functional python3 runtime environment. 

### Birdie install

Install procedure is deadly easy. You have to decide for development or (limited) production instance and follow the directions below.

#### Development mode

Install dependencies in the site-package directory of the sandbox, and basically deploy the package of the app itself in a way that it can still be edited directly from its source checkout:

    > python setup.py develop

Then you have to initialize the database (sqlite backend) creating the required schema for the app model: 

	> initialize_birdie_db development.ini

Ultimately, the *waitress* web server is invoked with all the settings in the *wsgi* server configuration section of the `development.ini` file, to serve the web pages of the **Birdie** app:  

    > pserve development.ini --reload

The `--reload` option allows to update the source code and immediately (by refreshing the web page) observe the modifications on the running instance.

#### Production mode

It roughly works the same way than the development mode (see above).

    > python setup.py install
	> initialize_birdie_db production.ini
    > pserve production.ini


Whatever your decision, an instance of the **Birdie** web app is located at [http://localhost:6543](http://localhost:6543)

Enjoy!

#### Caveats

There are (at least) two known issues you may face when running the **Birdie** app.
 
 1. port 6543 is assigned to another app: kill the app or change the port in the `production.ini` and/or `development.ini` file;
 2. there is a residual cookie from a previous Birdie installation: delete it within your web browser.  











