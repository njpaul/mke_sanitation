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

    def test_st_name_suffix_is_added(self):
        addrs = [
            # Try some of the single-digit streets
            ("1234 North 1 Street", "1ST"),
            ("1234 North 2 Street", "2ND"),
            ("1234 North 3 Street", "3RD"),
            ("1234 North 4 Street", "4TH"),

            # 10-19 always end with "TH"
            ("1234 North 10 Street", "10TH"),
            ("1234 North 11 Street", "11TH"),
            ("1234 North 12 Street", "12TH"),
            ("1234 North 13 Street", "13TH"),
            ("1234 North 14 Street", "14TH"),
            ("1234 North 15 Street", "15TH"),
            ("1234 North 16 Street", "16TH"),
            ("1234 North 17 Street", "17TH"),
            ("1234 North 18 Street", "18TH"),
            ("1234 North 19 Street", "19TH"),

            # Try each of the last digits from 0-9
            ("1234 North 20 Street", "20TH"),
            ("1234 North 21 Street", "21ST"),
            ("1234 North 22 Street", "22ND"),
            ("1234 North 33 Street", "33RD"),
            ("1234 North 44 Street", "44TH"),
            ("1234 North 55 Street", "55TH"),
            ("1234 North 66 Street", "66TH"),
            ("1234 North 77 Street", "77TH"),
            ("1234 North 88 Street", "88TH"),
            ("1234 North 99 Street", "99TH"),

            # Likewise 110-119 also end with "TH"
            ("1234 North 110 Street", "110TH"),
            ("1234 North 111 Street", "111TH"),
            ("1234 North 112 Street", "112TH"),
            ("1234 North 113 Street", "113TH"),
            ("1234 North 114 Street", "114TH"),
            ("1234 North 115 Street", "115TH"),
            ("1234 North 116 Street", "116TH"),
            ("1234 North 117 Street", "117TH"),
            ("1234 North 118 Street", "118TH"),
            ("1234 North 119 Street", "119TH"),
        ]

        for addr, exp in addrs:
            with self.subTest(addr=addr, exp=exp):
                parts = AddrParts.from_text(addr)
                self.assertEqual(parts.st_name, exp)

    def test_st_suffix_is_valid(self):
        addrs = [
            ("1234 North Fake Ave", AddrSuffix.AVE),
            ("1234 North Fake Avenue", AddrSuffix.AVE),
            ("1234 North Fake Boulevard", AddrSuffix.BLVD),
            ("1234 North Fake BLVD", AddrSuffix.BLVD),
            ("1234 North Fake Circle", AddrSuffix.CIRCLE),
            ("1234 North Fake CIR", AddrSuffix.CIRCLE),
            ("1234 North Fake Court", AddrSuffix.COURT),
            ("1234 North Fake CT", AddrSuffix.COURT),
            ("1234 North Fake Drive", AddrSuffix.DRIVE),
            ("1234 North Fake DR", AddrSuffix.DRIVE),
            ("1234 North Fake Lane", AddrSuffix.LANE),
            ("1234 North Fake LN", AddrSuffix.LANE),
            ("1234 North Fake PKWY", AddrSuffix.PKWY),
            ("1234 North Fake Place", AddrSuffix.PLACE),
            ("1234 North Fake PL", AddrSuffix.PLACE),
            ("1234 North Fake Road", AddrSuffix.ROAD),
            ("1234 North Fake RD", AddrSuffix.ROAD),
            ("1234 North Fake Square", AddrSuffix.SQUARE),
            ("1234 North Fake SQ", AddrSuffix.SQUARE),
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
