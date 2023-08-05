# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanimals']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyanimals',
    'version': '0.1.4',
    'description': 'Get animal images and facts with easy plug-and-play syntax!',
    'long_description': '# PyAnimals\n*Created by Cesiyi and KsIsCute*\n\n## Examples:\n\n```py\nimport PyAnimals # Importing the library\npicture = PyAnimals.picture("dog") # Get a dog picture\nprint(picture) # Print the link to the required picture',
    'author': 'Cesiyi, ksIsCute',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ksIsCute/PyAnimals',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
