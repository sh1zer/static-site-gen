import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("\nTesting TextNode equal method")
        node = TextNode("This is a test node", "bold", "url.com")
        node2 = TextNode("This is a test node", "bold", "url.com")
        self.assertEqual(node, node2)

if __name__ == '__main__':
    unittest.main()