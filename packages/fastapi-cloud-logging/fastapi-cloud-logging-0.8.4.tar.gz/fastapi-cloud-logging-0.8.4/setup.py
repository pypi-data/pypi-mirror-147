# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloud_logging']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.71', 'google-cloud-logging>=3,<4']

setup_kwargs = {
    'name': 'fastapi-cloud-logging',
    'version': '0.8.4',
    'description': 'Cloud Logging For FastAPI',
    'long_description': '# fastapi-cloud-logging\n\n## Installation\n\n```sh\npip install fastapi-cloud-logging\n```\n\n## Usage\n\nAdd middleware and handler to send a request info to cloud logging.\n\n```python\nfrom fastapi import FastAPI\nfrom google.cloud.logging import Client\nfrom google.cloud.logging_v2.handlers import setup_logging\n\nfrom fastapi_cloud_logging import FastAPILoggingHandler, RequestLoggingMiddleware\n\napp = FastAPI()\n\n# Add middleware\napp.add_middleware(RequestLoggingMiddleware)\n\n# Use manual handler\nhandler = FastAPILoggingHandler(Client())\nsetup_logging(handler)\n```\n',
    'author': 'quoth',
    'author_email': '4wordextinguisher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quoth/fastapi-cloud-logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
