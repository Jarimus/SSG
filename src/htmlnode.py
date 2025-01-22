class HTMLNode():
    def __init__(self, tag: str =None, value: str =None, children: list =None, props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other: "HTMLNode"):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props = ""
        for attribute, value in self.props.items():
            props += f' {attribute}="{value}"'
        return props




if __name__ == '__main__':
    test = HTMLNode("<a>", "eeeet", ["div", "span"], {"href": "www.test.site", "target":"_blank"})
    repr = test.__repr__()
    print(repr)
    test2 = HTMLNode('<a>', 'eeeet', ['div', 'span'], {'href': 'www.test.site', 'target': '_blank'})
    print(test.__repr__() == test2.__repr__())