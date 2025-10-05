# cli.py
import sys, os
import errors as E
from fs import FileSystem

MENU = """
Mini File System — pick an option:
  1) Create directory
  2) Delete directory
  3) Create file
  4) Read file
  5) Delete file
  6) Show tree
  7) Export to real folder
  0) Exit
> """

def prompt_path(prompt: str) -> str:
    return input(prompt).strip()

def input_multiline() -> str:
    print("Enter file content. Finish with a single line containing 'EOF':")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "EOF":
            break
        lines.append(line)
    return "\n".join(lines)

def main() -> int:
    fs = FileSystem()
    print("Initialized empty filesystem with root '/'.")

    while True:
        try:
            choice = input(MENU).strip()
        except EOFError:
            print("\nExiting.")
            return 0

        if choice == "0":
            print("Bye!")
            return 0

        try:
            if choice == "1":
                path = prompt_path("Directory path to create (absolute, e.g. /docs): ")
                fs.mkdir(path)
                print("OK: created directory.")
                fs.tree()

            elif choice == "2":
                path = prompt_path("Directory path to delete: ")
                fs.rmdir(path)
                print("OK: removed directory.")
                fs.tree()

            elif choice == "3":
                path = prompt_path("File path to create: ")
                content = input_multiline()
                fs.create_file(path, content)
                print("OK: created file.")
                fs.tree()

            elif choice == "4":
                path = prompt_path("File path to read: ")
                content = fs.read_file(path)
                print("\n----- file content start -----")
                print(content)
                print("-----  file content end  -----\n")

            elif choice == "5":
                path = prompt_path("File path to delete: ")
                fs.delete_file(path)
                print("OK: deleted file.")
                fs.tree()

            elif choice == "6":
                fs.tree()

            elif choice == "7":
                dest = prompt_path("Export destination folder (e.g. out_fs): ").strip() or "out_fs"
                if os.path.exists(dest):
                    ans = prompt_path(f"'{dest}' exists. Overwrite/merge? [y/N]: ").lower()
                    if ans != "y":
                        print("Export cancelled.")
                        continue
                fs.export_to_real_fs(dest)
                print(f"Exported to ./{dest} — open it in Finder or VS Code Explorer to verify.")

            else:
                print("Please choose a valid option (0–7).")

        except (E.MiniFSError, AssertionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nInterrupted. Type 0 to exit.")
        except Exception as e:
            print(f"Unexpected error ({type(e).__name__}): {e}")

if __name__ == "__main__":
    sys.exit(main())