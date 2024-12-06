Development
===========

This guide will help you set up your development environment and contribute to the project.

Setting Up Development Environment
-----------------------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/argearriojas/singlecell-cookbook.git
       cd singlecell-cookbook

2. Create the development environment:

   Using venv:

   .. code-block:: bash

       python -m venv .venv
       source .venv/bin/activate
       pip install -e ".[dev]"

   Using conda:

   .. code-block:: bash

       conda env create --file environment.yml
       conda activate singlecell-cookbook

Code Style and Formatting
-------------------------

This project uses Ruff for code formatting and linting. The configuration is in ``ruff.toml``,
which specifies:

- Line length of 88 characters
- Double quotes for strings
- 4-space indentation
- Other Python code style rules

Editor Setup
------------

While you can use any editor, here are the minimal recommended settings for popular editors:

VSCode
~~~~~~

1. Install the Ruff extension
2. Configure formatting:

   .. code-block:: json

       {
           "[python]": {
               "editor.formatOnSave": true,
               "editor.defaultFormatter": "charliermarsh.ruff",
               "editor.codeActionsOnSave": {
                   "source.fixAll": "explicit",
                   "source.organizeImports": "explicit"
               }
           }
       }

PyCharm
~~~~~~~

1. Install the Ruff plugin
2. Enable "Format on Save"
3. Set Ruff as the default formatter

Running Tests
-------------

To run the tests:

.. code-block:: bash

    pytest tests/

Version Management
------------------

This project uses `bump2version` for version management. To bump the version:

1. For a patch release (bug fixes):

   .. code-block:: bash

       bump2version patch

2. For a minor release (new features, backwards compatible):

   .. code-block:: bash

       bump2version minor

3. For a major release (breaking changes):

   .. code-block:: bash

       bump2version major

This will:
- Update version numbers in all configured files
- Create a git commit with the version change
- Create a git tag for the new version

Building Documentation
----------------------

To build the documentation:

.. code-block:: bash

    cd docs
    make html

The built documentation will be in ``docs/build/html``.
