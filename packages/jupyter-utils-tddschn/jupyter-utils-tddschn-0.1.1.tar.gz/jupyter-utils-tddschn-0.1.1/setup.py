# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_utils_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'ipykernel>=6.13.0,<7.0.0',
 'ipython>=8.2.0,<9.0.0',
 'nbformat>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'jupyter-utils-tddschn',
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
