# run_demo_step1.py
from nodes import Directory, File

def print_tree(dir_: Directory, indent: int = 0) -> None:
    spacer = "  " * indent
    name = "/" if dir_.parent is None else dir_.name + "/"
    print(f"{spacer}{name}")
    for child in dir_.children.values():
        if child.is_dir():
            print_tree(child, indent + 1)
        else:
            print(f'{"  " * (indent + 1)}{child.name}')

def main() -> None:
    root = Directory(name="/", parent=None)
    docs = Directory(name="docs")
    root.add(docs)

    notes = File(name="notes.txt", content="hello world")
    docs.add(notes)

    print("Paths:")
    print(" root ->", root.path())
    print(" docs ->", docs.path())
    print(" notes ->", notes.path())
    print("\nTree:")
    print_tree(root)

if __name__ == "__main__":
    main()
