# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['costack_sdk',
 'costack_sdk.costack_temporal_sdk',
 'costack_sdk.costack_temporal_sdk.context',
 'costack_sdk.lambda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'costack-sdk',
    'version': '0.1.1',
    'description': 'the sdk to support lambda workflows and seamless integrations',
    'long_description': None,
    'author': 'perseus.yang',
    'author_email': 'ry82@cornell.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
