============
idem-sources
============

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

Generic sls-source plugins for idem

About
=====

This project provides generic sls-sources for idem.
sls-sources can be used to collect ``params`` data or ``state`` definitions.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.6+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-sources``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

  pip install idem-sources

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com/vmware/idem/idem-sources.git
   cd idem-sources

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

SLS sources are directory trees, archives, and remote stores that contain sls files.
SLS and param sources can come from many different places.
The plugins that can be used to process SLS sources are in idem/idem/sls.

The format for an sls sources is:

.. code-block::

    <protocol>://<resource>

The format for authenticated sls sources is:

.. code-block::

    <protocol_plugin>://<acct_profile>@<resource>

The named acct profile associated with the protocol_plugin provider will have it's values passed to ``ctx.acct`` of the appropriate "cache" function.

File sources that have a mimetype, such as zip files, will be unarchived before further processing.

This is an example of an idem config file that specifies ``sls_sources`` and ``param_sources``:

.. code-block:: yaml

    idem:
      sls_sources:
        - file://path/to/sls_tree
        - file://path/to/sls_source.zip
        - git://github.com/my_user/my_project.git
        - git+http://github.com/my_user/my_project.git
        - git+https://github.com/my_user/my_project.git
      param_sources:
        - file://path/to/sls_tree
        - file://path/to/sls_source.zip
        - git://github.com/my_user/my_project.git
        - git+http://github.com/my_user/my_project.git
        - git+https://github.com/my_user/my_project.git

``sls_sources`` and ``param_sources`` can also be specified from the CLI.

.. note

    CLI options override config file definitions.

.. code-block:: bash

    $ idem state my.sls.ref \
          --sls-sources \
          "file://path/to/sls_tree" \
          "file://path/to/sls_source.zip" \
          "git://github.com/my_user/my_project.git" \
          "git+http://github.com/my_user/my_project.git"
          "git+https://github.com/my_user/my_project.git"
          --param-sources \
          "file://path/to/sls_tree" \
          "file://path/to/sls_source.zip" \
          "git://github.com/my_user/my_project.git"
          "git+http://github.com/my_user/my_project.git"
          "git+https://github.com/my_user/my_project.git"

Roadmap
=======

Reference the `open issues <https://gitlab.com/vmware/idem/idem-sources/issues>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
