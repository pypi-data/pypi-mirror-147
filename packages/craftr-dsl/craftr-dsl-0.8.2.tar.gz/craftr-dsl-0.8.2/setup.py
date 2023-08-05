# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsl']

package_data = \
{'': ['*']}

install_requires = \
['nr.util>=0.7.0,<1.0.0', 'termcolor>=1.1.0,<2.0.0', 'typing-extensions>=3.0.0']

setup_kwargs = {
    'name': 'craftr-dsl',
    'version': '0.8.2',
    'description': 'Domain specific language for the Craftr build system.',
    'long_description': '# craftr-dsl\n\nA domain specific language purpose-built for the Craftr build system.\n\nThe Craftr DSL is an "almost superset" of Python 3; adding a lot of syntactical features that make it more\nconvenient to describe build configurations at the cost of some other syntax features of the native Python\nlanguage (like set literals).\n\n## Installation\n\n    $ pip install craftr-dsl\n\nThe `craftr-dsl` package requires at least Python 3.8.\n\n## Projects using Craftr DSL\n\n* [Novella](https://niklasrosenstein.github.io/novella/)\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
