#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

import birdie_stress

setup(
    name='birdie_stress',
    version=birdie_stress.__version__,
    packages=find_packages(),
    author="gr-",
    author_email="",
    description="Stress test suite for Birdie app powerded by locust.io",
    long_description=long_description,
    install_requires= [ 'locustio',
                        'pyzmq',
                        'SQLAlchemy>=0.8',
                        'requests',
                        'loremipsum',
                        'beautifulsoup4',],
    include_package_data=True,
    url='http://github.com/gr-/b',
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Intended Audience :: Education",
    ],
    entry_points = {
        'console_scripts': [
            'initialize_fakedb = birdie_stress.utils:populate_db',
        ],
    },
 
    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    license="WTFPL",
 
    # Il y a encore une chiée de paramètres possibles, mais avec ça vous
    # couvrez 90% des besoins
 
)