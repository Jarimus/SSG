import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props1(self):
        node = HTMLNode("<p>", "a test paragraph", None, {"class": "main-paragraphs", "id": "first-paragraph"})
        prop_target = ' class="main-paragraphs" id="first-paragraph"'
        self.assertEqual(node.props_to_html(), prop_target, f"\nWANT {prop_target},\nGOT {node.props_to_html()}")
    
    def test_props2(self):
        node = HTMLNode("<p>", "a test paragraph")
        prop_target = ""
        self.assertEqual(node.props_to_html(), prop_target, f"\nWANT {prop_target},\nGOT {node.props_to_html()}")
    
    def test_props3(self):
        node = HTMLNode("<p>", "a test paragraph", None, {"id": "introduction"})
        prop_target = ' id="introduction"'
        self.assertEqual(node.props_to_html(), prop_target, f"\nWANT {prop_target},\nGOT {node.props_to_html()}")

if __name__ == '__main__':
     unittest.main()