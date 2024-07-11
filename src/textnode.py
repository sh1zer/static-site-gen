from htmlnode import LeafNode, HTMLNode, ParentNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

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
        return LeafNode(tag=None, value=text_node.text)
    
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
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        text:str = '' + node.text
        if text.count(delimiter) % 2 != 0:
            raise SyntaxError("Invalid markdown syntax (no closing delimiter)")
        segments = text.split(delimiter)
        for i in range(len(segments)):
            if i % 2:
                new_nodes.append(TextNode(segments[i], text_type))
            else:
                if len(segments[i]) > 0:
                    new_nodes.append(TextNode(segments[i], node.text_type))
        
    return new_nodes

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        text = '' + node.text
        final = []
        images = extract_markdown_images(node.text)
        for image in images:
            text = text.split(f"![{image[0]}]({image[1]})", 1)
            new_nodes.append(TextNode(text[0], node.text_type))
            new_nodes.append(TextNode(image[0], "image", image[1]))
            text = text[1]

        if len(text) > 0:
            new_nodes.append(TextNode(text, node.text_type))
    
    return new_nodes

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        text = '' + node.text
        final = []
        links = extract_markdown_links(node.text)
        for link in links:
            text = text.split(f"[{link[0]}]({link[1]})", 1)
            new_nodes.append(TextNode(text[0], node.text_type))
            new_nodes.append(TextNode(link[0], "link", link[1]))
            text = text[1]

        if len(text) > 0:
            new_nodes.append(TextNode(text, node.text_type))
    
    return new_nodes


def extract_markdown_images(text:str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text:str) -> list[tuple]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def text_to_text_nodes(text:str) -> list[TextNode]:
    new_nodes = split_nodes_image([TextNode(text, "text")])
    
    new_nodes = split_nodes_link(new_nodes)
    
    new_nodes = split_nodes_delimiter(new_nodes, "**", "bold")
    
    new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
    
    new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
    
    return new_nodes


def markdown_to_blocks(markdown:str) -> list[str]:
    lines = markdown.split('\n')
    final = ['']
    for line in lines:
        if line:
            final[-1] += line + '\n'
        elif final[-1] != '':
            final.append('')
    final = [block[:-1] for block in final]
    return final


def block_to_block_type(block:str) -> str:
    if len(block.split()[0]) == block.split()[0].count("#") and block.split()[0].count("#") in range(1,7):
        return block_type_heading
    
    if block[:4] == "```\n" and block[-4:] == "\n```":
        return block_type_code

    lines = block.split('\n')
    if len(lines) == [line[:2] for line in lines].count('> '):
        return block_type_quote

    if len(lines) == [line[:2] for line in lines].count('- ') or len(lines) == [line[:2] for line in lines].count('* '):
        return block_type_unordered_list
    
    for i in range(1, len(lines) + 1):
        if f"{i}. " != lines[i - 1][:len(f"{i}. ")]:
            break
        if i == len(lines):
            return block_type_ordered_list

    return block_type_paragraph


def block_heading_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_heading:
        raise ValueError(f"Incorrect block type ({block_to_block_type(block)})")
    level = block.split()[0].count("#")
    return HTMLNode(tag=f"h{level}", value=block[level + 1:], children=None, props=None)

def block_code_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_code:
        raise ValueError("Incorrect block type")
    return HTMLNode(tag="code", value=block[4:-4], children=None, props=None)

def block_quote_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_quote:
        raise ValueError("Incorrect block type")
    lines = block.split('\n')
    return HTMLNode(tag="blockquote", value='\n'.join([line[2:] for line in lines]), children=None, props=None)

def block_unordered_list_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_unordered_list:
        raise ValueError("Incorrect block type")
    lines = block.split('\n')
    return HTMLNode(tag="ul", value='\n'.join([f'<li>{line[2:]}</li>' for line in lines]), children=None, props=None)

def block_ordered_list_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_ordered_list:
        raise ValueError("Incorrect block type")
    lines = block.split('\n')
    return HTMLNode(tag="ol", value='\n'.join([f'<li>{' '.join(line.split()[1:])}</li>' for line in lines]), children=None, props=None)

def block_paragraph_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) != block_type_paragraph:
        raise ValueError(f"Incorrect block type ({block_to_block_type(block)})")
    return HTMLNode(tag="p", value=block, children=None, props=None)


def block_to_html(block:str) -> HTMLNode:
    if block_to_block_type(block) == block_type_heading:
        return block_heading_to_html(block)
    if block_to_block_type(block) == block_type_code:
        return block_code_to_html(block)
    if block_to_block_type(block) == block_type_quote:
        return block_quote_to_html(block)
    if block_to_block_type(block) == block_type_paragraph:
        return block_paragraph_to_html(block)
    if block_to_block_type(block) == block_type_ordered_list:
        return block_ordered_list_to_html(block)
    if block_to_block_type(block) == block_type_unordered_list:
        return block_unordered_list_to_html(block)
    raise ValueError("idk wtf happened here")
    

def text_to_children(text:str) -> list[HTMLNode]:
    res = []
    text_nodes = text_to_text_nodes(text)
    for node in text_nodes:
        res.append(text_node_to_html_node(node))
    #print(res)
    return res

def markdown_to_html_node(markdown:str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    og_children = [block_to_html(block) for block in blocks]
    new_children = []
    for kid in og_children:

        if kid.tag == "code":
            new_children.append(ParentNode("pre", children=[ParentNode(kid.tag, text_to_children(kid.value), kid.props)]))
        elif len(text_to_children(kid.value)) == 1:
            new_children.append(LeafNode(kid.tag, kid.value, kid.props))
            
        else:
            if kid.tag != "code":
                new_children.append(ParentNode(kid.tag, text_to_children(kid.value), kid.props))
            #else:
               # new_children.append(ParentNode("pre", children=[ParentNode(kid.tag, text_to_children(kid.value), kid.props)]))


    #print(HTMLNode(tag=None, value=None, children=new_children))
    return ParentNode(tag="div", children=new_children)
    