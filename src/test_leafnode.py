import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_LeafNodeNoProps(self):
       node = LeafNode("p", "This is a paragraph of text.")
       target = "<p>This is a paragraph of text.</p>"
       self.assertEqual(node.to_html(), target, f"\nWANT {target},\ngot {node.to_html()}")

    def test_LeafNodeProps(self):
       node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
       target = '<a href="https://www.google.com">Click me!</a>'
       self.assertEqual(node.to_html(), target, f"\nWANT {target},\ngot {node.to_html()}")

    def test_LeafNodeValueOnly(self):
        node = LeafNode(None, "This is a test value")
        target = "This is a test value"
        self.assertEqual(node.to_html(), target, f"\nWANT {target},\ngot {node.to_html()}")

    def test_LeafNodeNoValue(self):
        node = LeafNode("a", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == '__main__':
     unittest.main()