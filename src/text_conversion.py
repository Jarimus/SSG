from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
import re


def text_to_text_nodes(text: str):
    """Converts a string to text nodes: normal, code, bold, italic, image, and link."""
    new_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [("`", TextType.CODE), ("**", TextType.BOLD), ("*", TextType.ITALIC)]

    #split with each function. nested text types are not handled -> functions can be called separately.
    for delimiter, type in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def text_node_to_html_node(text_node: TextNode):
    """Converts text nodes to corresponding HTML nodes. They all convert to LeafNodes, because text nodes do not have children nodes."""
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
    """Converts a string to HTML nodes that can be converted to HTML with their method to_html().
    The LeafNodes are contained in a ParentNode whose type (paragraph, heading, list, ...) is defined by it's markdown block type.
    See markdown_conversion.py for the block type definition."""
    text_nodes = text_to_text_nodes(block_text)
    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append( text_node_to_html_node(text_node) )
    return ParentNode(tag, child_nodes)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Splits TextNodes with TEXT-type to other types of TextNodes: BOLD, ITALIC, CODE, LINK, IMAGE."""
    new_nodes = []

    for node in old_nodes:
        #only TEXT types are split
        if not node.text_type.TEXT:
            new_nodes.append(node)
            continue
        else:
            #Make sure there are an even number of delimiters for the split.
            if node.text.count(delimiter) == 0:
                new_nodes.append(node)
                continue
            elif node.text.count(delimiter) % 2 != 0:
                raise Exception("Closing delimiter not found. Every opening delimiter should pair with a closing delimiter.")
            
            #start splitting the node into smaller nodes
            text_parts = node.text.split(delimiter)
            #remove "" texts
            for text_part in text_parts:
                if text_part == "":
                    text_parts.remove(text_part)
            if node.text.index(delimiter) == 0:
                for i, text_part in enumerate(text_parts):
                    if i % 2 == 0:
                        new_node = TextNode(text_part, text_type)
                    else:
                        new_node = TextNode(text_part, TextType.TEXT)

                    new_nodes.append(new_node)
            else:
                for i, text_part in enumerate(text_parts):
                    if i % 2 == 0:
                        new_node = TextNode(text_part, TextType.TEXT)
                    else:
                        new_node = TextNode(text_part, text_type)

                    new_nodes.append(new_node)
    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    """Parses markdown image links from TextNodes."""
    new_nodes = []

    for node in old_nodes:
        imgs = extract_markdown_images(node.text) #extract potential nodes
        
        #no images -> append the node as is
        if imgs == []:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        while True: #images -> start splitting the node and appending to new_nodes
            image_text, image_url = imgs.pop(0)
            sep = f"![{image_text}]({image_url})"
            text, remaining_text = remaining_text.split(sep, maxsplit=1)

            
            new_image = TextNode(image_text, TextType.IMAGE, image_url)
            #if the string starts with an image, the split creates an exmpty string. Ignore it, append only IMAGE.
            if text == "":
                new_nodes.append(new_image)
            else: #otherwise create a TEXT and a IMAGE to append to the new_nodes.
                new_text = TextNode(text, TextType.TEXT)
                new_nodes.append(new_text)
                new_nodes.append(new_image)


            if imgs == [] and remaining_text == "":
                break
            elif imgs == []:
                final_text = TextNode(remaining_text, TextType.TEXT)
                new_nodes.append(final_text)
                break
            elif text == "":
                while imgs != []:
                    image_text, image_url = imgs.pop(0)
                    new_image = TextNode(image_text, TextType.IMAGE, image_url)
                    new_nodes.append(new_image)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    """Parses markdown links from TextNodes."""
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text) #extract potential nodes
        
        #no links -> append the node as is
        if links == []:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        while True: #links -> start splitting the node and appending to new_nodes
            link_text, link_url = links.pop(0)
            sep = f"[{link_text}]({link_url})"
            text, remaining_text = remaining_text.split(sep, maxsplit=1)

            
            new_link = TextNode(link_text, TextType.LINK, link_url)
            #if the string starts with a link, the split creates an exmpty string. Ignore it, append only LINK.
            if text == "":
                new_nodes.append(new_link)
            else: #otherwise create a TEXT and a LINK to append to the new_nodes.
                new_text = TextNode(text, TextType.TEXT)
                new_nodes.append(new_text)
                new_nodes.append(new_link)


            if links == [] and remaining_text == "":
                break
            elif links == []:
                final_text = TextNode(remaining_text, TextType.TEXT)
                new_nodes.append(final_text)
                break
            elif text == "":
                while links != []:
                    link_text, link_url = links.pop(0)
                    new_link = TextNode(link_text, TextType.LINK, link_url)
                    new_nodes.append(new_link)

    return new_nodes


def extract_markdown_images(markdown: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)


def extract_markdown_links(markdown: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)