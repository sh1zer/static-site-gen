import unittest
from generate_page import *

class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# hello"
        self.assertEqual(extract_title(md), "hello")

        md = "# hello\nnot header anymore"
        self.assertEqual(extract_title(md), "hello")
    
    def test_generate_page(self):
        generate_page("content/index.md", "template.html", "test/hehe.html")