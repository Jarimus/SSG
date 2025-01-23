import re

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


if __name__ == '__main__':
    text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![random image](https://random.image)"
    print(extract_markdown_links(text))