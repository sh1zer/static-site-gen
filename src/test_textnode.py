import unittest

from htmlnode import LeafNode
from textnode import *


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
                                    TextNode("test node", "bold",),])
        

    def test_extract_markdown_images(self):
        print("\nTesting extract_markdown_images ")
        text = extract_markdown_images("This is text with an ![image](https://link.com.png) and ![another](https://link2.com.png)")

        self.assertEqual(text, [("image", "https://link.com.png"), ("another", "https://link2.com.png")])


    def test_extract_markdown_links(self):
        print("\nTesting extract_markdown_links")
        text = extract_markdown_links("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)")

        self.assertEqual(text, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        

    def test_split_nodes_image(self):
        print("\nTesting split_nodes_image")
        nodes = split_nodes_image([TextNode("This is text with an ![image](https://link.com.png) and another ![second image](https://url.com.png)","text")])
        nodes2 = split_nodes_image([TextNode("This is text with an ![image](https://link.com.png) and another ![second image](https://url.com.png)","text"),
                                    TextNode("This is text with an ![image](https://link.com.png) and another ![second image](https://url.com.png)","text")])

        self.assertEqual(nodes, [TextNode("This is text with an ", "text"),
                                TextNode("image", "image", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second image", "image", "https://url.com.png")])
        self.assertEqual(nodes2, [TextNode("This is text with an ", "text"),
                                TextNode("image", "image", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second image", "image", "https://url.com.png"),
                                TextNode("This is text with an ", "text"),
                                TextNode("image", "image", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second image", "image", "https://url.com.png"),])
        




if __name__ == '__main__':
    unittest.main()