import unittest

from htmlnode import LeafNode
from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("\nTesting TextNode equal method")
        node = TextNode("This is a test node", "bold", "url.com")
        node2 = TextNode("This is a test node", "bold", "url.com")
        self.assertEqual(node, node2)
    
    def test_text_to_html(self):
        print("\nTesting textNode to HTMLNode OK")
        node = text_node_to_html_node(TextNode("This is a test node", "text"))
        node2 = text_node_to_html_node(TextNode("This is a test node", "bold"))
        node3 = text_node_to_html_node(TextNode("This is a test node", "italic"))
        node4 = text_node_to_html_node(TextNode("This is a test node", "code"))
        node5 = text_node_to_html_node(TextNode("This is a test node", "link", "url.com"))
        node6 = text_node_to_html_node(TextNode("This is a test node", "image", "srcofimg.com"))

        self.assertEqual(node, LeafNode(tag=None, value="This is a test node", props=None))
        self.assertEqual(node2, LeafNode(tag="b", value="This is a test node", props=None))
        self.assertEqual(node3, LeafNode(tag="i", value="This is a test node", props=None))
        self.assertEqual(node4, LeafNode(tag="code", value="This is a test node", props=None))
        self.assertEqual(node5, LeafNode(tag="a", value="This is a test node", props={"href":"url.com"}))
        self.assertEqual(node6, LeafNode(tag="img", value="This is a test node", props={"src":"srcofimg.com"}))

    def test_split_by_delimiter(self):
        print("\nTesting split TextNode by delimiter")
        node = TextNode("This `is` a test node", "text")
        node2 = TextNode("This is a **test node**", "italic")
        node3 = TextNode("This is a test node", "italic")
        node4 = TextNode("This is a test node", "code")
        
        new_nodes1 = split_nodes_delimiter([node], '`', "code")
        new_nodes2 = split_nodes_delimiter([node, node2], '`', "code")
        new_nodes3 = split_nodes_delimiter([node, node2], '**', "bold")

        self.assertEqual(new_nodes1, [TextNode("This ", "text"),
                                    TextNode("is", "code",),
                                    TextNode(" a test node", "text")])
        self.assertEqual(new_nodes2, [TextNode("This ", "text"),
                                    TextNode("is", "code",),
                                    TextNode(" a test node", "text"),
                                    TextNode("This is a **test node**", "italic")])
        self.assertEqual(new_nodes3, [TextNode("This `is` a test node", "text"),
                                    TextNode("This is a ", "italic"),
                                    TextNode("test node", "bold",),
                                    TextNode("", "italic"),])
        

if __name__ == '__main__':
    unittest.main()