# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pony-stubs']

package_data = \
{'': ['*'],
 'pony-stubs': ['flask/*',
                'orm/*',
                'orm/dbproviders/*',
                'orm/integration/*',
                'thirdparty/*',
                'utils/*']}

setup_kwargs = {
    'name': 'pony-stubs',
    'version': '0.1.0',
    'description': 'Type stubs for Pony ORM',
    'long_description': None,
    'author': 'Joonas Palosuo',
    'author_email': 'joonas.palosuo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
