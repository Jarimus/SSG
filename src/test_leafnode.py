import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_LeafNodeNoProps(self):
       node = LeafNode("p", "This is a paragraph of text.")
       self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_LeafNodeProps(self):
       node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
       self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_LeafNodeValueOnly(self):
        node = LeafNode(None, "This is a test value")
        self.assertEqual(node.to_html(), "This is a test value")

    def test_LeafNodeNoValue(self):
        node = LeafNode("a", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == '__main__':
     unittest.main()