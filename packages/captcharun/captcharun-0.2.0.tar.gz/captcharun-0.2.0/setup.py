# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captcharun']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'captcharun',
    'version': '0.2.0',
    'description': '',
    'long_description': '# CaptchaRun Python SDK\n',
    'author': 'CaptchaRun',
    'author_email': 'admin@captcha.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://captcha.run',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
