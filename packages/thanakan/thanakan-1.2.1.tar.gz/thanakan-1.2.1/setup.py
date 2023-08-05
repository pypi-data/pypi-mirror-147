# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thanakan',
 'thanakan.models',
 'thanakan.services',
 'thanakan.services.model',
 'thanakan.slip']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'crccheck>=1.0,<2.0',
 'fastapi-utils>=0.2.1,<0.3.0',
 'furl>=2.1.0,<3.0.0',
 'google-cloud-documentai>=1.4.0,<2.0.0',
 'google-cloud-secret-manager>=2.7.2,<3.0.0',
 'httpx-auth>=0.14.1,<0.15.0',
 'httpx>=0.22.0,<0.23.0',
 'locate>=1.1.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'onepasswordconnectsdk>=1.1.0,<2.0.0',
 'parse-with-dot-access>=1.18.0,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyzbar-x>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'thanakan',
    'version': '1.2.1',
    'description': 'Awesome `thanakan` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# thanakan\nPython Interface for Thai Bank API, KBANK, SCB, QR Code and slip verification\n\n## Pre-Requisite\n```\nsudo apt-get install libzbar0\n```\nmore on [pyzbar](https://pypi.org/project/pyzbar/)\n',
    'author': 'codustry',
    'author_email': 'hello@codustry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codustry/thanakan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
