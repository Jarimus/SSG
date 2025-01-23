import unittest
from textnode import TextNode, TextType
from text_conversion import text_to_text_nodes

class TestTextConversion(unittest.TestCase):

    def test_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_nodes(text)
        target = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, target)
    
    def test_no_delimiter_split(self):
        text = "[This](link) text has no bold, italic or code blocks ![cat image](image url)"
        new_nodes = text_to_text_nodes(text)
        target = [
            TextNode("This", TextType.LINK, "link"),
            TextNode(" text has no bold, italic or code blocks ", TextType.TEXT),
            TextNode("cat image", TextType.IMAGE, "image url")
        ]
        self.assertEqual(new_nodes, target)

if __name__ == '__main__':
    unittest.main()