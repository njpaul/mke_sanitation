import unittest
from datetime import date
from function import *
from sanitation import UnknownCollectionDate


class TestCollDateToSpeech(unittest.TestCase):

    def test_raises_UnknownCollectionDate_when_in_past(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 21)

        with self.assertRaises(UnknownCollectionDate):
            convert_collection_date_to_speech(now, coll_date)

    def test_returns_today_when_0_days_away(self):
        now = date(2019, 4, 22)
        coll_date = date(2019, 4, 22)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(speech, 'today')

    def test_returns_tomorrow_when_1_day_away(self):
        dates = [
            # Same month
            (date(2019, 4, 22), date(2019, 4, 23)),

            # Different month, same year
            (date(2019, 4, 30), date(2019, 5, 1)),

            # Different year
            (date(2019, 12, 31), date(2020, 1, 1)),
        ]

        for now, coll_date in dates:
            with self.subTest(now=now, coll_date=coll_date):
                speech = convert_collection_date_to_speech(now, coll_date)
                self.assertEqual(speech, 'tomorrow')

    def test_returns_day_when_less_than_7_days_away(self):
        dates = [
            # Same month
            (date(2019, 4, 22), date(2019, 4, 24), "Wednesday"),

            # Different month, same year
            (date(2019, 4, 30), date(2019, 5, 2), "Thursday"),

            # Different year
            (date(2019, 12, 31), date(2020, 1, 3), "Friday"),
        ]

        for now, coll_date, exp in dates:
            with self.subTest(now=now, coll_date=coll_date):
                speech = convert_collection_date_to_speech(now, coll_date)
                self.assertEqual(speech, exp)

    def test_returns_day_and_month_when_at_least_7_days_away_and_same_year(self):
        fmt = '{}, <say-as interpret-as="date" format="md">{}</say-as>'
        dates = [
            # Same month
            (date(2019, 4, 22), date(2019, 4, 29), fmt.format("Monday", "04/29")),

            # Different month, same year
            (date(2019, 4, 22), date(2019, 5, 2), fmt.format("Thursday", "05/02")),
        ]

        for now, coll_date, exp in dates:
            with self.subTest(now=now, coll_date=coll_date):
                speech = convert_collection_date_to_speech(now, coll_date)
                self.assertEqual(speech, exp)

    def test_returns_day_month_year_when_at_least_7_days_away_and_year_changes(self):
        now = date(2019, 12, 30)
        coll_date = date(2020, 1, 6)
        speech = convert_collection_date_to_speech(now, coll_date)
        self.assertEqual(
            speech,
            'Monday, <say-as interpret-as="date" format="mdy">01/06/2020</say-as>'
        )
