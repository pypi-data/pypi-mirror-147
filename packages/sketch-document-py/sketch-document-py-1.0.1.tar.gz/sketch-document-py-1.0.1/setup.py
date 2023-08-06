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
    'version': '1.0.1',
    'description': 'This project contains the APIs to work with Sketch documents and document elements in Python dataclass.',
    'long_description': '# `.sketch` document for python\n\n[Sketch](https://sketch.com) stores documents in `.sketch` format, a zipped\narchive of JSON formatted data and binary data such as images.\n\nInspired by [sketch-hq/sketch-document](https://github.com/sketch-hq/sketch-document)\n\n## Sketch file format schemas and APIs.\n\nThis project contains the APIs to work with Sketch\ndocuments and document elements in Python dataclass.\n\n- `sketch-file-format-py`: Python dataclass type hint to strongly type objects\n  representing Sketch documents, or fragments of Sketch documents in TypeScript\n  projects.\n- `sketch-file`: Python APIs to read and write `.sketch` files.\n\n## Development\n\nTo build this project, you need install Python build dependency management tool [Poetry](https://python-poetry.org/), to install Poetry , follow [Poetry installation guide](https://python-poetry.org/docs/#installation)\n\nTo install nessasary deps and CLI tools, including a task runner [Poe the Poet](https://github.com/nat-n/poethepoet)(CLI executable named `poe`) that work with Poetry, run command:\n```shell\npoetry install\n```\n\nTo generate Sketch Dataclass type file, which is nessasary for build or install development, run command:\n```shell\npoe gen_types\n```\n\n\n\nFor further usages of Poetry, check [Poetry Documentation](https://python-poetry.org/docs)\nFor further usages of Poe the Poet,  check [Poe the Poet Homepage](https://github.com/nat-n/poethepoet)\n\n',
    'author': 'Borealin',
    'author_email': 'shichuning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Borealin/sketch-document-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
