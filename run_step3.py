# run_step3.py
import errors as E
from fs import FileSystem
from nodes import Directory, File

def print_tree(dir_, indent: int = 0) -> None:
    spacer = "  " * indent
    name = "/" if dir_.parent is None else dir_.name + "/"
    print(f"{spacer}{name}")
    for child in dir_.children.values():
        if hasattr(child, "children"):  # Directory
            print_tree(child, indent + 1)
        else:  # File
            print(f'{"  " * (indent + 1)}{child.name}')

def main() -> None:
    fs = FileSystem()

    # Build /docs and /docs/notes.txt using the traversal helpers
    parent, name = fs._resolve_parent_and_name("/docs")
    parent.add(Directory(name=name))  # create /docs

    parent, name = fs._resolve_parent_and_name("/docs/notes.txt")
    parent.add(File(name=name, content="hello step3"))

    # Resolve existing paths
    print("Resolve checks:")
    print(" / ->", fs.resolve("/").path())
    print(" /docs ->", fs.resolve("/docs").path())
    print(" /docs/notes.txt ->", fs.resolve("/docs/notes.txt").path())

    # Try a missing path
    print("\nMissing path check:")
    try:
        fs.resolve("/docs/missing.txt")
    except E.NotFoundError as e:
        print(" NotFoundError:", e)

    # Try to traverse "through" a file
    print("\nTraverse through file check:")
    try:
        # Pretend notes.txt had a child (illegal) by resolving "/docs/notes.txt/something"
        fs.resolve("/docs/notes.txt/something")
    except E.NotADirectoryError as e:
        print(" NotADirectoryError:", e)

    print("\nCurrent tree:")
    print_tree(fs.root)

if __name__ == "__main__":
    main()