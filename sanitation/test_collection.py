import unittest
from .collection import *


class TestCollectionType(unittest.TestCase):
    def test_returns_valid_when_type_is_known(self):
        coll_types = [
            ("Garbage", CollectionType.GARBAGE),
            ("garbage", CollectionType.GARBAGE),
            ("Recycling", CollectionType.RECYCLING),
            ("recycling", CollectionType.RECYCLING),
        ]

        for text, exp in coll_types:
            with self.subTest(text=text, exp=exp):
                coll_type = CollectionType.from_text(text)
                self.assertEqual(coll_type, exp)

    def test_raises_UnknownCollectionType_when_type_is_not_known(self):
        coll_types = [
            "",
            "Blah",
            "Garbage Day",
            "Day of recycling"
        ]

        for text in coll_types:
            with self.subTest(text=text), self.assertRaises(UnknownCollectionType):
                CollectionType.from_text(text)
