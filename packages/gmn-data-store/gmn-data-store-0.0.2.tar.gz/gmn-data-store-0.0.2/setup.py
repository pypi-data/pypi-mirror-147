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
 'click==8.0.4',
 'gmn-python-api==0.0.5',
 'sqlalchemy-views==0.3.1']

entry_points = \
{'console_scripts': ['gmn-data-store = gmn_data_store.__main__:main']}

setup_kwargs = {
    'name': 'gmn-data-store',
    'version': '0.0.2',
    'description': 'GMN Data Store',
    'long_description': 'GMN Data Store\n==============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/gmn-data-store.svg\n   :target: https://pypi.org/project/gmn-data-store/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/gmn-data-store.svg\n   :target: https://pypi.org/project/gmn-data-store/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/gmn-data-store\n   :target: https://pypi.org/project/gmn-data-store\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/gmn-data-platform/gmn-data-store\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/gmn-data-store/latest.svg?label=Read%20the%20Docs\n   :target: https://gmn-data-store.readthedocs.io/\n   :alt: Read the documentation at https://gmn-data-store.readthedocs.io/\n.. |Tests| image:: https://github.com/gmn-data-platform/gmn-data-store/workflows/Tests/badge.svg\n   :target: https://github.com/gmn-data-platform/gmn-data-store/actions?query=workflow%3ATests+branch%3Amain\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/gmn-data-platform/gmn-data-store/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/gmn-data-platform/gmn-data-store\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n`Global Meteor Network`_ (GMN) database models, controllers and scripts.\n\nThis project stores GMN meteor data in a relational SQLite database where the database schema is generated using the gmn-python-api_ library. The Python package provided here is used by the `GMN Data Store Ingestion`_ to add/update data in the database. A Datasette_ instance is run for the `GMN Data Portal`_ and it accesses this data to provide user-facing data select querying and a web interface to view the data.\n\n`Database entity relationship diagram`_\n\nThe Python package gmn-data-store provides functions for setting up the database, querying data in the database and inserting data into the database. The main insert function is insert_trajectory_summary which takes an AVRO formatted JSON dictionary of meteor trajectory data (more info in the `gmn-python-api docs`_) and inserts the data into the database. The `GMN Data Store Ingestion`_ project inserts trajectory summary Kafka messages using this function.\n\nA Makefile_ is also provided to initially setup the database using Docker. Use the init_all_services Makefile task to create the .db file and the gmn_data_store Docker volume. By default the gmn-data-store package gets the .db file from ~/.gmn_data_store/gmn_data_store.db so mount the volume at ~/gmn_data_store to use the Python package with the .db file in the Docker volume (example_).\n\nRequirements\n------------\n\n* Python 3.7.1+, 3.8, 3.9 or 3.10\n\n\nInstallation\n------------\n\nYou can install *GMN Data Store* via pip_ from `PyPI`_:\n\n.. code:: console\n\n   $ pip install gmn-data-store\n\nOr for the latest development code, through TestPyPI_ or directly from GitHub_ via pip_:\n\n.. code:: console\n\n   $ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-data-store==<version>\n   Or\n   $ pip install git+https://github.com/gmn-data-platform/gmn-data-store\n\n\nUsage\n-----\n\nTo create the .db SQLite file and gmn_data_store Docker volume:\n\n.. code:: console\n\n   $ make DB_DIR="<local target dir>" init_all_services\n\nSee the Makefile for more provided tasks.\n\nRefer to the `docs API reference page`_ for function and variable definitions.\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*GMN Data Store* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\n`Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/project/gmn-data-store/\n.. _TestPyPI: https://test.pypi.org/project/gmn-data-store/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/rickybassom/gmn-data-store/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://gmn-data-store.readthedocs.io/en/latest/usage.html\n.. _Global Meteor Network: https://globalmeteornetwork.org/\n.. _GitHub: https://github.com/gmn-data-platform/gmn-data-store\n.. _docs API reference page: https://gmn-data-store.readthedocs.io/en/latest/autoapi/gmn_data_store/index.html\n.. _gmn-python-api: https://github.com/gmn-data-platform/gmn-python-api\n.. _Datasette: https://datasette.io/\n.. _GMN Data Portal: https://github.com/gmn-data-platform/gmn-data-endpoints/tree/main/services/gmn_data_portal\n.. _GMN Data Store Ingestion: https://github.com/gmn-data-platform/gmn-data-store-ingestion\n.. _GMN Data Platform: https://github.com/gmn-data-platform\n.. _gmn-python-api docs: https://gmn-python-api.readthedocs.io/en/latest/search.html?q=avro&check_keywords=yes&area=default\n.. _functions: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/meteor_summary_reader/index.html#gmn_python_api.meteor_summary_reader.read_meteor_summary_csv_as_dataframe\n.. _Makefile: https://github.com/gmn-data-platform/gmn-data-store/blob/main/Makefile\n.. _Database entity relationship diagram: https://github.com/gmn-data-platform/gmn-data-store/blob/main/database_schema.md\n.. _example: https://github.com/gmn-data-platform/gmn-data-store-ingestion/blob/2104c97d767a9ef82f0f9a1948bd25c2f7712b01/services/kafka_database_sink/docker-compose.yaml#L11\n',
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
