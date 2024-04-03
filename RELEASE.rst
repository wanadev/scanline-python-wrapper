Things to do when releasing a new version
=========================================

This file is a memo for the maintainer.


0. Checks
---------

* Check copyright years in ``LICENSE``
* Check copyright years in ``doc/conf.py``


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``doc/conf.py``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated :)


3. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog
