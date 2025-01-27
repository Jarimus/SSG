from pathlib import Path
import shutil
from markdown_conversion import markdown_to_html_node, extract_title


def build_public_from_static():
    """Recreates the contents for the public directory using the content from the static directory."""
    root_dir = Path(__file__).parent.parent
    public_dir = root_dir / "public"
    static_dir = root_dir / "static"

    #remove current public directory
    remove_dir(public_dir)
    
    #recreate 'public' from 'static'
    if not public_dir.exists():
        public_dir.mkdir()
    create_public_dir(static_dir)


def remove_dir(path: Path):
    """Removes a directory by unlinking all the files and removing subdirectories."""
    if path.exists():
        for child in path.iterdir():
            if child.is_dir():
                remove_dir(child)
            if child.is_file():
                child.unlink()
        path.rmdir()


def create_public_dir(current_path: Path):
    """A helper function that copies files and subdirectories from static to public."""
    for child in current_path.iterdir():
        if child.is_dir():
            new_public_dir = Path( str(child).replace("/static/", "/public/") )
            if not new_public_dir.exists():
                new_public_dir.mkdir()
            create_public_dir(child)
        if child.is_file():
            dst = Path( str(child).replace("/static", "/public/") )
            shutil.copy2(child, dst)


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    """Generates a single HTML file from a markdown file."""
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

    if dest_path.exists():
        dest_path.unlink()
    dest_path.write_text(final_html)


def generate_pages_recursive(src: Path, template_path: Path, dst: Path):
    """Crawls every entry in the src directory and its subdirectories for markdown files, which are converted to html files which are saved in the dst directory.
    Retains subdirectory structure."""
    for child in src.iterdir():
        src_item = src / child.name
        if child.is_dir():
            dst_item = dst / child.name
            dst_item.mkdir(exist_ok=True)
            generate_pages_recursive(src_item, template_path, dst_item)
        elif child.is_file() and str(child).endswith(".md"):
            dst_item = dst / (child.name[:-2] + "html")
            generate_page(src_item, template_path, dst_item)


def main():
    root_dir = Path(__file__).parent.parent
    public_path = Path(root_dir / "public")
    template_path = Path(root_dir / "template.html")
    content_path = Path(root_dir / "content")

    #build the public dir and include any files from static
    build_public_from_static()

    #generate html files in "public" dir from markdown files from "content" dir while retaining subdir structure
    generate_pages_recursive(content_path, template_path, public_path)


main()