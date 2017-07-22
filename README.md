# BigBoat docker dashboard Python API

[![PyPI](https://img.shields.io/pypi/v/bigboat.svg)](https://pypi.python.org/pypi/bigboat)
[![Build 
Status](https://travis-ci.org/ICTU/bigboat-python-api.svg?branch=master)](https://travis-ci.org/ICTU/bigboat-python-api)
[![Coverage 
Status](https://coveralls.io/repos/github/ICTU/bigboat-python-api/badge.svg?branch=master)](https://coveralls.io/github/ICTU/bigboat-python-api?branch=master)

Python wrapper library for the BigBoat API. This API can create, retrieve, 
update and delete application definitions, do similar operations for instances 
and poll for status.

Support for v2 and the deprecated v1 APIs (limited to certain operations) is 
included.

## Requirements

The BigBoat Python API has been tested to work on Python 2.7 and 3.6. The API 
has few dependencies; see `requirements.txt` for the list of installation 
requirements. The short list is also repeated here:

- [Future](http://python-future.org/overview.html)
- [Requests](http://docs.python-requests.org/en/master/user/install/)
- [PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation)

## Installation

Install the latest version from PyPI using:

```
pip install bigboat
```

## Functionality

First, import the library:

```python
import bigboat
```

Next, determine the URL of your BigBoat instance. In this example we use 
`http://BIG_BOAT`. Also check whether to use the v1 or v2 version of the API. 
v1 is limited (deprecated in newer versions) and v2 requires an API key. 
Example:

```python
api = bigboat.Client_v2('http://BIG_BOAT', 'MY_API_KEY')
```

You can then use various methods on the client API, namely:
- `api.apps()`: List of Applications
- `api.get_app(name, version)`: Retrieve a specific Application
- `api.update_app(name, version)`: Register an Application
- `api.delete_app(name, version`: Delete an Application
- `api.instances()`: List of Instances
- `api.get_instance()`: Retrieve a specific Instance
- `api.update_instance(name, app_name, version, ...)`: Start an Instance
- `api.delete_instance(name)`: Stop an Instance

In addition to the common methods, v2 has the following API methods:
- `api.get_compose(name, version, file_name)`: Retrieve a docker compose or 
  bigboat compose file for an Application
- `api.update_compose(name, version, file_name, content)`: Update a docker 
  compose or bigboat compose file for an Application
- `api.statuses()`: Retrieve a list of satus dictionaries

## Development

- [Travis](https://travis-ci.org/ICTU/bigboat-python-api) is used to run unit 
  tests and report on coverage.
- [Coveralls](https://coveralls.io/github/ICTU/bigboat-python-api) receives 
  coverage reports and tracks them.
- You can perform local lint checks, tests and coverage during development 
  using `make pylint`, `make test` and `make coverage`, respectively.
- We publish releases to [PyPI](https://pypi.python.org/pypi/bigboat) using 
  `make release` which performs lint and unit test checks.

## License

The API wrapper library is licensed under the Apache 2.0 License.

## References

- [Docker Dashboard](https://github.com/ICTU/docker-dashboard)
