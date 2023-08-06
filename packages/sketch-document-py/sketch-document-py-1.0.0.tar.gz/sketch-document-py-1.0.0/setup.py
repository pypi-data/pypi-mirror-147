# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sketch_document_py',
 'sketch_document_py.sketch_file',
 'sketch_document_py.sketch_file_format']

package_data = \
{'': ['*']}

install_requires = \
['fastclasses-json>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'sketch-document-py',
    'version': '1.0.0',
    'description': 'This project contains the APIs to work with Sketch documents and document elements in Python dataclass.',
    'long_description': None,
    'author': 'Borealin',
    'author_email': 'shichuning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
