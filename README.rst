Scanline Python Wrapper
=======================

|Github| |Discord| |PYPI Version| |Build Status| |Black| |License|

Scanline Python Wrapper is a wrapper library for the scanline_ CLI tool.

Scanline is a CLI tool to scan documents on macOS through Apple's Image Capture
Core API.


Install
-------

You should install the scanline_ tool first. Jut follow instructions from its
README:

* https://github.com/klep/scanline?tab=readme-ov-file#installing-scanline

Then install ``scanline-python-wrapper`` from PyPI::

    pip install scanline-python-wrapper


Usage
-----

List scanners:

.. code-block:: python

   >>> import scanline_wrapper
   >>> scanline_wrapper.list_scanners()
   ... ['HP Color LaserJet MFP M281fdw (035F4A)', 'My other scanner']

Scan a document:

.. code-block:: python

   >>> import scanline_wrapper
   >>> scanline_wrapper.scan_flatbed("./out.tiff")

Scan a document (more options):

.. code-block:: python

   >>> import scanline_wrapper
   >>> scanline_wrapper.scan_flatbed(
   >>>     "./out.jpg",
   >>>     scanner="HP Color LaserJet MFP M281fdw (035F4A)",
   >>>     page_size=scanline_wrapper.PageSize.LETTER,        # A4, LEGAL or LETTER
   >>>     file_format=scanline_wrapper.FileFormat.JPEG,      # AUTO, PDF, TIFF or JPEG
   >>>     color=scanline_wrapper.Color.COLOR,                # COLOR or MONOCHROME
   >>>     resolution=150,                                    # DPI
   >>> )

Complete documentation:

* https://wanadev.github.io/scanline-python-wrapper/


Development
-----------

To run development commands, you must install `Nox <https://nox.thea.codes>`__ first::

    pip install nox


Lint
~~~~


To lint the code, run the following command::

    nox -s lint

To fix codding style, run::

    nox -s black_fix


Run tests
~~~~~~~~~

To run the tests, use::

    nox -s test

You can use following commands to run the tests only on a certain Python version (the corresponding Python interpreter must be installed on your machine)::

    nox -s test-3.8
    nox -s test-3.9
    nox -s test-3.10
    nox -s test-3.11
    nox -s test-3.12


Build the documentation
~~~~~~~~~~~~~~~~~~~~~~~

To build the Sphinx documentation, run::

    nox -s gendoc


License
-------

* This wrapper is licensed under the `BSD 3 Clause license <https://github.com/wanadev/scanline-python-wrapper/blob/master/LICENSE>`__
* The Scanline CLI tool is licensed under the `MIT license <https://github.com/klep/scanline/blob/master/LICENSE>`__


Changelog
---------

* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet ;)

* **v1.0.0:**

  * First release
  * feat: List available scanners
  * feat: Scan a document using a flatbed scanner


.. _scanline: https://github.com/klep/scanline

.. |Github| image:: https://img.shields.io/github/stars/wanadev/scanline-python-wrapper?label=Github&logo=github
   :target: https://github.com/wanadev/scanline-python-wrapper
.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/BmUkEdMuFp
.. |PYPI Version| image:: https://img.shields.io/pypi/v/scanline-python-wrapper.svg
   :target: https://pypi.python.org/pypi/scanline-python-wrapper
.. |Build Status| image:: https://github.com/wanadev/scanline-python-wrapper/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/wanadev/scanline-python-wrapper/actions
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/
.. |License| image:: https://img.shields.io/pypi/l/scanline-python-wrapper.svg
   :target: https://github.com/wanadev/scanline-python-wrapper/blob/master/LICENSE
