"""
Clients that connect to the BigBoat API.

Copyright 2017 ICTU

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import yaml
from .application import Application

class Client(object):
    """
    Generic client base class, enforcing minimum required interface.
    """

    def __init__(self, base_url, **kwargs):
        self._base_url = base_url
        self._options = kwargs

    @property
    def base_url(self):
        """
        The base URL of the BigBoat instance.
        """

        return self._base_url

    def apps(self):
        """
        Retrieve all application definitions from the API.

        Returns:
            :obj:`list` of :obj:`application.Application`
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def get_app(self, name, version):
        """
        Retrieve a specific application definition from the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            :obj:`application.Application` or `None`: The application definition
            if it was found or `None` if the definition does not exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def update_app(self, name, version):
        """
        Register an application definition in the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            :obj:`application.Application` or `None`: The application definition
            if it was successfully created.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def delete_app(self, name, version):
        """
        Delete an application definition in the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            bool: Whether the application was successfully deleted.
        """

        raise NotImplementedError('Must be implemented by subclasses')

class Client_v1(Client):
    """
    Client for the deprecated BigBoat v1 API.
    """

    def _format_url(self, path):
        return '{}/api/v1/{}'.format(self._base_url, path)

    def _get(self, path):
        return requests.get(self._format_url(path))

    def _post(self, path, body=None):
        return requests.post(self._format_url(path), data=body)

    def _delete(self, path):
        return requests.delete(self._format_url(path))

    def apps(self):
        return []

    def get_app(self, name, version):
        try:
            request = self._get('appdef/{}/{}'.format(name, version))
        except requests.exceptions.ConnectionError:
            return None

        document = yaml.load(request.text)

        return Application(self, document['name'], str(document['version']))

    def update_app(self, name, version):
        # Cannot create new apps through v1 API
        return None

    def delete_app(self, name, version):
        request = self._delete('appdef/{}/{}'.format(name, version))

        if request.status_code == 404:
            return False

        return request.status_code == 200

class Client_v2(Client):
    """
    Client for the BigBoat v2 API.
    """

    def __init__(self, base_url, api_key):
        super(Client_v2, self).__init__(base_url)
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({'api-key': self._api_key})

    def _format_url(self, path):
        return '{}/api/v2/{}'.format(self._base_url, path)

    def _get(self, path):
        return self._session.get(self._format_url(path))

    def _put(self, path, content_type=None, data=None):
        headers = {}
        if content_type is not None:
            headers['Content-Type'] = content_type

        return self._session.put(self._format_url(path), headers=headers,
                                 data=data)

    def _delete(self, path):
        return self._session.delete(self._format_url(path))

    def _format_app(self, app):
        return Application(self, app['name'], app['version'])

    def apps(self):
        request = self._get('apps')
        return [self._format_app(app) for app in request.json()]

    def get_app(self, name, version):
        request = self._get('app/{}/{}'.format(name, version))
        if request.status_code == 404:
            return None

        return self._format_app(request.json())

    def update_app(self, name, version):
        try:
            request = self._put('app/{}/{}'.format(name, version))
        except requests.exceptions.ConnectionError:
            return None

        return self._format_app(request.json())

    def delete_app(self, name, version):
        request = self._delete('app/{}/{}'.format(name, version))
        if request.status_code == 404:
            return False

        return True
