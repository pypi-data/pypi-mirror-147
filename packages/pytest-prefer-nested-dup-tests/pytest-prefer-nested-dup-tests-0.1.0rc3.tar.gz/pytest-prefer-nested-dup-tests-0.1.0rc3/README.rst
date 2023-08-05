pytest-prefer-nested-dup-tests
===================================

by Marximus Maximus (https://www.marximus.com)

.. image:: http://img.shields.io/pypi/v/pytest-prefer-nested-dup-tests.svg
   :target: https://pypi.python.org/pypi/pytest-prefer-nested-dup-tests

.. image:: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/workflows/main/badge.svg
  :target: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/actions

A Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.

By default, when de-duplicating tests, all sub-packages become top level packages. This plugin keeps
the subpackage structure intact.


Installation
------------

You can install via `pip`_ from `PyPI`_::

    $ pip install pytest-prefer-nested-dup-tests


Usage
-----

The plugin is enabled by default, no other action is necessary.


Contributing
------------

Contributions are very welcome.

Development Environment First Time Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install ``conda`` (tested w/ `miniforge`_)

2. ``cd`` into repo directory.

3. Setup conda environment:

    $ conda env create --name pytest-prefer-nested-dup-tests --file ./conda-environment.yml -v

4. Activate conda env:

    $ conda activate pytest-prefer-nested-dup-tests

5. Install dependencies via poetry:

    $ poetry install

6. Pin poetry based dependencies:

    $ poetry show | awk '{if ($1 !~ /six|packaging|pyparsing/ ) {print "pypi::" $1}}' >"$CONDA_PREFIX"/conda-meta/pinned

Development Environment Updating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Update conda env:

    $ conda env update --name "${MY_DIR_BASENAME}" --file ./conda-environment.yml --prune -v

2. Update additional dependencies via poetry:

    $ poetry install

3. Pin poetry based dependencies:

    $ poetry show | awk '{if ($1 !~ /six|packaging|pyparsing/ ) {print "pypi::" $1}}' >"$CONDA_PREFIX"/conda-meta/pinned


Moving Forward Dependencies' Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Conda:
  - Manually update version pins in conda-environment.yml
- Poetry:
  - Option 1: Manually update dependencies in pyproject.toml
  - Option 2: Use ``poetry update`` command.

Testing
^^^^^^^

A cross-python version test matrix can be run locally with `tox`_:

    $ tox

Current python version only tests can be run locally with `pytest`_:

    $ pytest


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-prefer-nested-dup-tests" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Like My Work & Want To Support It?
----------------------------------

- Main Website: https://www.marximus.com
- Patreon (On Going Support): https://www.patreon.com/marximus
- Ko-fi (One Time Tip): https://ko-fi.com/marximusmaximus


.. _`file an issue`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/issues
.. _`miniforge`: https://github.com/conda-forge/miniforge
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
