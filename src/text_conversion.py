from textnode import TextNode, TextType
from split_nodes import split_nodes_image, split_nodes_delimiter, split_nodes_link

def text_to_text_nodes(text: str):
	new_nodes = [TextNode(text, TextType.TEXT)]
	delimiters = [("`", TextType.CODE), ("**", TextType.BOLD), ("*", TextType.ITALIC)]
	
	#split with each function. nested text types are not handled -> functions can be called separately.
	for delimiter, type in delimiters:
		new_nodes = split_nodes_delimiter(new_nodes, delimiter, type)
	new_nodes = split_nodes_image(new_nodes)
	new_nodes = split_nodes_link(new_nodes)
	return new_nodes


if __name__ == '__main__':
	text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
	result = text_to_text_nodes(text)
	print(result)