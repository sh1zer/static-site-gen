from textnode import TextNode
from copy_static import copy_dir
from generate_page import generate_page
import shutil
import os

def main():
    if os.path.isdir('public'):
        shutil.rmtree('public')
    os.mkdir('public')
    copy_dir("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")
    #print(node)

main()
