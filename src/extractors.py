import re
from md_to_blocks import markdown_to_blocks, block_to_block_type

def extract_markdown_images(markdown: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)

def extract_markdown_links(markdown: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading1":
            return block[2:].strip()
    else:
        raise Exception("Heading 1 (h1) not found to create a <title>.")