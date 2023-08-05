# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_randomtkk']

package_data = \
{'': ['*'], 'nonebot_plugin_randomtkk': ['resource/*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0',
 'pillow>=9.0.1,<10.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-randomtkk',
    'version': '0.1.1',
    'description': 'Find Tan Kuku!',
    'long_description': None,
    'author': 'KafCoppelia',
    'author_email': 'k740677208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
