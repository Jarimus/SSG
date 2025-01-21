from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        self.tag = tag
        self.value = None
        self.children = children
        self.props = props
    
    def to_html(self):
        if not self.tag:
            raise ValueError("A ParentNode requires a tag.")
        if not self.children:
            raise ValueError("A ParentNode requires child nodes.")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

if __name__ == '__main__':
    child1 = LeafNode("p", "This is paragraph1.")
    child2 = LeafNode("p", "This is paragraph two.", {"id": "test-para-2", "class": "key-paragraphs"})
    parent1 = ParentNode("section", [child1, child2], {"style": "color:red"})
    parent2 = ParentNode("body", [parent1])

    print(parent2.to_html())