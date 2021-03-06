#!/usr/bin/env python
from setuptools import setup, find_packages

# I'm pretty unexperienced in writing setup.py. Will welcome advices, thanks.

setup(name='useful',
      version='0.5',
      packages=find_packages(),
      package_data={'useful': ['django/locale/cs/LC_MESSAGES/django.*']},
      description = "Everyday use utilities for writing Python/Django apps",
      author = "Vlada Macek",
      author_email = "macek@sandbox.cz",
      url = "https://github.com/tuttle/python-useful",
)
