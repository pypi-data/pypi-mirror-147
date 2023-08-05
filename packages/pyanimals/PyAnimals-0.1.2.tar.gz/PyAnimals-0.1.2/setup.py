# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanimals']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyanimals',
    'version': '0.1.2',
    'description': 'Get animal images and facts with easy plug-and-play syntax!',
    'long_description': None,
    'author': 'ksIsCute Cesiyi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
