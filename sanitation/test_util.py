import unittest
from .util import *


class TestCaseInsensitiveLookup(unittest.TestCase):
    def setUp(self):
        self.data = {"blah": 1}

    def test_returns_value_when_lowercase(self):
        self.assertEqual(case_insensitive_lookup(self.data, "blah"), 1)

    def test_returns_value_when_uppercase(self):
        self.assertEqual(case_insensitive_lookup(self.data, "BLAH"), 1)

    def test_returns_value_when_mixed_case(self):
        self.assertEqual(case_insensitive_lookup(self.data, "BlaH"), 1)

    def test_raises_KeyError_when_not_found(self):
        with self.assertRaises(KeyError):
            case_insensitive_lookup(self.data, "Not here")
