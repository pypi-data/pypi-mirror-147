# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfig', 'cfig.sample', 'cfig.sources', 'cfig.tests']

package_data = \
{'': ['*']}

install_requires = \
['lazy-object-proxy>=1.7.1,<2.0.0']

extras_require = \
{'cli': ['click>=8.1.2,<9.0.0', 'colorama>=0.4.4,<0.5.0']}

setup_kwargs = {
    'name': 'cfig',
    'version': '0.2.0',
    'description': 'A configuration manager for Python',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
