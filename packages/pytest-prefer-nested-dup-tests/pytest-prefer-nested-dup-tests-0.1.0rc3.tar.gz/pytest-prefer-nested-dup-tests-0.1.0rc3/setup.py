# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_prefer_nested_dup_tests']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.1,<8.0.0']

entry_points = \
{'pytest11': ['prefer-nested-dup-tests = pytest_prefer_nested_dup_tests']}

setup_kwargs = {
    'name': 'pytest-prefer-nested-dup-tests',
    'version': '0.1.0rc3',
    'description': 'A Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.',
    'long_description': 'pytest-prefer-nested-dup-tests\n===================================\n\nby Marximus Maximus (https://www.marximus.com)\n\n.. image:: http://img.shields.io/pypi/v/pytest-prefer-nested-dup-tests.svg\n   :target: https://pypi.python.org/pypi/pytest-prefer-nested-dup-tests\n\n.. image:: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/workflows/main/badge.svg\n  :target: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/actions\n\nA Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.\n\nBy default, when de-duplicating tests, all sub-packages become top level packages. This plugin keeps\nthe subpackage structure intact.\n\n\nInstallation\n------------\n\nYou can install via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-prefer-nested-dup-tests\n\n\nUsage\n-----\n\nThe plugin is enabled by default, no other action is necessary.\n\n\nContributing\n------------\n\nContributions are very welcome.\n\nDevelopment Environment First Time Setup\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n1. Install ``conda`` (tested w/ `miniforge`_)\n\n2. ``cd`` into repo directory.\n\n3. Setup conda environment:\n\n    $ conda env create --name pytest-prefer-nested-dup-tests --file ./conda-environment.yml -v\n\n4. Activate conda env:\n\n    $ conda activate pytest-prefer-nested-dup-tests\n\n5. Install dependencies via poetry:\n\n    $ poetry install\n\n6. Pin poetry based dependencies:\n\n    $ poetry show | awk \'{if ($1 !~ /six|packaging|pyparsing/ ) {print "pypi::" $1}}\' >"$CONDA_PREFIX"/conda-meta/pinned\n\nDevelopment Environment Updating\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n1. Update conda env:\n\n    $ conda env update --name "${MY_DIR_BASENAME}" --file ./conda-environment.yml --prune -v\n\n2. Update additional dependencies via poetry:\n\n    $ poetry install\n\n3. Pin poetry based dependencies:\n\n    $ poetry show | awk \'{if ($1 !~ /six|packaging|pyparsing/ ) {print "pypi::" $1}}\' >"$CONDA_PREFIX"/conda-meta/pinned\n\n\nMoving Forward Dependencies\' Versions\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n- Conda:\n  - Manually update version pins in conda-environment.yml\n- Poetry:\n  - Option 1: Manually update dependencies in pyproject.toml\n  - Option 2: Use ``poetry update`` command.\n\nTesting\n^^^^^^^\n\nA cross-python version test matrix can be run locally with `tox`_:\n\n    $ tox\n\nCurrent python version only tests can be run locally with `pytest`_:\n\n    $ pytest\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-prefer-nested-dup-tests" is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n\nLike My Work & Want To Support It?\n----------------------------------\n\n- Main Website: https://www.marximus.com\n- Patreon (On Going Support): https://www.patreon.com/marximus\n- Ko-fi (One Time Tip): https://ko-fi.com/marximusmaximus\n\n\n.. _`file an issue`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/issues\n.. _`miniforge`: https://github.com/conda-forge/miniforge\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`pip`: https://pypi.python.org/pypi/pip/\n.. _`PyPI`: https://pypi.python.org/pypi\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.org/en/latest/\n',
    'author': 'Marximus Maximus',
    'author_email': 'marximus@marximus.com',
    'maintainer': 'Marximus Maximus',
    'maintainer_email': 'marximus@marximus.com',
    'url': 'https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
