import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import locations


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.locations = locations.Locations(3,4,7)

    def test_attrs(self):
        self.assertIsInstance(self.locations.l, list)
        self.assertEqual(self.locations._Locations__x, 3)
        self.assertEqual(self.locations._Locations__y, 4)
        self.assertEqual(self.locations._Locations__z, 7)

    def test_get_location_index(self):
        # check if the index is obtained correctly
        res = self.locations._Locations__get_location_index(2,2,2)
        self.assertEqual(res, 17-1)
        res = self.locations._Locations__get_location_index(1,3,7)
        self.assertEqual(res, 79-1)
        res = self.locations._Locations__get_location_index(1,1,5)
        self.assertEqual(res, 49-1)
        res = self.locations._Locations__get_location_index(3,4,6)
        self.assertEqual(res, 72-1)
        res = self.locations._Locations__get_location_index(2,3,4)
        self.assertEqual(res, 44-1)
        # index out
        with self.assertRaisesRegex(Exception, r"Location not found") as ex:
            self.locations._Locations__get_location_index(2,2,10)

    def test_element(self):
        # check if the element is obtained correctly
        res = self.locations.element(2,2,2)
        self.assertEqual(res, 17)
        res = self.locations.element(1,3,7)
        self.assertEqual(res, 79)
        res = self.locations.element(1,1,5)
        self.assertEqual(res, 49)
        res = self.locations.element(3,4,6)
        self.assertEqual(res, 72)
        res = self.locations.element(2,3,4)
        self.assertEqual(res, 44)
        # index out
        with self.assertRaisesRegex(Exception, r"Location not found") as ex:
            self.locations.element(2,2,10)

    def test_add(self):
        # check before change
        self.assertEqual(self.locations.element(2,2,2), 17)
        # check after change
        res = self.locations.add("something", 2,2,2)
        self.assertEqual(res, None)
        self.assertEqual(self.locations.element(2,2,2), "something")
        # z out of range
        with self.assertRaisesRegex(Exception, r"Location not found") as ex:
            self.locations.add("something", 2,2,10)

    def test_list_all(self):
        res = self.locations.list_all()
        self.assertEqual(res, [i+1 for i in range(84)])
