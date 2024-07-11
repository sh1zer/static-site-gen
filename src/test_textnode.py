import unittest

from htmlnode import LeafNode
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("\nTesting TextNode equal method", end='')
        node = TextNode("This is a test node", "bold", "url.com")
        node2 = TextNode("This is a test node", "bold", "url.com")
        self.assertEqual(node, node2)
    

    def test_text_to_html(self):
        print("\nTesting textNode to HTMLNode", end='')
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
        print("\nTesting split TextNode by delimiter", end='')
        node = TextNode("This `is` a test node", "text")
        node2 = TextNode("This is a **test node**", "text")
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
                                    TextNode("This is a **test node**", "text")])
        self.assertEqual(new_nodes3, [TextNode("This `is` a test node", "text"),
                                    TextNode("This is a ", "text"),
                                    TextNode("test node", "bold",),])
        

    def test_extract_markdown_images(self):
        print("\nTesting extract_markdown_images ", end='')
        text = extract_markdown_images("This is text with an ![image](https://link.com.png) and ![another](https://link2.com.png)")

        self.assertEqual(text, [("image", "https://link.com.png"), ("another", "https://link2.com.png")])


    def test_extract_markdown_links(self):
        print("\nTesting extract_markdown_links", end='')
        text = extract_markdown_links("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)")

        self.assertEqual(text, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        

    def test_split_nodes_image(self):
        print("\nTesting split_nodes_image", end='')
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
        
    def test_split_nodes_link(self):
        print("\nTesting split_nodes_link", end='')
        nodes = split_nodes_link([TextNode("This is text with an [link](https://link.com.png) and another [second link](https://url.com.png)","text")])
        nodes2 = split_nodes_link([TextNode("This is text with an [link](https://link.com.png) and another [second link](https://url.com.png)","text"),
                                    TextNode("This is text with an [link](https://link.com.png) and another [second link](https://url.com.png)","text")])

        self.assertEqual(nodes, [TextNode("This is text with an ", "text"),
                                TextNode("link", "link", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second link", "link", "https://url.com.png")])
        self.assertEqual(nodes2, [TextNode("This is text with an ", "text"),
                                TextNode("link", "link", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second link", "link", "https://url.com.png"),
                                TextNode("This is text with an ", "text"),
                                TextNode("link", "link", "https://link.com.png"),
                                TextNode(" and another ", "text"),
                                TextNode("second link", "link", "https://url.com.png"),])

    def test_text_to_text_nodes(self):
        print("\nTesting text_to_text_nodes", end='')
        nodes = text_to_text_nodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)")

        self.assertEqual(nodes, [
                                TextNode("This is ", "text"),
                                TextNode("text", "bold"),
                                TextNode(" with an ", "text"),
                                TextNode("italic", "italic"),
                                TextNode(" word and a ", "text"),
                                TextNode("code block", "code"),
                                TextNode(" and an ", "text"),
                                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                                TextNode(" and a ", "text"),
                                TextNode("link", "link", "https://boot.dev"),])
        
    def test_markdown_to_blocks(self):
        print("\nTesting markdown_to_blocks", end='')
        md = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        md2 = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list
* with items"""

        self.assertEqual(markdown_to_blocks(md), ["This is **bolded** paragraph", 
                                                  "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                                                  "* This is a list\n* with items"])
        self.assertEqual(markdown_to_blocks(md2), ["This is **bolded** paragraph", 
                                                  "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                                                  "* This is a list\n* with items"])
        
    def test_block_to_block_type(self):
        print("\nTesting block_to_block_type", end='')
        block1 = "### heading text"
        self.assertEqual(block_to_block_type(block1), block_type_heading)

        block1 = "####### not heading text"
        self.assertNotEqual(block_to_block_type(block1), block_type_heading)

        block1 = "#notheading text"
        self.assertNotEqual(block_to_block_type(block1), block_type_heading)

        block1 = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block1), block_type_code)

        block1 = "``\ncode block\n```"
        self.assertNotEqual(block_to_block_type(block1), block_type_code)

        block1 = "```code block```"
        self.assertEqual(block_to_block_type(block1), block_type_code)

        block1 = "> hi\n> this is a quote\n> dont get it twisted"
        self.assertEqual(block_to_block_type(block1), block_type_quote)

        block1 = "* hi\n* this is an unordered list\n* dont get it twisted"
        self.assertEqual(block_to_block_type(block1), block_type_unordered_list)

        block1 = "* hi\n- this is an unordered list\n* dont get it twisted"
        self.assertNotEqual(block_to_block_type(block1), block_type_unordered_list)

        block1 = "- hi\n- this is an unordered list\n- dont get it twisted"
        self.assertEqual(block_to_block_type(block1), block_type_unordered_list)

        block1 = "- hi\n-this is an unordered list\n- dont get it twisted"
        self.assertNotEqual(block_to_block_type(block1), block_type_unordered_list)

        block1 = "1. hi\n2. this is an ordered list\n3. dont get it twisted"
        self.assertEqual(block_to_block_type(block1), block_type_ordered_list)

        block1 = "1. hi\n2.this is an ordered list\n3. dont get it twisted"
        self.assertNotEqual(block_to_block_type(block1), block_type_ordered_list)

        block1 = "1. hi\n2. this is an ordered list\n2. dont get it twisted"
        self.assertNotEqual(block_to_block_type(block1), block_type_ordered_list)

    def test_block_type_to_html(self):
        print("\nTesting block_[type]_to_html", end='')
        block = "### heading text"
        self.assertEqual(block_heading_to_html(block), HTMLNode(tag="h3", value="heading text", children=None, props=None))
        
        block = "```heading text```"
        self.assertEqual(block_code_to_html(block), HTMLNode(tag="code", value="heading text", children=None, props=None))
        
        block = "```heading\n text```"
        self.assertEqual(block_code_to_html(block), HTMLNode(tag="code", value="heading\n text", children=None, props=None))
        
        block = ">heading text\n>heading text"
        self.assertEqual(block_quote_to_html(block), HTMLNode(tag="blockquote", value="heading text\nheading text", children=None, props=None))
        
        block = "- heading text\n- heading text"
        self.assertEqual(block_unordered_list_to_html(block), HTMLNode(tag="ul", value="<li>heading text</li>\n<li>heading text</li>", children=None, props=None))
        
        block = "* heading text\n* heading text"
        self.assertEqual(block_unordered_list_to_html(block), HTMLNode(tag="ul", value="<li>heading text</li>\n<li>heading text</li>", children=None, props=None))
        
        block = "1. heading text\n2. heading text"
        self.assertEqual(block_ordered_list_to_html(block), HTMLNode(tag="ol", value="<li>heading text</li>\n<li>heading text</li>", children=None, props=None))
        
        block = "heading text\nheading text"
        self.assertEqual(block_paragraph_to_html(block), HTMLNode(tag="p", value="heading text\nheading text", children=None, props=None))
        
        block = "### heading text"
        self.assertEqual(block_to_html(block), HTMLNode(tag="h3", value="heading text", children=None, props=None))
        
        block = "```heading text```"
        self.assertEqual(block_to_html(block), HTMLNode(tag="code", value="heading text", children=None, props=None))
        

    def test_text_to_children(self):
        print("\nTesting text_to_children", end='')
        block = "heading text **bold text** `code text` just some more *italics* hehe ![image](https://url.com.png) hoho [link](https://link.edu.pl) hahaha"
        self.assertEqual(text_to_children(block), [LeafNode(tag=None, value="heading text ", props=None),
                                                    LeafNode(tag="b", value="bold text", props=None),
                                                    LeafNode(tag=None, value=" ", props=None),
                                                    LeafNode(tag="code", value="code text", props=None),
                                                    LeafNode(tag=None, value=" just some more ", props=None),
                                                    LeafNode(tag="i", value="italics", props=None),
                                                    LeafNode(tag=None, value=" hehe ", props=None),
                                                    LeafNode(tag="img", value="image", props={"src":"https://url.com.png"}),
                                                    LeafNode(tag=None, value=" hoho ", props=None),
                                                    LeafNode(tag="a", value="link", props={"href":"https://link.edu.pl"}),
                                                    LeafNode(tag=None, value=" hahaha", props=None),])
        
    def test_markdown_to_html_node(self):
        print("\nTesting markdown_to_html_node", end='')
        block = "heading text**bold text** `code text` just some more *italics* hehe ![image](https://url.com.png) hoho [link](https://link.edu.pl) hahaha"
        mth_block = markdown_to_html_node(block)
        expected = ParentNode(tag="div", children=[ParentNode(tag="p", children=[LeafNode(tag=None, value="heading text", props=None),
                                                                                        LeafNode(tag="b", value="bold text", props=None),
                                                                                        LeafNode(tag=None, value=" ", props=None),
                                                                                        LeafNode(tag="code", value="code text", props=None),
                                                                                        LeafNode(tag=None, value=" just some more ", props=None),
                                                                                        LeafNode(tag="i", value="italics", props=None),
                                                                                        LeafNode(tag=None, value=" hehe ", props=None),
                                                                                        LeafNode(tag="img", value="image", props={"src":"https://url.com.png"}),
                                                                                        LeafNode(tag=None, value=" hoho ", props=None),
                                                                                        LeafNode(tag="a", value="link", props={"href":"https://link.edu.pl"}),
                                                                                        LeafNode(tag=None, value=" hahaha", props=None),], props=None)])
        #for i in range(len(str(mth_block).split('LeafNode'))):
        #    print(f"{str(mth_block).split('LeafNode')[i]}\n{str(expected).split('LeafNode')[i]}\n\n")
        self.assertEqual(mth_block, expected)

        block = "# heading text**bold text** `code text`\n\n- just some more\n- *italics* hehe ![image](https://url.com.png)\n\n> hoho [link](https://link.edu.pl)\n\n```codeblock*bangbang*```"
        mth_block = markdown_to_html_node(block)
        expected = ParentNode(tag="div", children=[ParentNode(tag="h1", children=[LeafNode(tag=None, value="heading text", props=None),
                                                                                        LeafNode(tag="b", value="bold text", props=None),
                                                                                        LeafNode(tag=None, value=" ", props=None),
                                                                                        LeafNode(tag="code", value="code text", props=None),]),
                                                            ParentNode(tag="ul", children=[LeafNode(tag=None, value="<li>just some more</li>\n<li>", props=None),
                                                                                        LeafNode(tag="i", value="italics", props=None),
                                                                                        LeafNode(tag=None, value=" hehe ", props=None),
                                                                                        LeafNode(tag="img", value="image", props={"src":"https://url.com.png"}),
                                                                                        LeafNode(tag=None, value="</li>", props=None),]),
                                                            ParentNode(tag="blockquote", children=[LeafNode(tag=None, value=" hoho ", props=None),
                                                                                        LeafNode(tag="a", value="link", props={"href":"https://link.edu.pl"}),]),
                                                            ParentNode(tag="pre", children=[ParentNode("code", children=[LeafNode(tag=None, value="codeblock"),
                                                                                                                        LeafNode(tag='i', value="bangbang"),])])                            
                                                                                        ])
        #for i in range(len(str(mth_block).split('LeafNode'))):
        #    print(f"{str(mth_block).split('LeafNode')[i]}\n{str(expected).split('LeafNode')[i]}\n\n")
        #print(mth_block.to_html())
        self.assertEqual(str(mth_block), str(expected))

        


if __name__ == '__main__':
    unittest.main()