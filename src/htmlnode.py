
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        res = ""
        for ele in self.props:
            res += f" {ele}=\"{self.props[ele]}\""
        return res

    def __repr__(self) -> str:
        return f"HTMLNode(tag=\"{self.tag}\", value=\"{self.value}\", children={self.children}, props={self.props})"
    
    def __eq__(self, other) -> bool:
        return (self.tag == other.tag and 
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        if value == None:
            raise ValueError("No value provided for leaf")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("No value in LeafNode")
        if self.tag == None:
            return self.value
        
        all_props = self.props_to_html() if self.props else ""
        return f"<{self.tag}{all_props}>{self.value}</{self.tag}>"
    def __repr__(self) -> str:
        return f"LeafNode(tag=\"{self.tag}\", value=\"{self.value}\", children={self.children}, props={self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        if children == None:
            raise ValueError("No children provided for parent")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided for parent")
        if self.children == None:
            raise ValueError("No children provided for parent")
        
        res = f'<{self.tag}{self.props_to_html() if self.props else ""}>'
        for child in self.children:
            res += child.to_html()
        res += f'</{self.tag}>'
        return res
    
    def __repr__(self) -> str:
        return f"ParentNode(tag=\"{self.tag}\", value=\"{self.value}\", children={self.children}, props={self.props})"