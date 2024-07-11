import re

def extract_title(markdown:str) -> str:
    return re.findall(r"# (.*)", markdown)[0].split('\n')[0]