# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['js', 'js.typeahead']

package_data = \
{'': ['*'], 'js.typeahead': ['resources/js/*']}

install_requires = \
['fanstatic>=1.2,<2.0', 'js.jquery>=3.3.1,<4.0.0']

entry_points = \
{'fanstatic.libraries': ['js_typeahead = js.typeahead:lib']}

setup_kwargs = {
    'name': 'js.typeahead',
    'version': '0.11.1',
    'description': "Fanstatic Package of Twitter's Typeadhead.js",
    'long_description': None,
    'author': 'Manuel Vázquez Acosta',
    'author_email': 'manuel@merchise.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/merchise-autrement/js.typeahead',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
