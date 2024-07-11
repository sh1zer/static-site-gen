import re
import os
from htmlnode import HTMLNode
from textnode import markdown_to_html_node

def extract_title(markdown:str) -> str:
    return re.findall(r"# (.*)", markdown)[0].split('\n')[0]

def generate_page(source_path:str, template_path:str, dest_path:str) -> None:
    print(f"generating page from {source_path} into {dest_path} using {template_path} as template\n\n")

    markdown = ""
    with open(source_path) as src:
        markdown += src.read()

    template = ""
    with open(template_path) as temp:
        template += temp.read()

    html_string = markdown_to_html_node(markdown).to_html()
    #print(html_string + '\n\n')


    template = template.replace("{{ Title }}", extract_title(markdown), 1)
    template = template.replace("{{ Content }}", html_string, 1)
    #print(template)
    if os.path.isdir('/'.join(dest_path.split('/')[:-1])):
        with open(dest_path, "w") as dest:
            dest.write(template)
    else:
        raise Exception("Directory doesnt exist")
