try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'An engine for building text adventure or command line games in python.',
	'author': 'Brandon Keith Biggs',
	'url': 'Url to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'brandonkeithbiggs@gmail.com',
	'version': '0.01a',
	'install_requires': [''],
	'packages': ['pytgame'],
	'scripts': [],
	'name': 'Py T Game'
	}


setup(**config)