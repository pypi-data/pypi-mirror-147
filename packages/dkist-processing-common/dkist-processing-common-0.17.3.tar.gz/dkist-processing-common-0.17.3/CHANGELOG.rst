v0.17.1 (2022-03-31)
====================

Features
--------

- Sentinel `Thorn` class that indicates a Bud/Stem shouldn't be picked. Allows for Buds that just check stuff without returning a value. (`#90 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/90>`__)


Misc
----

- Increase verbosity in message publishing APM steps (`#89 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/89>`__)


Documentation
-------------

- Add changelog (`#91 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/91>`__)


v0.17.0 (2022-03-24)
====================

Features
--------

- Exposure "teardown_enabled" configuration kwarg to optionally skip the Teardown task (`#85 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/85>`__)
- Add `.from_path` class method to FitsAccess (`#88 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/88>`__)


Bugfixes
--------

- Fix name of "fpa_exposure_time" parameter (`#86 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/86>`__)
- Report correct units (adu / s) for quality report RMS values (`#87 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/87>`__)
- Save resources in quality metrics task by using paths instead of full FitsAccess objects (`#88 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/88>`__)


v0.16.3 (2022-03-18)
====================

Bugfixes
--------

- Remove some vestigial raw `self.apm_step` calls

v0.16.2 (2022-03-18)
====================

Features
--------

- Increase usefulness of APM logging with type-specific spans (`#84 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/84>`__)

v0.16.1 (2022-03-10)
====================

Misc
----

- Add graphviz to build env so docs render correctly

v0.16.0 (2022-03-10)
====================

First version to be used on DKIST summit data
