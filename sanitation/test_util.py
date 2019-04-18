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


class TestStripHtmlTags(unittest.TestCase):
    def test_strip_html_tags_returns_without_tags(self):
        HTML = "<a href=\"blah\">some link <br/> and <strong>text <> with content</strong>"
        text = strip_html_tags(HTML)
        self.assertEqual(text, "some link  and text  with content")

    def test_strip_html_tags_returns_input_when_no_tags_are_present(self):
        HTML = "No tags in this text"
        text = strip_html_tags(HTML)
        self.assertEqual(text, "No tags in this text")

    def test_strip_html_tags_returns_empty_string_when_given_empty_string(self):
        HTML = ""
        text = strip_html_tags(HTML)
        self.assertEqual(text, "")
