# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workflow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'alfred-workflow-tddschn',
    'version': '0.1.1',
    'description': 'Full-featured helper library for writing Alfred 2/3/4 workflows, with Python 3',
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
