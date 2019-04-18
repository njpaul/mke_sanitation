import unittest
from datetime import date
from .collection import *
from .collection import _read_garbage_date, _read_recycling_date


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


class TestReadResponse(unittest.TestCase):
    def test_returns_date_when_found_in_text(self):
        # A small but representative version of the response to expect.
        # The real version has much more, and it varies, so that can be
        # checked with end-to-end testing.
        RESPONSE_TEXT = (
            "<h2>Next Scheduled Garbage Pickup:</h2>"
            "The summer garbage pickup route for this location is "
            "<strong>NG3-2C</strong>.<br/><br/>The next garbage collection "
            "pickup for this location is: <strong>WEDNESDAY APRIL 17, 2019</strong>"
            "<br/><br/>Click <a target='_blank' "
            "href='http://mpw.milwaukee.gov/san_collection_files/SUMMER/Garbage - Yellow.pdf'>"
            "here</a> to see your complete garbage collection schedule.<br/><br/>"
            "<h2>Next Scheduled Recycling Pickup:</h2>"
            "The summer recycling pickup route for this location is "
            "<strong>NR01-1-01</strong>.<br/><br/>The next recycling collection "
            "pickup for this location is: <strong>FRIDAY APRIL 12, 2019</strong>"
            "<br/><br/>Click <a target='_blank' "
            "href='http://mpw.milwaukee.gov/san_collection_files/SUMMER/Recycling - "
            "EOW - 1.pdf'>here</a> to see your complete recycling collection "
            "schedule.<br/><br/>"
        )

        with self.subTest(coll_type="garbage"):
            date_response = _read_garbage_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 4, 17))

        with self.subTest(coll_type="recycling"):
            date_response = _read_recycling_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 4, 12))

    def test_returns_date_when_day_is_single_digit(self):
        # A small but representative version of the response to expect.
        # The real version has much more, and it varies, so that can be
        # checked with end-to-end testing.
        RESPONSE_TEXT = (
            "<strong>NG3-2C</strong>.<br/><br/>The next garbage collection "
            "pickup for this location is: <strong>WEDNESDAY MAY 1, 2019</strong>"
            "<h2>Next Scheduled Recycling Pickup:</h2>"
            "<strong>NR01-1-01</strong>.<br/><br/>The next recycling collection "
            "pickup for this location is: <strong>MONDAY MAY 6, 2019</strong>"
        )

        with self.subTest(coll_type="garbage"):
            date_response = _read_garbage_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 5, 1))

        with self.subTest(coll_type="recycling"):
            date_response = _read_recycling_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 5, 6))

    def test_returns_date_when_month_starts_with_capital_letter(self):
        # A small but representative version of the response to expect.
        # The real version has much more, and it varies, so that can be
        # checked with end-to-end testing.
        RESPONSE_TEXT = (
            "<strong>NG3-2C</strong>.<br/><br/>The next garbage collection "
            "pickup for this location is: <strong>WEDNESDAY May 1, 2019</strong>"
            "<h2>Next Scheduled Recycling Pickup:</h2>"
            "<strong>NR01-1-01</strong>.<br/><br/>The next recycling collection "
            "pickup for this location is: <strong>MONDAY May 6, 2019</strong>"
        )

        with self.subTest(coll_type="garbage"):
            date_response = _read_garbage_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 5, 1))

        with self.subTest(coll_type="recycling"):
            date_response = _read_recycling_date(RESPONSE_TEXT)
            self.assertEqual(date_response, date(2019, 5, 6))

    def test_raises_UnknownCollectionDate_when_not_found_in_text(self):
        # A small but representative version of the response to expect.
        RESPONSE_TEXT = (
            "<h2>Next Scheduled Garbage Pickup:</h2>"
            "Your garbage collection schedule could not be determined.<br/><br/>"
            "Please try back after April 1st.<br/><br/>"
            "<h2>Next Scheduled Recycling Pickup:</h2>"
            "<h2>Clean & Green week:</h2>"
        )

        with self.subTest(coll_type="garbage"), self.assertRaises(UnknownCollectionDate):
            _read_garbage_date(RESPONSE_TEXT)

        with self.subTest(coll_type="recycling"), self.assertRaises(UnknownCollectionDate):
            _read_recycling_date(RESPONSE_TEXT)

    def test_raises_CollectionResponseError_when_response_is_not_recognized(self):
        RESPONSE_TEXT = (
            "Address: 0   <br/>"
            "The following 3 errors were found with your submission: <br/><br/>"
            "<span style='color:red;'>1 </span>- You must enter a street name..<br/>"
            "<span style='color:red;'>2 </span>- House number is not valid "
            "(must be a number - do not include apt.)..<br/>"
            "<span style='color:red;'>3 </span>- The address was not recognized "
            "as a valid Milwaukee address..<br/>"
        )

        with self.subTest(coll_type="garbage"), self.assertRaises(CollectionResponseError):
            _read_garbage_date(RESPONSE_TEXT)

        with self.subTest(coll_type="recycling"), self.assertRaises(CollectionResponseError):
            _read_recycling_date(RESPONSE_TEXT)
