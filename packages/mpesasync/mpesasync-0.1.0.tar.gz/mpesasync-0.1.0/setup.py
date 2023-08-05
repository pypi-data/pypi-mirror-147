# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mpesasync', 'mpesasync.contracts', 'mpesasync.mpesa_business']

package_data = \
{'': ['*'], 'mpesasync': ['certificates/*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'httpx>=0.19.0,<0.20.0',
 'pydantic>=1.8.2,<2.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'mpesasync',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pius Dan',
    'author_email': 'npiusdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
