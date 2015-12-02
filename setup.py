try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description':
    'convert a tropicos export to a Bauble importable json object',
    'author': 'Mario Frasca',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'YoviDiaz',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['taxonlist2json'],
    'scripts': [],
    'name': 'taxonlist2json'
}

setup(**config)
