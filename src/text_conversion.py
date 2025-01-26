from textnode import TextNode, TextType
from split_nodes import split_nodes_image, split_nodes_delimiter, split_nodes_link
from leafnode import LeafNode
from parentnode import ParentNode

def text_to_text_nodes(text: str):
	new_nodes = [TextNode(text, TextType.TEXT)]
	delimiters = [("`", TextType.CODE), ("**", TextType.BOLD), ("*", TextType.ITALIC)]
	
	#split with each function. nested text types are not handled -> functions can be called separately.
	for delimiter, type in delimiters:
		new_nodes = split_nodes_delimiter(new_nodes, delimiter, type)
	new_nodes = split_nodes_image(new_nodes)
	new_nodes = split_nodes_link(new_nodes)
	return new_nodes

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
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
	raise Exception("Invalid TextType for TextNode")

def text_to_html_nodes(block_text: str, tag: str):
    text_nodes = text_to_text_nodes(block_text)
    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append( text_node_to_html_node(text_node) )
    return ParentNode(tag, child_nodes)


if __name__ == '__main__':
	text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
	result = text_to_text_nodes(text)
	print(result)