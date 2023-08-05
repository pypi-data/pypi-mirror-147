# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.helper', 'berhoel.helper.test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bhoelhelper',
    'version': '1.2.3',
    'description': 'Misc helper functionalities.',
    'long_description': '====================\n bhoelHelper module\n====================\n\nSome helper modules used in my other modules.\n\nInstallation\n============\n\npip install bhoelHelper\n\nAvailability\n============\n\nThe latest version should be available at my `GitLab\n<https://gitlab.com/berhoel/python/bhoelHelper.git>`_ repository, the\npackage is avaliable at `pypi\n<https://pypi.org/project/bhoelHelper/>`_ via ``pip install\nbhoelHelper``.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berhoel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python.xn--hllmanns-n4a.de/bhoelHelper/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.6,<4.0',
}


setup(**setup_kwargs)
