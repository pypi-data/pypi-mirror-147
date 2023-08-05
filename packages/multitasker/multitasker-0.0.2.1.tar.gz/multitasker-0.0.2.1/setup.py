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
['SQLAlchemy>=1.4.35,<2.0.0',
 'gevent>=21.12.0,<22.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=10.6.0,<11.0.0',
 'typer>=0.4.1,<0.5.0',
 'wpy>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['multitasker = multitasker.cli.main:main']}

setup_kwargs = {
    'name': 'multitasker',
    'version': '0.0.2.1',
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
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
