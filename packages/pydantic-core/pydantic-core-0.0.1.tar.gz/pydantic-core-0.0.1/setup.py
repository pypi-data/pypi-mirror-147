# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydantic-core',
    'version': '0.0.1',
    'description': 'Placeholder until pydantic-core is released.',
    'long_description': '# pydantic-core\n\nPlaceholder until pydantic-core is released.\n',
    'author': 'Samuel Colvin',
    'author_email': 's@muelcolvin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/samuelcolvin/pydantic-core',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
