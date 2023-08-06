# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thoth', 'thoth.handler']

package_data = \
{'': ['*'], 'thoth': ['static/*', 'static/text/dt/*']}

install_requires = \
['click>=8.0,<9.0',
 'graphviz>=0.18,<1.0',
 'isort>=5.10,<6.0',
 'jsonschema==3.2',
 'pandas>=1.3.4,<1.4.0',
 'scikit-learn>=1.0.1,<1.1.0',
 'streamlit>=1.8,<2.0',
 'watchdog>=2.1.6,<2.2.0']

extras_require = \
{':extra == "docs"': ['mkdocstrings[python]>=0.18.1,<0.19.0'],
 'docs': ['mkdocs>=1.3.0,<1.4.0',
          'mkdocs-material>=8.2.9,<8.3.0',
          'mkdocs-include-markdown-plugin>=3.3.0,<3.4.0',
          'mkdocs-click>=0.5.0,<0.6.0']}

entry_points = \
{'console_scripts': ['thoth = thoth.cli:thoth']}

setup_kwargs = {
    'name': 'thoth-ml',
    'version': '0.1.0',
    'description': 'Interactive playground for machine learning',
    'long_description': "# Thoth 𓅝\n\nThoth is designed to be an interactive explanation of a number of common Machine Learning methods. Built upon [Streamlit](https://www.streamlit.io/), Thoth offers an intuitive way to understand and experiment with fundamental AI tools and methods.\n\n## Installation\n\nThe easiest way to get started with Thoth is through [pipx](https://pypa.github.io/pipx/). Once you have installed pipx by following their installation instructions, you can install Thoth by running the following command:\n\n```bash\npipx install thoth-ml\n```\n\nAlternatively, if you don't need Thoth to be installed in its own environment, then you can simply install it with pip\n\n```bash\npip install --user thoth-ml\n```\n\nYou can then start the Thoth application by simply running the following:\n\n```bash\nthoth\n```\n\n<!-- End Inclusion -->\n\nFor more information please see [the full documentation!](https://thoth-ml.readthedocs.io/en/latest/)",
    'author': 'Felix Lonergan Corti',
    'author_email': 'felix.lonergan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://thoth-ml.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
