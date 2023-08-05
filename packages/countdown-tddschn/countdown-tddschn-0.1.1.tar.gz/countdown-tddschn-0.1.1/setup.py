# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['countdown_tddschn', 'countdown_tddschn.bin']

package_data = \
{'': ['*']}

install_requires = \
['pync>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'countdown-tddschn',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
