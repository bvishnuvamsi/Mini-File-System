# run_step4.py
import errors as E
from fs import FileSystem
from nodes import Directory, File

def print_tree(dir_, indent: int = 0) -> None:
    spacer = "  " * indent
    name = "/" if dir_.parent is None else dir_.name + "/"
    print(f"{spacer}{name}")
    for child in dir_.children.values():
        if isinstance(child, Directory):
            print_tree(child, indent + 1)
        else:
            print(f'{"  " * (indent + 1)}{child.name}')

def main():
    fs = FileSystem()

    print("1) mkdir /docs")
    fs.mkdir("/docs")
    print_tree(fs.root)

    print("\n2) create_file /docs/notes.txt")
    fs.create_file("/docs/notes.txt", "hello world")
    print_tree(fs.root)

    print("\n3) read_file /docs/notes.txt")
    print("   ->", fs.read_file("/docs/notes.txt"))

    print("\n4) mkdir /docs (should error AlreadyExistsError)")
    try:
        fs.mkdir("/docs")
    except E.AlreadyExistsError as e:
        print("   Expected:", e)

    print("\n5) rmdir /docs (should error DirectoryNotEmptyError)")
    try:
        fs.rmdir("/docs")
    except E.DirectoryNotEmptyError as e:
        print("   Expected:", e)

    print("\n6) delete_file /docs/notes.txt")
    fs.delete_file("/docs/notes.txt")
    print_tree(fs.root)

    print("\n7) rmdir /docs (now empty, should succeed)")
    fs.rmdir("/docs")
    print_tree(fs.root)

    print("\n8) read_file /docs/notes.txt (should error NotFoundError)")
    try:
        fs.read_file("/docs/notes.txt")
    except E.NotFoundError as e:
        print("   Expected:", e)

if __name__ == "__main__":
    main()