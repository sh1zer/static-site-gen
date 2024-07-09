import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        print("\nTesting HTMLNode")
        node = HTMLNode(tag="p", value="testValue", children=None, props={"testKey":"testItem"})
        parentNode = HTMLNode(tag="p2", value="testValue2", children=[node], props={"testKey2":"testItem2"})

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "testValue")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"testKey": "testItem"})
        
        self.assertEqual(parentNode.tag, "p2")
        self.assertEqual(parentNode.value, "testValue2")
        self.assertEqual(parentNode.children[0], node)
        self.assertEqual(parentNode.props, {"testKey2": "testItem2"})

    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="testValue", children=None, props={"testKey":"testItem"})
        parentNode = HTMLNode(tag="p2", value="testValue2", children=[node], props={"testKey2":"testItem2"})
        self.assertEqual(node.props_to_html(), " testKey=\"testItem\"")
        self.assertEqual(parentNode.children[0].props_to_html(), " testKey=\"testItem\"")

class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        print("\nTesting LeafNode")
        leaf2 = LeafNode("a", "testValue2", {"href":"htpps://link.com"})
        leaf = LeafNode("p", "testValue")

        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "testValue")
        self.assertEqual(leaf.props, None)

        self.assertEqual(leaf2.tag, "a")
        self.assertEqual(leaf2.value, "testValue2")
        self.assertEqual(leaf2.props, {"href":"htpps://link.com"})

    def test_to_html(self):
        leaf = LeafNode("p", "testValue")
        leaf2 = LeafNode("a", "testValue2", {"href":"htpps://link.com"})

        self.assertEqual(leaf.to_html(), "<p>testValue</p>")
        self.assertEqual(leaf2.to_html(), "<a href=\"htpps://link.com\">testValue2</a>")
        

class TestParentNode(unittest.TestCase):
    def test_constructor(self):
        print("\nTesting ParentNode")
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )        

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children,  [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), 
                                        LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.props, None)


        
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )    
        node2 = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href":"htpps://link.com"}
        )    
        node3 = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
            {"href":"htpps://link.com"}
        )    
   

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(node2.to_html(), "<a href=\"htpps://link.com\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>")
        self.assertEqual(node3.to_html(), "<a href=\"htpps://link.com\"><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></a>")

if __name__ == "__main__":
    unittest.main()
