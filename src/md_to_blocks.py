import re

def markdown_to_blocks(text: str) -> list[str]:
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