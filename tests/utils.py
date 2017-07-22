"""
Tests for utilities.

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
from bigboat.utils import readonly, Inherited as inherit

@readonly(['name', 'version'], rest='other')
class Item(object):
    """
    Item with some readonly attributes.
    """

    def __init__(self):
        self._name = 'foo'
        self._version = '1'
        self._rest = 'data'

    def get(self):
        """
        Retrieve data.
        """

        return self._name

    @classmethod
    def execute(cls):
        """
        Perform some dummy task.

        Returns:
            bool: Success value
        """

        return True

    def __getattr__(self, name):
        raise AttributeError

class Subitem(Item):
    """
    Extending class.
    """

    @inherit
    def get(self):
        """
        Inheriting method which has custom documentation.
        """

        return self._version

    @inherit
    def get_other(self):
        """
        New method that is incorrrecty marked as inheriting.
        """

        return self._rest

    @inherit
    @classmethod
    def execute(cls):
        return False

    @inherit
    @classmethod
    def new_execute(cls): # pylint: disable=missing-docstring
        # New classmethod that is incorrectly marked as inheriting, but it has
        # no documentation block itself.
        return None

class Utils_Test(unittest.TestCase):
    """
    Tests for utilities.
    """

    def test_readonly(self):
        """
        Test the readonly decorator.
        """

        item = Item()
        self.assertEqual(item.name, 'foo')
        self.assertEqual(item.version, '1')
        self.assertEqual(item.other, 'data')
        with self.assertRaises(AttributeError):
            dummy = item.nonexistent

    def test_inherit(self):
        """
        Test the Inherited decorator.
        """

        item = Item()
        sub_item = Subitem()
        # Custom documentation on inheriting method is retained.
        self.assertEqual(sub_item.get.__doc__.strip(),
                         'Inheriting method which has custom documentation.')
        self.assertEqual(item.get(), 'foo')
        self.assertEqual(sub_item.get(), '1')
        self.assertEqual(sub_item.get_other(), 'data')

        self.assertEqual(Subitem.execute.__doc__, Item.execute.__doc__)
        self.assertTrue(Item.execute())
        self.assertFalse(Subitem.execute())
        self.assertIsNone(Subitem.new_execute())
