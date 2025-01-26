from pathlib import Path
import shutil
from md_to_htmlnode import markdown_to_html_node
from extractors import extract_title

def build_public_from_static():
    """This function recreates the contents for the public directory using the content from the static directory."""
    root_dir = Path(__file__).parent.parent
    public_dir = root_dir / "public"
    static_dir = root_dir / "static"

    #remove current public directory
    remove_dir(public_dir)
    
    #recreate 'public' from 'static'
    if not public_dir.exists():
        public_dir.mkdir()
    create_public_subdirs(static_dir)

def remove_dir(path: Path):
    if path.exists():
        for child in path.iterdir():
            if child.is_dir():
                remove_dir(child)
            if child.is_file():
                child.unlink()
        path.rmdir()


def create_public_subdirs(current_path: Path):
    for child in current_path.iterdir():
        if child.is_dir():
            new_public_dir = Path( str(child).replace("/static/", "/public/") )
            if not new_public_dir.exists():
                new_public_dir.mkdir()
            create_public_subdirs(child)
        if child.is_file():
            dst = Path( str(child).replace("/static", "/public/") )
            shutil.copy2(child, dst)

def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"{"#"*30}\nGenerating page\nfrom {from_path}\nto {dest_path}\nusing {template_path}\n{"#"*30}")
    
    if not (from_path.exists() or template_path.exists()):
        raise FileNotFoundError("Markdown or template file not found.")

    #Read and store the contents of the markdown and html tempalte.
    markdown = from_path.open().read()
    final_html = template_path.open().read()
    title = extract_title(markdown)

    html_content = markdown_to_html_node(markdown).to_html()

    final_html = final_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    print(final_html)

    if dest_path.exists():
        dest_path.unlink()
    dest_path.write_text(final_html)


def main():
    root_dir = Path(__file__).parent.parent
    from_path = Path(root_dir / "content" / "index.md")
    dest_path = Path(root_dir / "public" / "index.html")
    template_path = Path(root_dir / "template.html")

    #build the public dir and include any files from static
    build_public_from_static()

    #generate the index.html from a markdown file and a html template. Write to /public/index.html
    generate_page(from_path, template_path, dest_path)



main()