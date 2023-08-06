# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['euler_math']

package_data = \
{'': ['*']}

install_requires = \
['gmpy2>=2.1.2,<3.0.0', 'numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'euler-math',
    'version': '0.4.3',
    'description': 'Utilities for Project Euler',
    'long_description': 'euler-math\n==========\n\nUtility methods for Project Euler\n\nInstallation\n------------\n\npip install euler-math',
    'author': 'David Carlson',
    'author_email': 'mndrake2222@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mndrake/euler-math',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
