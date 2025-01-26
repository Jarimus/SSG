from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props
    
    def to_html(self):
        if self.value == None:
            print(self)
            raise ValueError("A LeafNode must have a value.")
        elif self.tag == None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"