======
skelly
======

Generate a project skeleton so you can start coding right away.

Installation
============

::

  git clone https://gitlab.com/narvin/skelly
  cd skelly
  pip install .

Usage
=====

Once installed, `skelly` can be run as a module:

::

  python -m skelly.main

or as a console application:

::

  skelly

`skelly` has a plugin architecture where `skelly.builders` can be registered to
create different types of projects. The default builder builds Python projects.

Python Project
--------------

Python projects built by the default builder, using its default template, include:

- a `venv` using the Python installation from which `skelly` was invoked
- packaging with `setuptools` configured via `setup.cfg`
- tooling configured via `setup.cfg`

  - code formatting with `black`
  - linting with `pylint`
  - PEP 8 style checking with `pycodestyle`
  - strict type checking with `mypy`
  - unit testing with `pytest`
  - running all of the above tools with `tox`
  - building and uploading a distribution with `build` and `twine`

- the project package, itself, is `pip` installed in the `venv` in editable mode

Prompt the user for values required by the template, then create a project in the
current directory.

::

  skelly

Create a project in the directory `/tmp/mypkg`, without prompting the user because
all of the required template values are provided in the command.

::

  skelly \
    -t author "Narvin Singh" \
    -t email "Narvin.A.Singh@gmail.com" \
    -t description "A sample project." \
    -t repo "https://gitlab.com/narvin/mypkg" \
    /tmp/mypkg

Only prompt the user for the repo, which is required by the template, then create
a project in the current directory.

::

  skelly \
    -t author "Narvin Singh" \
    -t email "Narvin.A.Singh@gmail.com" \
    -t description "A sample project."

This command will raise an error because the repo wasn't specified, and the `-s`
option was used to prevent prompting the user for missing template values.

::

  skelly \
    -s \
    -t author "Narvin Singh" \
    -t email "Narvin.A.Singh@gmail.com" \
    -t description "A sample project."

Create a project in `/tmp/mypkg` with its `venv` in `/tmp/mypkg/.venv310`, and
install the packages specified in `~/requirements.txt` in the `venv`. The `env_dir`
builder option, unless specified as an absolute path, is relative to the `target`
directory. The `req_file` builder option, unless specified as an absolute path,
is relative to the current directory.

::

  cd ~
  skelly \
    -o env_dir .venv310 \
    -o req_file requirements.txt \
    /tmp/mypkg

Create a project in the current directory using a custom template. The user won't
be prompted for any template values.

::

  skelly \
    -p ~/my_template \
    -t my_template_var foo

Other Types of Projects
=======================

Coming soon.

If there was a hypothetical builder called `javascript`, this command would use it
to build a project in the current directory.

::

  skelly -b javascript

