# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gmn_data_store']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.35',
 'click>=7.1.2,<8.0.0',
 'gmn-python-api==0.0.4',
 'sqlalchemy-views==0.3.1']

entry_points = \
{'console_scripts': ['gmn-data-store = gmn_data_store.__main__:main']}

setup_kwargs = {
    'name': 'gmn-data-store',
    'version': '0.0.1',
    'description': 'GMN Data Store',
    'long_description': 'GMN Data Store\n==============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/gmn-data-store.svg\n   :target: https://pypi.org/project/gmn-data-store/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/gmn-data-store.svg\n   :target: https://pypi.org/project/gmn-data-store/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/gmn-data-store\n   :target: https://pypi.org/project/gmn-data-store\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/gmn-data-platform/gmn-data-store\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/gmn-data-store/latest.svg?label=Read%20the%20Docs\n   :target: https://gmn-data-store.readthedocs.io/\n   :alt: Read the documentation at https://gmn-data-store.readthedocs.io/\n.. |Tests| image:: https://github.com/gmn-data-platform/gmn-data-store/workflows/Tests/badge.svg\n   :target: https://github.com/gmn-data-platform/gmn-data-store/actions?query=workflow%3ATests+branch%3Amain\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/gmn-data-platform/gmn-data-store/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/gmn-data-platform/gmn-data-store\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n`Global Meteor Network`_ (GMN) database models, controllers and scripts.\n\n\nRequirements\n------------\n\n* Python 3.7, 3.8, 3.9 or 3.10\n\n\nInstallation\n------------\n\nYou can install *GMN Data Store* via pip_ from `PyPI`_:\n\n.. code:: console\n\n   $ pip install gmn-data-store\n\nOr for the latest development code, through TestPyPI_ or directly from GitHub_ via pip_:\n\n.. code:: console\n\n   $ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-data-store==<version>\n   Or\n   $ pip install git+https://github.com/gmn-data-platform/gmn-data-store\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*GMN Data Store* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\n`Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/project/gmn-data-store/\n.. _TestPyPI: https://test.pypi.org/project/gmn-data-store/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/rickybassom/gmn-data-store/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://gmn-data-store.readthedocs.io/en/latest/usage.html\n.. _Global Meteor Network: https://globalmeteornetwork.org/\n.. _GitHub: https://github.com/gmn-data-platform/gmn-data-store\n',
    'author': 'Ricky Bassom',
    'author_email': 'rickybas12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rickybassom/gmn-data-store',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
