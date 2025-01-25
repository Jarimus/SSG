from md_to_blocks import markdown_to_blocks, block_to_block_type
from text_conversion import text_to_html_nodes
from parentnode import ParentNode

def markdown_to_html_node(markdown: str) -> ParentNode:
    md_blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in md_blocks: # text to TextNodes (text_to_text_nodes) -> TextNodes to LeafNodes ()
        block_type = block_to_block_type(block)
        block_text = remove_md_prefix(block, block_type) #MD Prefixes and suffixes (#, >, ```, ...) removed

        #go through all the options for a block type: heading, paragraph, code, quote, ul, ol
        if 'heading' in block_type: #<h#> ParentNode, direct LeafNode children
            heading_number = block_type[-1]
            html_nodes.append( text_to_html_nodes(block_text, "h" + heading_number) )
        elif block_type == 'paragraph': #<p> ParentNode, direct LeafNode children
            html_nodes.append( text_to_html_nodes(block_text, "p") )
        elif block_type == 'code': #<pre> ParentNode with <code> ParentNode child, with LeafNode children.
            html_nodes.append( ParentNode("pre", [text_to_html_nodes(block_text, "code")]) )
        elif block_type == 'quote': #<blockquote> ParentNode with LeafNode children.
            html_nodes.append( text_to_html_nodes(block_text, "blockquote") )
        elif block_type == 'ul': #<ul>=ParentNode, <li>=ParentNode, children of <ul>, LeafNodes children of <li>s
            lines = block_text.split("\n")
            list_items = []
            for line in lines:
                list_items.append( text_to_html_nodes(line, "li") )
            html_nodes.append( ParentNode( "ul", list_items ))
        elif block_type == 'ol': #<ol>=ParentNode, <li>=ParentNode, children of <ul>, LeafNodes children of <li>s
            lines = block_text.split("\n")
            list_items = []
            for line in lines:
                list_items.append( text_to_html_nodes(line, "li") )
            html_nodes.append( ParentNode( "ol", list_items ))
    return ParentNode("div", html_nodes)

def remove_md_prefix(text: str, block_type: str) -> str:
    """Returns a markdown text without the prefixes of a heading (#), code (```), quote (>) and such.
    Also removes the suffix ```of a code block."""
    if 'heading' in block_type:
        return text.split(" ", maxsplit=1)[1].strip()
    elif block_type == 'paragraph':
        return text.strip()
    elif block_type == 'code':
        return text[3:-3].strip()
    elif block_type == 'quote':
        lines = text.split("\n")
        text = ""
        for line in lines:
            text += line[1:].strip() + "\n"
        return text.strip()
    elif block_type in ['ul', 'ol']:
        lines = text.split("\n")
        text = ""
        for line in lines:
            text += line[2:].strip() + "\n"
        return text.strip()

if __name__ == '__main__':
    md = "This is a **paragraph** with some *inline* [elements](wiki.com/element)"
    html_nodes = markdown_to_html_node(md)
    print( html_nodes.to_html() )