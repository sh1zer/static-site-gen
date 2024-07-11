import unittest
from generate_page import *

class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# hello"
        self.assertEqual(extract_title(md), "hello")

        md = "# hello\nnot header anymore"
        self.assertEqual(extract_title(md), "hello")