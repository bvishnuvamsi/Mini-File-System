# run_step5.py
from fs import FileSystem
import errors as E

def main():
    fs = FileSystem()
    fs.tree()  # just "/"

    print("\nCreate /docs and two files:")
    fs.mkdir("/docs")
    fs.create_file("/docs/notes.txt", "hello")
    fs.create_file("/docs/todo.txt", "1. learn python")

    print("\nCurrent tree:")
    fs.tree()

    print("\nDelete one file and show tree again:")
    fs.delete_file("/docs/notes.txt")
    fs.tree()

    print("\nTry to remove /docs while non-empty (should error):")
    try:
        fs.rmdir("/docs")
    except E.DirectoryNotEmptyError as e:
        print("Expected:", e)

if __name__ == "__main__":
    main()
