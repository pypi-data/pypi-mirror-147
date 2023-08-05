.. |ci| image:: https://github.com/djmattyg007/freiner/workflows/CI/badge.svg?branch=master
   :target: https://github.com/djmattyg007/freiner/actions?query=branch%3Amaster+workflow%3ACI
.. |codecov| image:: https://codecov.io/gh/djmattyg007/freiner/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/djmattyg007/freiner
.. |pypi| image:: https://img.shields.io/pypi/v/freiner.svg
   :target: https://pypi.org/project/freiner
.. |license| image:: https://img.shields.io/pypi/l/freiner.svg
   :target: https://pypi.org/project/freiner

*******
Freiner
*******
|ci| |codecov| |pypi| |license|

*Freiner* provides utilities to implement rate limiting using various strategies and storage
backends such as Redis & Memcached.

The French word "freiner" means "to slow down", which is what you'll need to do if you are
rate-limited :)

Currently this project supports Python 3.8, 3.9 and 3.10.

History
-------

Freiner is a fork of a project named `limits <https://github.com/alisaifee/limits>`_. I forked it
to add type hints, and to resolve several outstanding problems at the time.

Links
-----

* `Documentation <https://freiner.readthedocs.io/>`_
* `PyPI <https://pypi.org/project/freiner/>`_
* `Changelog <https://freiner.readthedocs.io/en/latest/changelog.html>`_
