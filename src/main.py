from pathlib import Path
import shutil

def build_public_from_static():
    """This function recreates the contents for the public directory using the content from the static directory."""
    root_dir = Path(__file__).parent.parent
    public_dir = root_dir / "public"
    images_dir = public_dir / "images"
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



def main():
    build_public_from_static()

main()