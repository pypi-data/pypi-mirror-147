# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymemeru', 'pymemeru.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'httpx>=0.21.0,<0.22.0',
 'lxml>=4.8.0,<5.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pymemeru',
    'version': '0.2.0',
    'description': 'memepedia.ru parser for python',
    'long_description': '# pymemeru\nmemepedia.ru parser for python\n',
    'author': 'Daniel Zakharov',
    'author_email': 'daniel734@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
