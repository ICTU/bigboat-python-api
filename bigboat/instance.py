"""
Instance entity from the API.

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

from .entity import Entity
from .utils import readonly

@readonly("name", "current_state", "desired_state", "application", "services",
          "parameters", "options")
class Instance(Entity):
    """
    A deployed (parameterized) application instance entity.
    """

    def __init__(self, client, name, current_state=None, **kwargs):
        super(Instance, self).__init__(client)
        self._name = name
        self._current_state = current_state
        self._desired_state = kwargs.get('desired_state')
        self._application = kwargs.get('application')
        self._services = kwargs.get('services')

        self._parameters = kwargs.get('parameters')
        self._options = kwargs.get('options')

    def update(self):
        """
        Request the instance to be created with a desired state of 'running'.
        """

        if self.application is None:
            raise ValueError('Application information required to start instance')

        return self.client.update_instance(self.name, self.application.name,
                                           self.application.version,
                                           self.parameters, self.options)

    def delete(self):
        """
        Request the instance to be stopped.
        """

        return self.client.delete_instance(self.name)

    def __repr__(self):
        parts = [
            ('name', self.name),
            ('current_state', self.current_state),
            ('desired_state', self.desired_state),
            ('application', self.application),
            ('services', self.services),
            ('parameters', self.parameters),
            ('options', self.options)
        ]
        properties = ['{}={!r}'.format(key, value) for (key, value) in parts]

        return 'Instance({})'.format(', '.join(properties))
