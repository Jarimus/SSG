class HTMLNode():
    def __init__(self, tag: str =None, value: str =None, children: list =None, props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode('{self.tag}', '{self.value}', {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
<<<<<<< HEAD
            return None
=======
            return ""
>>>>>>> 04bc2c8 (implement LeafNode)
        result = ""
        for attribute, value in self.props.items():
            result += f' {attribute}="{value}"'
        return result




if __name__ == '__main__':
    test = HTMLNode("<a>", "eeeet", ["div", "span"], {"href": "www.test.site", "target":"_blank"})
    repr = test.__repr__()
    print(repr)
    test2 = HTMLNode('<a>', 'eeeet', ['div', 'span'], {'href': 'www.test.site', 'target': '_blank'})
    print(test.__repr__() == test2.__repr__())