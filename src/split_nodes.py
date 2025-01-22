from textnode import TextType, TextNode

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