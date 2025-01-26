import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from text_conversion import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq2(self):
        node1 = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("Is this a test?", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_nq1(self):
        node1 = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("This is a test", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_TEXT_to_html(self):
        text_node = TextNode("Text", TextType.TEXT)
        target = LeafNode(None, "Text")
        self.assertEqual(text_node_to_html_node(text_node), target)

    def test_BOLD_to_html(self):
        text_node = TextNode("Some very bold text", TextType.BOLD)
        target = LeafNode("b", "Some very bold text")
        self.assertEqual(text_node_to_html_node(text_node), target)

    def test_ITALIC_to_html(self):
        text_node = TextNode("Some Italian text", TextType.ITALIC)
        target = LeafNode("i", "Some Italian text")
        self.assertEqual(text_node_to_html_node(text_node), target)

    def test_CODE_to_html(self):
        text_node = TextNode("L33t code", TextType.CODE)
        target = LeafNode("code", "L33t code")
        self.assertEqual(text_node_to_html_node(text_node), target)

    def test_LINK_to_html(self):
        text_node = TextNode("Link anchor text", TextType.LINK, "www.website.io")
        target = LeafNode("a", "Link anchor text", {"href": text_node.url})
        self.assertEqual(text_node_to_html_node(text_node), target)

    def test_IMAGE_to_html(self):
        text_node = TextNode("Alt text", TextType.IMAGE)
        target = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        self.assertEqual(text_node_to_html_node(text_node), target)


if __name__ == '__main__':
    unittest.main()
