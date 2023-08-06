# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mognet',
 'mognet.app',
 'mognet.backend',
 'mognet.broker',
 'mognet.cli',
 'mognet.context',
 'mognet.decorators',
 'mognet.exceptions',
 'mognet.middleware',
 'mognet.model',
 'mognet.primitives',
 'mognet.service',
 'mognet.state',
 'mognet.tasks',
 'mognet.testing',
 'mognet.tools',
 'mognet.tools.backports',
 'mognet.worker']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.8.0,<7.0.0',
 'aioredis[hiredis]>=2.0.0,<3.0.0',
 'aiorun>=2021.10.1,<2022.0.0',
 'pydantic>=1.8.0,<2.0.0',
 'tabulate>=0.8.0,<0.9.0',
 'treelib>=1.6.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=3.10.0.0']}

entry_points = \
{'console_scripts': ['mognet = mognet.cli.main:main']}

setup_kwargs = {
    'name': 'mognet',
    'version': '1.3.1',
    'description': '',
    'long_description': None,
    'author': 'André Carvalho',
    'author_email': 'afecarvalho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
