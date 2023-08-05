# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multitasker',
 'multitasker.cli',
 'multitasker.common',
 'multitasker.models',
 'multitasker.multi_worker']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0', 'rich>=12.2.0,<13.0.0', 'wpy>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'multitasker',
    'version': '0.0.2',
    'description': '多任务处理器',
    'long_description': None,
    'author': 'wxnacy',
    'author_email': 'wxnacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
