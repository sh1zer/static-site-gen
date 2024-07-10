from htmlnode import LeafNode
import re

class TextNode:
    def __init__(self, text:str, text_type:str, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == "text":
        return LeafNode(value=text_node.text)
    
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    
    elif text_node.text_type == "link":
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    
    elif text_node.text_type == "image":
        return LeafNode(tag="img", value=text_node.text, props={"src":text_node.url})
    
def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:str) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        text:str = '' + node.text
        if text.count(delimiter) % 2 != 0:
            raise SyntaxError("Invalid markdown syntax (no closing delimiter)")
        segments = text.split(delimiter)
        for i in range(len(segments)):
            if i % 2:
                new_nodes.append(TextNode(segments[i], text_type))
            else:
                new_nodes.append(TextNode(segments[i], node.text_type))
        
    return new_nodes


def extract_markdown_images(text:str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text:str) -> list[tuple]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
