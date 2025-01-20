import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq2(self):
        node1 = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("Is this a test?", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_nq1(self):
        node1 = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("This is a test", TextType.TEXT)
        self.assertNotEqual(node1, node2)


if __name__ == '__main__':
    unittest.main()