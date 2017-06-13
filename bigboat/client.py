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

from builtins import str
from builtins import object
import requests
import yaml
from .application import Application
from .instance import Instance
from .utils import Inherited as inherit

class Client(object):
    """
    Generic client base class, enforcing minimum required interface.
    """

    def __init__(self, base_url, **kwargs):
        self._base_url = base_url.rstrip('/')
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
            :obj:`bigboat.application.Application` or `None`: The application
            definition if it was found or `None` if the definition does not
            exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def update_app(self, name, version):
        """
        Register an application definition in the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            :obj:`bigboat.application.Application` or `None`: The application
            definition if it was successfully created.
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

    def instances(self):
        """
        Retrieve all live instances from the API.

        Returns:
            :obj:`list` of :obj:`bigboat.instance.Instance`
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def get_instance(self, name):
        """
        Retrieve a specific live instance from the API.

        Args:
            name (str): The name of the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was found or `None` if the instance does not exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def update_instance(self, name, app_name, version, **kwargs):
        """
        Request the instance to be created with a desired state of 'running'.

        Args:
            name (str): The name of the instance to be started.
            app_name (str): The name of the application to be started.
            version (str): The version of the application to be started.
            **kwargs: Additional properties to use when starting the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was started or `None` if the instance failed to start.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def delete_instance(self, name):
        """
        Retrieve a specific live instance from the API.

        Args:
            name (str): The name of the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was found or `None` if the instance does not exist.
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

    @inherit
    def apps(self):
        return []

    @inherit
    def get_app(self, name, version):
        try:
            request = self._get('appdef/{}/{}'.format(name, version))
        except requests.exceptions.ConnectionError:
            return None

        document = yaml.load(request.text)

        return Application(self, document['name'], str(document['version']))

    @inherit
    def update_app(self, name, version):
        # Cannot create new apps through v1 API
        return None

    @inherit
    def delete_app(self, name, version):
        request = self._delete('appdef/{}/{}'.format(name, version))

        if request.status_code == 404:
            return False

        return request.status_code == 200

    @inherit
    def instances(self):
        request = self._get('instances')

        if request.status_code == 404:
            return []

        data = request.json()
        return [Instance(self, name) for name in data['instances']]

    @inherit
    def get_instance(self, name):
        request = self._get('state/{}'.format(name))

        if request.status_code == 404:
            return []

        state = 'running' if request.text == 'active' else request.text

        return Instance(self, name, state)

    @inherit
    def update_instance(self, name, app_name, version, **kwargs):
        request = self._get('start-app/{}/{}/{}'.format(app_name, version, name))

        if request.status_code == 404:
            return None

        return Instance(self, name, current_state='running',
                        application=Application(self, app_name, version))

    @inherit
    def delete_instance(self, name):
        request = self._get('stop-app/{}'.format(name))

        if request.status_code == 404:
            return None

        return Instance(self, name, 'created')

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

    def _put(self, path, content_type=None, data=None, json=None):
        headers = {}
        if content_type is not None:
            headers['Content-Type'] = content_type
        elif json is not None:
            headers['Content-Type'] = 'application/json'

        return self._session.put(self._format_url(path), headers=headers,
                                 data=data, json=json)

    def _delete(self, path):
        return self._session.delete(self._format_url(path))

    @staticmethod
    def _check_bad_request(request):
        # Bad Request should raise an exception
        if request.status_code == 400:
            if request.headers['Content-Type'] == 'application/json':
                response = request.json()
                raise ValueError(response['message'])
            else:
                raise ValueError(request.text)

    def _format_app(self, app):
        return Application(self, app['name'], app['version'])

    @inherit
    def apps(self):
        request = self._get('apps')
        return [self._format_app(app) for app in request.json()]

    @inherit
    def get_app(self, name, version):
        request = self._get('apps/{}/{}'.format(name, version))
        if request.status_code == 404:
            return None

        return self._format_app(request.json())

    @inherit
    def update_app(self, name, version):
        try:
            request = self._put('apps/{}/{}'.format(name, version))
        except requests.exceptions.ConnectionError:
            return None

        return self._format_app(request.json())

    @inherit
    def delete_app(self, name, version):
        request = self._delete('apps/{}/{}'.format(name, version))
        if request.status_code == 404:
            return False

        return True

    def get_compose(self, name, version, file_name):
        """
        Retrieve a docker compose or bigboat compose file for the application.

        Args:
            name (str): The name of the application
            version (str): The version of the application
            file_name (str): 'dockerCompose' or 'bigboatCompose'

        Returns:
            :obj:`str` or `None`: The application definition's docker compose
            file contents if the application was found, or `None` if the
            definition does not exist.
        """

        path = 'apps/{}/{}/files/{}'.format(name, version, file_name)
        request = self._get(path)
        if request.status_code == 404:
            return None

        content_type = request.headers.get('content-type')
        if content_type not in ('text/plain', 'text/yaml'):
            return None

        return request.text

    def update_compose(self, name, version, file_name, content):
        """
        Update a docker compose or bigboat compose file for the application.

        Args:
            name (str): The name of the application
            version (str): The version of the application
            file_name (str): 'dockerCompose' or 'bigboatCompose'
            content (str): The file contents

        Returns:
            bool: Whether the compose fille was successfully updated.

        Raises:
        """

        path = 'apps/{}/{}/files/{}'.format(name, version, file_name)
        request = self._put(path, content_type='text/plain', data=content)
        if request.status_code == 404:
            return False

        self._check_bad_request(request)

        if request.status_code != 201:
            return False

        return True

    def _format_instance(self, instance, name=None):
        if 'app' in instance:
            if name is not None:
                application = Application(self, instance['app'],
                                          instance['version'])
            else:
                application = self._format_app(instance['app'])
        else:
            application = None

        services = instance.get('services')

        if 'name' in instance:
            name = instance['name']

        state = instance.get('state', {})

        return Instance(self, name,
                        current_state=state.get('current', 'running'),
                        desired_state=state.get('desired'),
                        application=application, services=services)

    @inherit
    def instances(self):
        request = self._get('instances')
        return [self._format_instance(instance) for instance in request.json()]

    @inherit
    def get_instance(self, name):
        request = self._get('instances/{}'.format(name))

        if request.status_code == 404:
            return None

        return self._format_instance(request.json())

    @inherit
    def update_instance(self, name, app_name, version, **kwargs):
        data = {
            'app': app_name,
            'version': version,
            'parameters': kwargs.get('parameters') or {},
            'options': kwargs.get('options') or {}
        }
        request = self._put('instances/{}'.format(name), json=data)

        self._check_bad_request(request)

        return self._format_instance(request.json())

    @inherit
    def delete_instance(self, name):
        request = self._delete('instances/{}'.format(name))

        self._check_bad_request(request)

        return self._format_instance(request.json())

    def statuses(self):
        """
        Retrieve all status items reported by BigBoat.

        Returns:
            :obj:`list` of :obj:`dict`: The status items
        """

        return self._get('status').json()
