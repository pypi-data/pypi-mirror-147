# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['snalnaya_akrepka']
setup_kwargs = {
    'name': 'snalnaya-akrepka',
    'version': '0.1.0',
    'description': 'Clip say message',
    'long_description': None,
    'author': 'fit4a-m',
    'author_email': 'andrey.maslov2005@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
