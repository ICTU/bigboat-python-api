"""
Tests for instance entity from the API.

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

import unittest
from mock import MagicMock
from bigboat.client import Client
from bigboat.application import Application
from bigboat.instance import Instance

class ApplicationTest(unittest.TestCase):
    """
    Tests for the application instance entity.
    """

    def setUp(self):
        self.client = MagicMock(spec_set=Client)
        self.application = Application(self.client, 'nginx', 'latest')
        self.instance = Instance(self.client, 'nginx', current_state='starting',
                                 desired_state='running',
                                 application=self.application,
                                 services={'www': {'state': 'starting'}},
                                 parameters={'SETTING': 'value'},
                                 options={'storageBucket': 'custom'})

    def test_update(self):
        """
        Test the Instance.update method.
        """

        # Test that instances without application information cannot be started
        incomplete_instance = Instance(self.client, 'foo')
        with self.assertRaises(ValueError):
            incomplete_instance.update()

        value = self.instance.update()
        update_instance = self.client.update_instance
        update_instance.assert_called_once_with('nginx', 'nginx', 'latest',
                                                parameters={
                                                    'SETTING': 'value'
                                                },
                                                options={
                                                    'storageBucket': 'custom'
                                                })
        self.assertEqual(value, update_instance.return_value)

    def test_delete(self):
        """
        Test the Instance.delete method.
        """

        value = self.instance.delete()
        self.client.delete_instance.assert_called_once_with('nginx')
        self.assertEqual(value, self.client.delete_instance.return_value)

    def test_repr(self):
        """
        Test the Instance.__repr__ method.
        """

        application = "Application(name='nginx', version='latest')"
        services = "{'www': {'state': 'starting'}}"
        instance = "Instance(name='nginx', current_state='starting', " + \
                   "desired_state='running', application=" + \
                   application + ", services=" + services + ", " + \
                   "parameters={'SETTING': 'value'}, " + \
                   "options={'storageBucket': 'custom'})"
        self.assertEqual(repr(self.instance), instance)
