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
    'version': '0.4.0',
    'description': 'Type stubs for Pony ORM',
    'long_description': "# Pony stubs\n\nPython type hint stubs for [Pony ORM](https://github.com/ponyorm/pony)\n\n**NOTE:** This project is still very much a WIP, the types shouldn't be expected to be anywhere close to completion.\n\n## Goals\n1. Provide type hints for Pony ORM that support both MyPy and Pyright on their strictest modes\n2. Integrate the contents of this package into the official Pony ORM repository (self-deprecation)\n3. Focus primarily on the aspects that users of Pony ORM most often run into (defining models, querying them etc.)\n\n## Progress so far\n1. Model fields should get dynamically typed correctly by using `Required`, `Set` etc.\n2. Querying models (without using attribute lifting) should be well typed\n\n## Development\nThe development environment for this package requires `poetry` (https://python-poetry.org/docs/master/#installing-with-the-official-installer)\n\nUsing VSCode as the editor is recommended!\n\n### Setting up the repo\n1. Clone the repo\n    - `git clone git@github.com:Jonesus/pony-stubs.git`\n2. Install dependencies\n    - `poetry install`\n3. Install commit hooks\n    - `poetry run pre-commit install --install-hooks`\n4. Type ahead!\n\n## Contributing\nContributions are always most welcome! Please run the pre-commit hooks before setting up a pull request, and in case the Github actions fail, please try to fix those issues so the review itself can go as smoothly as possible\n\n## License\nThis project is licensed under the MIT license (see LICENSE.md)\n",
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
