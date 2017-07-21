"""
Tests for clients that connect to the BigBoat API.

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
import requests
import requests_mock
from bigboat.client import Client, Client_v1, Client_v2

class Client_Test(unittest.TestCase):
    """
    Tests for the generic client base class.
    """

    URL = 'http://dashboard.example/'
    CANONICAL_URL = 'http://dashboard.example'

    def setUp(self):
        super(Client_Test, self).setUp()
        self.client = Client(self.URL, other='data')

    def test_base_url(self):
        """
        Test the Client.base_url property.
        """

        # The base_url should return an URL without trailing slash.
        self.assertEquals(self.client.base_url, self.CANONICAL_URL)

    def test_interface(self):
        """
        Test whether the abstract base class requires the minimal interface.
        """

        with self.assertRaises(NotImplementedError):
            self.client.apps()
        with self.assertRaises(NotImplementedError):
            self.client.get_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.update_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.delete_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.instances()
        with self.assertRaises(NotImplementedError):
            self.client.get_instance('bar')
        with self.assertRaises(NotImplementedError):
            self.client.update_instance('bar', 'foo', 'latest', extra='yes')
        with self.assertRaises(NotImplementedError):
            self.client.delete_instance('bar')

class RequestsTestCase(unittest.TestCase):
    """
    A base unit test class that uses requests.

    This class provides a requests_mock member variable during the test run.
    """

    def setUp(self):
        super(RequestsTestCase, self).setUp()
        self.requests_mock = requests_mock.mock(case_sensitive=True)
        self.requests_mock.start()

    def tearDown(self):
        super(RequestsTestCase, self).tearDown()
        self.requests_mock.stop()

class Client_v1_Test(RequestsTestCase):
    """
    Tests for the BigBoat v1 API.
    """

    URL = 'http://dashboard.example/'
    PATH = 'api/v1/'

    def setUp(self):
        super(Client_v1_Test, self).setUp()
        self.client = Client_v1(self.URL)

    def test_apps(self):
        """
        Test the Client_v1.apps dummy method.
        """

        self.assertEqual(self.client.apps(), [])

    def test_get_app(self):
        """
        Test the Client_v1.get_app method.
        """

        self.requests_mock.get(self.URL + self.PATH + 'appdef/foo/latest',
                               text='''name: foo
version: latest
instance:
  image: hello-world
''')
        application = self.client.get_app('foo', 'latest')
        self.assertEqual(application.name, 'foo')
        self.assertEqual(application.version, 'latest')

        # Test connection error for nonexistent applications.
        self.requests_mock.get(self.URL + self.PATH + 'appdef/does/notexist',
                               exc=requests.exceptions.ConnectionError)
        self.assertIsNone(self.client.get_app('does', 'notexist'))

    def test_update_app(self):
        """
        Test the Client_v1.update_app dummy method.
        """

        self.assertIsNone(self.client.update_app('foo', 'latest'))

    def test_delete_app(self):
        """
        Test the Client_v1.delete_app method.
        """

        self.requests_mock.delete(self.URL + self.PATH + 'appdef/foo/latest')
        self.requests_mock.delete(self.URL + self.PATH + 'appdef/does/notexist',
                                  status_code=404)

        self.assertTrue(self.client.delete_app('foo', 'latest'))
        self.assertFalse(self.client.delete_app('does', 'notexist'))

    def test_instances(self):
        """
        Test the Client_v1.instances method.
        """

        self.requests_mock.get(self.URL + self.PATH + 'instances',
                               status_code=404)
        self.assertEqual(self.client.instances(), [])

        self.requests_mock.get(self.URL + self.PATH + 'instances',
                               json={
                                   "statusCode": 200,
                                   "instances": ['foo', 'bar', 'baz']
                               })
        instances = self.client.instances()
        names = list(sorted(instance.name for instance in instances))
        self.assertEqual(names, ['bar', 'baz', 'foo'])

    def test_get_instance(self):
        """
        Test the Client_v1.get_instance method.
        """

        self.requests_mock.get(self.URL + self.PATH + 'state/qux',
                               status_code=404)
        self.requests_mock.get(self.URL + self.PATH + 'state/foo',
                               text='active')

        self.assertIsNone(self.client.get_instance('qux'))
        instance = self.client.get_instance('foo')
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'running')

    def test_update_instance(self):
        """
        Test the update_instance method.
        """

        url = self.URL + self.PATH
        self.requests_mock.get(url + 'start-app/does/notexist/qux',
                               status_code=404)
        self.requests_mock.get(url + 'start-app/foo/latest/foo')

        self.assertIsNone(self.client.update_instance('qux', 'does', 'notexist',
                                                      more='args'))
        instance = self.client.update_instance('foo', 'foo', 'latest')
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'running')
        self.assertEqual(instance.application.name, 'foo')
        self.assertEqual(instance.application.version, 'latest')

    def test_delete_instance(self):
        """
        Test the Client_v1.delete_instance method.
        """

        self.requests_mock.get(self.URL + self.PATH + 'stop-app/qux',
                               status_code=404)
        self.requests_mock.get(self.URL + self.PATH + 'stop-app/foo')

        self.assertIsNone(self.client.delete_instance('qux'))
        instance = self.client.delete_instance('foo')
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'created')

class Client_v2_Test(RequestsTestCase):
    """
    Tests for the BigBoat v2 API.
    """

    URL = 'http://dashboard.example/'
    KEY = 'my-api-key'

    def setUp(self):
        self.client = Client_v2(self.URL, self.KEY)
        self.fail('not yet implemented')
