import re
from parentnode import ParentNode
from text_conversion import text_to_html_nodes

def markdown_to_blocks(text: str) -> list[str]:
    """Converts a markdown string into a list of blocks that relate to html elements:
    headings, quotes, codeblocks, paragraphs, unordered lists, and ordered lists."""
    lines = text.split("\n")
    blocks = []
    current_block = ""

    for line in lines:
        line = line.strip()
        #if the line is empty, append the current block if it is not empty after stripping any leading or trailing whitespaces.
        if line == "":
            if current_block.strip() != "":
                current_block = current_block.strip()
                blocks.append(current_block)
            current_block = ""
        else:
            current_block += line.strip() + "\n"
    else: #When you of lines, append the final non-empty block
        current_block = current_block.strip()
        if current_block != "":
            blocks.append(current_block.strip())
    
    return blocks

def block_to_block_type(md_block: str):
    """Identifies the type of a markdown file: headings (1-6), code, quote, unordered list, ordered list or a paragraph."""
    #headings start with 1-6 # and a whitespace
    if re.match(r'#+ ', md_block):
        heading_level = len( re.match(r'#+', md_block).group() )
        return 'heading' + str(heading_level)
    #code blocks start and end in three backticks ```
    elif re.search(r'^```', md_block) and re.search(r'```$', md_block):
        return 'code'
    #every line in a quote block starts with a >
    elif re.match(r'>', md_block) and len( re.findall(r'^>', md_block, flags=re.MULTILINE) ) == len( md_block.split("\n") ):
        return 'quote'
    #every line in an unordered list starts with a * or -
    elif re.match(r'[*-] ', md_block) and len( re.findall(r'^[*-] ', md_block, flags=re.MULTILINE) ) == len( md_block.split('\n') ):
        return 'ul'
    #ordered lists start with a number and a dot ., number ascending from 1 (1. 2. 3. 4.)
    elif md_block.startswith('1. '):
        for index, line in enumerate( md_block.split('\n') ):
            if not line.startswith( str(index + 1) + '. ' ):
                break
        else:
            return 'ol'
    return 'paragraph'


def extract_title(markdown: str):
    """Extracts the level 1 heading to be used as a <title> for a html page."""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading1":
            return block[2:].strip()
    else:
        raise Exception("Heading 1 (h1) not found to create a <title>.")
    

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts a markdown string to HTML nodes that can be further coverted to a HTML with its method."""
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