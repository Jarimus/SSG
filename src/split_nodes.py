from textnode import TextType, TextNode
from extractors import extract_markdown_images, extract_markdown_links
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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
    new_nodes = []

    for node in old_nodes:
        imgs = extract_markdown_images(node.text) #extract potential nodes
        
        #no links -> append the node as is
        if imgs == []:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        while True: #links -> start splitting the node and appending to new_nodes
            link_text, link_url = imgs.pop(0)
            sep = f"![{link_text}]({link_url})"
            text, remaining_text = remaining_text.split(sep, maxsplit=1)

            
            new_link = TextNode(link_text, TextType.IMAGE, link_url)
            #if the string starts with a link, the split creates an exmpty string. Ignore it, append only LINK.
            if text == "":
                new_nodes.append(new_link)
            else: #otherwise create a TEXT and a LINK to append to the new_nodes.
                new_text = TextNode(text, TextType.TEXT)
                new_nodes.append(new_text)
                new_nodes.append(new_link)


            if imgs == [] and remaining_text == "":
                break
            elif imgs == []:
                final_text = TextNode(remaining_text, TextType.TEXT)
                new_nodes.append(final_text)
                break
            elif text == "":
                while imgs != []:
                    link_text, link_url = imgs.pop(0)
                    new_link = TextNode(link_text, TextType.IMAGE, link_url)
                    new_nodes.append(new_link)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
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
