# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=3,<4', 'sphinx-redactor-theme>=0.0.1,<0.0.2']}

setup_kwargs = {
    'name': 'space-classy',
    'version': '0.1',
    'description': 'classification tool for minor bodies using reflectance spectra and visual albedos',
    'long_description': '[![arXiv](https://img.shields.io/badge/arXiv-2203.11229-f9f107.svg)](https://arxiv.org/abs/2203.11229) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/classy/main/docs/gfx/logo_classy.png">\n</p>\n\nThe `classy` classification tool for minor bodies of the Solar System will be made available upon acceptance of article.\n\nIn the meantime, you can have a look at the [preprint](https://arxiv.org/abs/2203.11229).\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmahlke/classy',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
