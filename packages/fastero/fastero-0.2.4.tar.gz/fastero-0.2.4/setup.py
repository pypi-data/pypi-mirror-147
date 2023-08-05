# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastero']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.2',
 'prompt_toolkit==3.0.29',
 'ptpython==3.0.20',
 'rich-click==1.3.0',
 'rich==12.2.0']

extras_require = \
{'export': ['matplotlib', 'numpy', 'pillow', 'pyyaml', 'selenium']}

setup_kwargs = {
    'name': 'fastero',
    'version': '0.2.4',
    'description': 'Python timeit CLI for the 21st century.',
    'long_description': None,
    'author': 'Wasi Master',
    'author_email': 'arianmollik323@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fastero.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
