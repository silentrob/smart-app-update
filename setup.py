#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='gitosis_update_listener',
    version='0.1',
    description='an amqp consumer that watches for git updates from gitosis',
    author='Anders Conbere',
    author_email='aconbere@joyent.com',
    url='http://joyent.com/',
    packages=find_packages(),

    install_requires = [
        #"txamqp >= 1.2.0",
        "twisted >= 8.2.0",
        "simplejson >= 2.0.0",
        ],
      )
