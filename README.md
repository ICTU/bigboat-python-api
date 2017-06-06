# BigBoat docker dashboard Python API

Python wrapper library for the BigBoat API. This API can create, retrieve, 
update and delete application definitions, do similar operations for instances 
and poll for status.

Support for v2 and the deprecated v1 APIs (limited to certain operations) is 
included.

## Requirements

See `requirements.txt` for the list of requirements. The short list is also 
repeated here:

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

## License

The API wrapper library is licensed under the Apache 2.0 License.

## References

- [Docker Dashboard](https://github.com/ICTU/docker-dashboard)
