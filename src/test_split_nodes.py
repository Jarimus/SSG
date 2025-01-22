import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplittingNodes(unittest.TestCase):

    def test_empty_list(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        target = []
        self.assertEqual(new_nodes, target)
    
    def test_CODE_Splitting(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        target = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target)

    def test_BOLD_Splitting_Delimiter_Beginning(self):
        node = TextNode("**This** word is very bold.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        target = [
            TextNode("This", TextType.BOLD),
            TextNode(" word is very bold.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target)
    
    def test_ITALIC_Delimiter_end(self):
        node = TextNode("Last word: *italian*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        target = [
            TextNode("Last word: ", TextType.TEXT),
            TextNode("italian", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, target)

    def test_NO_Splitting(self):
        node = TextNode("Just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        target = [
            TextNode("Just text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)

    def test_multiple_split_sections(self):
        node = TextNode("Madness? **This** is **SPARTA**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        target = [
            TextNode("Madness? ", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("SPARTA", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, target)

    def test_multiple_nodes(self):
        node1 = TextNode("Madness? **This** is **SPARTA**", TextType.TEXT)
        node2 = TextNode("Last word: **bold**", TextType.TEXT)
        node3 = TextNode("This is text with a NON-**code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        target = [
            TextNode("Madness? ", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("SPARTA", TextType.BOLD),
            TextNode("Last word: ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("This is text with a NON-", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target)

if __name__ == '__main__':
     unittest.main()