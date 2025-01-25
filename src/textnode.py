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
		if not self.url:
			return f"TextNode('{self.text}', TextType.{self.text_type.name})"
		return f"TextNode('{self.text}', TextType.{self.text_type.name}, {self.url})"