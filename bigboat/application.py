"""
Application entity from the API.

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

@readonly("name", "version")
class Application(Entity):
    """
    An application definition entity.
    """

    def __init__(self, client, name, version):
        super(Application, self).__init__(client)

        self._name = name
        self._version = version

    def update(self):
        self.client.update_app(self.name, self.version)

    def delete(self):
        self.client.delete_app(self.name, self.version)

    def __repr__(self):
        return 'Application(name={!r}, version={!r})'.format(self.name, self.version)
