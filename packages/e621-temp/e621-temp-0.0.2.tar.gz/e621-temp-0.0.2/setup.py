# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e621']

package_data = \
{'': ['*']}

install_requires = \
['backports.cached-property>=1.0.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'e621-temp',
    'version': '0.0.2',
    'description': 'e621.net API wrapper written in Python',
    'long_description': '# e621\ne621 is a low-level e621.net API wrapper written for Python.\n\n# Requirements\n+ Python 3.6\n+ requests\n+ json\n\n# Installation\n\n## From master branch\n```bash\n$ git clone https://github.com/PatriotRossii/e621-py.git \n$ pip install -e e621-py\n``` \n\n## From PyPi\n```bash\n$ pip install e621\n```\n',
    'author': 'PatriotRossii',
    'author_email': 'patriotrossii2019@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PatriotRossii/e621-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
