"""
Tests for generic base entity.

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
from bigboat.entity import Entity

class Entity_Test(unittest.TestCase):
    """
    Tests for entity from the BigBoat API.
    """

    def test_interface(self):
        """
        Test the enforcement of abstract interface.
        """

        client = MagicMock(spec_set=Client)
        entity = Entity(client)

        # Test the client property.
        self.assertEqual(entity.client, client)

        # Test the interface
        with self.assertRaises(NotImplementedError):
            entity.update()

        with self.assertRaises(NotImplementedError):
            entity.delete()

        # Test unknown attribute access
        with self.assertRaises(AttributeError):
            dummy = entity.nonexistent
