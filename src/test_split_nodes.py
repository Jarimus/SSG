import unittest
from text_conversion import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplittingNodes(unittest.TestCase):

    #TESTS FOR SPLITTING CODE, BOLD, and ITALIC TYPES
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
    
    #TESTS FOR SPLITTING LINKS
    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
        "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
        )
        ]
        self.assertEqual(new_nodes, target)

    def test_split_link_beginning(self):
        node = TextNode(
        "[This](a link) text starts with a link.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
        TextNode("This", TextType.LINK, "a link"),
        TextNode(" text starts with a link.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)
    
    def test_split_link_end(self):
        node = TextNode(
        "This text ends in a [link text](link)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
        TextNode("This text ends in a ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "link")
        ]
        self.assertEqual(new_nodes, target)
    
    def test_split_links_adjacent(self):
        node = TextNode(
            "This text has [two](link1)[ links](link2) next to each other.",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        target = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("two", TextType.LINK, "link1"),
            TextNode(" links", TextType.LINK, "link2"),
            TextNode(" next to each other.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)

    #TESTS FOR SPLITTING iMAGES
    def test_split_images(self):
        node = TextNode(
        "This is text with an image ![bootdev logo](boot.dev/logo) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
        TextNode("This is text with an image ", TextType.TEXT),
        TextNode("bootdev logo", TextType.IMAGE, "boot.dev/logo"),
        TextNode(" and a link [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, target)

    def test_split_img_beginning(self):
        node = TextNode(
        "![random img](link to img) This text starts with an image.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
        TextNode("random img", TextType.IMAGE, "link to img"),
        TextNode(" This text starts with an image.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)
    
    def test_split_img_end(self):
        node = TextNode(
        "This text ends in an ![image](img link)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
        TextNode("This text ends in an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "img link")
        ]
        self.assertEqual(new_nodes, target)
    
    def test_split_images_adjacent(self):
        node = TextNode(
            "This text has two images: ![This is image1](image1 link)![This is image2](image2 link)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        target = [
            TextNode("This text has two images: ", TextType.TEXT),
            TextNode("This is image1", TextType.IMAGE, "image1 link"),
            TextNode("This is image2", TextType.IMAGE, "image2 link")
        ]
        self.assertEqual(new_nodes, target)

        

if __name__ == '__main__':
     unittest.main()