# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvplus', 'cvplus.cli', 'cvplus.gui', 'cvplus.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'Shapely>=1.8.1,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'cvplus',
    'version': '0.1.1',
    'description': 'CV Tools',
    'long_description': None,
    'author': 'Daiju Watanabe',
    'author_email': '11362284+daizyu@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
