from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text: str, text_type: TextType, url:str=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other: "TextNode"):
		return self.text_type == other.text_type and self.text == other.text and self.url == other.url
	
	def __repr__(self):
		return f"TextNode('{self.text}', TextType.{self.text_type.name}, {self.url})"
	
def text_node_to_html_node(text_node: TextNode):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
	raise Exception("Invalid TextType for TextNode")