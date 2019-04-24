import unittest
from .addr import *


class TestAddrParts(unittest.TestCase):
    def test_st_num_is_valid(self):
        addrs = [
            ("1234 North Fake Street", 1234),
            ("5678 North Fake Street", 5678),
            ("9012 North Fake Street", 9012)
        ]

        for addr, exp in addrs:
            with self.subTest(addr=addr, exp=exp):
                parts = AddrParts.from_text(addr)
                self.assertEqual(parts.st_num, exp)

    def test_st_num_is_invalid(self):
        addrs = [
            "A123 North Fake Street",
            "678Z North Fake Street",
            "ABCD North Fake Street",
            "ABCD North Fake Street",
        ]

        for addr in addrs:
            with self.subTest(addr=addr), self.assertRaises(AddrError):
                AddrParts.from_text(addr)

    def test_st_dir_is_valid(self):
        addrs = [
            ("1234 N Fake Street", AddrDir.NORTH),
            ("1234 North Fake Street", AddrDir.NORTH),
            ("1234 S Fake Street", AddrDir.SOUTH),
            ("1234 South Fake Street", AddrDir.SOUTH),
            ("1234 E Fake Street", AddrDir.EAST),
            ("1234 East Fake Street", AddrDir.EAST),
            ("1234 W Fake Street", AddrDir.WEST),
            ("1234 West Fake Street", AddrDir.WEST)
        ]

        for addr, exp in addrs:
            with self.subTest(addr=addr, exp=exp):
                parts = AddrParts.from_text(addr)
                self.assertEqual(parts.st_dir, exp)

    def test_st_dir_is_invalid(self):
        addrs = [
            "1234 Zamboni Fake Street",
            "1234 4567 Fake Street",
            "1234 Cat Fake Street",
        ]

        for addr in addrs:
            with self.subTest(addr=addr), self.assertRaises(AddrError):
                AddrParts.from_text(addr)

    def test_st_name_is_valid(self):
        addrs = [
            ("1234 N Fake Street", "FAKE"),
            ("1234 North Blah Blorg Street", "BLAH BLORG"),
            ("1234 S Fake Terrace Ave", "FAKE TERRACE"),
            ("1234 North 51st Street", "51ST"),
        ]

        for addr, exp in addrs:
            with self.subTest(addr=addr, exp=exp):
                parts = AddrParts.from_text(addr)
                self.assertEqual(parts.st_name, exp)

    def test_st_name_is_invalid(self):
        addrs = [
            "1234 North Street",
        ]

        for addr in addrs:
            with self.subTest(addr=addr), self.assertRaises(AddrError):
                AddrParts.from_text(addr)

    def test_st_suffix_is_valid(self):
        addrs = [
            ("1234 North Fake Ave", AddrSuffix.AVE),
            ("1234 North Fake Avenue", AddrSuffix.AVE),
            ("1234 North Fake Boulevard", AddrSuffix.BLVD),
            ("1234 North Fake Circle", AddrSuffix.CIRCLE),
            ("1234 North Fake Court", AddrSuffix.COURT),
            ("1234 North Fake Drive", AddrSuffix.DRIVE),
            ("1234 North Fake Lane", AddrSuffix.LANE),
            ("1234 North Fake Park", AddrSuffix.PARK),
            ("1234 North Fake Parkway", AddrSuffix.PARK),
            ("1234 North Fake Place", AddrSuffix.PLACE),
            ("1234 North Fake Road", AddrSuffix.ROAD),
            ("1234 North Fake Square", AddrSuffix.SQUARE),
            ("1234 North Fake Street", AddrSuffix.STREET),
            ("1234 North Fake Terrace", AddrSuffix.TERRACE),
            ("1234 North Fake Way", AddrSuffix.WAY)
        ]

        for (addr, exp) in addrs:
            with self.subTest(addr=addr, exp=exp):
                parts = AddrParts.from_text(addr)
                self.assertEqual(parts.st_suffix, exp)

    def test_st_suffix_is_invalid(self):
        addrs = [
            "1234 North Fake",
            "1234 North Fake Stroll",
        ]

        for addr in addrs:
            with self.subTest(addr=addr), self.assertRaises(AddrError):
                AddrParts.from_text(addr)
