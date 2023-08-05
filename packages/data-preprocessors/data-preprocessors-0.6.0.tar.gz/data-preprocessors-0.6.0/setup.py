# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_preprocessors']

package_data = \
{'': ['*']}

install_requires = \
['deep-translator>=1.8.3,<2.0.0',
 'flair>=0.11.1,<0.12.0',
 'nltk>=3.7,<4.0',
 'spacy>=3.2.4,<4.0.0',
 'textblob>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'data-preprocessors',
    'version': '0.6.0',
    'description': 'An easy to use tool for Data Preprocessing specially for Text Preprocessing',
    'long_description': '# Data-Preprocessor\nAn easy to use tool for Data Preprocessing specially for Text Preprocessing\n\n## Installation\nInstall the stable release<br>\nFor windows<br>\n`$ pip install -U data-preprocessors`\n\nFor Linux/WSL2<br>\n`$ pip3 install -U data-preprocessors`\n\n## Quick Start\n```python\nfrom data_preprocessors import text_preprocessor as tp\nsentence = "bla! bla- ?bla ?bla."\nsentence = tp.remove_punc(sentence)\nprint(sentence)\n\n>> bla bla bla bla\n```\n\n',
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MusfiqDehan/data-preprocessors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
