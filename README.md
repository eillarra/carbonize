Carbonize
=========

[![github-tests-badge]][github-tests]
[![github-mypy-badge]][github-mypy]
[![codecov-badge]][codecov]
[![pypi-badge]][pypi]
[![pypi-versions]][pypi]
[![license-badge]](LICENSE)


Basic usage
-----------

```python
from carbonize import Footprint

fp = Footprint()
fp.add_flight(a="BRU", b="BIO", two_way=True)
fp.add_train(distance=100)
fp.emissions  # in CO2e (kg)
```

Running tests
-------------

    $ pytest --cov=carbonize --cov-report=term

Updating the underlying data
----------------------------

The Pickle files in the data folder can be updated using the `bin/update_data.py` file.


[codecov]: https://codecov.io/gh/eillarra/carbonize
[codecov-badge]: https://codecov.io/gh/eillarra/carbonize/branch/master/graph/badge.svg
[github-mypy]: https://github.com/eillarra/carbonize/actions?query=workflow%3Amypy
[github-mypy-badge]: https://github.com/eillarra/carbonize/workflows/mypy/badge.svg
[github-tests]: https://github.com/eillarra/carbonize/actions?query=workflow%3Atests
[github-tests-badge]: https://github.com/eillarra/carbonize/workflows/tests/badge.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[pypi]: https://pypi.org/project/carbonize/
[pypi-badge]: https://badge.fury.io/py/carbonize.svg
[pypi-versions]: https://img.shields.io/pypi/pyversions/carbonize.svg
