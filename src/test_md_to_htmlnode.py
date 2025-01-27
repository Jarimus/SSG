import unittest
from markdown_conversion import markdown_to_html_node

class TestMdToHtmlNodes(unittest.TestCase):

    def test_paragraph(self):
        md = "This is a **paragraph** with some *inline* [elements](wiki.com/element)"
        html_nodes = markdown_to_html_node(md).to_html()
        target = '<div><p>This is a <b>paragraph</b> with some <i>inline</i> <a href="wiki.com/element">elements</a></p></div>'
        self.assertEqual(html_nodes, target)

if __name__ == '__main__':
    unittest.main()