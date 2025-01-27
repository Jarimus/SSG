import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_ParentNodeNoChildren(self):
        parent = ParentNode("section", None)
        self.assertRaises(ValueError, parent.to_html)
    
    def test_ParentNodeNoTag(self):
        child1 = LeafNode("p", "This is paragraph1.")
        child2 = LeafNode("p", "This is paragraph two.", {"id": "test-para-2", "class": "key-paragraphs"})
        parent = ParentNode(None, [child1, child2])
        self.assertRaises(ValueError, parent.to_html)

    def test_ParentNodeChildrenNotNested(self):
        child1 = LeafNode("p", "This is paragraph1.")
        child2 = LeafNode("p", "This is paragraph two.", {"id": "test-para-2", "class": "key-paragraphs"})
        parent1 = ParentNode("section", [child1, child2], {"style": "color:red"})
        target = '<section style="color:red"><p>This is paragraph1.</p><p id="test-para-2" class="key-paragraphs">This is paragraph two.</p></section>'
        self.assertEqual(parent1.to_html(), target)

    def test_ParentNodeChildrenNested(self):
        child1 = LeafNode(None, "A paragraph", {"prop1": "value1", "prop2": "value2"})
        child2 = LeafNode("p", "Another paragraph", {"props": "values"})
        child3 = LeafNode("p", "A third paragraph", {"more-props": "with-values"})
        parent2 = ParentNode("div", [child1], {"class": "div-class"})
        parent3 = ParentNode("section", [child2, child3], {"class": "main-section"})
        parent1 = ParentNode("body", [parent2, parent3])

        target = '<body><div class="div-class">A paragraph</div><section class="main-section"><p props="values">Another paragraph</p><p more-props="with-values">A third paragraph</p></section></body>'
        self.assertEqual(parent1.to_html(), target)

if __name__ == '__main__':
     unittest.main()