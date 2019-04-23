import unittest
from datetime import date
from function import *
from sanitation import UnknownCollectionDate


class TestCollDateToSpeech(unittest.TestCase):

    def test_returns_today(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 22)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(speech, 'today')

    def test_returns_day_when_less_than_7_days_and_in_same_month(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 28)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(speech, 'Sunday')

    def test_returns_tomorrow_when_1_day_away_and_in_same_month(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 23)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(speech, 'tomorrow')

    def test_returns_day_and_month_when_at_least_7_days_and_in_same_month(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 29)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'Monday, <say-as interpret-as="date" format="md">04/29</say-as>'
        )

    def test_returns_day_and_month_when_month_changes(self):
        now = date(2019, 4, 29)
        coll_date = date(2019, 5, 1)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'Wednesday, <say-as interpret-as="date" format="md">05/01</say-as>'
        )

    def test_returns_tomorrow_day_and_month_when_1_day_away_and_month_changes(self):
        now = date(2019, 4, 30)
        coll_date = date(2019, 5, 1)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'tomorrow, Wednesday, <say-as interpret-as="date" format="md">05/01</say-as>'
        )

    def test_returns_day_month_year_when_year_changes(self):
        now = date(2019, 12, 30)
        coll_date = date(2020, 1, 1)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'Wednesday, <say-as interpret-as="date" format="mdy">01/01/2020</say-as>'
        )

    def test_returns_tomorrow_day_month_year_when_year_changes(self):
        now = date(2019, 12, 31)
        coll_date = date(2020, 1, 1)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'tomorrow, Wednesday, <say-as interpret-as="date" format="mdy">01/01/2020</say-as>'
        )

    def test_raises_UnknownCollectionDate_when_in_past(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 21)

        with self.assertRaises(UnknownCollectionDate):
            convert_collection_date_to_speech(now, coll_date)
