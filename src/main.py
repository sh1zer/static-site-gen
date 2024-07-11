from textnode import TextNode
from copy_static import copy_dir

def main():
    node = TextNode("test text", "text type", "this is a url")

    copy_dir("static", "public")
    #print(node)

main()
